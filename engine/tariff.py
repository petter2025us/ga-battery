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


class MonthlyBill(NamedTuple):
    bill: float
    kwh: float


# Georgia Power Residential Service (Schedule R) base energy rates, cents/kWh.
# Winter is flat; summer is tiered. The per-kWh RATES below are sourced from
# the same 2026-09-05 pass as TOU-OA-14 (see README "What is verified vs.
# assumed"). The summer TIER BREAKPOINTS (kWh thresholds) are NOT in this
# repo and have not been pulled from the filed Schedule R tariff -- so this
# function approximates the summer bill using the middle published tier rate
# (14.6c) as a flat rate, rather than guessing at breakpoints. This makes
# `annual_bill_baseline` / `kwh_for_target_bill` (and therefore the
# "gross annual benefit" and "free switch" figures that depend on the
# Residential Service baseline) directional, not tariff-verified.
#
# The battery-only benefit (switch_only - with_battery, see breakeven.py)
# does NOT depend on this function at all -- it nets out of the baseline
# entirely -- so that number (the project's central finding) is unaffected
# by this approximation.
RESIDENTIAL_SERVICE_WINTER_RATE = 0.082
RESIDENTIAL_SERVICE_SUMMER_RATE_APPROX = 0.146  # middle of 8.8c/14.6c/15.1c; unverified breakpoints


def residential_service_month(
    kwh: float,
    month: int,
    a: Assumptions,
    schedule: UtilitySchedule | None = None,
) -> float:
    """Monthly bill on Georgia Power Residential Service (flat/tiered baseline).

    See module-level note above `RESIDENTIAL_SERVICE_SUMMER_RATE_APPROX`:
    the summer figure is an unverified approximation, not a tiered calc.
    """
    if schedule is None:
        schedule = GEORGIA_POWER_OA  # only used for basic_service_per_day/riders/franchise_fee

    is_summer = month in (6, 7, 8, 9)
    rate = RESIDENTIAL_SERVICE_SUMMER_RATE_APPROX if is_summer else RESIDENTIAL_SERVICE_WINTER_RATE

    energy = kwh * rate
    riders = kwh * schedule.riders_per_kwh
    basic = schedule.basic_service_per_day * a.days_per_month
    return (energy + riders + basic) * (1 + schedule.franchise_fee)


def overnight_advantage_month(
    kwh: float,
    month: int,
    shape: LoadShape,
    a: Assumptions,
    battery: Battery | None,
    schedule: UtilitySchedule | None = None,
) -> MonthlyBill:
    """Monthly bill on Georgia Power Overnight Advantage (TOU-OA-14).

    If `battery` is None: bill for the plan switch alone, no hardware.
    If `battery` is given: dispatch is "perfect" -- charges every night in
    the super off-peak window, discharges into whichever window would
    otherwise be most expensive that day (on-peak on summer weekdays,
    off-peak every other day). This is the dispatch the README documents
    ("Charges every night, discharges peak-first") and the exact split
    (peak weekdays vs. shoulder days) behind the README's hand cross-check.
    """
    if schedule is None:
        schedule = GEORGIA_POWER_OA

    on_rate = schedule.rate_for("on_peak")
    off_rate = schedule.rate_for("off_peak")
    sop_rate = schedule.rate_for("super_off_peak")

    is_summer = month in (6, 7, 8, 9)
    on_kwh = kwh * shape.peak_share if is_summer else 0.0
    sop_kwh = kwh * shape.super_off_peak_share
    off_kwh = kwh - on_kwh - sop_kwh

    if battery is not None:
        peak_days = a.weekdays_per_summer_month if is_summer else 0
        other_days = a.days_per_month - peak_days
        displaced_on = battery.usable_kwh * peak_days
        displaced_off = battery.usable_kwh * other_days
        charge_kwh = battery.usable_kwh * a.days_per_month / battery.round_trip_efficiency

        on_kwh = max(on_kwh - displaced_on, 0.0)
        off_kwh = max(off_kwh - displaced_off, 0.0)
        sop_kwh = sop_kwh + charge_kwh

    energy = on_kwh * on_rate + off_kwh * off_rate + sop_kwh * sop_rate
    total_kwh = on_kwh + off_kwh + sop_kwh
    riders = total_kwh * schedule.riders_per_kwh
    basic = schedule.basic_service_per_day * a.days_per_month
    bill = (energy + riders + basic) * (1 + schedule.franchise_fee)
    return MonthlyBill(bill=bill, kwh=total_kwh)


def utility_schedule(name: str) -> UtilitySchedule:
    """Retrieve a schedule by name."""
    if name not in SCHEDULES:
        raise ValueError(
            f"Unknown utility: {name}. Available: {list(SCHEDULES.keys())}"
        )
    return SCHEDULES[name]
