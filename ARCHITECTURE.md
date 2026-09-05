# Georgia Battery Model — Architecture & Data Blockers

## Current State

### Implemented & Verified

- **Georgia Power TOU-OA-14** (Overnight Advantage)
  - Tariff PDF extracted and verified 2026-09-05
  - Model produces correct $459/yr arbitrage ceiling for 13.5 kWh battery
  - Cross-checked by hand: 10.5 kWh × 84 peak weekdays × spread = $241 + $228 shoulder = $459

### Architecture

- `engine/tariff.py`: Generalized `UtilitySchedule` dataclass accepts rate data
- `engine/breakeven.py`: Computes break-even lease payment
- `engine/lease.py`: Lessor cost floor vs. what battery earns

Adding a new utility is now **data entry, not code**: define the `Window` objects with rates/hours/months, create a `UtilitySchedule` instance, add to `SCHEDULES` dict.

### Not Yet Implemented

The stubs in `tariff.py` (`bill_baseline`, `bill_on_schedule`) need the full load-distribution logic. The Georgia code has it; refactoring to a parameterized version is straightforward once rate data is in hand.

## Critical Blockers for Orlando

### 1. OUC (Orlando Utilities Commission) Rate Schedule

**Need:** Residential TOU rate plan name and rates

- Basic service charge ($/day)
- Peak rate (¢/kWh) — what times?
- Off-peak rate (¢/kWh)
- Super off-peak rate (¢/kWh) — if offered
- Applicable months for each window
- Riders (fuel, ECCR, DSM, franchise fee)

**Where to get it:**

- OUC website: www.ouc.com → Schedule of Charges
- OUC filings with Florida PSC

**Why it matters:** Arbitrage is `usable_kwh × (peak_rate - off_peak_rate)`. Georgia Power's 27.6¢ spread (29.79¢ peak, 2.19¢ super off-peak) is unusually wide. If OUC's spread is 10¢, battery earnings drop to ~$170/yr, well below the $106+/mo lease cost.

### 2. Duke Energy Florida (if targeting that territory)

**Need:** Same as above for Duke's residential TOU schedule
**Where:** FPSC tariff filings or Duke's website
**Why:** Multiple utilities serve central Florida; need to know which territories are target

### 3. FPL (Florida Power & Light) (if targeting that territory)

**Need:** Same as above
**Where:** FPSC filings
**Note:** FPL serves largest share of central Florida; check this first

## Testing the Model

Once rate data is populated:

```bash
python -m engine.breakeven --utility ouc_orlando
```

Output will show:

- Break-even lease payment by bill size and load shape
- Whether Orlando arbitrage case is viable (likely not, if spread < Georgia)

## The Resilience Pivot

If arbitrage doesn't work in Orlando, the honest product is **backup power** (SAIDI-based insurance). That doesn't require TOU rates at all — it requires outage frequency/duration data for the target ZIPs.

Central Florida has worse outage exposure than Georgia (Hurricanes Ian, Helene, Milton), so the resilience case is likely _better_ in Orlando than Georgia even if arbitrage is _worse_. That's the orthogonal bet.

## Next Steps

1. **Obtain rate schedules** (OUC first, then Duke/FPL if needed)
2. **Populate Window definitions** in `tariff.py`
3. **Run breakeven model** to confirm spread < Georgia means economics don't close
4. **Get SAIDI data** for central Florida from PSC/utility filings
5. **Decide:** Arbitrage dead + resilience viable → pivot to backup power
6. **Obtain real lease pricing** and installer economics (step 1 on the critical path)

## Compliance Notes (Orlando-Specific)

Not modelled yet; separate from the economics engine:

- **FTSA** (Florida Telephone Solicitation Act): State-level TCPA equivalent with private right of action; high-risk jurisdiction for AI voice + text. **Needs counsel review.**
- **FDACS licensing** (FL Dept of Agriculture & Consumer Services): Commercial telephone sellers must be licensed. **Applies to Orlando-based sales operation.**
- **DBPR** (Division of Business and Professional Regulation): Battery installation requires state-licensed electrical contractor.
- **Cooling-off provision**: Home solicitation sales in Florida have statutory 3-day cancellation right.

None of these change the economics calculation, but all must be in the compliance plan before ads spend or calls go out.
