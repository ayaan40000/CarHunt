# Method — How the Sweep and Refresh Work

So a future run can repeat this exactly and produce a dashboard in the same format.

## Access rule: Pi browser only for Facebook

- Facebook Marketplace is accessed **only through the Pi browser** (the shared persistent Chromium on Ayaan's Raspberry Pi, via `pib`), never through Muse's own browser. Logged-in / bot-hostile sites route to the Pi per the standing routing rules.
- Session rule: reuse the existing logged-in Pi session; do not log in fresh, do not create accounts, do not contact sellers, send messages, submit forms, or make any purchase. Research only.
- Bot checks on Pi work: the agent tries first under the owner's protocol (one attempt per site entry); only on failure does it escalate to the owner in the live view. Never charge money, never delete anything.

## Sweep method (Oct 26, 2026 run; criteria updated 2026-10-31)

1. Search Facebook Marketplace from the Houston / Stafford TX 77477 area for the candidate families in the spec — sedans (Fusion, Accord, Civic, Elantra, Forte, Sonata, Optima, Mazda6, Malibu, Legacy, Corolla) and, since 2026-10-31, SUV/crossover families (RAV4, CR-V, CX-5, Tucson, Sportage, Forester, Outback; more only after their matrix rows and reliability checks exist) — under the $15,000 / ≤100,000-mile frame (budget raised from $12,000 by the owner on 2026-11-04), any body type except trucks and compact hatchbacks — while also recording same-family near-misses that explain the market (over-miles, over-price, rebuilt) so market estimates have a visible basis.
2. Open each listing; record only what the listing states or what factory fit for that exact year/trim establishes, labelled as inference in the notes. Never invent a feature: unstated = `null`.
3. Apply the **exclusion rule** (below) before anything else: excluded models never reach the dashboard.
4. Estimate market value per the **Value estimates** section (CarMax + leading providers primary; same-sweep comparables as cross-check, named in each record's notes), then grade the deal A+ to F per the **Grading rubric**.
5. Flag `deal_flag` when asking is ≥10% below the value estimate. The flag is advisory: a discount explained by a rebuilt title, suspect miles, or a non-clean title is recorded as such in the notes, not as a bargain.
6. Only the fresh sweep ships. Older sweeps are **not** carried forward or re-labelled as current — the Sep 28, 2026 listings were not re-verified on Oct 26 and are presumed sold, so they are excluded from this dashboard entirely. Daily staged records (see Cadence) are re-opened and re-verified on Thursday before they may ship.

## Fixed schema (do not change fields between runs)

Each record in `data/listings.json` has exactly these fields, in this order of meaning:

`url, year, make, model, trim, price, mileage, location, seller, hybrid, android_auto, reverse_cam, lane_assist, reliability_score (1–5), market_value_estimate, discount_pct, deal_flag (true/false), pref_score (0–10), meets_criteria (true/false), notes`

Fields added 2026-10-31 (append; never remove or reorder the originals): `body_type, fuel, transmission, seller_type (private/dealer), grade (A+ to F), estimate_sources`

Fields appended 2026-11-04 (Phase 0; append-only, after the fields above): `engine, engine_evidence, title_status (clean-stated / paid-off-only / clear-history-only / rebuilt / salvage / flood / unknown / physically-verified-clean), title_evidence, verification_blockers, first_seen_at, last_seen_at, last_verified_at, listing_status`

Fields appended 2026-11-07 (Phases 1–2; append-only, after the Phase 0 fields): `photo_urls` (list of listing-photo URLs captured by a sweep; empty until photo capture starts — see **Photos**), `photo_checked_at` (date the photo URLs were captured/checked, else `null`), `price_history` (list of `{date, price}` points, seeded 2026-11-07 only with prices already on record — the current price at `last_verified_at` for every record, plus the one documented change, the 2021 Forte LXS Houston $9,550 on 2026-11-03 → $9,000 on 2026-11-05; never backfill an undated or unrecorded price), `estimate_components` (list of `{provider, figure, figure_type, date}` — the individual provider figures behind the median, parsed from the figures already recorded in each record's notes; figure types: `asking`, `average-asking`, `comparable-asking`, `fair-purchase`, `retail`, `resale`, `private-party`, `trade-in`, `offer`, `range-low`, `current-price`), `estimate_confidence` (`High` / `Medium` / `Low` — rule below), `estimate_confidence_reason` (one line), `estimate_carmax_note` (whether a CarMax figure is in the estimate — policy below).

Field appended 2026-11-17 (Phase 3; append-only, after the Phase 1/2 fields): `listing_source` (where the listing was found — `Facebook Marketplace`, `Carvana`, etc.). Absence of the field means Facebook Marketplace (every record before Phase 3 came from there). See **Non-Facebook sources** below.

Fields appended 2026-11-18 (append-only, after the Phase 3 field): `negotiation_notes` (2–4 negotiation pointers written from this record's own evidence — asking-vs-estimate gap, listing age and price drops, seller-type tactics, the record's own blockers as document asks, model-specific issues from docs/RESEARCH.md; never generic filler, and where a car is already far under estimate the honest note is to move fast and verify paperwork rather than invent leverage), `representative_image` (hotlinked URL of a generation-correct representative photo of the car's year/make/model — NOT a listing photo; see **Photos**), `representative_image_source` (the source and file name, for traceability).

## Data management — SQLite canonical store (2026-11-18)

The working store is a SQLite database, **`data/carhunt.db`** (Python stdlib `sqlite3`, no dependencies), maintained by **`tools/carhunt_db.py`**. It lives with the project in `reserved-1/data/` because the publish pipeline works there; it is a **local working store only** — it is binary and the GitHub push route takes plain-text files, so the repo keeps carrying the generated `data/listings.json` exactly as before. `listings.json` is now an **export** of the database, in the canonical format the pipeline has always used (`json.dumps(indent=2, ensure_ascii=False)` + trailing newline, authored key order preserved — the fixed schema above is unchanged).

- Tables: `listings` (the published board; the full record kept verbatim as JSON text with key order preserved, plus extracted trait columns — `body_type`, `hybrid`, `seller_type`, `grade`, `reliability_score`, `price`, `mileage`, `meets_criteria` — so trait queries are real SQL), `staging` (daily sweep records imported from the goal workspace staging JSON, keyed by staging date + URL), `meta` (bookkeeping).
- Commands: `import-board` (load `data/listings.json` into the DB, losslessly), `export-board` (write `data/listings.json` from the DB), `verify` (import → export → compare: deep-equal **and** byte-identical, or it fails), `stage-import <dir>` (load staging JSON files), `stats` (trait counts from SQL).
- **Round-trip rule:** no publish ships unless `carhunt_db.py verify` passes against the exact `data/listings.json` being published. The seed import (2026-11-18) was verified lossless against the Nov 18 board, and re-verified after the 2026-11-18 field appends.
- Flow from 2026-11-18: daily sweeps keep staging JSON in the goal workspace (unchanged transport); the Thursday publish loads staging into the DB (`stage-import`), makes its edits against the DB / a candidate JSON, refreshes the board (`import-board`), exports (`export-board`), and must pass `verify` before the dashboard is rebuilt. Dashboard trait transforms are applied by `tools/apply_traits.py`, which reads the exported JSON.

(In the Sep 28 spec the list is the same set; the Oct 26 records add the derived `discount_pct` and `meets_criteria` fields that the sweep tooling already emitted — a future run should keep emitting exactly the Oct 26 field set so the dashboard code does not change.)

Rules inside the schema:

- Feature fields are `true / false / null`. `null` = not stated in the listing. Null stays null in the data file.
- `pref_score`: hybrid +3, reliability (5→+3, 4→+2, 3→+1), year 2019+ +1, under 50,000 mi +1. Max 10. (Until 2026-11-04 the formula also gave lane assist +2. The owner dropped lane assist from the criteria on 2026-10-31, so from the 2026-11-04 Phase 0 pass it earns no points; the `lane_assist` field is still recorded, and all published pref_scores were recomputed without it.)
- `meets_criteria` is true only when **every** must-have is confirmed: price < $15,000 (raised from $12,000 on 2026-11-04), mileage ≤ 100,000, factory Android Auto confirmed, reverse camera confirmed, body not a truck or compact hatchback, model not on the exclusion list. Unconfirmed (`null`) does not count as met.
- `notes` carries the reasoning: why it misses, title statements, duplicate relationships, red flags, and the comparables behind the market estimate. The dashboard's short miss line is a condensation of the notes, never a replacement for them.

## Matrix-over-seller-claim rule (dashboard)

- The Android Auto badge on each card comes from the **expert matrix** (expert guide Part 1) for that year/make/model/trim — not from the seller's claim and not from the record's raw `android_auto` field alone.
- If seller claim and matrix disagree, the card shows the matrix verdict and a visible mismatch flag, e.g.:
  - 2019 Fusion S: matrix = AA only with the 8″ SYNC 3 screen (listing inference said "no AA").
  - 2019 Elantra SEL with a blank listing: matrix = AA standard on SEL (seller said nothing).
  - 2018–19 Kia Optima: matrix = UNVERIFIED by trim — seller AA claims are shown as unverified, check in person.
- Corrections baked into the matrix: Corolla sedan AA 2021+ (not 2020); 2019 Fusion S conditional; Mazda6 2018 Touring+ (upgrade) / Sport excluded; "eligible ≠ installed" for 2016 Chevy 8″ MyLink and 2015–16 Hyundai/Kia update cars.
- Pursue / Caution / Avoid badge per card comes from the expert dossiers (Part 2), with a one-line plain-language reason.

## Exclusion rule (owner-set 2026-10-31)

Models with reliability concerns or major recalls are **excluded from the dashboard entirely** — not published with a caution badge. The expert guide's Avoid dossiers are the starting list (Fusion 1.5L EcoBoost, Honda 1.5T oil-dilution years, Theta II Sonata/Optima, 2013–18 Altima CVT, PowerShift Focus/Fiesta, Fusion Energi / Sonata Plug-in, and any model-year with a major engine/transmission recall pattern). A staged record for an excluded model is kept in staging with `excluded: <reason>` and never ships. Title problems (rebuilt/salvage/non-clean) also exclude the individual listing regardless of model.

## Value estimates (owner-set 2026-10-31)

- For each published listing, get a market value estimate for the same model/year/trim at a similar mileage from **CarMax** (comparable CarMax asking prices) and other leading providers where accessible (KBB, Edmunds, Carvana, Cars.com comparables).
- `market_value_estimate` = the median of the provider figures found; `estimate_sources` names them. Same-sweep Facebook comparables stay in the notes as a cross-check.
- The owner's target is a price **below** estimated value; `discount_pct` is measured against this estimate.

## Grading rubric — A+ to F (owner-set 2026-10-31)

Grade ladder: A+, A, A-, B+, B, B-, C+, C, C-, D+, D, D-, F.

1. Base grade from `discount_pct` (asking vs value estimate): ≥25% under → A · 18–25% → B+ · 12–18% → B · 7–12% → C+ · 3–7% → C · 0–3% → D · priced above estimate → F.
2. Step adjustments (one ladder step each): reliability_score 5 → +1 · reliability_score 3 → −1 (score ≤2 is excluded, never graded) · mileage ≤60,000 → +1 · mileage 90,000–100,000 → −1 · private (non-dealer) seller → +1.
3. Not-preferred penalties: manual transmission, diesel, or electric → −1 step each, max −2 total.
4. Caps: if factory Android Auto or reverse camera is unconfirmed (`null`), the grade is capped at C+ until confirmed. A car that fails a must-have outright (AA or camera confirmed absent for its year/trim) is likewise capped at C+ — it may be listed for context but cannot rank as a deal.
5. **A+ is reserved**: base A AND reliability_score 5 AND mileage ≤75,000 AND both must-haves confirmed AND private seller AND no penalties. A+ means a great deal at a great price — most listings should not reach it.
6. The grade replaces `pref_score` as the displayed rank (sort by grade, then discount). `pref_score` is still computed for continuity.

## Estimate confidence and CarMax policy (2026-11-07, Phase 2)

Every record carries `estimate_confidence` with a one-line `estimate_confidence_reason`. Grades do **not** change with confidence — the grade still comes from the rubric and the central estimate; confidence says how much to trust the estimate behind it.

- **High:** at least 3 component figures are preserved in `estimate_components`, captured in the same cycle, for the same trim, from at least 2 distinct providers, with compatible figure types (market-value measures: asking / fair-purchase / retail / resale / private-party) and no model-wide-average or mileage-mismatched input.
- **Medium:** a multi-source estimate from the current or immediately prior cycle without preserved components meeting the High bar, or a multi-source estimate with exactly one proxy input (a comparable from a different trim, a model-wide average, a mileage-mismatched comparable, a mixed-in trade-in figure, or a range endpoint).
- **Low:** a carried estimate older than one cycle, a single-provider estimate, or an estimate for a car whose trim is not stated (a proxy-trim estimate).

Apply it honestly: most records are Medium or Low. Do not inflate a record to High because its grade is good. On the Nov 5, 2026 board as scored 2026-11-07: 0 High, 10 Medium, 5 Low.

**CarMax policy:** each record's `estimate_carmax_note` states plainly whether a CarMax figure is in its estimate. A CarMax *recent offer* is a liquidation reference, not a retail comparable: it may stay in a median only when it is named as an offer in `estimate_components` (figure type `offer`) and in the record's note — never silently treated as a CarMax asking price. On the Nov 5, 2026 board, only the 2019 Forte (Houston) estimate includes a CarMax figure (a $9,000 recent offer at 58,000 mi, one of four inputs); every other record's note says no CarMax figure is included.

## Finalists view and the Thursday regeneration contract (2026-11-07, Phases 1–2)

The dashboard has a fourth tab, **Finalists (3)**, built 2026-11-07 by direct edit of `index.html` (no separate generator was introduced — the Phase 1/2 build deliberately took the direct-edit route so the working page could not be broken by a builder rewrite). A Thursday run that rebuilds `index.html` MUST regenerate all of it from `data/listings.json`, or carry the sections forward verbatim:

- **Finalist selection is data-driven:** the top 3 records with `meets_criteria = true`, ranked by grade (A+ → F ladder) then `discount_pct`, highest first. The *viewing order* shown may differ from that rank when blocker severity justifies it (a washed-title flag outranks a discount); the strip must state the rank it used and the reason for the order it shows. On the Nov 5 board the rank is Malibu (A, 42.5%) → 2024 Forte LXS (A, 34.4%) → Forte GT-Line Katy (A, 34.2%), and the viewing order is Forte LXS → Malibu → GT-Line Katy, for the reasons stated on the page.
- **Comparison strip:** one table comparing the 3 finalists on price, mileage, grade, discount, blockers, seller type, listing age (`first_seen_at`), estimated all-in cash at the estimator defaults, and next action, ordered by viewing order with a #1 pick and a one-line reason per car.
- **Per-finalist cockpit:** photo area (renders `photo_urls`, else the fallback line in **Photos**); a VIN panel (paste box, copy button, links to NHTSA VIN Decoder, NHTSA Recalls, NICB VINCheck, and the NMVTIS / TxDMV Title Check route from docs/FAQ.md, plus done-checkboxes) — **the VIN itself is never stored**: not in the repo, not in the page, not in browser storage; the checkboxes persist only done/not-done state in localStorage key `carhunt-checks-v1`; a copy-ready seller message generated from the car's `verification_blockers` plus its model-specific questions (scripts only — nothing is ever sent); the all-in cash estimator; and a tailored test-drive/PPI checklist (walk-away triggers first, then the universal items from docs/FAQ.md plus model-specific items from docs/RESEARCH.md, with checkboxes persisted the same way, and print-friendly rendering).
- **All-in cash estimator defaults (Texas):** asking price; sales tax 6.25% on the **greater** of the asking price or an editable Standard Presumptive Value (default = asking price); title fee $33 default (editable — $28 in Harris County, $33 in most other counties, per docs/PAPERWORK.md); registration $50.75 + editable county fees; PPI allowance $125; one paid history report $30; a dealer doc-fee field shown only for dealer sellers; an immediate-repairs reserve that defaults blank and, while blank, is shown as "unknown — not included", never as $0. Output: estimated total cash before repairs, the asking price's headroom against the $15,000 cap, and a separate warning when total cash passes $15,000 (the budget caps the asking price, not the total).
- **Freshness on every card:** the badges row carries a "Checked <last_verified_at>" tag and an "Estimate confidence: <level>" tag; a "Price changed: $<old> → $<new>" tag appears only when `price_history` holds 2+ differing points. The card's details carry a Freshness line (live-verified date, first-seen date and age at that check, and the price history, labelled as starting with our records) and an Estimate line (confidence, its reason, and the CarMax note).

## Non-Facebook sources (Phase 3, 2026-11-17)

Evaluated 2026-11-17 with normal web access (search + page reads); full per-source evidence in the goal workspace (`hidden_files/phase3-work/source-yield.md`). Facebook remains the primary sweep; these sources are supplements, never replacements. Every record from a non-Facebook source carries `listing_source` naming it.

**ADOPTED — Carvana (search-results screening only).**
- *How it is swept:* read Carvana search-results pages (Houston SRP plus per-family SRPs for the rotation families) with normal web access; a car counts as a candidate only when the SRP card itself shows an eligible year/trim, price < $15,000 and mileage ≤ 100,000. Expect low yield: on 2026-11-17, ~69 listings read produced 2 candidates, both marginal Kia Fortes just under the price line.
- *How records carry their source:* `listing_source: "Carvana"`; `url` is the SRP where the car appeared until a per-car URL is captured at verification; `listing_status: "sourced-unverified"`; everything the SRP card does not state (exact mileage, location/shipping to 77477, engine, title, Android Auto/camera statements) stays `null`/unstated and is listed in `verification_blockers`. No grade and no estimate until verification.
- *How Thursday re-verifies:* Carvana detail pages do not render their price/mileage/VIN/history to a text read, so verification is a live-browser check (the Pi browser, as with Facebook): open the car's detail page, confirm exact mileage, location or shipping cost to 77477, VIN, title/history statement, and Android Auto/camera; then run the normal estimate + grade. A car that cannot be found on Carvana at the Thursday check is dropped as dead, same as a dead Facebook listing.

**ADOPTED — Government & public auction sources (2026-11-24, owner directive).**
Texas public bodies sell surplus vehicles to the public, and CarHunt is not Facebook-only. The source directory, buyer rules and fit rules live on the dashboard's Gov Auctions page (`gov.html`). Sources: TFC State Surplus storefront + published vehicle list (fixed price, Austin), Public Surplus (State of Texas agency auctions), GovDeals, Rene Bates Auctioneers (cities/counties), Lone Star Auctioneers (state online auctions, city fleet sales, universities), GSA Auctions / GSA Fleet (federal).
- *How it is swept:* screen the portals with normal web access during the rotation; a candidate counts only when the listing itself shows an eligible family/year, a price under $15,000 and mileage ≤ 100,000. Expect low yield — most fleet retirements are 120,000+ miles and police packages fail Android Auto; under-100k admin/pool sedans and small SUVs are the target.
- *How records carry their source:* `listing_source` names the portal (`"GovDeals"`, `"Public Surplus (TX)"`, `"Rene Bates"`, `"Lone Star"`, `"TFC Surplus"`, `"GSA"`); `seller_type` is `"government"`; auction finds are staged as `listing_status: "sourced-unverified"` with the auction end date recorded in the notes.
- *Pricing rule:* a live auction's current bid is NOT a price and is never graded. Grades and estimates use a verified fixed price (storefront) or a closed result, and always the all-in figure — bid + buyer's premium (GovDeals sellers set 5–12.5%; Rene Bates sales vary, ~10% seen) + stated fees.
- *Exclusions:* impound / abandoned / seized stock (city auto pounds) is excluded by default — unknown history, frequent non-runners; fleet-surplus stock only. The model exclusion list and reliability cross-check apply unchanged.

**ADOPTED — Bank & credit-union repo sources (2026-11-24, owner directive).**
Lenders repossess cars and resell them; the slice a private buyer can actually reach is credit unions and smaller banks selling their own repos direct. The directory, terms and fit notes live on `gov.html` next to the government sources. Adopted channels: RepoFinder.com (free aggregator that links straight to the selling lender — no fees, no commissions, it is not the seller; listings carry the lender's price, mileage and often the VIN, browsable by state; verified live 2026-11-24 with fresh November listings), Rave Financial (Beaumont TX — own repo page: no-haggle prices plus offers, viewing/test drives by appointment, payment by cashier's check or wire within three business days, sold as-is with a warranty of ownership only; phone 800-892-1111) and RBFCU (own repossessed-vehicles page — "a small number of vehicles available for sale online", offers to the credit union). SSFCU is watch-list only: its dedicated Texas repo-lot site (ssfcu-repos.org) now redirects into ssfcu.org's auto pages and no standalone public list was verifiable on 2026-11-24; its stock surfaces via RepoFinder. Checked with no public repo list found on 2026-11-24: TDECU, Texas Trust CU, Wellby Financial (formerly JSC FCU) and the Houston First Community CU (the big autos-for-sale page under that name belongs to a Wisconsin credit union).
- *How it is swept:* screen RepoFinder's Texas listings and the adopted lenders' pages with normal web access during the rotation; a candidate counts only when the listing itself shows an eligible family/year, an asking price under $15,000 and mileage ≤ 100,000. Expect low, lumpy yield — each lender lists a handful of cars at a time, and the one verified Texas seller's current stock skews to over-frame trucks.
- *How records carry their source:* `listing_source` names the channel (`"RepoFinder"`, `"Rave Financial"`, `"RBFCU"`); `seller_type` is `"lender"`; records are staged as `listing_status: "sourced-unverified"` until Thursday verification, same as the other non-Facebook sources.
- *Pricing rule:* grades use the lender's asking price against the same market estimates as every other record — the repo discount is measured, never assumed (buyer guides put typical direct-sale repo pricing roughly 10–30% below retail guide value; no blanket percentage is published as fact, and no buyer's premium applies on direct sales). Bid/offer-format cars with no published asking figure are staged ungraded: a live bid is not a price (same rule as gov auctions).
- *Condition and title:* every repo record carries the as-is flag in its notes ("sold as-is, no warranty") and condition unknowns in `verification_blockers`. The seller is the lienholder, so title is normally clean with the lien released at sale — but `title_status` is verified per car like any other record, and a branded title excludes as usual. The model exclusion list and reliability cross-check apply unchanged.
- *Excluded channels (not directly buyable):* Manheim / ADESA / SmartAuction are licensed-dealer-only wholesale, where most big-lender repo volume goes. Copart and IAA in Texas sell clean-title cars to private buyers only through a registered broker (Copart's own state licensing table; IAA public buyers — $225/yr registration per IAA's help center — are limited to salvage titles in Texas), and their direct public lanes are salvage titles, which the title rule excludes anyway; neither is a CarHunt source. No public listing feed or API for repo inventory was found — screening is page reads, as with Carvana.

**REJECTED (2026-11-17, with the concrete reason):**
- **CarMax** — inventory unreadable via web access (JS shell, no listings extracted), and the national snippets that do surface price eligible families above the frame (2019 Forester at $19,998). CarMax figures still serve value estimates per **Value estimates**; CarMax is not a listing source.
- **Hertz Car Sales** — the Houston search page returns no listings to web reads and its indexed snippets strip model names, so eligibility cannot be assigned; detail pages are excellent (VIN + AutoCheck with title section) but no eligible Houston listing could be reached.
- **Enterprise Car Sales** — vehicle pages strip to footer/disclaimers; the search index carries essentially none of its Houston listings. Nothing to screen.
- **OfferUp** — Houston car inventory not searchable/readable (dealer profiles only); the one readable car was a dealer-syndicated, out-of-area, over-budget listing; title quality unassessable. Adds nothing over the Facebook sweep of the same private-party pool.
- **Cars.com / Autotrader** — Cars.com pages not discoverable via web search at all; Autotrader SRPs extract only the filter taxonomy, no listings. Zero in-frame listings surfaced.

*Caveat kept on record:* several rejections are readability limits of web-text access, not proof of empty inventory. A live-browser session could overturn them (Cars.com/Autotrader most likely), but their stock is dealer inventory of the kind already visible through other channels, so the expected incremental yield is duplicates, not a new pool. Do not re-evaluate without a live-browser session and a reason to expect a different result.

**Cross-source duplicate detection.** The canonical key stays the listing URL within its source. When the same car appears on two sources: match on VIN when a VIN is safely available (VINs live only in private staging data, never in the published repo — see the Finalists contract), otherwise on year + trim + price + mileage + location + photo similarity. A non-VIN match is a warning, not proof: record "possible duplicate of <source record>" in both records' notes and let Thursday's verification resolve it. State "also listed elsewhere" only on a reliable match (VIN match, or exact price + mileage + photo match). A confirmed duplicate merges into ONE canonical record (the more complete/reliable source wins), with the other source named in its notes and its `listing_source` history preserved there.

## Cadence (owner-set 2026-10-31)

- **Daily incremental sweeps**: rotate model families across the week, stage records into the goal's `hidden_files/staging/` (never publish), re-check exclusions and matrix gaps for new families. Pi pacing ~60 pages/hour on Facebook, ~25 pages/day. A standout find (grade A or better after a same-day estimate check) is reported the same day.
- **Thursday full update**: re-open and re-verify every staged record (dead listings dropped), run a fresh sweep of the core families, compute value estimates and grades, rebuild `index.html` + `data/listings.json`, update the data stamp, publish, verify live, and report in chat.

## Data stamp rule

Every published dashboard carries this line, visibly, at the top:

> Listings from Facebook Marketplace sweep, Oct 31, 2026 — listings sell fast; a car shown here may already be gone.

On a refresh, replace the date with the new sweep date. Never publish a dashboard without the stamp, and never mix two sweep dates in one listings file.

Since 2026-11-18 the stamp renders on the page as a single line (date + the sell-fast warning). The full run notes that used to be appended to the stamp text (what was re-verified, what was dropped, estimate-source disclosures such as the CarMax rule) are published verbatim in the FAQ & Help tab's **Run notes** section instead — the disclosure requirement is unchanged, only its placement.

## Photos

The Oct 26 records carry no photo URLs, so the dashboard embeds no photos. If a future sweep records photo URLs, link/embed the URL only — never commit image binaries to this repo, and keep every file ≤ ~110 KB (files are uploaded individually).

**Photo-capture rule (2026-11-07, Phase 1):** from the next sweep onward, when a sweep opens a listing it also records up to three useful photo URLs from the listing page into `photo_urls` (exterior, dashboard/screen, rear/camera or odometer view where available) and sets `photo_checked_at` to the capture date. The Finalists view and the cards render photos when `photo_urls` is non-empty; while it is empty they show the explicit fallback: "Photos not captured yet — photo capture starts with the next sweep. Open the Marketplace listing to see photos." Never invent, guess, or hotlink a photo URL that was not captured from the listing page, and never publish a photo showing a full VIN or a title document. (Size note: with the Phase 1 cockpit inline, `index.html` is ~116 KB as of 2026-11-07 — above the ~110 KB guideline above; the single-file rule wins for now, and the parent agent's push route handles the file as-is.)

**Representative images (2026-11-18) — not listing photos.** Separate from `photo_urls`, each record may carry a `representative_image`: one hotlinked photo per year/make/model **generation** (a 2018 Malibu shows the 2016–18 car, not the 2019+ facelift), shared by every listing of that car, sourced from Wikimedia Commons or another stable hotlinkable source, with the file named in `representative_image_source`. Rules: hotlink only — never commit an image binary; every URL is verified to load **and** to depict the right model/generation before it ships (a car whose image cannot be verified ships without one); the card always labels it "Representative image — not the actual car". A representative image never substitutes for `photo_urls` and is never presented as the seller's car.

## Listing links — Facebook app on Android (owner rule, 2026-10-31)

Card links stay as static `https://www.facebook.com/marketplace/item/<id>/` hrefs in the HTML. Every rebuild of `index.html` MUST keep the small app-link script block just before `</body>`: on Android it rewrites each Marketplace link to an `intent://` URL for the Facebook app (package `com.facebook.katana`) with the web URL as `browser_fallback_url`, so taps open the app and fall back to the browser if the app is missing. Desktop and no-JS keep the plain https links. If the script is missing from a rebuild, the links are wrong — treat it as a failed self-check.

## App icon & inline manifest (owner rule, 2026-11-01)

Every rebuild of `index.html` MUST keep, in `<head>`: the `rel="icon"` and `rel="apple-touch-icon"` links (SVG data URIs — cream car front on the deep-green tile) plus the `theme-color` meta; and just before `</body>`, AFTER the app-link script: the inline manifest script (generates the web app manifest from the favicon, name "CarHunt"). Together they are what makes the phone home-screen icon the CarHunt logo instead of a generic letter/screenshot. Missing either block = failed self-check, same as the app-link script.

## Publish flow

1. Build/refresh files locally in this repo: `index.html`, `data/listings.json`, `docs/FAQ.md`, `docs/RESEARCH.md`, `docs/METHOD.md`, `docs/PAPERWORK.md`, `README.md`.
2. Self-check before publishing: HTML parses, JSON parses, listing count in the page matches the JSON count, no file over ~110 KB.
3. Upload the files individually to GitHub repo **ayaan40000/CarHunt** (parent agent handles the upload and any approvals; builders stage locally and do not push).
4. GitHub Pages serves the repo at **https://ayaan40000.github.io/CarHunt/** (Pages enabled; the repo was renamed from Reserved-1 to CarHunt on 2026-10-31 and the Pages address moved with it).
5. A refresh run repeats the sweep, replaces `data/listings.json` wholesale with the new sweep only, regenerates the cards, updates the data stamp date everywhere it appears (page, README, FAQ), and republishes.

## Dashboard UI rules (owner-set 2026-11-04)

The owner found the board text-heavy: descriptions filled the screen and the controls crowded out the listings. Every rebuild of `index.html` MUST keep this structure:

- **Compact cards.** A card shows only: title, price line, grade/meets badges, the underpriced deal line, and the Marketplace CTA. ALL descriptive text — Why, Miss/note, Blockers, the Android Auto line, the specs line, the seller line, and the full sweep notes — lives inside the card's collapsible `<div class="card-more" hidden>` region, opened by that card's "Show details" toggle button (class `card-toggle`). The toolbar's "Show all details" button expands/collapses every card at once. A rebuild that renders the descriptive text always-visible is a failed self-check.
- **Body-type filter.** Every card carries `data-body` (normalised from the record's `body_type`: `sedan`, `suv` for SUV/crossover, `hatchback`, `coupe`, `wagon`, `van`) and the filters include the Body type select (`#fBody`) wired into `apply()` and the active-filter badge count.
- **Three tabs:** Listings, FAQ & Help, and Paperwork (TX) — the Texas private-party paperwork process (title transfer, Form 130-U, 6.25% tax on the greater of price or Standard Presumptive Value, 30-day filing, transfer notification). The paperwork content is mirrored in `docs/PAPERWORK.md`; keep both in sync.
- **Fourth tab — Finalists (2026-11-07, Phases 1–2):** the tabs row also carries a Finalists tab (`#tabFin`, view `#view-fin`) with the comparison strip and the per-finalist cockpit described in **Finalists view and the Thursday regeneration contract** above. Every rebuild MUST preserve the Finalists view, the per-card freshness/confidence tags and detail lines, and the Phase 1/2 script block (checkbox persistence, copy buttons, VIN copy, estimator, print) that sits immediately before the Android app-link script. A rebuild that drops any of these is a failed self-check.
- **Slim chrome.** The sticky control deck stays one compact block (tabs + sort/filters row), and the filters panel starts collapsed at every screen width. Keep header and stamp padding at the slim values in the stylesheet.
- **Slim entrance (2026-11-18).** The top of the page is only: a slim brand header (logo + name + a one-line board summary — listing count, how many meet all must-haves, date), the data stamp rendered as **one line**, the control deck, then the listings. No long prose above the first card. All reading matter that used to sit in the header (the criteria paragraph, the honest-headline paragraph) and the full run notes from the stamp live in the FAQ & Help tab under **About this board** / **Run notes**, moved verbatim — slimming the entrance never deletes METHOD-required content, it relocates it.
- **Trait icons (2026-11-18).** Every card face carries a row of trait chips (badges, so the compact-card rule holds): body type (glyph + label; only the body types present in the data get glyphs), hybrid (leaf glyph, shown **only** when `hybrid` is `true` — an unstated trait gets no icon, never an inferred one), seller (person = private, storefront = dealer), grade (star glyph + the exact grade), and reliability (shield glyph + `Rel x/5`). Every chip has a visible text label — meaning is never icon-only. **Clicking a chip filters the board to that trait**: it sets the matching filter control (body → `#fBody`, hybrid → `#fHybrid`, seller → `#fSeller`, grade band → `#fGrade`, reliability → `#fRel` as a minimum), active traits combine with AND alongside every other filter, clicking an active chip clears that trait, the active state shows on the chips themselves and in the filters panel + active-filter badge count, and the panel carries a **Clear all filters** button (`#fClear`). Cards carry `data-seller` and `data-rel` alongside the existing `data-*` attributes so `apply()` can test them. The chips' active state is synced from `apply()` via `window.__syncTraits(...)`; the wiring lives in its own script block after the manifest script so no preserved block moves.
- **Representative images + Visual tab (2026-11-18).** Each card face shows the record's `representative_image` (hotlinked, never a committed binary) with the caption "Representative image — not the actual car" (also the image's alt text). It is strictly separate from `photo_urls`: a representative image shows what the car model looks like, never the seller's car. A fifth tab, **Visual** (`#tabVisual`, view `#view-visual`), groups the board by model/generation with the representative image prominent and a "Show in Listings" button per group that sets the model filter and switches to the Listings tab.
- **Negotiation block (2026-11-18).** Inside each card's collapsible details, a **Negotiation** block renders the record's `negotiation_notes` — per-car pointers from its own evidence (see the schema section). It is descriptive text, so it lives in the collapsed region like the other detail lines.
- The icon/manifest and Android app-link rules above still apply unchanged.

## Publish gate — Phase 0 (owner green-lit 2026-11-04)

Added after the November 2026 development-plan review found the same car published and staged with conflicting figures. Every publish (Thursday full update or an owner-ordered out-of-cycle publish) passes this gate first:

- **Canonical key is the Marketplace item ID / URL.** Before publishing, check every staged URL against the published set and prior staging. A car that appears twice is merged into ONE canonical record with a change log in its notes (what changed, which figure superseded which, and when). Never publish two records for one item ID.
- **Source hierarchy for conflicts:** (1) the expert guide in this repo (docs/FAQ.md matrix, docs/RESEARCH.md dossiers) — the project's factory-fit and reliability authority; (2) the seller's explicit listing statements, re-read live; (3) general factory knowledge — inference only, labelled as such, never a confirmation. A staged note that contradicts the guide is an error to correct in the open, not a second truth.
- **A record may ship as "meets all must-haves" only when:** the listing is live at re-verification; the opened page matches the record's URL/ID; the model/year/trim is not excluded; the engine is known or the trim makes an excluded engine impossible; Android Auto and reverse camera are confirmed under the schema rules (matrix verdict or seller statement, per the matrix-over-seller-claim rule); the title status is not rebuilt/salvage/flood and not unknown-without-explanation; the estimate is current; and the grade recomputes from the preserved inputs under the rubric (including the current pref_score formula — no lane-assist points since 2026-11-04).
- **Blockers are shown, not buried.** Every published card lists its open verification blockers (title gaps, unconfirmed features, estimate-source gaps). When an estimate source named in the owner's criteria (e.g. CarMax) could not be obtained for a board, the stamp or headline says so plainly. A car with unresolved title evidence may remain a verification candidate but is never described as fully de-risked; physical title verification stays a purchase-stage requirement.
- **Decision note.** Each gated publish leaves a short private decision note in the goal workspace: top publishable cars, cars held back with their exact blocker, duplicate/conflict resolutions, records dropped, and any correction to something previously reported.
