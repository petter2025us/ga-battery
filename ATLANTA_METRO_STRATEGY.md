# Georgia, Deep — Atlanta Metro Strategy

**Status: this is now the only active market.** Florida research (utility-territory and ZIP-level analysis, organic traffic copy) was removed as pre-pivot documentation — it concluded a weaker/unconfirmed utility incentive and no installer relationships in-territory, which is why the focus moved here. Georgia has the installer relationships already in place; that execution advantage plus a newly-material utility incentive is why the focus is deep here rather than spread across two states.

---

## 1. The finding that changes the Georgia math

The original Georgia analysis ([README.md](README.md)) concluded the battery-lease economics don't close on bill savings — earns $459/yr, lease costs $1,164+/yr — and named one open variable that could flip the sign: _"Georgia Power's VPP is a 50 MW solar-plus-storage pilot, not yet open to direct consumer participation. There is no dispatch-payment revenue line to underwrite a lease today."_

That has changed. Georgia Power's **Customer-Sited Solar Plus Storage Pilot** — 50 MW, approved in the 2025 Integrated Resource Plan, with a PSC-approved stipulation this year — has two tracks ([Georgia Power](https://www.georgiapower.com/news-hub/innovation/the-essential-role-of-battery-energy-storage-systems.html), [Better Tomorrow Solar](https://www.bettertomorrowsolar.com/blog/georgia-power-vpp-pilot-program-partnership-explained/)):

- **Customer-directed model:** load curtailment with performance-based payments, $15/kW upfront
- **Utility-directed model:** continuous utility operation of the storage system, **$750/kW upfront incentive for standard customers, $1,000/kW for low-to-moderate-income residential customers**

### Why this matters more than SECO's Florida VPP did

