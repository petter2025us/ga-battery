"""Break-even lease payment for a Georgia Power residential battery.

The commercially decisive output is NOT "estimated savings". It is:

    what is the largest monthly lease payment at which this household is not
    made worse off?

That single curve is simultaneously the go/no-go on the business and the ICP
threshold the funnel was supposed to discover from ad spend.

Run:  python -m engine.breakeven
"""

from __future__ import annotations

from .tariff import (
    Assumptions,
    Battery,
    LoadShape,
    monthly_kwh_profile,
    overnight_advantage_month,
    residential_service_month,
)


def annual_bill_baseline(annual_avg_kwh: float, a: Assumptions) -> float:
    profile = monthly_kwh_profile(annual_avg_kwh, a)
    return sum(residential_service_month(k, m, a) for m, k in profile.items())


def annual_bill_with_battery(
    annual_avg_kwh: float, shape: LoadShape, a: Assumptions, battery: Battery
) -> float:
    profile = monthly_kwh_profile(annual_avg_kwh, a)
    return sum(
        overnight_advantage_month(k, m, shape, a, battery).bill
        for m, k in profile.items()
    )


def annual_bill_plan_switch_only(
    annual_avg_kwh: float, shape: LoadShape, a: Assumptions
) -> float:
    """Overnight Advantage with NO battery -- isolates the tariff-switch risk."""
    profile = monthly_kwh_profile(annual_avg_kwh, a)
    return sum(
        overnight_advantage_month(k, m, shape, a, None).bill for m, k in profile.items()
    )


def kwh_for_target_bill(target_monthly_bill: float, a: Assumptions) -> float:
    """Invert the baseline bill to find the average monthly kWh behind it."""
    lo, hi = 50.0, 6000.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if annual_bill_baseline(mid, a) / 12 < target_monthly_bill:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def breakeven_lease(
    target_monthly_bill: float,
    shape: LoadShape,
    a: Assumptions,
    battery: Battery,
) -> dict:
    kwh = kwh_for_target_bill(target_monthly_bill, a)
    base = annual_bill_baseline(kwh, a)
    switch = annual_bill_plan_switch_only(kwh, shape, a)
    with_bat = annual_bill_with_battery(kwh, shape, a, battery)
    return {
        "target_bill": target_monthly_bill,
        "avg_kwh_month": kwh,
        "baseline_annual": base,
        "switch_only_annual": switch,
        "with_battery_annual": with_bat,
        "gross_annual_benefit": base - with_bat,
        "breakeven_lease_monthly": (base - with_bat) / 12,
        "tariff_switch_penalty_annual": switch - base,
    }


def _fmt(x: float) -> str:
    return f"{x:>8,.0f}"


def main() -> None:
    a = Assumptions()
    battery = Battery()

    print("Georgia Power residential battery -- break-even lease payment")
    print("Battery: 13.5 kWh nameplate, 80% DoD, 90% RTE, 97% availability")
    print(f"         -> {battery.usable_kwh:.1f} kWh delivered per daily cycle")
    print("Dispatch: perfect. Charges every night, discharges peak-first.")
    print()

    header = (
        f"{'bill/mo':>9} {'kWh/mo':>8} {'peak%':>6} {'gross/yr':>9}"
        f" {'free switch':>12} {'battery-only':>13} {'B/E lease':>11}"
    )
    print(header)
    print("-" * len(header))

    for bill in (150, 200, 250, 350, 500):
        for peak_share in (0.12, 0.20, 0.30):
            shape = LoadShape(peak_share=peak_share)
            r = breakeven_lease(bill, shape, a, battery)
            free = -r["tariff_switch_penalty_annual"]
            battery_only = r["gross_annual_benefit"] - free
            # A household the tariff switch would HURT will not switch, so its
            # payable ceiling is the whole-package gain, not the battery's
            # marginal value on a plan it would never have moved to.
            ceiling = min(r["gross_annual_benefit"], battery_only)
            print(
                f"{bill:>9} {r['avg_kwh_month']:>8,.0f} {peak_share:>6.0%}"
                f" {r['gross_annual_benefit']:>9,.0f}"
                f" {free:>12,.0f}"
                f" {battery_only:>13,.0f}"
                f" {ceiling / 12:>10,.0f}/mo"
            )
        print()

    print(
        "gross/yr     = total annual bill reduction vs staying on Residential Service"
    )
    print("free switch  = the part obtainable by CHANGING RATE PLAN ALONE, no battery,")
    print("               no lease, one phone call. Negative = the switch costs money.")
    print("battery-only = gross minus free switch. This is what the hardware earns,")
    print("               and it is the only part a lease payment may honestly claim.")
    print("B/E lease    = min(gross, battery-only)/12. A household the switch would")
    print("               hurt will not switch, so its ceiling is the whole package.")


if __name__ == "__main__":
    main()
