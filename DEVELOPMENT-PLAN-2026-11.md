# CarHunt — Development Plan

**Prepared:** November 3, 2026  
**Status:** Plan only — no dashboard, data, GitHub, or seller changes are authorized by this document.  
**Product:** CarHunt, Ayaan Pathan's used-car deal dashboard  
**Live dashboard:** https://ayaan40000.github.io/CarHunt/  
**Repository:** `ayaan40000/CarHunt`  
**Local source reviewed:** `~/workspace/reserved-1/`  
**Goal record reviewed:** `~/workspace/goals/reliable-car-under-12k/`

## Executive recommendation

CarHunt does not need a broad rebuild. It needs to become more reliable at the exact moment it matters: deciding which one or two cars deserve a viewing, an inspection, and cash.

The immediate priority is not more listings or a prettier board. It is **record truth**:

- reconcile duplicate and conflicting records before the Thursday, November 5 publish;
- make title, engine, Android Auto, camera, estimate, and liveness evidence structured and visible;
- stop any standout from publishing until its blockers are cleared;
- then turn each finalist card into a buying cockpit with photos, VIN-check actions, seller questions, an all-in cost estimate, and a tailored test-drive/PPI checklist.

The search ends when Ayaan buys a car. The plan therefore gives most weight to the next publish and the next viewing decision, not to building a long-lived car-market platform.

### Recommended sequence

