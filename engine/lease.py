"""What a battery lease must cost the lessor, versus what it can honestly earn.

Section 25D (the 30% homeowner credit) terminated for systems installed after
31 Dec 2025. Section 48E survives for third-party-owned systems, which is
precisely why the lease structure is the only viable one in 2026 -- the lessor
claims the credit, not the customer.

Run:  python -m engine.lease
"""

from __future__ import annotations

from .breakeven import breakeven_lease
from .tariff import Assumptions, Battery, LoadShape


def amortized_monthly(principal: float, annual_rate: float, years: int) -> float:
    r = annual_rate / 12.0
    n = years * 12
    if r == 0:
        return principal / n
    return principal * r / (1.0 - (1.0 + r) ** -n)


def lease_cost_floor(
    installed_cost: float,
    itc_rate: float = 0.30,
    cost_of_capital: float = 0.08,
    term_years: int = 25,
    om_monthly: float = 10.0,
    cac: float = 4000.0,
) -> dict:
    """Lessor's break-even payment: the point at which it earns zero margin."""
    net_capital = installed_cost * (1.0 - itc_rate) + cac
    capital_payment = amortized_monthly(net_capital, cost_of_capital, term_years)
    return {
        "installed_cost": installed_cost,
        "net_capital": net_capital,
        "term_years": term_years,
        "capital_payment": capital_payment,
        "om_monthly": om_monthly,
        "floor_monthly": capital_payment + om_monthly,
    }


def main() -> None:
    a = Assumptions()
    battery = Battery()
    shape = LoadShape(peak_share=0.20)

    r = breakeven_lease(250, shape, a, battery)
    free = -r["tariff_switch_penalty_annual"]
    honest_ceiling = (r["gross_annual_benefit"] - free) / 12

    print("What the battery earns, versus what the lease must cost")
    print("=" * 62)
    print(
        f"Honest customer-side ceiling (battery-only benefit): ${honest_ceiling:,.0f}/mo"
    )
    print("  -- and it does NOT rise with bill size; it is capacity-limited.")
    print()
    print("Lessor cost floor (zero margin, CAC $4,000, O&M $10/mo, 8% capital):")
    print()
    print(
        f"{'installed':>10} {'term':>6} {'net capital':>12} {'floor':>10} {'gap':>10}"
    )
    print("-" * 52)
    for installed in (12_000, 13_500, 16_000):
        for term in (10, 15, 25):
            f = lease_cost_floor(installed, term_years=term)
            gap = f["floor_monthly"] - honest_ceiling
            print(
                f"{installed:>10,} {term:>5}y {f['net_capital']:>12,.0f}"
                f" {f['floor_monthly']:>9,.0f}/mo {gap:>+9,.0f}/mo"
            )
    print()
    print("gap = how far underwater the customer is, before the lessor earns")
    print("      a single dollar of margin. Positive means the deal destroys")
    print("      customer value on bill savings alone.")


if __name__ == "__main__":
    main()
