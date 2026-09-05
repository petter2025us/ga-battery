"""Multi-state arbitrage analysis: GA, CA, TX, FL.

Compares battery economics across four markets to identify
which state(s) can support a lease-based business model.

Run: python -m engine.multistate_analysis
"""

from .breakeven import breakeven_lease, amortized_monthly
from .tariff import Assumptions, Battery, LoadShape
from .rates import ALL_SCHEDULES


def analyze_state(utility_name: str, state_label: str) -> dict:
    """Run full analysis for one utility."""
    if utility_name not in ALL_SCHEDULES:
        return {
            "state": state_label,
            "status": "UNAVAILABLE",
            "schedule_name": "N/A",
            "spread_cents": 0.0,
        }
    schedule = ALL_SCHEDULES[utility_name]

    # Extract spread from the schedule
    peaks = [w for w in schedule.windows if w.name == "on_peak"]
    offs = [w for w in schedule.windows if "off" in w.name]

    if not peaks or not offs:
        return {
            "state": state_label,
            "status": "INVALID",
            "schedule_name": schedule.name,
        }

    peak_rate = max(w.rate_cents_per_kwh for w in peaks)
    off_rate = min(w.rate_cents_per_kwh for w in offs)
    spread = peak_rate - off_rate

    # Model at $250/month bill, 20% peak share
    shape = LoadShape(peak_share=0.20)
    a = Assumptions()
    battery = Battery()

    r = breakeven_lease(250, shape, a, battery)

    # Lessor cost floor
    lessor_floor = (
        amortized_monthly(13500 * 0.70 + 4000, annual_rate=0.08, years=25) + 10.0
    )

    ceiling_monthly = min(r["gross_annual_benefit"], r["gross_annual_benefit"]) / 12
    if r["tariff_switch_penalty_annual"] < 0:
        ceiling_monthly = r["gross_annual_benefit"] / 12

    gap_monthly = ceiling_monthly - lessor_floor

    return {
        "state": state_label,
        "status": "OK",
        "utility": schedule.utility,
        "schedule_name": schedule.name,
        "peak_rate_cents": peak_rate,
        "off_peak_rate_cents": off_rate,
        "spread_cents": spread,
        "battery_earnings_annual": r["gross_annual_benefit"],
        "lease_cost_floor_monthly": lessor_floor,
        "lease_cost_floor_annual": lessor_floor * 12,
        "customer_ceiling_monthly": ceiling_monthly,
        "gap_monthly": gap_monthly,
        "gap_annual": gap_monthly * 12,
        "viable": gap_monthly > 0,
    }


def main() -> None:
    states = [
        ("georgia_power", "Georgia"),
        ("california_sdge", "California (SDG&E)"),
        ("texas_ercot", "Texas (ERCOT)"),
        ("fpl_florida", "Florida (FPL)"),
    ]

    print("=" * 100)
    print("MULTI-STATE BATTERY ARBITRAGE ANALYSIS")
    print("=" * 100)
    print()

    results = []
    for util_name, label in states:
        r = analyze_state(util_name, label)
        results.append(r)

    # Summary table
    print(
        f"{'State':<25} {'Spread':<12} {'Earnings/yr':<15} {'Lease Floor':<15} {'Gap/mo':<12} {'Viable?':<10}"
    )
    print("-" * 100)

    for r in results:
        if r["status"] != "OK":
            print(
                f"{r['state']:<25} {'N/A':<12} {'ERROR':<15} {'':<15} {'':<12} {'❌':<10}"
            )
            continue

        spread_str = f"{r['spread_cents']:.1f}¢"
        earnings_str = f"${r['battery_earnings_annual']:.0f}"
        floor_str = f"${r['lease_cost_floor_annual']:.0f}"
        gap_str = f"${r['gap_monthly']:+.0f}/mo"
        viable_str = "✓ YES" if r["viable"] else "✗ NO"

        print(
            f"{r['state']:<25} {spread_str:<12} {earnings_str:<15} {floor_str:<15} {gap_str:<12} {viable_str:<10}"
        )

    print()
    print("=" * 100)
    print("DETAILED RESULTS")
    print("=" * 100)

    for r in results:
        if r["status"] != "OK":
            print(f"\n{r['state']}: {r['status']}")
            continue

        print(f"\n{r['state'].upper()}")
        print(f"  Utility:                {r['schedule_name']}")
        print(f"  Peak rate:              {r['peak_rate_cents']:.2f}¢/kWh")
        print(f"  Off-peak rate:          {r['off_peak_rate_cents']:.2f}¢/kWh")
        print(f"  Spread:                 {r['spread_cents']:.2f}¢/kWh")
        print(f"  Battery earnings (yr):  ${r['battery_earnings_annual']:.0f}")
        print(f"  Lease cost floor (yr):  ${r['lease_cost_floor_annual']:.0f}")
        print(f"  Customer ceiling (mo):  ${r['customer_ceiling_monthly']:.0f}")
        print(f"  Gap (mo):               ${r['gap_monthly']:+.0f}")
        print(f"  Viable:                 {'✓ YES' if r['viable'] else '✗ NO'}")

    print()
    print("=" * 100)
    print("RECOMMENDATIONS")
    print("=" * 100)

    viable = [r for r in results if r.get("viable")]
    if not viable:
        print("No state shows viable arbitrage economics at $250/mo baseline.")
        print("RECOMMENDATION: Pivot to backup power (resilience insurance).")
        print("Price against generator cost, not bill savings.")
        print("Focus on SAIDI (outage frequency) in target markets.")
    else:
        print(f"Viable markets: {', '.join(r['state'] for r in viable)}")
        best = max(viable, key=lambda x: x.get("gap_monthly", -9999))
        print(f"Best market: {best['state']} (${best['gap_monthly']:.0f}/mo margin)")

    print()


if __name__ == "__main__":
    main()
