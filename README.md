# Georgia residential battery — economics before spend

> **Start here: [STATUS.md](STATUS.md)** — ground truth on where this project stands and the prioritized next steps. This README is the technical foundation (the economics model below); STATUS.md is the current state of the business.

A deterministic model of whether a Georgia Power residential battery lease can
be sold on bill savings. Built before any ad spend, because it answers the
question ad spend was going to answer expensively.

**This finding still holds for bill-savings claims specifically** — the pivot to Georgia is driven by a _backup-power_ pitch plus a newly-found utility incentive, not a reversal of the arbitrage math below.

```bash
python -m engine.breakeven   # break-even lease payment by bill size and load shape
python -m engine.lease       # what the lease must cost the lessor, vs. what it earns
```

## The finding

**The battery earns $26–38/month and does not scale with bill size. An honest
lease costs at least $106/month. The gap is $67–156/month.**

Three results, in order of how much they change the plan:

1. **Savings saturate.** Above roughly 850 kWh/month, the battery's own
   contribution pins at $459/year no matter how large the bill. The ceiling is
   set by usable kWh × price spread, not by the customer's consumption. Chasing
   $250+ or $500+ bills does not improve battery economics at all.

2. **Most of the advertised savings are free.** A large share of the bill
   reduction comes from moving to the Overnight Advantage tariff, which any
   customer can do alone with one phone call and no hardware. For a $500/month
   household at 12% peak share, the model now shows the plan switch alone is
   worth $550/year — more than the battery.[^1] Advertising that as battery
   savings is an advertising-substantiation problem, not a copywriting choice.

3. **Load shape dominates, and the funnel cannot see it.** The result swings
   with the fraction of summer kWh consumed 2–7pm weekdays. At a fixed bill
   size, a low-peak household gains hundreds of dollars a year from the
   switch; a high-peak household can lose money on it instead — the crossover
   is in the neighborhood of 30–50% peak share, and exactly where depends on
   the same unverified baseline as note [^1].[^1] A phone number and a bill
   total do not contain this variable. Either the savings claim is gated
   behind Georgia Power interval data, or it is generated from insufficient
   inputs.

[^1]: This figure comes from the Residential Service baseline, which this
    repo approximates (see "Cross-check" below) rather than verifies exactly —
    unlike the $459/yr and $26–38/month figures above, which do not depend on
    that baseline and are independently confirmed.

## What is verified vs. assumed

Verified against the filed tariff PDF (TOU-OA-14, eff. Jan 2025) and Georgia
Power's own rate pages on 2026-09-05:

- Overnight Advantage base energy: 29.7868¢ on-peak / 10.1676¢ off-peak /
  2.1859¢ super off-peak; basic service $0.4603/day.
- On-peak is 2–7pm Mon–Fri, June–September only. Super off-peak is 11pm–7am,
  every day, all year.
- **No demand charge.** No solar-pairing requirement, no grid-charging
  restriction — any residential customer in a separately metered dwelling may
  take this tariff. 12-month auto-renewing term.
- Georgia Power also offers a second, simpler TOU plan, **Nights & Weekends**
  (2-tier: 30.3¢ on-peak same hours/months as above, 7.8¢ off-peak all other
  hours). It is *not* the plan modeled here, and it's the worse choice for a
  battery: its off-peak rate (7.8¢) is what a battery would charge at, versus
  Overnight Advantage's super off-peak rate (2.19¢) for the same overnight
  hours. Net effective spread per kWh delivered (after 90% round-trip
  efficiency): Overnight Advantage ≈27.4¢, Nights & Weekends ≈21.6¢ — about
  21% narrower. Confirmed 2026-09-08 against Georgia Power's own
  Nights & Weekends rate page. This repo's tariff choice was already the
  more favorable one for the arbitrage case.
- Residential Service base: 8.2¢ winter flat; 8.8¢ / 14.6¢ / 15.1¢ summer tiers.
- §25D (30% homeowner credit) terminated for installs after 31 Dec 2025. §48E
  survives for third-party-owned systems — which is why the lease structure is
  the only 2026-viable one.
- Georgia Power's VPP is a 50 MW solar-plus-storage pilot, **not yet open to
  direct consumer participation**. There is no dispatch-payment revenue line to
  underwrite a lease today. This was the one thing that could have flipped the
  sign, and it is not available.

Assumed, and each is a named parameter in `engine/tariff.py`:

