# Orlando Metro ZIP Drilldown — Pass 2

**Correction to [FLORIDA_ZIP_INTELLIGENCE.md](FLORIDA_ZIP_INTELLIGENCE.md):** that doc's #1 ranking treated "Orlando metro (SECO + Duke FL)" as one territory. It isn't. **SECO Energy's service area is Citrus, Hernando, Lake, Levy, Marion, Pasco, and Sumter counties** ([SECO service territory](https://secoenergy.com/service-territory)) — rural/exurban Central Florida northwest of Orlando. **Duke Energy Florida's Orlando-area territory is Orange County and inner suburbs**, including Hunter's Creek (32837), where the utility's own battery pilot runs. These do not overlap. The Tesla VPP cash incentive (SECO) and the Duke demand-response pilot are two separate opportunities in two separate places, not one combined signal. Splitting them below.

---

## Track A: Duke Energy Florida / Orange County (Orlando proper)

Where the actual battery pilot is running, but **no SECO/Tesla VPP cash incentive is available here** — Duke's own pilot is closed enrollment (75 homes, utility-selected, utility-owned equipment, no customer cost or revenue).

| ZIP   | Area           | Median HH income | Homeownership            | Housing age                      | Notes                                                                                                                                                                                             |
| ----- | -------------- | ---------------- | ------------------------ | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 32837 | Hunter's Creek | $102,222         | 54.3%                    | Mostly 1970–1999 built           | Where Duke's pilot runs. Homeownership is moderate-low (54%) — mixed apartment/single-family stock softens the addressable homeowner base. [city-data](https://www.city-data.com/zips/32837.html) |
| 32836 | Dr. Phillips   | $109,918         | 67.1%                    | Newer/established suburban       | Higher income, higher homeownership than Hunter's Creek                                                                                                                                           | [incomebyzipcode.com](https://www.incomebyzipcode.com/florida/34786)         |
| 34786 | Windermere     | $134,214         | Majority owned/mortgaged | Newer, high-value ($684K median) | Highest income of the three, but high home values likely mean existing generator/backup investment already made — may be a harder or easier sell depending on framing                             | [zip-codes.com](https://www.zip-codes.com/zip-code/34786/zip-code-34786.asp) |

**Read on Track A:** Windermere and Dr. Phillips are higher-income, higher-homeownership, more affluent-suburban than Hunter's Creek itself — better WTP profile on paper — but neither is where Duke's pilot creates local awareness/social proof. Hunter's Creek carries the "your neighbor has one" story (once the pilot generates press/word of mouth) but has the weakest homeownership rate of the three. **No cash-flow-improving VPP mechanism found here** — the resilience pitch has to stand on hurricane-backup value alone, same constraint as the original Georgia/multistate analysis.

---

## Track B: SECO Energy territory (Lake/Sumter/Marion/Citrus/Hernando/Pasco/Levy)

Where the **Tesla VPP cash incentive is actually live** (up to ~$275/Powerwall/yr in SECO bill credits) — this is the only track with a real, confirmed revenue mechanism, _contingent on the still-unconfirmed question of whether a leased/TPO Powerwall qualifies_ (see open item below).

| ZIP   | Area                          | Median HH income               | Homeownership                             | Age profile                                                                      | Notes                                                                                                                                                                                                                                                             |
| ----- | ----------------------------- | ------------------------------ | ----------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 34748 | Leesburg                      | $53,768–$58,192 (sources vary) | 73%                                       | 43% of residents 65+ (median age 59.8)                                           | Retiree-heavy, lower income, but high homeownership and 62% receive Social Security — a fixed-income population may be highly rate-sensitive to a $60/mo *lease* even with a $275/yr credit offsetting it. [city-data](https://www.city-data.com/zips/34748.html) |
| 34711 | Clermont                      | $86,419–$90,245                | 77%                                       | Growing suburban                                                                 | Best combination found: solid income, high homeownership, fast-growing area (Clermont is one of the fastest-growing cities in Central FL)                                                                                                                         | [point2homes](https://www.point2homes.com/US/Neighborhood/FL/Clermont-Demographics.html) |
| 34714 | Clermont (south/Four Corners) | $75,392                        | Lower than 34711 (`DATA GAP` — not found) | Newer development, more short-term-rental/vacation-home mix near Disney corridor | Watch for high vacation-rental share diluting the owner-occupied resilience pitch                                                                                                                                                                                 | [incomebyzipcode.com](https://www.incomebyzipcode.com/florida/34714)                     |

**Read on Track B:** 34711 (Clermont core) is the strongest ZIP found in this pass — $86–90K median income, 77% homeownership, growing family/suburban population, inside SECO territory where the VPP credit is live. 34748 (Leesburg) has even higher homeownership (73%) but skews heavily retiree/fixed-income, which could go either way on WTP — resilience for medical equipment during outages is a real driver for an elderly population, but $60/mo on Social Security income is a harder sell than for a working household.

---

## Consolidated shortlist

| Priority | ZIP                      | Track               | Why                                                                                                                                                              |
| -------- | ------------------------ | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1        | **34711 (Clermont)**     | SECO/VPP            | Best income + homeownership + growth combination, inside the only territory with a live cash-incentive program                                                   |
| 2        | **32836 (Dr. Phillips)** | Duke/pilot-adjacent | Strong income/homeownership, close enough to Hunter's Creek pilot for regional press/word-of-mouth, no VPP revenue but strong resilience-only economics profile  |
| 3        | **34786 (Windermere)**   | Duke/pilot-adjacent | Highest income, but high existing home values may mean backup power (generators) already solved — test, don't assume                                             |
| 4        | **34748 (Leesburg)**     | SECO/VPP            | High homeownership + real medical/resilience need for an elderly population, but income and fixed-income status are a real affordability risk for a $60/mo lease |
| —        | 32837 (Hunter's Creek)   | Duke/pilot          | Deprioritized despite the pilot's local presence — homeownership rate (54%) is the weakest of any ZIP in this pass                                               |

---

## Still open before committing spend to any of these

- [ ] **SECO VPP + lease/TPO eligibility** — unresolved from pass 1, now the single highest-leverage unknown. If a leased Powerwall doesn't qualify for the SECO incentive, Track B loses its only advantage over Track A and the two tracks become economically identical (backup-value-only, no cash-flow assist).
- [ ] Actual §48E-eligible lease/TPO structure and installer partner with Central Florida coverage in both Lake and Orange counties — not yet identified (Georgia-based installer relationships don't currently extend here, per [ARCHITECTURE.md](ARCHITECTURE.md)/[README.md](README.md)).
- [ ] Homeownership rate for 34714 — flagged gap, matters because of suspected vacation-rental mix.
- [ ] Existing generator penetration in Windermere/Dr. Phillips — high-value homes in hurricane-exposed Florida frequently already own whole-home generators; this could mean the market is pre-solved, or that a battery is positioned as a premium upgrade. Needs direct market research (survey/calls), not desk research.
- [ ] Outage frequency/duration specific to these ZIPs — county/territory-level Duke and SECO reliability numbers, not found in searches; would need direct utility PSC filings or reliability report requests.

## Recommendation

Run the Week-1-style landing page + organic lead test (same bootstrap model as Georgia, [BOOTSTRAP_QUICK_START.md](BOOTSTRAP_QUICK_START.md)) simultaneously in **34711 (Clermont)** and **32836 (Dr. Phillips)** — one from each track — before committing to either. That resolves the SECO VPP question empirically (does the $275/yr credit change conversion or messaging response) rather than waiting on a phone call that may not get a clean answer.