1. **Phase 0 — Publish gate and record truth** — immediate, before the Thursday publish. **Done 2026-11-04.**
2. **Phase 1 — Finalist buying cockpit** — next; photos, VIN workflow, seller-question prep, all-in cost, tailored checklist. **Built 2026-11-07 (local build; see the Phase 1 status note).**
3. **Phase 2 — Freshness and estimate confidence** — basic stale checks first; deeper estimate automation only if the search continues. **Built 2026-11-07 (local build; see the Phase 2 status note).**
4. **Phase 3 — Coverage only where it can still matter** — complete blocked matrix families and selected non-Facebook sources if the first shortlist does not produce a purchase. **Built 2026-11-17 (owner's repo-development order of Nov 17; see the Phase 3 status note).**
5. **Phase 4 — Buy, close, and archive** — triggered by a chosen car; finish the transaction cleanly and stop the search machinery.

---

# 1. Current-state review

## 1.1 What exists now

CarHunt is a self-contained, single-file HTML dashboard backed by a fixed-schema JSON file.

### Published product

- `index.html` contains:
  - a Listings view with 10 cards;
  - filters for maximum price, maximum mileage, model, hybrid only, matrix-confirmed Android Auto, meets-criteria only, and underpriced only;
  - sorting by grade, price, mileage, discount, and legacy preference score;
  - an FAQ & Help view covering pursue/avoid guidance, the Android Auto matrix, VIN checks, PPI, and scam red flags;
  - Android Facebook-app intent links with web fallback;
  - the required inline SVG icon, Apple touch icon, theme colour, and generated inline manifest.
- `data/listings.json` contains the same 10 records in the fixed schema.
- `docs/FAQ.md`, `docs/RESEARCH.md`, and `docs/METHOD.md` preserve the buyer guidance, model dossiers, Android Auto matrix, exclusion rules, estimate method, grading rubric, and publish process.
- The current published set is from the October 31, 2026 sweep:
  - 6 records meet all must-haves;
  - 4 are context/verification candidates capped at C+;
  - grades are three A, three A-, and four C+;
  - 9 are private-seller listings and 1 is a dealer listing.

### Operating system around the dashboard

- Daily sweeps rotate model families and stage records in the goal's `hidden_files/staging/`; they do not publish.
- The Thursday run is supposed to re-open and re-verify every staged record, drop dead listings, calculate fresh estimates and grades, rebuild, publish, verify live, and report.
- Facebook Marketplace access is Pi-browser only, using the existing session, with pacing around 60 pages/hour and about 25 pages/day.
- A grade A-or-better candidate can be reported the same day, but reporting is not publishing; Thursday re-verification remains the gate.

### Research assets already available

The FAQ and research documents are unusually strong for a small dashboard:

- pursue/avoid dossiers by model, year, and engine;
- known failure modes and approximate repair exposure;
- hybrid-battery expectations;
- Houston flood and title-washing guidance;
- recall-confirmation lists;
- an Android Auto matrix with UNVERIFIED cells;
- a sensible VIN-check order;
- a generic PPI checklist and Marketplace scam guide.

The main product gap is that much of this knowledge remains prose. It is not yet attached to each candidate as a short, structured “what blocks this car?” workflow.

## 1.2 What is stale

### The published board is already ageing

The live data stamp is October 31, 2026. That is correct under the data-stamp rule, but by November 3 the board is three days old in a market where the method itself warns that listings sell fast. Its value now depends entirely on the November 5 re-verification, not on the October 31 grades remaining current.

### The November 3 Tomball Forte is not a new find

The staged standout at:

`https://www.facebook.com/marketplace/item/1625691275824447/`

is already published as the 2020 Kia Forte LXS in Tomball. The two records differ:

| Field | Published Oct 31 record | Staged Nov 3 record |
|---|---:|---:|
| Asking price | $8,900 | $8,900 |
| Mileage | 31,000 | 31,000 |
| Estimate | $11,650 | $12,072 |
| Discount | 23.6% | 26.3% |
| Grade | A | A |
| Evidence emphasis | Seller states engine, cameras, AA, warranty | Seller states AA and rear/front cameras; title, warranty, trim spelling, and anti-theft note remain cautions |

This should be treated as a **recheck of an existing published car with a refreshed estimate**, not as inventory growth. Thursday needs a duplicate-resolution rule so the same URL cannot be counted or described twice.

### The staged Sonata directly conflicts with the published Sonata

The same listing:

`https://www.facebook.com/marketplace/item/2099246277666831/`

appears in both the published set and November 3 staging with materially different conclusions:

| Field | Published Oct 31 record | Staged Nov 3 record |
|---|---|---|
| Meets criteria | `true` | `false` |
| Android Auto | `true` | `null` |
| Reverse camera | `true` | `true` |
| Reliability | 4 | 3 |
| Estimate | $14,300 | none — capped before estimate |
| Grade | A- | capped at C+ until AA is confirmed |
| Matrix basis | Published notes say AA is standard on 2022 Sonata SE/SEL | Staging says the goal notes have no 2020+ Sonata matrix row |

The FAQ matrix does state “2020+: AA standard all trims” for Sonata. Therefore the conflict is not simply “one record is wrong.” It exposes inconsistent source hierarchy among the FAQ, research notes, goal notes, and staging judgment. Thursday must adjudicate it explicitly:

- Is the FAQ/research matrix an authoritative goal matrix row for 2020+ Sonata?
- If yes, staging should inherit the verdict and explain why the November 3 cap was applied.
- If no, the published record's basis needs correction before it is carried forward.

No other feature matters more than resolving this class of conflict. A dashboard that simultaneously calls the same car A- and capped-C+ will lose trust exactly when Ayaan needs a decision.

## 1.3 Data-quality gaps verified in the files

### A. Title evidence is prose, not a field

There is no structured `title_status`, `title_evidence`, or `title_checked_at` field.

In the published set:

- 7 of 10 notes explicitly say the title is not stated, not explicitly clean, or must be physically verified;
- Facebook “clear history” is repeatedly—and correctly—not treated as proof of a clean Texas title brand;
- staged exclusions show why this matters: multiple otherwise attractive cars were excluded only after the seller's text revealed a rebuilt title, including one in Spanish.

**Implication:** title is currently the single largest hidden blocker. It should be a first-class publish gate, not a sentence buried in notes.

### B. Engine evidence is not structured

The fixed schema has no `engine` or `engine_evidence` field, even though engine identity determines several exclusions.

Published examples:

- three Fusion/Elantra records require engine or recall verification in prose;
- the 2018 Fusion with unstated trim could carry the excluded 1.5L EcoBoost;
- the 2020 Fusion could also carry the excluded 1.5L EcoBoost;
- staged records repeatedly distinguish Smartstream from Theta II in notes rather than data.

**Implication:** the sweep can accidentally grade an attractive car before proving it is not an excluded-engine car. Engine should be captured as structured evidence with values such as `seller-stated`, `VIN-decoded`, `photo-verified`, `inferred-from-trim`, or `unknown`.

### C. Must-have confirmation is incomplete on the context records

Published counts:

- Android Auto: 6 confirmed, 3 `null`, 1 confirmed absent;
- reverse camera: 8 confirmed, 2 `null`;
- 4 of 10 records do not meet all criteria.

That is honest and the C+ cap is working. The weakness is workflow: the dashboard does not turn each `null` into a specific next proof, such as “photo of the 8-inch screen,” “seller confirms engine,” or “plug-test required.” The buyer sees a blocker but not a compact resolution path.

### D. CarMax is absent from the published estimate sources

The owner's criteria call for CarMax plus other leading providers. In the published data:

- **0 of 10** `estimate_sources` values name CarMax;
- the sources are KBB, CarGurus, Edmunds, iSeeCars, and dealer comparables.

The November 2 staged Civic does include a CarMax figure, but it is described as a **CarMax recent offer**, not a comparable CarMax asking price. That should not silently be treated as the same kind of evidence as a retail comparable.

**Implication:** the current board should be described accurately: its published estimates are leading-provider medians without CarMax. Either obtain a genuine CarMax comparable set for finalists or revise the estimate label/method so the dashboard does not imply a source it did not use.

### E. The estimate median mixes unlike measures

Current estimates combine some or all of:

- Fair Purchase Price;
- resale value;
- trade-in value;
- retail value;
- model-average asking price;
- a specific dealer comparable.

Those are not interchangeable measures of the same market value. A median of retail, resale, and trade-in figures can create false precision.

Other estimate weaknesses:

- the same $14,440 estimate is used for two 2021 Forte GT-Line cars at 79,000 and 35,000 miles, so the estimate is not sufficiently mileage-specific;
- some records use a trim proxy because the actual trim is unknown;
- no structured fields preserve each component figure, its date, its mileage basis, or the spread between low and high estimates;
- no confidence rating distinguishes “three close, current, same-trim figures” from “three unlike figures with a proxy trim.”

**Implication:** grades look more exact than the evidence supports. A range and confidence label would be more truthful and more useful than another decimal place.

### F. Reliability scores use an undocumented fractional step

The rubric explicitly describes adjustments for reliability 5, 3, and 2-or-below. The data repeatedly uses **3.5**, including five published records. That may be reasonable expert judgment, but the method does not explain:

- what 3.5 means;
- whether it receives no adjustment, half an adjustment, or a rounded adjustment;
- which source hierarchy governs when published and staged records assign 4 and 3 to the same model.

**Implication:** define 3.5 explicitly or stop using it. Do not change historical grades silently; document the interpretation before the next rebuild.

### G. Lane assist is dropped from the criteria but still carried as scoring residue

The October 31 criteria dropped lane assist. Nevertheless:

- `lane_assist` remains in the schema;
- cards display it;
- `pref_score` still awards +2 for it;
- the dashboard still offers “Pref score” sorting;
- staged standouts discuss lane-keeping even when the field is `null`.

Keeping the raw observation is harmless. Giving it points and visual prominence is criteria drift. Lane assist should become informational only—no preference points and no role in ranking—unless Ayaan explicitly re-adds it.

### H. No lifecycle or freshness fields

Records have no:

- `first_seen_at`;
- `last_seen_at`;
- `last_verified_at`;
- `listing_status` (`live`, `sold`, `removed`, `unreachable`, `unknown`);
- price history;
- seller/listing age in structured form;
- duplicate-group identifier.

The global data stamp is not enough. A 7-week-old Forte and a 12-week-old Sonata appear in staging notes, but the board itself cannot show age, price movement, or last successful check per car.

### I. No photo or VIN workflow fields

`METHOD.md` records that the current sweep carried no photo URLs. The published dashboard therefore has no listing photos.

The schema also has no VIN field or VIN-status field. That is privacy-safe, but it means the existing FAQ's excellent VIN sequence cannot be attached to a finalist as a checklist. Some staged exclusions include full VINs in prose notes; those staged notes must never be copied into the public dashboard merely to enable a VIN feature.

### J. Coverage is narrower than the stated search scope

The goal says the search scope includes CarMax, Carvana, Facebook Marketplace, OfferUp, rental-car sellers, Costco Auto, Autotrader, and Cars.com where useful. The operating method and published board are effectively **Facebook-listing only**, with other sites used for value figures.

That may be the right practical scope, but the product should not imply broader listing coverage than it performs. Either:

- label the current scope honestly as Facebook-first; or
- deliberately add a small number of non-Facebook finalist/source checks in a later phase.

### K. Family and matrix coverage lag the rotation

The dashboard model filter contains only Ford Fusion, Hyundai Elantra, Hyundai Sonata, and Kia Forte—the models in the current published set.

Known matrix/coverage friction includes:

- SUV/crossover families were added to scope on October 31 but have produced no published listings; each still needs matrix and reliability gating;
- staging notes treat 2021 and 2024 Elantra rows as absent;
- staging and the FAQ conflict over whether 2020+ Sonata is an authoritative matrix row;
- several expert-matrix cells remain UNVERIFIED by design and require an in-person check.

This is manageable if the rotation refuses to publish a family until its gate exists. It becomes fragile when prose notes in different files disagree about whether the gate exists.

## 1.4 Technical and process fragility

### The dashboard duplicates the data

Listing content exists both in `data/listings.json` and as baked HTML cards. The October 31 generator lives in the goal's `hidden_files/`, not in the repository, and contains:

- hard-coded records;
- hard-coded local paths;
- date-specific string replacements;
- one-off headline and matrix edits.

That worked for a single rebuild, but it is not a durable generator. A future operator must know that the hidden build script exists and which parts were one-off. Any new fields or card features should move generation toward a checked-in, repeatable builder rather than another one-off patch.

### The fixed schema is both a strength and a constraint

The schema protects dashboard compatibility. It also means useful evidence cannot be added casually. The method says to append fields, never remove or reorder originals. Every phase below respects that rule.

### Facebook access is a single fragile channel

Observed operational constraints include:

- Pi browser only;
- existing-session dependence;
- bot-check escalation;
- SSH host-key failure after a Pi restart during the November 3 sweep;
- Marketplace URL price/mileage parameters returning false “no listings” results;
- search-result cards occasionally leading to a different listing than the visible result;
- listing IDs therefore need verification against the opened page.

A development plan that assumes a stable Facebook API or unlimited browsing would be fantasy. CarHunt must remain a paced, human-supervised research system.

### The public dashboard limits what can be stored

CarHunt is publicly served from GitHub Pages. It must not publish:

- full VINs;
- title-document photos;
- seller phone numbers or private contact details;
- private negotiation notes;
- inspection reports containing personal information.

A finalist workflow can store workflow state locally or in the private goal workspace, but public cards should carry only safe status labels such as “VIN checks complete” or “title brand physically verified,” never the underlying private evidence.

---

# 2. Phased development plan

## Phase 0 — Publish gate and record truth

**Timing:** Immediate; complete before the Thursday, November 5, 2026 publish.  
**Rough effort:** 0.5–1 focused agent day, plus the normal Thursday verification workload.  
**Purpose:** Prevent a duplicate, conflicting, or unverified car from being published with a confident grade.

### Scope

1. **Canonical-record reconciliation**
   - Use Marketplace item ID/URL as the canonical key.
   - Merge the published and staged Tomball Forte into one working record with a change log for estimate and evidence changes.
   - Adjudicate the Sonata matrix/reliability conflict and record the source hierarchy used.
   - Check every staged URL against the published set and prior staging before Thursday.

2. **Append-only evidence fields**
   Add fields after the existing schema fields; do not remove or reorder current fields:
   - `engine`
   - `engine_evidence`
   - `title_status` (`clean-stated`, `paid-off-only`, `clear-history-only`, `rebuilt`, `salvage`, `flood`, `unknown`, `physically-verified-clean`)
   - `title_evidence`
   - `verification_blockers` (short structured list)
   - `first_seen_at`
   - `last_seen_at`
   - `last_verified_at`
   - `listing_status`
   - `duplicate_of` or `duplicate_group`

3. **Publish-gate checklist**
   A record cannot ship as “meets all must-haves” unless:
   - listing is live at re-verification;
   - URL/ID matches the opened page;
   - model/year/trim is not excluded;
   - engine is known or the trim makes the excluded engine impossible;
   - Android Auto and reverse camera satisfy the schema's confirmation rules;
   - title status is not rebuilt/salvage/flood or unknown-without-explanation;
   - estimate is current enough for Thursday;
   - grade can be recomputed from preserved inputs.

   A car with unresolved title evidence may remain a verification candidate, but it must not be described as fully de-risked. Physical title verification remains a purchase-stage requirement.

4. **Thursday decision output**
   Produce a one-page private decision note for the publish run:
   - top three publishable cars;
   - cars held back and the exact blocker for each;
   - duplicate/conflict resolutions;
   - records dropped as dead or excluded;
   - any standout whose same-day report needs correction.

### Deliverables

- Reconciled working set for November 5.
- Updated method note defining duplicate handling and source hierarchy.
- Append-only schema proposal implemented in the working data, if the Thursday builder is ready; otherwise a private verification table that maps cleanly onto those fields.
- Publish-gate checklist used by the Thursday run.
- A short correction note if the Tomball Forte or Sonata interpretation changes what was previously reported.

### Dependencies

- Pi-browser access for live re-verification.
- Owner's existing criteria and grading rubric; no new owner decision is needed except the estimate-source question in Phase 2 if CarMax remains unavailable.

### Done looks like

- No URL appears twice under different conclusions.
- Every published or held record has explicit title, engine, must-have, estimate, and liveness states.
- The November 5 dashboard contains only records that passed the gate.
- The two current standouts are described accurately:
  - Civic: staged and unpublished until live, photo/car, and title checks pass;
  - Tomball Forte: an existing published car rechecked with a refreshed estimate, not a second discovery.

---

## Phase 1 — Finalist buying cockpit

**Status: BUILT 2026-11-07** (owner green-lit Nov 7; local build in the working tree, direct edit of `index.html` + appended fields in `data/listings.json` — no separate generator was introduced, and docs/METHOD.md now carries the regeneration contract a Thursday rebuild must follow). Live now: the Finalists tab with the comparison strip (data-driven top 3 by grade then discount; viewing order Forte LXS → Malibu → GT-Line Katy, reasons on the page), the VIN workflow (the VIN is never stored), copy-ready seller scripts generated from each finalist's blockers, the all-in cash estimator at the $15,000 budget frame, and the tailored checklists. **Starts with the next sweep:** photo capture — `photo_urls` is empty on every record and `photo_checked_at` is null, so the photo area shows the explicit fallback line until a sweep captures photo URLs from the listing pages. The plan text below still shows the old $12,000 frame in two places; the build uses $15,000 throughout.

**Timing:** Immediately after Phase 0; build only for cars that survive the publish gate.  
**Rough effort:** 1–2 focused agent days.  
**Purpose:** Turn the top two or three cards into everything Ayaan needs before contacting a seller or travelling to a viewing.

### Scope

1. **Listing-photo display**
   - Append `photo_urls` and `photo_checked_at` to working records.
   - Show up to three useful photos per finalist: exterior, dashboard/screen, and rear/camera or odometer view where available.
   - Link/embed URLs only; never commit Marketplace image binaries to the repo.
   - Keep a clear fallback: “Photos unavailable — open the Marketplace listing.”
   - Do not publish photos showing a full VIN or title document.

2. **Finalist comparison strip**
   - Compare up to three finalists side by side on:
     - asking price;
     - mileage;
     - grade and estimate range;
     - title/engine/AA/camera blockers;
     - seller type and listing age;
     - estimated all-in cash;
     - next action.
   - The comparison should answer “which car do I see first?” in under a minute.

3. **VIN-check launcher and evidence checklist**
   - Do **not** store a full VIN in the public repo or dashboard.
   - Provide a finalist workflow in the private goal workspace or browser-local state:
     - Ayaan pastes the VIN locally;
     - copy-VIN button;
     - open NHTSA VIN Decoder;
     - open NHTSA Recalls;
     - open NICB VINCheck;
     - open the TxDMV/NMVTIS title-check route described in the FAQ;
     - record only status/date/result labels, not the VIN itself, in any persistent shared record.
   - Show what each check proves and does not prove, using the FAQ's existing language.

4. **Seller-contact prep — scripts only**
   Generate a copy-ready message tailored to the blockers on that car. The agent does not send it.
   
   Base questions:
   - Is the car still available?
   - What is the VIN?
   - Is the title in your name, in hand, and what brand is printed on it?
   - What engine is fitted?
   - Can you send a photo of the dashboard screen and the car starting cold?
   - Has Android Auto been used with a cable in this car?
   - Are there open recalls or warning lights?
   - Will you allow a pre-purchase inspection at my mechanic?
   
   Tailored additions:
   - Elantra: proof that NHTSA 21V-301 was completed;
   - Fusion: engine and 8-inch SYNC 3 proof;
   - Civic: A/C performance and condenser-warranty history;
   - hybrid: battery-health/service evidence;
   - any car: title-jumping and curbstoner checks from the FAQ.

5. **All-in cash estimator**
   Show asking price separately from estimated cash needed:
   - asking price;
   - Texas vehicle sales-tax estimate, using editable assumptions and a warning that taxable value can be based on standard presumptive value rather than a low sale price;
   - title/registration/transfer estimate or county-specific input;
   - dealer document/processing fees only when the seller is a dealer;
   - PPI allowance of $100–$150 from the FAQ;
   - title/history allowance: NMVTIS/TxDMV route about $10–$20; one paid finalist report allowance using the FAQ's Carfax (~$45–$50) or AutoCheck (~$25–$30) figures;
   - immediate-repair reserve entered after PPI, initially shown as “unknown — not $0”;
   - insurance change as a manual quote input only; do not invent a premium.
   
   Output:
   - estimated cash needed before repairs;
   - headroom against the $12,000 car-price budget;
   - a separate warning if likely transaction costs push total cash above $12,000 even though the asking price qualifies.

6. **Tailored test-drive and PPI checklist**
   Convert the generic FAQ checklist into a per-car printable/mobile checklist:
   - universal cold-start, fluid, lift, flood, A/C, road-test, and title/VIN-match items;
   - Android Auto plug test with Ayaan's phone and a known-good data cable;
   - reverse-camera test;
   - model-specific checks from `RESEARCH.md`;
   - “walk away now” triggers at the top;
   - space for PPI findings and immediate-repair prices, kept private.

### Deliverables

- Photo-enabled finalist cards or a private finalist view if public photo URLs prove unstable.
- A reusable finalist template.
- VIN checklist with safe local handling.
- Tailored seller-question script generator or template.
- All-in cost calculator with editable assumptions.
- Per-car test-drive/PPI checklist.

### Dependencies

- Phase 0 evidence fields and adjudicated records.
- Photo URL availability from the Pi sweep.
- Ayaan supplies a VIN only when he chooses a finalist; no VIN is needed to build the workflow.

### Done looks like

For any finalist, Ayaan can answer in one place:

- Why this car?
- What is still unproven?
- What will it likely cost in total cash?
- What exactly should I ask the seller?
- What should I test first?
- What result makes me walk away?

---

## Phase 2 — Freshness and estimate confidence

**Status: BUILT 2026-11-07** (owner green-lit Nov 7; local build, same change set as Phase 1). Live now: freshness tags and detail lines on every card (checked date, first-seen age, price history labelled as starting with our records), `price_history` seeded only with on-record prices (one documented change: 2021 Forte LXS Houston $9,550 → $9,000), `estimate_components` parsed from the figures already recorded in each record's notes (every component set's median reproduces the published estimate exactly), and `estimate_confidence` under the rule now documented in docs/METHOD.md — on the Nov 5 board: 0 High, 10 Medium, 5 Low, honestly applied; grades unchanged. The CarMax policy is documented in docs/METHOD.md (an offer is a liquidation reference, not a retail comparable; only the 2019 Forte's estimate includes one, and its record says so). **Not built:** the semi-automated estimate-capture form (Phase 2 item 5) and any scraper — deliberately left out, per this plan's own warning against automating the mixed-median method before the component model has run for a cycle; the Thursday operator still captures components by hand into the notes, and they are parsed into `estimate_components` at build time.

**Timing:** Start with the lightweight version in the first week; deepen only if no purchase follows the first finalist round.  
**Rough effort:** 2–4 focused agent days spread across one to two weeks.  
**Purpose:** Reduce the chance that Ayaan acts on a sold car, a changed price, or a falsely precise grade.

### Scope

1. **Lightweight stale-listing detection**
   - Daily verification queue ordered by decision value, not by rotation alone:
     1. published cars that meet all must-haves;
     2. staged A/A- candidates;
     3. unconfirmed cars whose blocker could be resolved from the listing;
     4. context cars.
   - Record `listing_status`, `last_seen_at`, price, mileage, and title/feature text at each check.
   - Badge records as `Checked today`, `Checked Thu`, `Price changed`, `Possibly sold`, or `Removed`.
   - A removed/sold result should hide the car from the active board but preserve it in the private history.

2. **Price and evidence history**
   - Append a compact private history per canonical listing ID:
     - date;
     - live/dead;
     - asking price;
     - mileage if changed;
     - new title/engine/feature evidence;
     - estimate version.
   - Surface only meaningful changes on the dashboard: price drop, price rise, newly confirmed feature, newly discovered exclusion.

3. **Structured estimate components**
   Replace the single opaque estimate basis with an append-only `estimate_components` structure in working data:
   - provider;
   - figure;
   - figure type (`asking`, `fair-purchase`, `retail`, `resale`, `trade-in`, `offer`);
   - year/trim used;
   - mileage of the comparable or valuation;
   - mileage difference from the candidate;
   - date captured;
   - source URL or private capture note.

4. **Estimate confidence**
   - Show a range and confidence label:
     - **High:** at least three current, same-trim, mileage-close figures of compatible type;
     - **Medium:** usable figures but one proxy, stale input, or wide spread;
     - **Low:** mixed valuation types, major mileage mismatch, unknown trim, or only one credible source.
   - Grade from the central estimate, but display the range so a big discount does not hide uncertainty.
   - Decide explicitly whether a CarMax “recent offer” belongs in the same median as retail asking figures. Recommended default: show it separately as a liquidation/offer reference, not as a retail comparable.

5. **Semi-automated estimate capture**
   - Build a capture form/checklist for the Thursday operator: provider, figure type, trim, mileage, date, and URL.
   - Let a script validate completeness, calculate the chosen central estimate, preserve the spread, and recompute discount/grade.
   - Do not begin with unrestricted scraping of KBB, CarMax, Edmunds, or CarGurus. Those sources can be login-, bot-, or terms-sensitive, and a wrong automated figure is worse than a slower manual one.

### Deliverables

- Freshness queue and per-record status/history.
- Dashboard freshness badges.
- Structured estimate component capture.
- Estimate range/confidence display.
- A documented CarMax policy: genuine comparable, separate offer reference, or unavailable.

### Dependencies

- Phase 0 canonical IDs and lifecycle fields.
- A repeatable builder rather than one-off HTML replacement.
- Pi-browser pacing remains the limiting factor for Facebook liveness checks.

### Done looks like

- No active card is silently more than one publish cycle old.
- A price or status change is visible and dated.
- Every grade can be traced to dated estimate components.
- Ayaan can see whether a “42% under” claim is strong evidence or a wide, mixed-source estimate.

---

## Phase 3 — Coverage only where it can still matter

**Timing:** Later; start only if Phases 0–2 do not produce a purchasable car, or if a blocked family is strategically important.  
**Rough effort:** 3–5 focused agent days spread over several sweep cycles.  
**Purpose:** Expand the candidate pool without weakening the exclusion, matrix, or title gates.

**Status: BUILT 2026-11-17** (owner's repo-development order of Nov 17, 2026; docs-only build — no dashboard or listing-data change; the Thursday update remains the publish gate). What shipped: (1) **Matrix gates completed.** The 2020+ Sonata authority conflict is resolved with one verdict everywhere — the FAQ row stands, now sourced: AA + camera standard on all DN8 trims/years, and the published 2022 SEL reliability 4 is confirmed (RepairPal 4.0/5) with an oil-history condition and an engine split (1.6T = 3 with recall 25V-796 as a hard gate; Hybrid = 3; N Line = project avoid). A dated addendum in the expert guide carries the new rows so sweeps stop recording "no row exists." 2021+ Elantra rows added before any grading (8-inch = wireless, 10.25-inch = wired; 2024 SEL wired change noted): gas cars score 3 (2021–22) / 4 (2023), Hybrid 4, with the IVT caution, the pretensioner/camera recall stack, and a Campaign 993 theft gate for key-start 2021–22 cars. Kia K5 (DL3a — not DN8) and Malibu 2021+ rows added on the same pass (both were blocking real records: a staged K5, and the published board's #1 car, whose AA/camera are now verified from GM's own 2024 media sheet; Malibu 2021+ scores 3 with the CVT caution and the 2023–25 camera recall as a blocker). SUV/crossover rows completed family by family — RAV4, CR-V, CX-5, Tucson, Sportage, Forester, Outback — reconciled from the November 2026 SUV research notes into docs/RESEARCH.md and docs/FAQ.md, not re-researched. (2) **Reliability gate packs** for every new family in docs/RESEARCH.md: pursue/avoid years+engines, recall-confirm lists, hybrid-battery notes (Sonata/Elantra/RAV4/CR-V hybrids), model-specific cautions, and UNVERIFIED cells flagged as such (no CR score is used for DN8/CN7; no failure rate is quoted for the Elantra IVT or Malibu CVT — none exists in the sources). (3) **Non-Facebook sources evaluated one at a time** (full evidence in the goal workspace, `hidden_files/phase3-work/source-yield.md`): **Carvana ADOPTED for search-results screening only** (method, record-carrying, and Thursday live-browser re-verification documented in docs/METHOD.md; schema gained one appended field, `listing_source`, absence = Facebook Marketplace; two SRP-level Forte candidates staged as sourced-unverified, not published). **Rejected with concrete reasons:** CarMax (inventory unreadable via web access; eligible families price above frame), Hertz (Houston search returns no assignable listings), Enterprise (pages strip to footer), OfferUp (Houston inventory not searchable; title unassessable), Cars.com/Autotrader (not discoverable / taxonomy-only extraction) — several rejections are web-text readability limits, recorded as such in METHOD.md, not proof of empty inventory. (4) **Cross-source duplicate detection** documented in docs/METHOD.md (VIN in private data only; otherwise similarity as a warning; "also listed elsewhere" only on a reliable match). The plan text's "under $12,000" source test is superseded by the owner's 2026-11-04 budget raise — sources were judged against the $15,000 frame. **Not done / left open:** Sportage 2023+ reliability score (assign before staging one), CR-V 2023+ gas and CX-5 diesel decisions (explicitly undecided in RESEARCH.md), Elantra 2024–25 scores, and any live-browser re-test of the rejected sources.

### Scope

1. **Complete the matrix gates for active rotation families**
   Priority order should follow likely value, not alphabetical completeness:
   - explicitly resolve 2020+ Sonata authority across FAQ, research, and goal notes;
   - add or verify 2021+ Elantra rows before grading those cars;
   - avoid grading 2024 Elantra from inference until its row exists;
   - complete SUV/crossover rows family by family before any SUV is published: RAV4, CR-V, CX-5, Tucson, Sportage, Forester, Outback.

2. **Reliability gate pack per new family**
   Before the first listing from a family can ship, create:
   - pursue/avoid years and engines;
   - recall-confirm list;
   - hybrid-battery note if applicable;
   - flood/title cautions specific to the model;
   - AA matrix source and UNVERIFIED cells.

3. **Selected non-Facebook listing sources**
   Add sources one at a time, with the source named in the record:
   - CarMax and Carvana comparable or sale listings;
   - Hertz/Enterprise rental-car sales;
   - OfferUp only if identity/title quality can be assessed;
   - Autotrader/Cars.com dealer listings where they add a genuinely different car.
   
   Do not scrape every source merely because the goal lists it. A source earns a place only if it produces eligible, verifiable candidates under $12,000.

4. **Cross-source duplicate detection**
   Match by VIN when safely available in private working data; otherwise use year/trim/price/mileage/location/photo similarity as a warning, not proof.
   
   The public record should show “also listed elsewhere” only when the match is reliable.

### Deliverables

- Matrix/reliability gate pack for each newly activated family.
- A source-by-source yield note: eligible cars found, exclusions, dead ends, and operator time.
- Duplicate warnings across sources where evidence is strong.

### Dependencies

- Phases 0 and 2, so new coverage does not multiply conflicting records.
- Pi-browser or other permitted access routes for each source.
- Research time for model dossiers before sweep time.

### Done looks like

- Every published family has an explicit matrix and reliability gate.
- Every non-Facebook source in use has produced enough eligible candidates to justify its operator time.
- No family is graded from an inferred matrix row without the inference being labelled and capped.

---

## Phase 4 — Buy, close, and archive

**Timing:** Triggered when Ayaan selects a car.  
**Rough effort:** 0.5–1 focused agent day, plus Ayaan's in-person steps.  
**Purpose:** Convert a good dashboard decision into a clean purchase and then stop the search.

### Scope

1. **Purchase-day packet**
   - Finalist summary and agreed maximum cash.
   - Seller-question answers and unresolved blockers.
   - VIN-check status sheet.
   - Physical-title inspection checklist:
     - VIN plate = door sticker = title;
     - seller ID name = title name;
     - brand printed on title;
     - lien/paid-off evidence;
     - no title jumping or blank transfer chain.
   - PPI result and immediate-repair estimate.
   - Payment/meeting safety checklist from the FAQ.

2. **Post-selection cost close-out**
   - Replace estimates with actual tax, title, registration, inspection, history-report, and repair figures.
   - Record total cash paid and variance from the Phase 1 estimate.

3. **Insurance and registration task list**
   - Insurance quote/binder step supplied by Ayaan; CarHunt records only completion status, not policy details.
   - County title/registration appointment and document checklist.
   - Plate/registration confirmation.

4. **Archive and shutdown**
   - Mark the bought car and final outcome in the private goal record.
   - Preserve the final dashboard and sweep history for learning.
   - Stop or retire daily/Thursday CarHunt search jobs once the purchase is complete, subject to Ayaan's instruction.
   - Write a short retrospective:
     - which estimate was closest;
     - which blocker mattered most;
     - which sources produced real candidates;
     - what would be reused for a future vehicle search.

### Deliverables

- Private purchase packet.
- Actual-versus-estimated cost record.
- Search archive and retrospective.
- A clear end state for the recurring CarHunt cadence.

### Dependencies

- A selected finalist.
- PPI and physical-title inspection.
- Ayaan's decisions on payment, insurance, and registration; the agent does not purchase, negotiate, or submit forms.

### Done looks like

- The car is bought, titled/registered, and insured according to Ayaan's own completion checks.
- The actual total cash is known.
- CarHunt stops searching instead of continuing as an orphaned dashboard.

---

# 3. Feature proposals

## Priority key

- **Do now:** build in Phase 0 or Phase 1 because it changes the next buying decision.
- **Later:** useful if the search continues, but not ahead of verification and finalist workflow.
- **Skip:** do not build under the current goal, constraints, or time horizon.

| # | Feature | Value to Ayaan | Build cost | Priority |
|---:|---|---|---:|---|
| 1 | Canonical duplicate detection and conflict view | Prevents the same car being treated as two discoveries or carrying two grades | Low–medium | **Do now** |
| 2 | Structured title/engine/verification blockers | Turns hidden prose risks into a clear publish and viewing gate | Low–medium | **Do now** |
| 3 | Listing-photo display | Lets him judge condition, screen size, interior, and obvious damage before travelling | Medium | **Do now** |
| 4 | VIN-check launcher and private evidence checklist | Makes the existing VIN sequence executable for a finalist without publishing the VIN | Low | **Do now** |
| 5 | Seller-contact prep scripts | Produces the exact questions needed for each car's blockers; Ayaan sends manually | Low | **Do now** |
| 6 | All-in cash estimator | Shows that an $11,900 car is not an $11,900 purchase and protects the cash ceiling | Low–medium | **Do now** |
| 7 | Tailored test-drive/PPI checklist | Converts generic advice into car-specific walk-away tests | Low | **Do now** |
| 8 | Finalist comparison strip | Forces a first-choice decision among the top cars instead of ten loosely ranked cards | Low | **Do now** |
| 9 | Basic stale-listing detection | Prioritises live, decision-worthy cars and removes sold inventory quickly | Medium | **Do now — basic version** |
| 10 | Estimate range and confidence | Stops mixed-source medians from looking falsely precise | Medium | **Do now — display; automation later** |
| 11 | Estimate-source automation | Saves operator time and preserves dated components | Medium–high | **Later — semi-automate first** |
| 12 | Price/evidence history | Reveals drops, stale listings, and changing seller stories | Medium | **Later** |
| 13 | SUV and missing-year matrix completion | Unlocks families already in scope without unsafe inference | Medium per family | **Later, gated by need** |
| 14 | Non-Facebook source expansion | May add candidates not visible on Marketplace | Medium–high per source | **Later, one source at a time** |
| 15 | Local saved-finalist notes | Lets Ayaan keep private impressions without publishing them | Low–medium | **Later** |
| 16 | Automated seller messaging or negotiation | Conflicts with research-only rule and creates account/safety risk | High | **Skip** |
| 17 | One-click paid history-report purchase | Money movement and account/payment handling are outside the research workflow | Medium | **Skip** |
| 18 | Financing calculator or lender workflow | The purchase is cash-only | Low | **Skip** |
| 19 | Restoring lane-assist points/ranking | Lane assist was dropped from the owner's criteria | Low | **Skip unless re-added** |
| 20 | Native app, account system, or public comments | No buying value before purchase; adds privacy and maintenance burden | High | **Skip** |

## 3.1 Canonical duplicate detection and conflict view

**What it is:** Every listing is keyed by Marketplace item ID. A private working view lists records whose same ID appears in published data, staging, or prior sweeps with different grades, estimates, reliability, or feature verdicts.

**Value:** Directly prevents the current Tomball Forte double-count and Sonata contradiction.

**Build cost:** Low for URL/ID matching; medium if cross-source fuzzy matching is added later.

**Priority:** **Do now.** It is a correctness feature, not an enhancement.

**Design rule:** Same ID never creates a second active record. New evidence updates the canonical record and preserves a dated change note.

## 3.2 Structured verification blockers

**What it is:** Each card gets a compact blocker line, for example:

- `Blocked by: physical title brand`
- `Blocked by: engine not proven non-excluded`
- `Blocked by: AA is matrix-inferred; plug test required`
- `Ready for viewing: PPI and title still required`

**Value:** Ayaan can scan blockers without opening full notes. The Thursday operator can also see exactly what evidence would change the record.

**Build cost:** Low–medium. Requires append-only fields and a generator change, but the information already exists in prose.

**Priority:** **Do now.** This is the foundation for photos, VIN workflow, scripts, and publish gating.

## 3.3 Listing-photo display

**What it is:** Up to three listing photos on finalist cards, chosen for decision value rather than decoration:

1. front three-quarter exterior;
2. dashboard/infotainment screen;
3. odometer, rear view/camera, engine bay, or visible damage—whichever is most informative.

**Value:**

- distinguishes a real car from a bait listing;
- helps verify screen size and interior condition;
- makes the board faster to use from a phone;
- gives Ayaan a visual memory of each finalist.

**Build cost:** Medium. The sweep must capture and check photo URLs; the card layout must handle missing/expired images; file and privacy rules must be followed.

**Priority:** **Do now for finalists; later for every context record.** Photographing all ten cards is less valuable than getting the top three right.

**Constraints:**

- link/embed URLs only;
- never commit image binaries;
- respect the repository's ~110 KB per-file publish approach by not embedding image data;
- do not show title documents or full VIN plates;
- always keep the Marketplace link as the authoritative photo source if a CDN URL expires.

## 3.4 VIN-check deep links and workflow

**What it is:** A finalist-only VIN panel with two layers:

- public card: only status labels, such as `VIN not yet supplied`, `Decoder checked`, `Open recalls checked`, `NICB checked`, `Title check done`, `Dealer printout requested`;
- private/local workflow: Ayaan pastes the VIN, copies it into each official service, and ticks off the result.

Official destinations already documented in the FAQ:

- NHTSA VIN Decoder: https://www.nhtsa.gov/vin-decoder
- NHTSA Recalls: https://www.nhtsa.gov/recalls
- NICB VINCheck: https://www.nicb.org/vincheck
- NMVTIS/TxDMV title-check routes named in the FAQ.

**Value:** Turns a long FAQ section into a sequence Ayaan can complete in minutes once a seller supplies a VIN.

**Build cost:** Low for links/copy/status; medium if browser-local persistence is added.

**Priority:** **Do now.** It is cheap and directly reduces title/history risk.

**Important limitation:** Do not assume every service accepts a reliable VIN query parameter. Where a service requires a form or CAPTCHA, the correct design is “copy VIN + open official service,” not a fake deep link. Never store the full VIN in the public dashboard or repository.

## 3.5 Seller-contact prep

**What it is:** A copy-ready question script generated from the car's blockers and model-specific risks. It can be generic, evidence-focused, or “before I travel” versions.

**Value:**

- avoids wasted trips for title, engine, or screen problems;
- creates a written seller answer that can be compared with the car;
- helps Ayaan ask for a VIN and PPI permission early;
- keeps the agent within the standing research-only rule.

**Build cost:** Low. Most content already exists in notes, FAQ, and research.

**Priority:** **Do now.**

**Boundary:** CarHunt prepares the script. It does not message the seller, negotiate, make an offer, arrange payment, or submit a form unless Ayaan separately changes the standing rule and authorises a specific action.

## 3.6 Total-cost estimates

**What it is:** An all-in cash panel next to asking price, with editable assumptions and a clear separation between:

- price of the car;
- transaction costs;
- verification costs;
- known immediate repairs;
- unknown repair reserve;
- insurance input supplied by Ayaan.

**Value:**

- a $9,500 car and an $11,900 car have very different risk headroom;
- dealer fees and Texas transaction costs can erase an apparent discount;
- PPI findings can be added immediately to the negotiation ceiling;
- supports a firm “maximum cash for this car” number before emotion enters the viewing.

**Build cost:** Low–medium. A static calculator is enough; no backend or live tax integration is needed.

**Priority:** **Do now.**

**Accuracy rule:** Label every non-asking figure as an estimate or owner-entered quote. Do not present a generic registration or insurance figure as a quote.

## 3.7 Tailored test-drive checklist

**What it is:** A one-car checklist generated from the universal PPI list plus the candidate's model and blockers.

Examples:

- **All cars:** cold start, VIN/title match, flood protocol, A/C torture test, full scan, lift inspection, AA plug test, camera test.
- **Fusion:** engine identification, SYNC 3 screen proof, shifter-bushing/recall status.
- **Civic 2.0L:** A/C temperature and condenser history, fuel-pump recall status.
- **Elantra:** 21V-301 completion proof, oil condition/history.
- **Hybrid:** battery cell spread, 15-minute drive, replacement quote.
- **Hyundai/Kia of applicable years:** ABS/HECU fire-recall status by VIN.

**Value:** The checklist is used at the decisive moment and reduces reliance on memory.

**Build cost:** Low.

**Priority:** **Do now.** The content already exists; it needs packaging per finalist.

## 3.8 Stale-listing detection

**What it is:** A status and age layer:

- `Live — checked <date>`
- `Price changed — <old> to <new>`
- `No longer available`
- `Seller page changed — re-verify`
- `Stale — not checked since <date>`

**Value:** Prevents Ayaan from planning around sold cars and focuses daily Pi time on cars that could actually be bought.

**Build cost:** Medium. Basic manual/Pi checks are cheap; reliable automation is constrained by Facebook access and pacing.

**Priority:** **Do now — basic version.** Start with published qualifiers and staged A/A- cars. Do not attempt to recheck the entire market daily.

## 3.9 Estimate-source automation

**What it is:** Initially, a structured capture and calculation assistant—not a scraper. Later, source-specific capture helpers could prefill provider, figure, trim, mileage, and date where access is stable and permitted.

**Value:**

- less manual transcription;
- fewer mixed figure types;
- reproducible grade calculations;
- estimate history and confidence.

**Build cost:** Medium for semi-automation; high for robust multi-site scraping.

**Priority:** **Later.** First fix the estimate model and preserve components manually for one publish. Automating the current mixed-median method would only produce the wrong answer faster.

**CarMax-specific recommendation:** For finalists, capture one of three explicit states:

1. `CarMax comparable found` — same/near model, trim, year, and mileage, with asking price and date;
2. `CarMax offer only` — shown separately and excluded from the retail median unless the method is deliberately changed;
3. `CarMax unavailable` — estimate label says so instead of implying coverage.

## 3.10 Coverage expansion

**What it is:** Activate additional families and listing sources only after their gates exist.

**Value:** More eligible cars, especially if the current Forte/Civic/Sonata pool does not close.

**Build cost:** Medium per family/source, plus continuing sweep time.

**Priority:** **Later.** The present problem is not a lack of prose research or raw listings; it is conflicting evidence on cars already found. Coverage expansion before Phase 0 would multiply that problem.

---

# 4. Risks and constraints

## 4.1 Facebook Marketplace access

- Marketplace research is **Pi browser only**.
- Use the existing logged-in session; do not create accounts or log in fresh as a workaround.
- Pacing is about 60 pages/hour and about 25 pages/day.
- Bot checks get one agent attempt per site entry under the owner's protocol, then escalation; do not loop retries.
- Marketplace search URL parameters for price/mileage are unreliable and can return false empty results; use plain searches and manual filtering.
- Search-result cards can mislead; verify the item ID against the opened listing page.
- Pi or SSH failures can interrupt a sweep. A partial sweep must be labelled partial, never published as complete.

## 4.2 Research-only boundary

Current standing rules prohibit:

- contacting sellers;
- sending messages;
- submitting forms;
- creating accounts;
- making purchases;
- paying for reports through CarHunt automation.

Seller scripts, VIN workflows, and purchase packets are preparation only. Any change to that boundary needs a specific owner instruction for a specific action.

## 4.3 Estimate accuracy

- Provider figures are not appraisals.
- Asking, retail, resale, trade-in, and offer figures answer different questions.
- Averages can hide trim, condition, mileage, accident, and regional differences.
- A very large discount can signal a title, odometer, condition, or scam problem rather than a bargain.
- CarMax coverage must be named accurately. Until a CarMax comparable is actually captured, do not imply that the published median includes CarMax.
- Grades should carry estimate confidence once Phase 2 begins; a letter grade alone overstates certainty.

## 4.4 Title and Houston flood risk

- Facebook “clear history” is not a Texas title-brand verification.
- A clean-looking Texas title still needs the printed brand checked.
- Title washing and flood history are material risks in Houston.
- Physical title, VIN plate, door sticker, and seller ID must match before money moves.
- Rebuilt/salvage/flood titles remain exclusions under the owner's criteria, regardless of discount.

## 4.5 Privacy and public-repository risk

CarHunt is public. Do not publish:

- full VINs;
- title images;
- seller phone numbers;
- private addresses;
- payment details;
- insurance policy details;
- private inspection documents.

Use status labels in public and keep evidence in the private goal workspace or Ayaan's local possession.

## 4.6 Never publish an unverified standout

A same-day standout report is an alert, not a publish decision.

In particular:

- the November 2 Civic remains staged until Thursday verifies it live, checks the car/photos, and resolves title evidence;
- the November 3 Tomball Forte remains subject to duplicate reconciliation and physical-title caution;
- a seller's “warranty,” “clean,” or “paid off” statement is evidence of a claim, not proof of the underlying fact;
- matrix inference can confirm factory fit where the matrix is authoritative, but it does not prove that a specific car's screen, camera, or Android Auto still works—the plug test does.

## 4.7 Rebuild preservation rules

Every rebuild must preserve:

- static Marketplace `https://www.facebook.com/marketplace/item/<id>/` hrefs in the HTML;
- the Android `intent://` rewrite script for `com.facebook.katana`, with web fallback;
- the `<head>` SVG favicon and Apple touch icon;
- the `theme-color` meta;
- the inline manifest script after the app-link script;
- the visible data stamp, updated to the new sweep date;
- the fixed schema's original fields and order, with new fields appended only.

A rebuild missing the app-link script, icon links, or manifest script is a failed self-check, even if the listings look correct.

Other publish constraints from `METHOD.md`:

- link/embed photo URLs only; never commit image binaries;
- keep individual published files to about 110 KB or less;
- verify that HTML and JSON parse;
- verify that the page listing count matches the JSON count;
- never mix two sweep dates in one listings file.

## 4.8 Time and opportunity risk

The largest product risk is overbuilding while good cars sell. Therefore:

- no phase should delay the November 5 verification publish;
- features should be built for finalists before they are built for every record;
- if a car passes the gates and Ayaan is ready to inspect it, the correct “development” action is to use the checklist and decide, not to start Phase 3;
- if the search ends, Phases 2 and 3 should stop rather than continue as speculative platform work.

---

# 5. Recommended next phase

## Recommendation: Phase 0 — publish gate and record truth

Phase 0 is the only phase that should start now.

### Why

1. **The next publish is imminent.** Thursday, November 5 is the decision point. A photo gallery or calculator built on top of conflicting records would preserve the wrong foundation.
2. **The risk is already demonstrated.** The same Sonata carries incompatible published and staged conclusions; the same Forte appears as both a published car and a new standout. These are not hypothetical data problems.
3. **Title and engine evidence drive the purchase.** Those blockers currently live in prose. Making them structured will improve every later feature without changing the owner's criteria.
4. **It is cheap relative to its value.** Canonical IDs, evidence fields, and a gate checklist require focused data work, not a platform rebuild.
5. **It protects trust.** Ayaan should be able to rely on “meets all must-haves” and a grade. Phase 0 makes those labels auditable.

### Phase 0 completion gate

Do not move to Phase 1 until the November 5 working set can answer “yes” to all of these:

- Is every active listing keyed once by Marketplace ID?
- Is the Tomball Forte treated as one canonical car?
- Has the Sonata matrix and reliability conflict been adjudicated in writing?
- Does every record have a title status and engine status, even if the honest value is `unknown`?
- Does every “meets” record satisfy the existing confirmation rules?
- Is each grade traceable to a current estimate and the rubric?
- Are the November 2 Civic and all other staged records still unpublished unless Thursday's live re-verification clears them?
- Are dead, duplicate, and excluded records removed from the active publish set but preserved in private history?

Once those gates pass, Phase 1 should begin immediately for the top two or three cars. That is where CarHunt stops being a search board and becomes a buying tool.
