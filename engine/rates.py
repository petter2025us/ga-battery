"""Rate schedules for all modeled utilities."""

from .tariff import Window, UtilitySchedule

# === Georgia Power TOU-OA-14 (Overnight Advantage) ===
GEORGIA_POWER_OA = UtilitySchedule(
    name="Georgia Power Overnight Advantage (TOU-OA-14)",
    utility="georgia_power",
    basic_service_per_day=0.4603,
    windows=[
        Window("on_peak", 29.7868, 5, (6, 7, 8, 9)),
        Window("off_peak", 10.1676, 8, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)),
        Window("super_off_peak", 2.1859, 8, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)),
    ],
    riders_per_kwh=0.055,
    franchise_fee=0.03,
)

# === California SDG&E TOU-ELEC (battery storage, non-EV) ===
CALIFORNIA_SDGE = UtilitySchedule(
    name="SDG&E San Diego TOU-ELEC (battery)",
    utility="california_sdge",
    basic_service_per_day=0.25,
    windows=[
        Window("on_peak", 65.0, 5, (6, 7, 8, 9, 10)),
        Window("off_peak", 28.0, 19, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)),
    ],
    riders_per_kwh=0.0,
    franchise_fee=0.0,
)

# === Texas ERCOT Retail TOU ===
TEXAS_ERCOT = UtilitySchedule(
    name="Texas ERCOT Retail TOU",
    utility="texas_ercot",
    basic_service_per_day=0.20,
    windows=[
        Window("on_peak", 22.0, 7, (6, 7, 8, 9)),
        Window("off_peak", 7.5, 17, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)),
    ],
    riders_per_kwh=0.0,
    franchise_fee=0.0,
)

# === Florida FPL RTR-1 ===
FPL_FLORIDA = UtilitySchedule(
    name="FPL RTR-1 Time of Use",
    utility="fpl_florida",
    basic_service_per_day=0.4603,
    windows=[
        Window("on_peak", 26.0, 9, (4, 5, 6, 7, 8, 9, 10)),
        Window("off_peak", 9.0, 15, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)),
    ],
    riders_per_kwh=0.0,
    franchise_fee=0.03,
)

ALL_SCHEDULES = {
    "georgia_power": GEORGIA_POWER_OA,
    "california_sdge": CALIFORNIA_SDGE,
    "texas_ercot": TEXAS_ERCOT,
    "fpl_florida": FPL_FLORIDA,
}
