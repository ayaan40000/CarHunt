# CarHunt — Reliable Car Under $15K Dashboard

Ayaan Pathan's used-car search dashboard: a filterable, single-file board of Houston-area listings, with an expert pursue/avoid workup, an Android Auto by year/trim matrix, and a VIN / inspection / scam guide. Every deal is graded A+ to F against a market value estimate. Updated every Thursday, with daily incremental sweeps. Reworked Nov 4, 2026: compact cards with collapsible details, a body-type filter, a slim control deck, a Texas paperwork tab, and the budget raised to $15,000 (see the headline below).

**Live:** https://ayaan40000.github.io/CarHunt/

**Data stamp:** Listings from Facebook Marketplace sweeps, Nov 18, 2026 — the Thursday publish run, a day early: every board and staged record re-verified live, fresh estimates run, Phase 3 gates applied. 9 checked listings were dead and dropped (including the Nov 12 board’s #3 car, the 2024 Forte LXS); 2024–25 Elantras are held back under the Phase 3 rule (not scored yet). Estimates are medians of the providers named on each card — no estimate on this board includes a CarMax figure. Listings sell fast; a car shown here may already be gone.

## Owner's criteria

- Under $15,000 cash, no financing (private / non-dealer sellers preferred) — budget raised from $12,000 on 2026-11-04
- Any car type — no trucks, no compact hatchbacks
- At most 100,000 miles
- Must have: factory Android Auto, reverse camera
- Preferred: gas, hybrid — Not preferred: diesel, electric, manual transmission
- Reliability first; every model reliability cross-checked; models with reliability concerns or major recalls are excluded
- Every deal graded A+ to F (A+ = great deal at a great price) against a CarMax / leading-provider value estimate — target is below estimated value

Honest headline (Nov 18, 2026): **39 of 47 listings meet all must-haves** — led by a 2018 Chevrolet Malibu 1LT in Houston ($5,000, 85,000 mi, grade A, 51.5% below estimate) and the 2024 Chevrolet Malibu LT in Katy ($9,799, 52,000 mi, grade A, 46.4% below estimate). The Nov 12 board’s #3 car, the 2024 Forte LXS, is dead and dropped; a new 2024 Forte LXS in Houston ($10,200, grade A) takes its place after the mandatory camera check. Fusion, Accord and Civic were swept fresh today and produced no new shippable car. 2024–25 Elantras are held back under the Phase 3 rule — they are not scored yet. No estimate on this board includes a CarMax figure.

## What's inside

| File | What it is |
|---|---|
| `index.html` | The dashboard — Listings tab (filters: max price, max mileage, body type, model, hybrid only, Android Auto confirmed-by-matrix, meets-criteria only, underpriced only; sort by grade / price / mileage / discount), a Finalists tab (added 2026-11-07, Phases 1–2: a comparison strip for the top 3 must-have cars plus a per-finalist buying cockpit — VIN-check workflow, copy-ready seller message, all-in Texas cash estimator, tailored test-drive/PPI checklist), FAQ & Help tab, and a Paperwork (TX) tab with the Texas private-party buying paperwork process. Every card also carries freshness and estimate-confidence tags (Phase 2). Cards are compact by default — title, price, grade, deal line and the Marketplace button; all descriptive text sits behind each card's "Show details" toggle (plus a "Show all details" button), and the filters panel starts collapsed. Self-contained, no frameworks, works on mobile. Marketplace links open the Facebook app on Android (web fallback if the app is missing). Installable as a phone web app with its own icon (cream car on deep green) via an inline manifest. |
| `data/listings.json` | The 47 records (Nov 18, 2026 full re-verification + fresh sweep), fixed schema plus the Phase 0 evidence fields appended 2026-11-04 (engine, title status/evidence, verification blockers, verification dates) and the Phase 1/2 fields appended 2026-11-07 (photo URLs, price history, estimate components, estimate confidence, CarMax note). |
| `docs/FAQ.md` | The same FAQ & Help content as the page, in Markdown. |
| `docs/RESEARCH.md` | Expert dossiers condensed: pursue/avoid per model-year-engine with failure modes, hybrid battery notes, Houston flood/salvage notes, recall-confirm list, AA matrix with UNVERIFIED flags. Phase 3 (2026-11-17) added full gate packs for the 2020+ Sonata, 2021+ Elantra, Kia K5, 2021+ Malibu, and all seven SUV/crossover families. |
| `docs/METHOD.md` | How the sweep and refresh work: Pi-browser-only Facebook access + session rule, sweep method, fixed schema, matrix-over-seller-claim rule, data stamp rule, dashboard UI rules, Phase 0 publish gate, publish flow. Phase 3 (2026-11-17) added the non-Facebook source rules: Carvana adopted for search-results screening (records carry a `listing_source` field), five sources evaluated and rejected with reasons, and cross-source duplicate detection. |
| `docs/PAPERWORK.md` | The Texas private-party car-buying paperwork process (title transfer, Form 130-U, 6.25% tax on the greater of price or Standard Presumptive Value, 30-day filing, transfer notification) — mirrored on the dashboard's Paperwork (TX) tab. |

Key dashboard rules: Android Auto on each card is the expert matrix verdict for that year/trim (not the seller's claim — mismatches are flagged), the underpriced flag is measured against the market estimate (median of KBB, CarGurus, Edmunds and dealer comparable figures, named per record), and every card shows its A+ to F grade from the rubric in `docs/METHOD.md`.

## How it updates

A refresh re-runs the Facebook Marketplace sweep via the Pi browser only (see `docs/METHOD.md`), replaces `data/listings.json` with the new sweep only, regenerates the dashboard, updates the data stamp date, and republishes the files to this repo. Every publish passes the Phase 0 publish gate in `docs/METHOD.md` first: duplicates are reconciled by Marketplace item ID, conflicts are adjudicated against the expert guide, and every card shows its open blockers. Since Phase 3 (2026-11-17), Carvana search results are also screened as a supplementary source; Carvana candidates are staged as sourced-unverified and are re-verified in a live browser on Thursdays before they can ship. Research only — no sellers are contacted and nothing is purchased.
