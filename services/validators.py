from __future__ import annotations

import re
from datetime import datetime

import pandas as pd


VALID_ADJUSTMENT_TYPES = {
    "regular_holiday",
    "special_holiday",
    "paid_leave",
    "unpaid_leave",
    "rest_day",
    "absent",
    "manual_adjustment",
    "half_day",
    "adjustment_days",
    "force_no_time_in",
    "force_no_time_out",
    "",
}

# FIX: Was r"^\\\\d{2}:\\\\d{2}$" — never matched any real time string.
TIME_PATTERN = re.compile(r"^\d{2}:\d{2}$")


def safe_int(value):
    try:
        # FIX: Guard against list/array which causes pd.isna() to raise ValueError.
        if isinstance(value, (list, dict)):
            return None
        if pd.isna(value):
            return None
        text = str(value).strip()
        return int(float(text)) if text else None
    except Exception:
        return None


def is_blank_row(row, fields: list[str]) -> bool:
    for field in fields:
        value = row.get(field, "")
        if pd.isna(value):
            value = ""
        if str(value).strip() != "":
            return False
    return True


def _is_valid_time(text: str) -> bool:
    text = str(text).strip()
    if text == "":
        return False
    if not TIME_PATTERN.match(text):
        return False
    try:
        datetime.strptime(text, "%H:%M")
        return True
    except ValueError:
        return False


def _is_valid_date_or_blank(text: str) -> bool:
    text = str(text).strip()
    if text == "":
        return True
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            datetime.strptime(text, fmt)
            return True
        except ValueError:
            continue
    return False


def validate_employee_df(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []

    if df.empty:
        issues.append("Employee directory is empty.")
        return issues

    required = {"employee_id", "short_name", "full_name", "schedule_in", "schedule_out"}
    missing = required - set(df.columns)
    if missing:
        issues.append(f"Employee directory missing columns: {', '.join(sorted(missing))}")
        return issues

    cleaned_ids = []
    schedule_issue_rows = []

    for idx, row in df.reset_index(drop=True).iterrows():
        row_no = idx + 1

        if is_blank_row(row, ["employee_id", "short_name", "full_name", "schedule_in", "schedule_out"]):
            continue

        emp_id = safe_int(row.get("employee_id"))
        if emp_id is None:
            issues.append(f"Row {row_no}: invalid employee ID.")
        else:
            cleaned_ids.append(emp_id)

        schedule_in  = str(row.get("schedule_in",  "") or "").strip()
        schedule_out = str(row.get("schedule_out", "") or "").strip()

        if schedule_in and not _is_valid_time(schedule_in):
            schedule_issue_rows.append(row_no)
        if schedule_out and not _is_valid_time(schedule_out):
            schedule_issue_rows.append(row_no)

    if len(cleaned_ids) != len(set(cleaned_ids)):
        issues.append("Duplicate employee IDs found in employee directory.")

    if schedule_issue_rows:
        unique_rows = sorted(set(schedule_issue_rows))
        joined = ", ".join(map(str, unique_rows[:10]))
        extra = f" and {len(unique_rows) - 10} more" if len(unique_rows) > 10 else ""
        issues.append(
            f"Invalid schedule format in employee rows: {joined}{extra}. "
            f"Use HH:MM format, e.g. 08:00 or 17:00."
        )

    return issues


def validate_adjustment_df(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []

    if df.empty:
        return issues

    required = {"date", "employee_id", "type", "value", "label", "remarks"}
    missing = required - set(df.columns)
    if missing:
        issues.append(f"Adjustment table missing columns: {', '.join(sorted(missing))}")
        return issues

    for idx, row in df.reset_index(drop=True).iterrows():
        row_no = idx + 1

        if is_blank_row(row, ["date", "employee_id", "type", "value", "label", "remarks"]):
            continue

        if not _is_valid_date_or_blank(str(row.get("date", ""))):
            issues.append(f"Adjustment row {row_no} has invalid date format.")

        adj_type = str(row.get("type", "")).strip()
        if adj_type and adj_type not in VALID_ADJUSTMENT_TYPES:
            issues.append(f"Adjustment row {row_no} has invalid type: {adj_type}")

    return issues


def get_punch_employee_id(punch):
    if isinstance(punch, dict):
        for key in ["employee_id", "emp_id", "id", "userid", "user_id"]:
            if key in punch:
                return safe_int(punch.get(key))
        return None
    for attr in ["employee_id", "emp_id", "id", "userid", "user_id"]:
        if hasattr(punch, attr):
            return safe_int(getattr(punch, attr))
    return None


def detect_unknown_employee_ids(punches, employee_df: pd.DataFrame) -> list[int]:
    known_ids = {
        safe_int(x)
        for x in (
            employee_df["employee_id"].tolist()
            if "employee_id" in employee_df.columns
            else []
        )
        if safe_int(x) is not None
    }
    found_ids = set()
    for punch in punches:
        emp_id = get_punch_employee_id(punch)
        if emp_id is not None:
            found_ids.add(emp_id)
    return sorted(found_ids - known_ids)


def append_unknown_employees(employee_df: pd.DataFrame, unknown_ids: list[int]) -> pd.DataFrame:
    df = employee_df.copy()
    existing = {
        safe_int(x)
        for x in (
            df["employee_id"].tolist()
            if "employee_id" in df.columns
            else []
        )
        if safe_int(x) is not None
    }
    new_rows = []
    for emp_id in unknown_ids:
        if emp_id not in existing:
            new_rows.append({
                "employee_id":  emp_id,
                "short_name":   f"EMP{emp_id}",
                "full_name":    f"New Employee {emp_id}",
                "schedule_in":  "08:00",
                "schedule_out": "17:00",
            })
    if new_rows:
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    return df