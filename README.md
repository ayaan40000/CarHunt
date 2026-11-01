# CarHunt — Reliable Car Under $12K Dashboard

Ayaan Pathan's used-car search dashboard: a filterable, single-file board of Houston-area listings, with an expert pursue/avoid workup, an Android Auto by year/trim matrix, and a VIN / inspection / scam guide. Every deal is graded A+ to F against a market value estimate. Updated every Thursday, with daily incremental sweeps.

**Live:** https://ayaan40000.github.io/CarHunt/

**Data stamp:** Listings from Facebook Marketplace sweep, Oct 31, 2026 — listings sell fast; a car shown here may already be gone.

## Owner's criteria

- Under $12,000 cash, no financing (private / non-dealer sellers preferred)
- Any car type — no trucks, no compact hatchbacks
- At most 100,000 miles
- Must have: factory Android Auto, reverse camera
- Preferred: gas, hybrid — Not preferred: diesel, electric, manual transmission
- Reliability first; every model reliability cross-checked; models with reliability concerns or major recalls are excluded
- Every deal graded A+ to F (A+ = great deal at a great price) against a CarMax / leading-provider value estimate — target is below estimated value

Honest headline for the Oct 31 sweep: **6 of 10 listings meet all must-haves** — led by the 2021 Kia Forte GT-Line in Katy ($9,500, 79,000 mi, grade A, 34.2% below estimate). The Oct 26 star, the 2019 Forte FE in Spring, has sold; 16 listings found this week were excluded under the reliability/title rule and are not shown. One Oct 26 listing (the 2018 Ford Fusion in Richmond) was re-verified Oct 31 and is included; the other Oct 26 listings were not re-verified and are not included.

## What's inside

| File | What it is |
|---|---|
| `index.html` | The dashboard — Listings tab (filters: max price, max mileage, model, hybrid only, Android Auto confirmed-by-matrix, meets-criteria only, underpriced only; sort by grade / price / mileage / discount) and FAQ & Help tab. Self-contained, no frameworks, works on mobile; listing text is in the page even with JavaScript off. Marketplace links open the Facebook app on Android (web fallback if the app is missing). |
| `data/listings.json` | The 10 verified Oct 31 records, fixed schema, unchanged from the sweep. |
| `docs/FAQ.md` | The same FAQ & Help content as the page, in Markdown. |
| `docs/RESEARCH.md` | Expert dossiers condensed: pursue/avoid per model-year-engine with failure modes, hybrid battery notes, Houston flood/salvage notes, recall-confirm list, AA matrix with UNVERIFIED flags. |
| `docs/METHOD.md` | How the sweep and refresh work: Pi-browser-only Facebook access + session rule, sweep method, fixed schema, matrix-over-seller-claim rule, data stamp rule, publish flow. |

Key dashboard rules: Android Auto on each card is the expert matrix verdict for that year/trim (not the seller's claim — mismatches are flagged), the underpriced flag is measured against the market estimate (median of KBB, CarGurus, Edmunds and dealer comparable figures, named per record), and every card shows its A+ to F grade from the rubric in `docs/METHOD.md`.

## How it updates

A refresh re-runs the Facebook Marketplace sweep via the Pi browser only (see `docs/METHOD.md`), replaces `data/listings.json` with the new sweep only, regenerates the dashboard, updates the data stamp date, and republishes the files to this repo. Research only — no sellers are contacted and nothing is purchased.