| Assumption              | Default | Why it matters                                                                                                 |
| ----------------------- | ------- | -------------------------------------------------------------------------------------------------------------- |
| `peak_share`            | 0.20    | The dominant swing factor. Unknowable from a bill total.                                                       |
| `riders_per_kwh`        | 5.5¢    | Fuel + ECCR + DSM. Flat per-kWh, so it cancels in the arbitrage differential; only bites on round-trip losses. |
| `franchise_fee`         | 3%      | Percentage of bill, so it does _not_ cancel.                                                                   |
| `round_trip_efficiency` | 0.90    |                                                                                                                |
| `depth_of_discharge`    | 0.80    | Warranty-safe daily cycling. 100% DoD raises the ceiling ~25% and voids warranties.                            |
| Dispatch                | perfect | Charges every night, discharges peak-first. A real install cannot beat this.                                   |

The attribution order is also generous to the battery. Crediting the tariff
switch first and the battery second gives the battery its _maximum_ residual
share: on flat 8.2¢ winter Residential Service there is no spread to arbitrage
at all, so under battery-first attribution the hardware earns close to nothing
for eight months of the year. The favourable ordering was chosen deliberately.

The model is generous to the seller everywhere it is uncertain. The economics
still do not close.

## Cross-check

Hand arithmetic, independent of the code: 10.5 kWh usable × 84 summer peak
weekdays × (0.297868 − 0.021859/0.90) = $241, plus 281 shoulder days ×
10.5 × (0.101676 − 0.024288) = $228, less $23 of rider cost on the kWh lost to
inefficiency, ×1.03 franchise fee = **$459/yr**. The engine returns $459.

**Verified 2026-09-08.** For a period this repo did not catch, that last
sentence was false: `engine/tariff.py` referenced an undefined name at import
time, and `engine/breakeven.py` called two functions (`overnight_advantage_month`,
`residential_service_month`) that had never been defined anywhere in this
repo's history — `python -m engine.breakeven` and `python -m engine.lease`
raised on the first line, they did not print $459. The $459 figure was real
(it matches the hand cross-check above and is now reproduced by running code),
but until this fix it had never actually been machine-verified — it was
carried over from an earlier, pre-refactor version of the model that no
longer existed in the committed code. Both bugs are fixed; both commands now
run and reproduce the numbers in this README. A third, unrelated import bug
in `engine/multistate_analysis.py` (a legacy, pre-Georgia-pivot module not
cited by any other doc) is also fixed, but that module has its own remaining
defect — see `ARCHITECTURE.md`.

**One number in this file is still not independently verified: the exact
kWh tier breakpoints for Residential Service** (the "8.8¢/14.6¢/15.1¢ summer
tiers" — the *rates* are sourced, the *breakpoints* are not). `engine/tariff.py`
now approximates the summer Residential Service bill with a flat 14.6¢ rather
than guessing at breakpoints. This has **no effect on the $459/yr ceiling or
the $26–38/month range** — the battery-only benefit is the difference between
two Overnight Advantage bills (with and without a battery) and the Residential
Service baseline cancels out of that subtraction entirely. It **does** affect
every number in this file computed relative to the Residential Service
baseline: "gross annual benefit," "free switch," and the two worked examples
below. Re-running the model today reproduces $459/yr and $26–38/month exactly,
but does not reproduce "$461/year" or "$143/yr gained, $134/yr lost" — with
the flat-rate approximation, the plan switch is never a net loss at 12/20/30%
peak share for any bill size in the model's default grid; it only turns
negative above roughly 45–50% peak share. The qualitative point (peak share
can flip the sign of the switch) still holds; the specific dollar examples do
not, until real Schedule R tier breakpoints replace the approximation.

## What this does not say

It does not say there is no business. It says there is no business _in selling
bill savings_. Backup power during outages is a real, sellable value that this
model does not price, because it is not an arbitrage — it is insurance, and it
is sold on a different promise with different substantiation requirements.

Before committing to that pivot, one number decides it: Georgia Power's
residential SAIDI (outage minutes per customer per year). Georgia Power
publicises directional improvements — 2023 restoration ~27 minutes faster than
2022, 15% fewer interruptions — but does not publish the level; it sits in the
Georgia PSC reliability filings. If typical annual outage exposure is only a
couple of hours, resilience will not carry a $106+/month payment either, and
there is no product here at any price. Get that number before anything else.
