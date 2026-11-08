# CarHunt — Changelog

## 2026-11-07 — Phases 1 and 2 built (feature build; listing data unchanged from Nov 5, 2026)

Built locally on the owner's green-light (Nov 7, 2026). This is a feature build, not a data refresh: the 15 records, grades, prices, and the Nov 5, 2026 data stamp are exactly as published.

**Phase 1 — Finalist buying cockpit (new Finalists tab):**
- Comparison strip for the data-driven top 3 must-have cars (grade, then discount): the 2024 Malibu LT, the 2024 Forte LXS, and the 2021 Forte GT-Line in Katy — shown in viewing order (Forte LXS first: the only finalist with a seller-stated clean title; the Malibu waits for home VIN checks because its discount sits in the washed-title flag zone), with price, mileage, grade, discount, blockers, seller type, listing age, estimated all-in cash, and next action per car.
- Per-finalist cockpit: photo area (no photo URLs exist in the data yet, so it shows the explicit fallback — photo capture starts with the next sweep); a VIN workflow (paste box, copy button, NHTSA Decoder / Recalls / NICB / NMVTIS-TxDMV links, done-checkboxes — the VIN itself is never stored anywhere); a copy-ready seller message generated from each car's blockers plus model-specific questions (prepared only, never sent); an all-in Texas cash estimator (6.25% tax on the greater of price or Standard Presumptive Value, $33 title-fee default, $50.75 registration, $125 PPI, $30 history report, repairs reserve shown as "unknown" until entered); and a tailored test-drive/PPI checklist with walk-away triggers first and print-friendly rendering.

**Phase 2 — Freshness and estimate confidence:**
- Every card now shows a "Checked Nov 5, 2026" freshness tag, its listing age, an estimate-confidence tag, and — only where the record supports it — a price-changed tag (one card: the 2021 Forte LXS in Houston, $9,550 → $9,000, documented Nov 3 → Nov 5).
- `data/listings.json` gained appended fields only: `photo_urls`, `photo_checked_at`, `price_history` (seeded only with prices already on record), `estimate_components` (the provider figures behind each median, parsed from the records' own notes), `estimate_confidence` + reason (rule in docs/METHOD.md; on this board: 0 High, 10 Medium, 5 Low), and a per-record CarMax note (only the 2019 Forte, Houston includes a CarMax figure — a $9,000 recent offer, named as an offer, not a comparable).
- Grades did not change. Docs updated in the same change: README, docs/METHOD.md (new fields, confidence rule, CarMax policy, photo-capture rule, Finalists regeneration contract, UI rules), DEVELOPMENT-PLAN-2026-11.md (Phases 1–2 marked built).

## 2026-11-05 — Phase 0 board published (Thursday full update)

- Full Thursday re-verification plus fresh sweep: 15 listings published, 10 meeting all must-haves, led by the 2024 Chevrolet Malibu LT in Katy ($9,799, grade A) and a new 2024 Kia Forte LXS in Houston ($10,500, grade A). Two Oct 31-board listings (2021 Forte S, and the Nov 2 staged Civic Sport standout) had sold or expired and were dropped; 13 checked listings were excluded (10 branded titles, 3 excluded engines).
- First board published under the Phase 0 publish gate (built Nov 4, 2026): duplicate/conflict reconciliation by Marketplace item ID, structured engine/title/blocker evidence fields on every record, lane-assist points removed from scoring, and a Blockers line on every card. Same-day UI rework (Nov 4): compact cards with collapsible details, body-type filter, and the Paperwork (TX) tab; budget raised to $15,000.
