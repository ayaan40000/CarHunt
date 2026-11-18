#!/usr/bin/env python3
"""CarHunt canonical data store (SQLite) — added 2026-11-18.

Why this exists (owner request, 2026-11-18): the board's data used to live
only as one big JSON file that every run rewrote wholesale. The working store
is now a SQLite database at data/carhunt.db (Python stdlib sqlite3, no
dependencies):

  * `listings`  — the published board, one row per record. The full record is
                  kept verbatim (JSON text, key order preserved) in `record`,
                  so nothing in the fixed schema can be lost; the trait
                  columns (body_type, hybrid, seller_type, grade,
                  reliability_score, price, mileage, meets_criteria) are
                  extracted alongside it so trait queries are real SQL
                  (that is what powers the dashboard's trait icons/filters).
  * `staging`   — daily sweep staging records, imported from the goal
                  workspace staging JSON files, keyed by (staging_date, url).
  * `meta`      — bookkeeping (schema version, last import/export).

The database is a LOCAL working store only: it is binary, and the GitHub
push route takes plain-text files, so the repo keeps carrying the generated
data/listings.json exactly as before. listings.json is now an EXPORT of this
database, in the canonical format the pipeline has always used
(json.dumps(indent=2, ensure_ascii=False) + trailing newline, authored key
order preserved).

Flow (see docs/METHOD.md, "Data management"):
  daily sweep  -> staging JSON files (goal workspace, unchanged)
  Thursday     -> carhunt_db.py stage-import <staging dir>
               -> carhunt_db.py import-board data/listings.json   (seed/refresh)
               -> edits happen against the DB / a candidate JSON
               -> carhunt_db.py export-board  (writes data/listings.json)
               -> carhunt_db.py verify        (round-trip proof, must pass)

Usage:
  carhunt_db.py [--db PATH] import-board [JSON]
  carhunt_db.py [--db PATH] export-board [--out JSON]
  carhunt_db.py [--db PATH] verify [JSON]        # import->export->compare
  carhunt_db.py [--db PATH] stage-import DIR     # load staging/*.json
  carhunt_db.py [--db PATH] stats                # trait counts from SQL
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "data" / "carhunt.db"
DEFAULT_JSON = ROOT / "data" / "listings.json"
SCHEMA_VERSION = "1"


def canonical_dumps(records) -> str:
    """The exact serialization data/listings.json has always used."""
    return json.dumps(records, indent=2, ensure_ascii=False) + "\n"


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        CREATE TABLE IF NOT EXISTS listings (
            url TEXT PRIMARY KEY,
            position INTEGER NOT NULL,
            record TEXT NOT NULL,
            year INTEGER,
            make TEXT,
            model TEXT,
            price INTEGER,
            mileage INTEGER,
            body_type TEXT,
            hybrid INTEGER,          -- 1 true, 0 false, NULL unstated
            seller_type TEXT,
            grade TEXT,
            reliability_score REAL,
            meets_criteria INTEGER
        );
        CREATE TABLE IF NOT EXISTS staging (
            staging_date TEXT NOT NULL,
            url TEXT NOT NULL,
            source_file TEXT,
            record TEXT NOT NULL,
            excluded TEXT,
            PRIMARY KEY (staging_date, url)
        );
        """
    )
    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', ?)",
        (SCHEMA_VERSION,),
    )
    return conn


def _trait_row(rec: dict, position: int):
    hybrid = rec.get("hybrid")
    return (
        rec.get("url"),
        position,
        json.dumps(rec, ensure_ascii=False),
        rec.get("year"),
        rec.get("make"),
        rec.get("model"),
        rec.get("price"),
        rec.get("mileage"),
        rec.get("body_type"),
        None if hybrid is None else (1 if hybrid else 0),
        rec.get("seller_type"),
        rec.get("grade"),
        rec.get("reliability_score"),
        None
        if rec.get("meets_criteria") is None
        else (1 if rec.get("meets_criteria") else 0),
    )


def import_board(conn: sqlite3.Connection, records) -> int:
    conn.execute("DELETE FROM listings")
    conn.executemany(
        "INSERT INTO listings (url, position, record, year, make, model, price,"
        " mileage, body_type, hybrid, seller_type, grade, reliability_score,"
        " meets_criteria) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [_trait_row(r, i) for i, r in enumerate(records)],
    )
    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('board_count', ?)",
        (str(len(records)),),
    )
    conn.commit()
    return len(records)


def export_board(conn: sqlite3.Connection):
    rows = conn.execute("SELECT record FROM listings ORDER BY position").fetchall()
    return [json.loads(r[0]) for r in rows]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_import_board(args) -> int:
    records = load_json(Path(args.json))
    conn = connect(Path(args.db))
    n = import_board(conn, records)
    print(f"imported {n} board records into {args.db}")
    return 0


