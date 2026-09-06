# Georgia residential battery — economics before spend

> **Current status:** active market is Georgia/Atlanta metro. See [ATLANTA_METRO_STRATEGY.md](ATLANTA_METRO_STRATEGY.md) for the live thesis, ZIP targeting, and the Georgia Power incentive that changes the math below — and [TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md) for the live landing page, data schema, and the claim-discipline rules that govern all marketing/sales copy. Florida research is deprioritized, not deleted (see [FLORIDA_ZIP_INTELLIGENCE.md](FLORIDA_ZIP_INTELLIGENCE.md)).

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
   household at 12% peak share, the plan switch alone is worth $461/year — more
   than the battery. Advertising that as battery savings is an advertising-
   substantiation problem, not a copywriting choice.

3. **Load shape dominates, and the funnel cannot see it.** The result swings
   with the fraction of summer kWh consumed 2–7pm weekdays. Two households with
   identical $250 bills land on opposite sides: a low-peak household gains $143/yr
   from the switch, a high-peak household _loses_ $134/yr. A phone number and a
   bill total do not contain this variable. Either the savings claim is gated
   behind Georgia Power interval data, or it is generated from insufficient
   inputs.

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
