# CarHunt — Reliable Car Under $15K Dashboard

Ayaan Pathan's used-car search dashboard: a filterable, single-file board of Houston-area listings, with an expert pursue/avoid workup, an Android Auto by year/trim matrix, and a VIN / inspection / scam guide. Every deal is graded A+ to F against a market value estimate. Updated every Thursday, with daily incremental sweeps. Reworked Nov 4, 2026: compact cards with collapsible details, a body-type filter, a slim control deck, a Texas paperwork tab, and the budget raised to $15,000 (see the headline below).

**Live:** https://ayaan40000.github.io/CarHunt/

**Data stamp:** Listings from Facebook Marketplace sweeps, Oct 31 – Nov 4, 2026 — reconciled Nov 4 (Phase 0); the three changed listings were re-verified live on Nov 4, and the full set is re-verified again Thu Nov 5. Estimates are medians of the providers named on each card — CarMax comparables were not available for any listing here, so no estimate on this board is a CarMax figure. Listings sell fast; a car shown here may already be gone.

## Owner's criteria

- Under $15,000 cash, no financing (private / non-dealer sellers preferred) — budget raised from $12,000 on 2026-11-04
- Any car type — no trucks, no compact hatchbacks
- At most 100,000 miles
- Must have: factory Android Auto, reverse camera
- Preferred: gas, hybrid — Not preferred: diesel, electric, manual transmission
- Reliability first; every model reliability cross-checked; models with reliability concerns or major recalls are excluded
- Every deal graded A+ to F (A+ = great deal at a great price) against a CarMax / leading-provider value estimate — target is below estimated value

Honest headline (Nov 4, 2026): **7 of 11 listings meet all must-haves** — led by the 2024 Chevrolet Malibu LT in Katy ($9,799, 52,000 mi, grade A, 42.5% below estimate), published Nov 4 at the owner's direction after live re-verification, with its title blockers stated on its card. The Nov 4 Phase 0 pass reconciled the duplicate Tomball Forte record (fresh estimate $12,072, 26.3% under) and the Richmond Sonata record (the published matrix-confirmed reading stands; a Nov 3 staged note misread the expert guide) against the expert guide, removed lane-assist points from all pref scores, and added per-record engine/title evidence and a visible Blockers line to every card. The Oct 26 star, the 2019 Forte FE in Spring, has sold; 16 listings in the Oct 31 sweep were excluded under the reliability/title rule and are not shown. One Oct 26 listing (the 2018 Ford Fusion in Richmond) was re-verified Oct 31 and is included; the other Oct 26 listings were not re-verified and are not included. The regular full Thursday publish still runs Nov 5 and re-verifies the whole set.

## What's inside

| File | What it is |
|---|---|
| `index.html` | The dashboard — Listings tab (filters: max price, max mileage, body type, model, hybrid only, Android Auto confirmed-by-matrix, meets-criteria only, underpriced only; sort by grade / price / mileage / discount), FAQ & Help tab, and a Paperwork (TX) tab with the Texas private-party buying paperwork process. Cards are compact by default — title, price, grade, deal line and the Marketplace button; all descriptive text sits behind each card's "Show details" toggle (plus a "Show all details" button), and the filters panel starts collapsed. Self-contained, no frameworks, works on mobile. Marketplace links open the Facebook app on Android (web fallback if the app is missing). Installable as a phone web app with its own icon (cream car on deep green) via an inline manifest. |
| `data/listings.json` | The 11 records (Oct 31 sweep + the Nov 4 Malibu), fixed schema plus the Phase 0 evidence fields appended 2026-11-04 (engine, title status/evidence, verification blockers, verification dates). |
| `docs/FAQ.md` | The same FAQ & Help content as the page, in Markdown. |
| `docs/RESEARCH.md` | Expert dossiers condensed: pursue/avoid per model-year-engine with failure modes, hybrid battery notes, Houston flood/salvage notes, recall-confirm list, AA matrix with UNVERIFIED flags. |
| `docs/METHOD.md` | How the sweep and refresh work: Pi-browser-only Facebook access + session rule, sweep method, fixed schema, matrix-over-seller-claim rule, data stamp rule, dashboard UI rules, Phase 0 publish gate, publish flow. |
| `docs/PAPERWORK.md` | The Texas private-party car-buying paperwork process (title transfer, Form 130-U, 6.25% tax on the greater of price or Standard Presumptive Value, 30-day filing, transfer notification) — mirrored on the dashboard's Paperwork (TX) tab. |

Key dashboard rules: Android Auto on each card is the expert matrix verdict for that year/trim (not the seller's claim — mismatches are flagged), the underpriced flag is measured against the market estimate (median of KBB, CarGurus, Edmunds and dealer comparable figures, named per record), and every card shows its A+ to F grade from the rubric in `docs/METHOD.md`.

## How it updates

A refresh re-runs the Facebook Marketplace sweep via the Pi browser only (see `docs/METHOD.md`), replaces `data/listings.json` with the new sweep only, regenerates the dashboard, updates the data stamp date, and republishes the files to this repo. Every publish passes the Phase 0 publish gate in `docs/METHOD.md` first: duplicates are reconciled by Marketplace item ID, conflicts are adjudicated against the expert guide, and every card shows its open blockers. Research only — no sellers are contacted and nothing is purchased.
