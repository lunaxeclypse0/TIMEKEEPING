from __future__ import annotations

import base64
import json
import sqlite3
from pathlib import Path

import pandas as pd

DEFAULT_EMPLOYEE_COLUMNS = [
    "employee_id",
    "short_name",
    "full_name",
    "schedule_in",
    "schedule_out",
]

DEFAULT_ADJUSTMENT_COLUMNS = [
    "date",
    "employee_id",
    "type",
    "value",
    "label",
    "remarks",
]


def init_storage(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_state (
            key TEXT PRIMARY KEY,
            json_value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def _load_state(db_path: Path, key: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT json_value FROM app_state WHERE key = ?", (key,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None
    return json.loads(row[0])


def _save_state(db_path: Path, key: str, value) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO app_state (key, json_value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET json_value=excluded.json_value
        """,
        (key, json.dumps(value)),
    )
    conn.commit()
    conn.close()


def default_employee_df() -> pd.DataFrame:
    from core import DEFAULT_EMPLOYEE_CONFIG

    return pd.DataFrame([
        {
            "employee_id": emp_id,
            "short_name": cfg.get("short_name", ""),
            "full_name": cfg.get("full_name", ""),
            "schedule_in": cfg.get("schedule_in", "08:00"),
            "schedule_out": cfg.get("schedule_out", "17:00"),
        }
        for emp_id, cfg in sorted(DEFAULT_EMPLOYEE_CONFIG.items())
    ])


def default_adjustments_df() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "date": "2025-12-30",
            "employee_id": "ALL",
            "type": "regular_holiday",
            "value": 1,
            "label": "Rizal Day",
            "remarks": "",
        },
        {
            "date": "2026-01-01",
            "employee_id": "ALL",
            "type": "regular_holiday",
            "value": 1,
            "label": "New Year's Day",
            "remarks": "",
        },
    ])


def load_employee_df(db_path: Path) -> pd.DataFrame:
    data = _load_state(db_path, "employee_directory")
    if not data:
        return default_employee_df()
    df = pd.DataFrame(data)
    for col in DEFAULT_EMPLOYEE_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[DEFAULT_EMPLOYEE_COLUMNS].fillna("")


def save_employee_df(db_path: Path, df: pd.DataFrame) -> None:
    cleaned = df.fillna("").copy()
    cleaned = cleaned[
        ~(
            (cleaned["employee_id"].astype(str).str.strip() == "")
            & (cleaned["short_name"].astype(str).str.strip() == "")
            & (cleaned["full_name"].astype(str).str.strip() == "")
            & (cleaned["schedule_in"].astype(str).str.strip() == "")
            & (cleaned["schedule_out"].astype(str).str.strip() == "")
        )
    ]
    payload = cleaned[DEFAULT_EMPLOYEE_COLUMNS].to_dict(orient="records")
    _save_state(db_path, "employee_directory", payload)


def load_adjustments_df(db_path: Path) -> pd.DataFrame:
    data = _load_state(db_path, "adjustments")
    if not data:
        return default_adjustments_df()
    df = pd.DataFrame(data)
    for col in DEFAULT_ADJUSTMENT_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[DEFAULT_ADJUSTMENT_COLUMNS].fillna("")


def save_adjustments_df(db_path: Path, df: pd.DataFrame) -> None:
    cleaned = df.fillna("").copy()
    cleaned = cleaned[
        ~(
            (cleaned["date"].astype(str).str.strip() == "")
            & (cleaned["employee_id"].astype(str).str.strip() == "")
            & (cleaned["type"].astype(str).str.strip() == "")
            & (cleaned["value"].astype(str).str.strip() == "")
            & (cleaned["label"].astype(str).str.strip() == "")
            & (cleaned["remarks"].astype(str).str.strip() == "")
        )
    ]
    payload = cleaned[DEFAULT_ADJUSTMENT_COLUMNS].to_dict(orient="records")
    _save_state(db_path, "adjustments", payload)


def load_settings(db_path: Path) -> dict:
    data = _load_state(db_path, "settings")
    return data if isinstance(data, dict) else {}


def save_settings(db_path: Path, data: dict) -> None:
    _save_state(db_path, "settings", data)


def find_logo_base64(base_dir: Path) -> str | None:
    possible_files = [
        "assets/1.png",
        "assets/1.jpg",
        "assets/1.jpeg",
        "assets/goclinic_logo.png",
        "assets/goclinic_logo.jpg",
        "assets/goclinic_logo.jpeg",
        "1.png",
        "1.jpg",
        "1.jpeg",
        "goclinic_logo.png",
        "goclinic_logo.jpg",
        "goclinic_logo.jpeg",
    ]

    for rel_path in possible_files:
        path = base_dir / rel_path
        if path.exists():
            return base64.b64encode(path.read_bytes()).decode("utf-8")

    return None
