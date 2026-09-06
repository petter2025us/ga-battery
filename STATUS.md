# Status & Next Steps

**Last updated:** 2026-09-06. **Read this first** — it's the single ground-truth doc for where this project actually stands. Everything else in this repo is supporting detail, cited below.

---

## Ground truth

- **Active market:** Georgia / Atlanta metro (North Fulton / South Forsyth corridor). Florida work is deprioritized, not deleted — kept as a record of why it was set aside (weaker/unconfirmed utility incentive, no installer relationships in-territory). See [FLORIDA_ZIP_INTELLIGENCE.md](FLORIDA_ZIP_INTELLIGENCE.md), [ORLANDO_ZIP_DRILLDOWN.md](ORLANDO_ZIP_DRILLDOWN.md).
- **The original economics finding still holds:** battery-only bill-savings arbitrage does not close in Georgia — the battery earns $459/yr against a lease that costs $1,164+/yr (see [README.md](README.md)). The Georgia pivot is not a reversal of this math; it's a different pitch (backup power, not savings) plus a new incentive that changes the _lease-cost_ side of the equation, not the arbitrage side.
- **What changed the picture:** Georgia Power's Customer-Sited Solar Plus Storage Pilot includes a utility-directed model paying **$750/kW upfront ($1,000/kW for low-to-moderate-income customers)**. Run against the lease-cost model, this could drop the break-even from ~$97/mo toward $46–59/mo — the first calculation in this project where a $60/mo lease price lands at or below cost. Full analysis: [ATLANTA_METRO_STRATEGY.md §1](ATLANTA_METRO_STRATEGY.md).
- **This is PROVISIONAL, not confirmed.** Two questions are still open and gate any customer-facing dollar claim:
  1. Does the incentive require pairing with **new solar**, or does storage-only qualify?
  2. Does a **third-party-owned/leased** system qualify, or only an owner-occupied one?
     Resolving this needs a phone call to Georgia Power's DER/interconnection group, or a read of **PSC docket #56002** once its documents are indexed — not more desk research. **Do not quote a specific incentive dollar figure to any customer, on any page or any call, until this is resolved.**
- **ZIP targeting:** 30004 (Milton) ranks first — the strongest confirmed income + homeownership combination, in Fulton County, which was directly hit by two real, dated outage events in the past year (Jan 2026 ice storm, March 2026 tornado-line storm). Full ranking: [ATLANTA_METRO_STRATEGY.md §2-3](ATLANTA_METRO_STRATEGY.md).
- **Claim discipline (non-negotiable, applies everywhere — landing pages, ads, phone scripts):** no bill-savings numbers, no specific incentive dollar figures until confirmed, backup-power framing only. This rule exists because a proposed ad claiming "$145/mo average savings" was rejected outright — it had no basis in this repo's own model and carried real deceptive-advertising exposure. Full rule set: [TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md).

## What's live right now

| Page             | URL                                                                  | ZIP   | Status                               |
| ---------------- | -------------------------------------------------------------------- | ----- | ------------------------------------ |
| Milton, GA       | https://claude.ai/code/artifact/99c53ae3-a04b-42c1-9492-61ef7b220a0d | 30004 | **Active** — current beachhead       |
| Clermont, FL     | https://claude.ai/code/artifact/225a6562-6d2a-4299-bc21-df223ecc14c2 | 34711 | Deprioritized, left live, no traffic |
| Dr. Phillips, FL | https://claude.ai/code/artifact/fc245a8c-73aa-4602-8dd2-b2abca4f9c4a | 32836 | Deprioritized, left live, no traffic |

Source for all three lives in `landing-pages/` in this repo (see [TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md) for the full frontend/data breakdown). The Milton page's "see how it works" section is a video placeholder — dropping a real video URL into one config line in the page's script activates it.

## Facebook ad campaign — PAUSED

