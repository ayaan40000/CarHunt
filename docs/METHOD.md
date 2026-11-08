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

## Cadence (owner-set 2026-10-31)

- **Daily incremental sweeps**: rotate model families across the week, stage records into the goal's `hidden_files/staging/` (never publish), re-check exclusions and matrix gaps for new families. Pi pacing ~60 pages/hour on Facebook, ~25 pages/day. A standout find (grade A or better after a same-day estimate check) is reported the same day.
- **Thursday full update**: re-open and re-verify every staged record (dead listings dropped), run a fresh sweep of the core families, compute value estimates and grades, rebuild `index.html` + `data/listings.json`, update the data stamp, publish, verify live, and report in chat.

## Data stamp rule

Every published dashboard carries this line, visibly, at the top:

> Listings from Facebook Marketplace sweep, Oct 31, 2026 — listings sell fast; a car shown here may already be gone.

On a refresh, replace the date with the new sweep date. Never publish a dashboard without the stamp, and never mix two sweep dates in one listings file.

## Photos

The Oct 26 records carry no photo URLs, so the dashboard embeds no photos. If a future sweep records photo URLs, link/embed the URL only — never commit image binaries to this repo, and keep every file ≤ ~110 KB (files are uploaded individually).

**Photo-capture rule (2026-11-07, Phase 1):** from the next sweep onward, when a sweep opens a listing it also records up to three useful photo URLs from the listing page into `photo_urls` (exterior, dashboard/screen, rear/camera or odometer view where available) and sets `photo_checked_at` to the capture date. The Finalists view and the cards render photos when `photo_urls` is non-empty; while it is empty they show the explicit fallback: "Photos not captured yet — photo capture starts with the next sweep. Open the Marketplace listing to see photos." Never invent, guess, or hotlink a photo URL that was not captured from the listing page, and never publish a photo showing a full VIN or a title document. (Size note: with the Phase 1 cockpit inline, `index.html` is ~116 KB as of 2026-11-07 — above the ~110 KB guideline above; the single-file rule wins for now, and the parent agent's push route handles the file as-is.)

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
- The icon/manifest and Android app-link rules above still apply unchanged.

## Publish gate — Phase 0 (owner green-lit 2026-11-04)

Added after the November 2026 development-plan review found the same car published and staged with conflicting figures. Every publish (Thursday full update or an owner-ordered out-of-cycle publish) passes this gate first:

- **Canonical key is the Marketplace item ID / URL.** Before publishing, check every staged URL against the published set and prior staging. A car that appears twice is merged into ONE canonical record with a change log in its notes (what changed, which figure superseded which, and when). Never publish two records for one item ID.
- **Source hierarchy for conflicts:** (1) the expert guide in this repo (docs/FAQ.md matrix, docs/RESEARCH.md dossiers) — the project's factory-fit and reliability authority; (2) the seller's explicit listing statements, re-read live; (3) general factory knowledge — inference only, labelled as such, never a confirmation. A staged note that contradicts the guide is an error to correct in the open, not a second truth.
- **A record may ship as "meets all must-haves" only when:** the listing is live at re-verification; the opened page matches the record's URL/ID; the model/year/trim is not excluded; the engine is known or the trim makes an excluded engine impossible; Android Auto and reverse camera are confirmed under the schema rules (matrix verdict or seller statement, per the matrix-over-seller-claim rule); the title status is not rebuilt/salvage/flood and not unknown-without-explanation; the estimate is current; and the grade recomputes from the preserved inputs under the rubric (including the current pref_score formula — no lane-assist points since 2026-11-04).
- **Blockers are shown, not buried.** Every published card lists its open verification blockers (title gaps, unconfirmed features, estimate-source gaps). When an estimate source named in the owner's criteria (e.g. CarMax) could not be obtained for a board, the stamp or headline says so plainly. A car with unresolved title evidence may remain a verification candidate but is never described as fully de-risked; physical title verification stays a purchase-stage requirement.
- **Decision note.** Each gated publish leaves a short private decision note in the goal workspace: top publishable cars, cars held back with their exact blocker, duplicate/conflict resolutions, records dropped, and any correction to something previously reported.
