# Georgia Battery Model — Architecture & Data Blockers

## Current State

### Implemented & Verified (as of 2026-09-08)

- **Georgia Power TOU-OA-14** (Overnight Advantage)
  - Tariff PDF extracted and verified 2026-09-05
  - Model produces correct $459/yr arbitrage ceiling for 13.5 kWh battery
  - Cross-checked by hand: 10.5 kWh × 84 peak weekdays × spread = $241 + $228 shoulder = $459
  - `python -m engine.breakeven` and `python -m engine.lease` actually run and
    reproduce these numbers. **This was not true before 2026-09-08** — see
    "Repo-integrity history" below. Do not trust a claim in any doc in this
    repo that a command "returns" a number without re-running the command;
    this project's own history is the counterexample.

### Known approximation

- **Residential Service baseline is not tier-exact.** `residential_service_month()`
  in `tariff.py` uses a flat 14.6¢/kWh for summer (the middle of the three
  published tier rates) because the actual kWh tier breakpoints for Schedule R
  were never pulled from the filed tariff and could not be fetched from this
  session (network egress here is restricted to GitHub). This has **no effect**
  on the $459/yr battery-only ceiling — that figure is a difference between two
  Overnight Advantage bills and the baseline cancels out — but it does affect
  every "gross annual benefit" / "free switch" number and the README's two
  worked examples in Finding #2/#3. Fix: pull the real Schedule R tier
  breakpoints from the filed tariff PDF and replace `RESIDENTIAL_SERVICE_SUMMER_RATE_APPROX`
  with a real tiered calculation.

### Architecture

- `engine/tariff.py`: Generalized `UtilitySchedule` dataclass accepts rate data,
  plus the Georgia-specific `overnight_advantage_month()` / `residential_service_month()`
  bill functions `breakeven.py` calls directly (these are not routed through the
  generic `SCHEDULES` dict — see "Not yet generalized" below).
- `engine/breakeven.py`: Computes break-even lease payment
- `engine/lease.py`: Lessor cost floor vs. what battery earns

### Not yet generalized

The "generalize to support multiple utilities" refactor (commit `45deb89`) added
the `UtilitySchedule`/`Window`/`SCHEDULES` scaffolding but never migrated
`breakeven.py` onto it — `breakeven.py` calls the Georgia-specific functions
directly and ignores `SCHEDULES` entirely, so adding a new utility is *not*
actually pure data entry yet: `overnight_advantage_month()` would need to
become schedule-agnostic (it already accepts an optional `schedule` param, but
`breakeven.py`'s callers don't pass one), and Orlando/Duke/FPL are still rate
placeholders (all-zero) regardless.

`engine/multistate_analysis.py` (pre-Georgia-pivot, not cited by any other doc)
has a further, separate bug: `analyze_state()` always calls the Georgia-hardcoded
`breakeven_lease()` regardless of which state's schedule was passed in, so its
printed "battery earnings" and "lease cost floor" are identical across all four
states even though it correctly reports different peak/off-peak rates for each.
Its output table's numbers should not be trusted; the qualitative conclusion
("no state closes on arbitrage") likely still holds but is not what the code
actually demonstrates. Not fixed as part of this review — the module is legacy
and out of scope for the active Georgia-only thesis.

### Repo-integrity history (2026-09-08 finding)

`engine/breakeven.py`, `engine/lease.py`, and `engine/multistate_analysis.py`
had never successfully run in this repo's history before this date, despite
README.md, STATUS.md, and this file all citing their output as verified fact:

1. `engine/tariff.py`'s `SCHEDULES` dict referenced `OUC_ORLANDO_SHIFT_SAVE`,
   a name never defined anywhere in the file (introduced in commit `c9833ca`,
   whose message claimed real OUC rates were added — the diff shows only the
   dict-key rename, no such rates were ever added). This raised `NameError` on
   `import engine.tariff`, before any model code ran.
2. Even with (1) fixed, `breakeven.py` imported `overnight_advantage_month`
   and `residential_service_month` from `.tariff` — names that were never
   defined in this repo (confirmed via `git log -p --all -- engine/tariff.py`).
   `tariff.py` had only stub placeholders (`bill_baseline`, `bill_on_schedule`)
   that unconditionally `return 0.0` and are unused by any caller. Both were
   introduced together in the very first commit that created these files
   (`45deb89`), whose own message claimed "breakeven.py and lease.py continue
   to work with generalized schedule" and "$459/yr arbitrage ceiling" —
   already false the moment it was written.
3. `engine/multistate_analysis.py` separately imported `amortized_monthly`
   from `.breakeven` instead of `.lease`, its actual home — a third,
   independent `ImportError`.

All three are fixed as of this commit: `tariff.py` now implements
`overnight_advantage_month()` and `residential_service_month()` (see "Known
approximation" above), the `SCHEDULES` dict points at the (empty) placeholder
instead of a name that doesn't exist, and `multistate_analysis.py` imports
from the right module. All three entry points (`python -m engine.breakeven`,
`python -m engine.lease`, `python -m engine.multistate_analysis`) now run to
completion. The $459/yr and $26–38/month figures — this project's central,
decision-driving finding — are now independently re-derived from the tariff
primitives (not just copied from the README) and match the hand cross-check
exactly, which is the strongest evidence available that the core conclusion
survives this bug, even though it was never actually machine-checked before.

## Critical Blockers for Orlando

**Stale, pre-pivot content below.** STATUS.md declares Florida/Orlando
deprioritized and says its research write-ups were removed; this section
predates that decision and was missed by that cleanup. Left in place (not
deleted) since Florida could be revisited, but nothing below should be acted
on without re-confirming it against STATUS.md first. The `--utility` flag in
"Testing the Model" below doesn't exist — `breakeven.py`'s `main()` takes no
arguments and is hardcoded to Georgia; that command would silently run the
Georgia table, not an Orlando one.


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