- A dedicated Facebook Page, **"Georgia Home Battery Solutions,"** was created and correctly branded — separate from ARF AI's own Page, which was originally (incorrectly) about to be used for this campaign before the mismatch was caught and corrected.
- Campaign "New Leads Campaign" exists in Meta Ads Manager: **$15/day budget, in draft, nothing published, nothing spent.**
- Configured so far: conversion location = Website (not Instant Forms), Performance goal = "Maximize number of landing page views," destination URL = the Milton page.
  - Performance goal is landing-page-views, not lead-conversion optimization, because the Milton page is hosted as a Claude Artifact, whose content-security policy blocks `connect.facebook.net` — a real Meta Pixel cannot fire on that page. This is a hosting constraint, not a settings choice; it holds regardless of Ads Manager configuration.
- **Blocked on:** the new Page has no linked Instagram account. The only Instagram account offered (`@juanpetter85`) is a personal profile — linking it would reintroduce the identity-mismatch problem the Page separation was meant to solve, and it likely isn't technically linkable anyway (Facebook generally requires a Business/Creator Instagram account for this).
- **Next action needed (a decision, not a task I can complete alone):** either (a) create/convert a Business Instagram account for Georgia Home Battery Solutions and link it, or (b) find a way to restrict ad placements to Facebook-only within this Advantage+ leads campaign structure (attempted, not yet successful through the UI).

## Organic path (available now, zero blockers)

Ready-to-post Nextdoor/Facebook-group copy exists for the Florida pages ([FLORIDA_ORGANIC_TRAFFIC_COPY.md](FLORIDA_ORGANIC_TRAFFIC_COPY.md)) as a template. **An equivalent Georgia/Milton version has not been written yet** — this is free and requires no Facebook Ads Manager resolution, so it's the fastest path to real traffic if the Instagram question stalls.

## Next steps, in priority order

1. **Unblock traffic:** either resolve the Instagram question above, or write Georgia/Milton organic post copy (Nextdoor + local Facebook groups) and start posting — doesn't require touching Ads Manager at all.
2. **Confirm the Georgia Power incentive eligibility** (PV-pairing requirement, TPO/lease eligibility) via a phone call or PSC docket #56002 — this determines whether the incentive can ever be mentioned with a real number.
3. **Verify installer coverage** — this repo has asserted "installers already in Georgia" as the rationale for this whole pivot but has never confirmed they actually cover North Fulton/Milton specifically.
4. **Produce the AI video** for the Milton page's placeholder slot and send the link to activate it.
5. **Once 1–2 are resolved:** launch traffic and start monitoring the `leads` database for real submissions (ask to have it checked, or read it directly per the schema in [TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md)).

## Document map

| File                                                                                                                                                                                 | Contents                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| [ATLANTA_METRO_STRATEGY.md](ATLANTA_METRO_STRATEGY.md)                                                                                                                               | Georgia Power incentive analysis, storm-risk evidence, ZIP ranking, incentive-eligibility research |
| [TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md)                                                                                                                                       | Frontend architecture, data schema, claim-discipline rules, deployment workflow                    |
| [README.md](README.md)                                                                                                                                                               | Original Georgia arbitrage economics model — still the technical foundation                        |
| [OPERATING_SYSTEM.md](OPERATING_SYSTEM.md)                                                                                                                                           | Full funnel/CRM/lifecycle architecture spec (product- and geography-agnostic)                      |
| [FLORIDA_ZIP_INTELLIGENCE.md](FLORIDA_ZIP_INTELLIGENCE.md), [ORLANDO_ZIP_DRILLDOWN.md](ORLANDO_ZIP_DRILLDOWN.md), [FLORIDA_ORGANIC_TRAFFIC_COPY.md](FLORIDA_ORGANIC_TRAFFIC_COPY.md) | Deprioritized Florida research, kept for the record                                                |
| `landing-pages/`                                                                                                                                                                     | Canonical HTML source for all three live pages                                                     |