def cmd_export_board(args) -> int:
    conn = connect(Path(args.db))
    records = export_board(conn)
    out = Path(args.out)
    out.write_text(canonical_dumps(records), encoding="utf-8")
    print(f"exported {len(records)} records to {out}")
    return 0


def cmd_verify(args) -> int:
    """Round-trip proof: JSON -> temp DB -> export must equal the source,
    field for field (deep equality) and byte for byte (canonical format)."""
    src_path = Path(args.json)
    raw = src_path.read_bytes()
    records = json.loads(raw)
    tmp = Path(args.db + ".verify-tmp")
    if tmp.exists():
        tmp.unlink()
    conn = connect(tmp)
    import_board(conn, records)
    back = export_board(conn)
    conn.close()
    tmp.unlink()
    deep_ok = back == records
    byte_ok = canonical_dumps(back).encode("utf-8") == raw
    print(f"records: {len(records)}  deep-equal: {deep_ok}  byte-identical: {byte_ok}")
    if not deep_ok:
        for i, (a, b) in enumerate(zip(records, back)):
            if a != b:
                print(f"first differing record index {i}: {a.get('url')}")
                for k in sorted(set(a) | set(b)):
                    if a.get(k) != b.get(k):
                        print(f"  field {k}: {a.get(k)!r} != {b.get(k)!r}")
                break
        return 1
    if not byte_ok:
        print("note: deep-equal but not byte-identical (serialization drift)")
        return 1
    print("ROUND-TRIP PASS")
    return 0


def cmd_stage_import(args) -> int:
    conn = connect(Path(args.db))
    total = 0
    for f in sorted(Path(args.dir).glob("*.json")):
        try:
            data = load_json(f)
        except Exception as e:  # a malformed staging file must not kill the run
            print(f"skip {f.name}: {e}")
            continue
        if isinstance(data, dict):
            data = data.get("listings", [])
        date = f.stem  # staging files are named YYYY-MM-DD.json
        for rec in data:
            if not isinstance(rec, dict) or not rec.get("url"):
                continue
            conn.execute(
                "INSERT OR REPLACE INTO staging (staging_date, url, source_file,"
                " record, excluded) VALUES (?,?,?,?,?)",
                (
                    date,
                    rec["url"],
                    f.name,
                    json.dumps(rec, ensure_ascii=False),
                    rec.get("excluded") if isinstance(rec.get("excluded"), str) else None,
                ),
            )
            total += 1
    conn.commit()
    n = conn.execute("SELECT COUNT(*) FROM staging").fetchone()[0]
    print(f"stage-import: {total} records read, staging table now holds {n} rows")
    return 0


def cmd_stats(args) -> int:
    conn = connect(Path(args.db))
    q = lambda s: conn.execute(s).fetchall()  # noqa: E731
    print("board records:", q("SELECT COUNT(*) FROM listings")[0][0])
    print("by body_type:", q("SELECT body_type, COUNT(*) FROM listings GROUP BY 1"))
    print(
        "hybrid: true=%d false=%d unstated=%d"
        % (
            q("SELECT COUNT(*) FROM listings WHERE hybrid=1")[0][0],
            q("SELECT COUNT(*) FROM listings WHERE hybrid=0")[0][0],
            q("SELECT COUNT(*) FROM listings WHERE hybrid IS NULL")[0][0],
        )
    )
    print("by seller_type:", q("SELECT seller_type, COUNT(*) FROM listings GROUP BY 1"))
    print(
        "by grade band:",
        q("SELECT substr(grade,1,1), COUNT(*) FROM listings GROUP BY 1"),
    )
    print(
        "reliability >= 4:",
        q("SELECT COUNT(*) FROM listings WHERE reliability_score>=4")[0][0],
    )
    print("staging rows:", q("SELECT COUNT(*) FROM staging")[0][0])
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="CarHunt SQLite data store")
    p.add_argument("--db", default=str(DEFAULT_DB))
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("import-board")
    sp.add_argument("json", nargs="?", default=str(DEFAULT_JSON))
    sp.set_defaults(fn=cmd_import_board)
    sp = sub.add_parser("export-board")
    sp.add_argument("--out", default=str(DEFAULT_JSON))
    sp.set_defaults(fn=cmd_export_board)
    sp = sub.add_parser("verify")
    sp.add_argument("json", nargs="?", default=str(DEFAULT_JSON))
    sp.set_defaults(fn=cmd_verify)
    sp = sub.add_parser("stage-import")
    sp.add_argument("dir")
    sp.set_defaults(fn=cmd_stage_import)
    sp = sub.add_parser("stats")
    sp.set_defaults(fn=cmd_stats)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
