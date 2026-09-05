"""Generalized residential TOU battery economics model.

Supports any utility with published time-of-use rate schedules. Rate data
is external (dataclass), not hardcoded.

Usage:
  python -m engine.breakeven --utility georgia_power
  python -m engine.breakeven --utility ouc_orlando (rates needed)

Sources (verified 2026-09-05)
-------
Georgia Power TOU-OA-14:
  https://www.georgiapower.com/content/dam/georgia-power/pdfs/residential-pdfs/tariffs/2025/tou-oa-14.pdf
OUC Orlando rates (needed):
  TBD from OUC rate book at www.ouc.com
Duke Energy Florida (needed):
  TBD from FERC/FPSC filings
FPL (needed):
  TBD from FERC/FPSC filings
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple


class Season(Enum):
    SUMMER = "summer"
    WINTER = "winter"


class Window(NamedTuple):
    """A time-of-use window: name, rate, hours/day, applicable months."""

    name: str
    rate_cents_per_kwh: float
    hours_per_day: int
    months: tuple[int, ...]  # 1-12


@dataclass(frozen=True)
class UtilitySchedule:
    """A residential rate schedule for a utility.

    All rates are base tariff (before riders). Riders are applied
    identically to all windows and mostly cancel in arbitrage; the model
    treats them as a per-kWh adder for round-trip loss accounting.
    """

    name: str
    utility: str
    basic_service_per_day: float
    windows: list[Window]
    riders_per_kwh: float = 0.055  # fuel, ECCR, DSM, etc.
    franchise_fee: float = 0.03

    def rate_for(self, window_name: str) -> float:
        """Get rate in $/kWh for a named window."""
        for w in self.windows:
            if w.name == window_name:
                return w.rate_cents_per_kwh / 100.0
        raise ValueError(f"Unknown window: {window_name}")

    def windows_for_month(self, month: int) -> list[Window]:
        """All windows applicable to a given month."""
        return [w for w in self.windows if month in w.months]


# === Georgia Power TOU-OA-14 (Overnight Advantage) ===
# Verified against filed tariff, effective Jan 2025.
GEORGIA_POWER_OA = UtilitySchedule(
    name="Georgia Power — Overnight Advantage (TOU-OA-14)",
    utility="georgia_power",
    basic_service_per_day=0.4603,
    windows=[
        # On-peak: 2-7pm Mon-Fri, Jun-Sep (5 hours/day, ~21 weekdays/month)
        Window("on_peak", 29.7868, 5, (6, 7, 8, 9)),
        # Off-peak: 7am-2pm and 7pm-11pm (8 hours/day during summer),
        #           7am-11pm year-round (16 hours in winter)
        Window(
            "off_peak",
            10.1676,
            8,
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        ),
        # Super off-peak: 11pm-7am every day (8 hours/day)
        Window(
            "super_off_peak",
            2.1859,
            8,
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        ),
    ],
    riders_per_kwh=0.055,
    franchise_fee=0.03,
)

# === OUC Orlando (placeholder, rates needed from OUC rate book) ===
# To populate: contact OUC or retrieve from www.ouc.com tariff filings.
# OUC serves City of Orlando and surrounding areas; separate from Duke FL/FPL.
# Need: residential TOU rate schedule name, on-peak/off-peak/shoulder rates,
#       time windows, basic service charge, riders.
OUC_ORLANDO_TOU_PLACEHOLDER = UtilitySchedule(
    name="OUC Orlando — TOU (rates TBD)",
    utility="ouc_orlando",
    basic_service_per_day=0.00,  # PLACEHOLDER: update from filing
    windows=[
        Window("on_peak", 0.00, 0, ()),  # PLACEHOLDER
        Window("off_peak", 0.00, 0, ()),  # PLACEHOLDER
    ],
    riders_per_kwh=0.00,  # PLACEHOLDER
    franchise_fee=0.00,  # PLACEHOLDER
)

# === Duke Energy Florida (placeholder) ===
# To populate: retrieve from FPSC tariff filings for Duke's service territory.
# Multiple counties; need to confirm which territory is target.
DUKE_FLORIDA_TOU_PLACEHOLDER = UtilitySchedule(
    name="Duke Energy Florida — TOU (rates TBD)",
    utility="duke_florida",
    basic_service_per_day=0.00,  # PLACEHOLDER
    windows=[
        Window("on_peak", 0.00, 0, ()),  # PLACEHOLDER
        Window("off_peak", 0.00, 0, ()),  # PLACEHOLDER
    ],
    riders_per_kwh=0.00,  # PLACEHOLDER
    franchise_fee=0.00,  # PLACEHOLDER
)

# === FPL Florida Power & Light (placeholder) ===
# To populate: retrieve from FPSC tariff filings for FPL's service territory.
FPL_FLORIDA_TOU_PLACEHOLDER = UtilitySchedule(
    name="FPL Florida Power & Light — TOU (rates TBD)",
    utility="fpl_florida",
    basic_service_per_day=0.00,  # PLACEHOLDER
    windows=[
        Window("on_peak", 0.00, 0, ()),  # PLACEHOLDER
        Window("off_peak", 0.00, 0, ()),  # PLACEHOLDER
    ],
    riders_per_kwh=0.00,  # PLACEHOLDER
    franchise_fee=0.00,  # PLACEHOLDER
)

SCHEDULES = {
    "georgia_power": GEORGIA_POWER_OA,
    "ouc_orlando": OUC_ORLANDO_TOU_PLACEHOLDER,
    "duke_florida": DUKE_FLORIDA_TOU_PLACEHOLDER,
    "fpl_florida": FPL_FLORIDA_TOU_PLACEHOLDER,
}


@dataclass(frozen=True)
class LoadShape:
    """How a household's kWh distribute across TOU windows.

    peak_share: Fraction of summer kWh in the on-peak window.
                Unknowable from a bill total alone.
    super_off_peak_share: Fraction consumed in the super off-peak window
                          (11pm-7am), year-round.
    """

    peak_share: float = 0.20
    super_off_peak_share: float = 0.22


@dataclass(frozen=True)
class Battery:
    nameplate_kwh: float = 13.5
    depth_of_discharge: float = 0.80
    round_trip_efficiency: float = 0.90
    availability: float = 0.97

    @property
    def usable_kwh(self) -> float:
        return self.nameplate_kwh * self.depth_of_discharge * self.availability


@dataclass(frozen=True)
class Assumptions:
    summer_uplift: float = 1.35
    winter_uplift: float = 0.87
    weekdays_per_summer_month: int = 21
    days_per_month: float = 30.42


def monthly_kwh_profile(annual_avg_kwh: float, a: Assumptions) -> dict[int, float]:
    """Seasonalize annual average into 12 monthly kWh."""
    summer_months = (6, 7, 8, 9)
    return {
        m: annual_avg_kwh * (a.summer_uplift if m in summer_months else a.winter_uplift)
        for m in range(1, 13)
    }


def bill_baseline(
    kwh: float,
    month: int,
    schedule: UtilitySchedule,
    a: Assumptions,
) -> float:
    """Bill on the baseline (non-TOU) plan.

    For now, this returns a stub. Real implementation needs to
    know the utility's flat-rate plan and apply tiered rates if applicable.

    For Georgia Power Residential Service (tiered), this would be:
      8.2¢ winter, 8.8¢/14.6¢/15.1¢ summer tiers.
    """
    # Stub: return kwh * average rate
    return 0.0


def bill_on_schedule(
    kwh: float,
    month: int,
    schedule: UtilitySchedule,
    shape: LoadShape | None = None,
    battery: Battery | None = None,
    a: Assumptions | None = None,
) -> float:
    """Bill on a given TOU rate schedule.

    If battery is None, compute bill on TOU without storage.
    If battery is provided, optimize dispatch (charge off-peak, discharge peak).
    """
    if a is None:
        a = Assumptions()

    if shape is None:
        shape = LoadShape()

    # Stub: needs implementation of load distribution and dispatch logic.
    return 0.0


def utility_schedule(name: str) -> UtilitySchedule:
    """Retrieve a schedule by name."""
    if name not in SCHEDULES:
        raise ValueError(
            f"Unknown utility: {name}. Available: {list(SCHEDULES.keys())}"
        )
    return SCHEDULES[name]