Florida's best live signal was SECO's Tesla VPP — up to ~$275/Powerwall/**year**, an ongoing bill credit. Georgia Power's utility-directed incentive is **$750–$1,000/kW paid upfront, once**. For a Powerwall-class system (5 kW continuous rating), that's **$3,750–$5,000 upfront** — not a trickle of annual credits but real capital that could directly offset the lessor's net installed cost.

Run it against the numbers already in this repo ([README.md](README.md)): $13,500 installed → $9,450 net after the §48E 30% credit (third-party-owned systems only — §25D expired for owner installs after 2025-12-31) → that was the basis for the **$97/month lease floor**. If the utility incentive stacks on top:

```
$9,450 net cost
− $3,750 (standard, $750/kW × 5kW)  → $5,700 remaining → lease floor scales down toward ~$59/mo
− $5,000 (LMI, $1,000/kW × 5kW)     → $4,450 remaining → lease floor scales down toward ~$46/mo
```

That is the first calculation in this entire project where a **$60/month lease price lands at or below the cost floor** instead of $37–$156/month above it. This is provisional arithmetic, not a verified model — engine/lease.py needs to be re-run with this as a parameter, not hand-waved — but it's the first time the sign has looked like it could actually flip.

### Two things this is NOT yet, and must be confirmed before betting on it

1. **Unconfirmed: does "solar plus storage" mean storage must be paired with new PV?** Every description of this pilot pairs "dispatchable battery energy storage systems with behind-the-meter solar systems." If PV is a hard requirement, a storage-only lease (the product this repo has modeled throughout) doesn't qualify as-is — the offer would need to become solar+battery, which changes installed cost, tax credit treatment, and installer scope. **This is the single highest-priority thing to verify before promising this incentive to any customer.**
2. **Unconfirmed: does a third-party-owned (leased) system qualify for the utility-directed incentive**, or does Georgia Power require the account holder to be the system owner? The original Georgia thesis depends entirely on TPO/lease structure for the tax credit (§48E survives, §25D doesn't) — if the utility incentive requires customer ownership, it conflicts with the lease structure the whole business model rests on, and the two benefits can't be stacked as assumed above.

**Action before any customer-facing claim:** call Georgia Power's DER/interconnection group (or find the actual pilot tariff filing at the Georgia PSC) and get written answers to both. Do not put a specific incentive number in front of a customer until this is confirmed — same discipline this project has applied everywhere else (the Georgia bill-savings claim was killed for the same reason: unverifiable at the point of sale).

---

## 2. Storm/outage risk — Atlanta metro, verified against real events

Unlike Florida (where both major utilities just posted record reliability, killing the "unreliable grid" pitch), **metro Atlanta has recent, real, county-identified outage events** to point to — this is a stronger evidentiary base than anything found in the Florida pass.

| Event                                  | Counties hit                     | Scale                                                                             | Source                                                                                                                                            |
| -------------------------------------- | -------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Jan 2026 ice storm                     | Fulton, Gwinnett                 | 5,300 outages (Fulton), 4,200 (Gwinnett)                                          | [11Alive](https://www.11alive.com/article/weather/georgia-power-outages-after-winter-storm-tracking-list/85-64cd21e4-8b82-40a1-8d92-10c054253164) |
| March 2026 severe storms/tornado watch | Gwinnett, Cherokee, Fulton, Cobb | 65,000+ customers out — 17,000 Gwinnett, 9,700 Cherokee, 8,500 Fulton, 2,500 Cobb | [Atlanta News First](https://www.atlantanewsfirst.com/2026/03/16/live-updates-tornado-watch-issued-ahead-strong-line-storms-set-move-through/)    |
| Separate severe storm event            | Fulton-heavy                     | 50,000+ customers out, 34,000+ in Fulton alone                                    | [Fox 5 Atlanta](https://www.fox5atlanta.com/news/storms-bring-down-trees-knock-out-power-50k-metro-atlanta)                                       |
| March 2025                             | Forsyth, Fulton, Gwinnett, Cobb  | Tornado watch issued                                                              | Atlanta News First                                                                                                                                |

Georgia Power's own messaging (2025 Grid Investment Program: 104 distribution projects, "up to 50% improvement" in outage metrics for 504,000 customers) tells the same story Duke/FPL told in Florida — the utility is actively improving reliability — but unlike Florida, actual named storm events with **county-level outage counts in the tens of thousands are on record from the last 12 months**, not excluded from a "record-low" press release. The honest pitch here is stronger and more specific: _"ice storms and spring tornado-line storms have knocked out power to tens of thousands of your neighbors twice in the last year."_ That's substantiable without a storm-exclusion caveat.

**Repeat offenders across all three events: Fulton, Gwinnett, Cherokee, Cobb.** This is the county shortlist for ZIP selection, not a guess.

---

## 3. ZIP candidates — North Fulton / South Forsyth corridor

This is where storm exposure (§2) and affluence/homeownership (WTP proxy) overlap most cleanly — a materially better overlap than anything found in the Florida pass, where the storm-risk counties (SW Florida) and the best economics counties didn't always coincide.

| ZIP   | Area                            | County         | Median HH income | Homeownership                    | Notes                                                                                                                                                                             |
| ----- | ------------------------------- | -------------- | ---------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 30005 | Johns Creek / South Forsyth     | Forsyth/Fulton | $176,957         | `DATA GAP` — not found this pass | Highest income found in this pass                                                                                                                                                 | [zipdatamaps](https://www.zipdatamaps.com/en/us/zip-maps/ga/city/hhi/johns-creek) |
| 30004 | Milton / Alpharetta             | Fulton         | $156,100         | **75.6%**                        | Best combination: high income + highest confirmed homeownership rate                                                                                                              | [city-data](https://www.city-data.com/zips/30004.html)                            |
| 30075 | Roswell                         | Fulton         | $157,335         | `DATA GAP`                       | Fulton County — directly named in the March 2026 65,000-outage event                                                                                                              | [incomebyzipcode.com](https://www.incomebyzipcode.com/georgia/30004)              |
| 30022 | Alpharetta / Johns Creek border | Fulton         | $130,607         | `DATA GAP`                       | Still affluent, but the weakest income of the four in this pass                                                                                                                   |
| 30327 | Buckhead (Tuxedo Park/Paces)    | Fulton         | $189,250         | `DATA GAP`                       | Highest income in Atlanta proper, but $1.1M+ median home value suggests existing generator penetration is likely already high — test, don't assume, same caution as Windermere FL |

**First-pass ranking:**

1. **30004 (Milton)** — the only ZIP with both a confirmed high income _and_ a confirmed high homeownership rate; Milton itself is named as the #1 richest city in Georgia for 2026 ($171,295 city-wide median, per [HomeSnacks](https://www.homesnacks.com/richest-neighborhoods-in-atlanta/))
2. **30005 (Johns Creek/S. Forsyth)** — highest raw income found, homeownership unconfirmed
3. **30075 (Roswell)** — directly named in a real 2026 outage event, strong income
4. **30022** — viable but weakest of the affluent set
5. 30327 (Buckhead) — deprioritized pending a generator-penetration check; likely a harder sell at this price point for a market that may have already solved backup power

---

## 4. Why Georgia over Florida, restated plainly

- **Installers already in place.** Florida had zero confirmed installer relationships; Georgia doesn't have that gap.
- **A real, upfront, dollar-denominated utility incentive** ($750–$1,000/kW) beats Florida's best signal (SECO's ~$275/yr trickle) by an order of magnitude in near-term cash impact — _contingent on the two open questions in §1_.
- **The outage story is substantiable with named, dated, county-level events**, not undermined by a "we just had our best reliability year ever" press release the way both Florida utilities' own numbers undermined the FL resilience pitch.
- **Storm-risk counties and high-income counties are the same counties** (Fulton, Forsyth) — in Florida those were often different territories requiring a tradeoff.

## 5. What has to happen before spending a dollar or making a claim

- [ ] **Confirm PV-pairing requirement** on the utility-directed incentive — does storage-only qualify, or must solar be included? This changes the product, not just the pitch.
- [ ] **Confirm TPO/lease eligibility** for the utility-directed incentive — can a third-party-owned leased system's owner (the lessor) receive and use the incentive, or does it require the account-holder/customer to own the system outright?
- [ ] **Re-run engine/lease.py** with the incentive as an explicit line item once both are confirmed — do not hand-wave the arithmetic in §1 into a customer promise.
- [ ] Confirm homeownership rate for 30005, 30075, 30022 (Census ACS pull, not found in this web pass)
- [ ] Generator/existing-backup penetration check for 30327 before deciding whether to include or exclude Buckhead
- [ ] Loop in the existing Georgia installer relationships early — confirm their coverage area actually includes North Fulton/South Forsyth before committing to that corridor as the beachhead

## 6. Recommendation

Don't launch a landing page or spend a dollar on this until the two incentive-eligibility questions in §1 are answered — that's a phone call or a PSC filing read, not a multi-week research project, and it determines whether the entire pitch is "$60/mo, cheaper than it's ever been" or the same unclosed economics as the original analysis with a different state name on it. Once confirmed, 30004 (Milton) is the strongest first ZIP: highest-confidence income and homeownership combination, in the exact county named in two of the three storm events pulled in §2.

## 7. Live landing page — Milton (30004)

**Live:** https://claude.ai/code/artifact/99c53ae3-a04b-42c1-9492-61ef7b220a0d

Built after a proposed version claiming "$145/mo average savings" was rejected — that number contradicted this repo's own verified economics (§1 of [README.md](README.md): battery earns $459/yr, lease costs $1,164+/yr) and had no basis beyond a generic solar-sales template. The live page instead uses the substantiated claim available today: **$0 out-of-pocket lease**, framed as backup power (not bill savings), with the Georgia Power incentive mentioned as "may qualify, confirmed on your call" — not a guaranteed number — until the two open eligibility questions in §1 are answered.

Form matches the requested OTP-close flow: name, phone, average monthly bill (range select), ZIP (defaulted to 30004), consent checkbox. Same `leads` collection pattern as the Florida pages, `track: "milton-gapower-30004"`.

**Still open before this should get real ad spend or AI-video traffic:** the PV-pairing and TPO-eligibility questions in §1. The page doesn't promise a dollar figure, so it's safe to run for lead capture now, but the phone close script should not quote a specific incentive amount until those are confirmed.

### Update: video section added (2026-09-06)

The "Why Milton, why now" text section on the live page was replaced with a video player slot per direct request (Justin's AI-video plan). Claude can't generate the video itself — no video-generation tool available — so the section instead hosts a "video coming soon" placeholder wired to accept a real embed URL (YouTube/Vimeo) or direct file link via one config line in the page's script. Drop the link in once the video exists; no other page changes needed.

### Update: incentive eligibility research (2026-09-06)

Could not place a phone call (no calling capability available) or access the actual tariff/rider text — Georgia PSC's docket search (correct docket: **#56002**, 2025 IRP) is a JS-rendered application whose document list doesn't expose itself to automated fetching. Web research instead:

**PV-pairing requirement — upgraded from "unconfirmed" to "likely required," still not a legal confirmation.** Every independent source describing this program — [Georgia Power's own site](https://www.georgiapower.com/news-hub/innovation/the-essential-role-of-battery-energy-storage-systems.html), [SEPA](https://sepapower.org/knowledge/vpp-der-policy-q3-2025/), [pv-magazine USA](https://pv-magazine-usa.com/2025/07/24/georgia-power-agrees-to-give-community-solar-a-path-forward/), [Southern Alliance for Clean Energy's policy analysis](https://cleanenergy.org/news/the-good-the-bad-and-the-uncertain-in-georgia-powers-proposed-irp-settlement/), and a solar installer's own explainer ([Better Tomorrow Solar](https://www.bettertomorrowsolar.com/blog/georgia-power-vpp-pilot-program-partnership-explained/)) — describes the program identically: "pairing dispatchable battery energy storage systems with behind-the-meter solar systems." None mentions a storage-only path. Consistent enough across independent sources to treat as a real signal, not proof.

**TPO/lease eligibility — still genuinely unconfirmed, no signal found either way.** No source addresses whether a third-party-owned or leased system qualifies for the utility-directed incentive. Notably, Better Tomorrow Solar's own explainer states the pilot is still pre-enrollment: _"The VPP Pilot Program is still in its early stages of development and regulatory approval, so direct consumer participation is not yet available."_ This may mean the operational eligibility rules (including TPO treatment) simply haven't been published yet.

**Also found:** the stipulation reportedly targets a minimum of 10,000 solar+battery customers program-wide, and a since-modified size cap that critics said was originally too small to run home heating/AC during an outage (Georgia Power agreed to revisit the interconnection study fee alongside a larger aggregate size limit, per pv-magazine).

**Still the recommended next step, unchanged:** a direct call to Georgia Power's DER/interconnection group, or a follow-up read of docket #56002 once its documents are indexed, before quoting any incentive figure to a customer.
