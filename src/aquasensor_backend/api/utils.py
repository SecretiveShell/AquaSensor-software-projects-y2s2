from datetime import datetime
from zoneinfo import ZoneInfo


def do_saturation_percent(temperature_celsius, measured_do_mg_l):
    """
    Calculates dissolved oxygen saturation percentage.
    Based on empirical equation for freshwater at sea level.
    Source: Weiss 1970 (simplified).
    """
    T = temperature_celsius
    # DO saturation in mg/L
    do_sat = 14.621 - 0.41022 * T + 0.0079910 * T**2 - 0.000077774 * T**3
    saturation_percent = (measured_do_mg_l / do_sat) * 100
    return saturation_percent

def normalize_date(date: datetime):
    return date.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)