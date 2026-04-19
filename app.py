from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from core import (
    build_daily_records,
    build_output_workbook,
    infer_cutoff_label,
    infer_payroll_label,
    normalize_punches,
    parse_adjustments_table,
    read_raw_rows,
    save_workbook_to_bytes,
)
from services.storage import (
    init_storage,
    load_adjustments_df,
    load_employee_df,
    load_settings,
    save_employee_df,
    save_settings,
    find_logo_base64,
)
from services.validators import (
    append_unknown_employees,
    detect_unknown_employee_ids,
    is_blank_row,
    safe_int,
    validate_employee_df,
)
from ui.banner import render_top_banner
from ui.styles import APP_CSS


st.set_page_config(
    page_title="Timekeeping System",
    page_icon="🕒",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Paths & Storage ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH  = DATA_DIR / "goclinic_timekeeping.db"

init_storage(DB_PATH)


# ── Session State Init ────────────────────────────────────────────────────────
if "employee_editor_df"   not in st.session_state:
    st.session_state.employee_editor_df   = load_employee_df(DB_PATH)
if "adjustment_editor_df" not in st.session_state:
    st.session_state.adjustment_editor_df = load_adjustments_df(DB_PATH)
if "unknown_ids"          not in st.session_state:
    st.session_state.unknown_ids          = []
if "last_processed_info"  not in st.session_state:
    st.session_state.last_processed_info  = {}
if "editing_employee_id"  not in st.session_state:
    st.session_state.editing_employee_id  = None
if "adding_employee"      not in st.session_state:
    st.session_state.adding_employee      = False


# ── Settings & Logo ───────────────────────────────────────────────────────────
settings     = load_settings(DB_PATH)
_logo_result = find_logo_base64(BASE_DIR)
if isinstance(_logo_result, tuple):
    logo_b64, logo_mime = _logo_result
else:
    logo_b64  = _logo_result
    logo_mime = "image/png"

st.markdown(APP_CSS, unsafe_allow_html=True)


# ── Schedule Presets ──────────────────────────────────────────────────────────
# ✅ UPDATED: Added 7AM-4PM and 6AM-6PM (full shift)
SCHEDULE_PRESETS = {
    "6:00 AM – 3:00 PM":  ("06:00", "15:00"),
    "7:00 AM – 4:00 PM":  ("07:00", "16:00"),
    "8:00 AM – 5:00 PM":  ("08:00", "17:00"),
    "9:00 AM – 6:00 PM":  ("09:00", "18:00"),
    "6:00 AM – 6:00 PM":  ("06:00", "18:00"),  # Full shift
}

AVATAR_COLORS = [
    "#2563eb", "#7c3aed", "#db2777", "#dc2626", "#d97706",
    "#059669", "#0891b2", "#4f46e5", "#9333ea", "#c026d3",
]

def get_avatar_color(emp_id: int) -> str:
    return AVATAR_COLORS[int(emp_id) % len(AVATAR_COLORS)]


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ System Control")

    raw_file    = st.file_uploader("1. Attendance File (.xls / .xlsx)", type=["xls", "xlsx"])
    config_file = st.file_uploader("2. Employee Directory Override (CSV, optional)", type=["csv"])
    adjust_file = st.file_uploader("3. Adjustments / Holidays (CSV, optional)", type=["csv"])

    st.divider()
    prepared_by    = st.text_input("Signatory Name",     value=settings.get("prepared_by", ""))
    prepared_title = st.text_input("Signatory Position", value=settings.get("prepared_title", ""))

    if st.button("💾 Save Signatory Info", use_container_width=True, key="save_signatory_info_btn"):
        save_settings(DB_PATH, {"prepared_by": prepared_by, "prepared_title": prepared_title})
        st.success("Signatory info saved.")


# ── Banner ────────────────────────────────────────────────────────────────────
render_top_banner(logo_b64, logo_mime)

tab1, tab2 = st.tabs(["👥 Employee Directory", "🚀 Processing Data"])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — Employee Directory
# ═════════════════════════════════════════════════════════════════════════════
with tab1:

    # ── Header Row ────────────────────────────────────────────────────────────
    hdr_l, hdr_r = st.columns([4, 1])
    with hdr_l:
        st.markdown('<div class="card-title">👥 Employee Directory</div>', unsafe_allow_html=True)
    with hdr_r:
        if st.button("➕ Add Employee", use_container_width=True, key="toggle_add_emp_btn"):
            st.session_state.adding_employee     = not st.session_state.adding_employee
            st.session_state.editing_employee_id = None
            st.rerun()

    # ── Add Employee Form ─────────────────────────────────────────────────────
    if st.session_state.adding_employee:
        st.markdown('<div class="emp-form-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="emp-form-header">'
            '<span class="emp-form-title">➕ New Employee</span>'
            '<span class="emp-form-subtitle">Fill in the employee details below</span>'
            '</div>'
            '<div class="emp-form-body">',
            unsafe_allow_html=True,
        )
        with st.form("add_employee_form", clear_on_submit=True):
            ef1, ef2 = st.columns(2)
            ef3, ef4 = st.columns(2)
            new_emp_id     = ef1.number_input("Employee ID *",         min_value=1, step=1)
            new_short_name = ef2.text_input("Short Name / Username *", placeholder="e.g. Kazz")
            new_full_name  = ef3.text_input("Full Name *",             placeholder="e.g. Pavia, Kazzela Aira C.")
            sched_label    = ef4.selectbox("Schedule Preset",          list(SCHEDULE_PRESETS.keys()), index=2)
            preset_in, preset_out = SCHEDULE_PRESETS[sched_label]
            ef5, ef6 = st.columns(2)
            new_sched_in   = ef5.text_input("Schedule In *",  value=preset_in)
            new_sched_out  = ef6.text_input("Schedule Out *", value=preset_out)
            fa1, fa2 = st.columns(2)
            submitted = fa1.form_submit_button("✅  Add Employee", use_container_width=True)
            cancelled = fa2.form_submit_button("✖  Cancel",        use_container_width=True)

            if submitted:
                new_row = pd.DataFrame([{
                    "employee_id":  int(new_emp_id),
                    "short_name":   new_short_name.strip(),
                    "full_name":    new_full_name.strip(),
                    "schedule_in":  new_sched_in.strip(),
                    "schedule_out": new_sched_out.strip(),
                }])
                candidate = pd.concat(
                    [st.session_state.employee_editor_df, new_row],
                    ignore_index=True,
                )
                issues = validate_employee_df(candidate)
                if issues:
                    st.error(issues[0])
                else:
                    st.session_state.employee_editor_df = candidate
                    save_employee_df(DB_PATH, candidate)
                    st.session_state.adding_employee = False
                    st.success("Employee added successfully.")
                    st.rerun()

            if cancelled:
                st.session_state.adding_employee = False
                st.rerun()

        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Table Header ──────────────────────────────────────────────────────────
    th1, th2, th3, th4, th5, th6 = st.columns([0.6, 2, 3, 2, 1, 1.5])
    th1.markdown('<div class="th-cell">ID</div>',        unsafe_allow_html=True)
    th2.markdown('<div class="th-cell">USERNAME</div>',  unsafe_allow_html=True)
    th3.markdown('<div class="th-cell">FULL NAME</div>', unsafe_allow_html=True)
    th4.markdown('<div class="th-cell">SCHEDULE</div>',  unsafe_allow_html=True)
    th5.markdown('<div class="th-cell">STATUS</div>',    unsafe_allow_html=True)
    th6.markdown('<div class="th-cell">ACTIONS</div>',   unsafe_allow_html=True)
    st.markdown('<div class="table-divider"></div>', unsafe_allow_html=True)

    # ── Employee Rows ─────────────────────────────────────────────────────────
    df_display = st.session_state.employee_editor_df.copy().reset_index(drop=True)

    if df_display.empty:
        st.info("No employees found. Add one using the button above.")
    else:
        for idx, row in df_display.iterrows():
            emp_id     = safe_int(row.get("employee_id")) or 0
            short_name = str(row.get("short_name", "") or "")
            full_name  = str(row.get("full_name",  "") or "")
            sched_in   = str(row.get("schedule_in",  "") or "")
            sched_out  = str(row.get("schedule_out", "") or "")
            initial    = (short_name[0] if short_name else str(emp_id)[0]).upper()
            color      = get_avatar_color(emp_id)
            is_editing = (st.session_state.editing_employee_id == emp_id)

            c1, c2, c3, c4, c5, c6 = st.columns([0.6, 2, 3, 2, 1, 1.5])

            with c1:
                st.markdown(
                    f'<div class="avatar-circle" style="background:{color}">{initial}</div>',
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f'<div class="emp-name-main">{short_name}</div>'
                    f'<div class="emp-id-sub">ID: {emp_id}</div>',
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f'<div class="emp-full-name">{full_name}</div>',
                    unsafe_allow_html=True,
                )
            with c4:
                st.markdown(
                    f'<div class="sched-badge">🕐 {sched_in} – {sched_out}</div>',
                    unsafe_allow_html=True,
                )
            with c5:
                st.markdown(
                    '<div class="status-active-badge">● Active</div>',
                    unsafe_allow_html=True,
                )
            with c6:
                btn_edit, btn_del = st.columns(2)
                with btn_edit:
                    edit_label = "✖️" if is_editing else "✏️"
                    if st.button(edit_label, key=f"edit_emp_{emp_id}_{idx}", help="Edit employee"):
                        if is_editing:
                            st.session_state.editing_employee_id = None
                        else:
                            st.session_state.editing_employee_id = emp_id
                            st.session_state.adding_employee     = False
                        st.rerun()
                with btn_del:
                    if st.button("🗑️", key=f"del_emp_{emp_id}_{idx}", help="Delete employee"):
                        updated = df_display.drop(index=idx).reset_index(drop=True)
                        st.session_state.employee_editor_df = updated
                        if is_editing:
                            st.session_state.editing_employee_id = None
                        save_employee_df(DB_PATH, updated)
                        st.success(f"Deleted: {short_name}")
                        st.rerun()

            # ── Inline Edit Form ──────────────────────────────────────────────
            if is_editing:
                st.markdown('<div class="emp-form-card">', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="emp-form-header">'
                    f'<span class="emp-form-title">✏️ Edit Employee</span>'
                    f'<span class="emp-form-subtitle">{full_name or short_name}</span>'
                    f'</div>'
                    f'<div class="emp-form-body">',
                    unsafe_allow_html=True,
                )
                with st.form(f"edit_form_{emp_id}_{idx}", clear_on_submit=False):
                    fe1, fe2 = st.columns(2)
                    fe3, fe4 = st.columns(2)
                    upd_id    = fe1.number_input("Employee ID",  value=int(emp_id), min_value=1, step=1)
                    upd_short = fe2.text_input("Short Name",     value=short_name)
                    upd_full  = fe3.text_input("Full Name",      value=full_name)

                    current_pair   = (sched_in, sched_out)
                    preset_options = list(SCHEDULE_PRESETS.keys()) + ["— Custom —"]
                    matched        = next(
                        (k for k, v in SCHEDULE_PRESETS.items() if v == current_pair),
                        "— Custom —",
                    )
                    sel_preset = fe4.selectbox(
                        "Schedule Preset", preset_options,
                        index=preset_options.index(matched),
                    )

                    if sel_preset != "— Custom —":
                        default_in, default_out = SCHEDULE_PRESETS[sel_preset]
                    else:
                        default_in, default_out = sched_in, sched_out

                    fe5, fe6  = st.columns(2)
                    upd_in    = fe5.text_input("Schedule In",  value=default_in)
                    upd_out   = fe6.text_input("Schedule Out", value=default_out)
                    fs1, fs2  = st.columns(2)
                    save_ok   = fs1.form_submit_button("💾  Save Changes", use_container_width=True)
                    cancel_ok = fs2.form_submit_button("✖  Cancel",        use_container_width=True)

                    if save_ok:
                        updated_df = st.session_state.employee_editor_df.copy()
                        match_rows = updated_df.index[
                            updated_df["employee_id"].apply(safe_int) == emp_id
                        ].tolist()
                        if match_rows:
                            r = match_rows[0]
                            updated_df.at[r, "employee_id"]  = int(upd_id)
                            updated_df.at[r, "short_name"]   = upd_short.strip()
                            updated_df.at[r, "full_name"]    = upd_full.strip()
                            updated_df.at[r, "schedule_in"]  = upd_in.strip()
                            updated_df.at[r, "schedule_out"] = upd_out.strip()
                        issues = validate_employee_df(updated_df)
                        if issues:
                            st.error(issues[0])
                        else:
                            st.session_state.employee_editor_df  = updated_df
                            st.session_state.editing_employee_id = None
                            save_employee_df(DB_PATH, updated_df)
                            st.success("Changes saved.")
                            st.rerun()

                    if cancel_ok:
                        st.session_state.editing_employee_id = None
                        st.rerun()

                st.markdown('</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="table-row-divider"></div>', unsafe_allow_html=True)

    # ── Footer Buttons ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    foot1, foot2 = st.columns(2)
    with foot1:
        st.download_button(
            "📤 Export CSV",
            data=st.session_state.employee_editor_df.to_csv(index=False).encode(),
            file_name="employees.csv",
            use_container_width=True,
            key="employee_export_csv_btn",
        )
    with foot2:
        if st.button("🔄 Reload from Database", use_container_width=True, key="employee_reload_btn"):
            st.session_state.employee_editor_df  = load_employee_df(DB_PATH)
            st.session_state.editing_employee_id = None
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — Processing Data
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    if raw_file is None:
        st.info("Upload the raw biometric Excel file from the sidebar to begin processing.")
    else:
        try:
            raw_rows = read_raw_rows(raw_file)
            punches  = normalize_punches(raw_rows)

            current_employee_df = st.session_state.employee_editor_df.copy()
            unknown_ids = detect_unknown_employee_ids(punches, current_employee_df)
            st.session_state.unknown_ids = unknown_ids

            if unknown_ids:
                st.markdown(
                    f'<div class="warn-box">⚠️ Unknown employee IDs found: '
                    f'<b>{", ".join(map(str, unknown_ids))}</b>. '
                    f'Please add them in the Employee Directory tab first.</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    "➕ Auto-add Unknown Employees",
                    use_container_width=True,
                    key="auto_add_unknown_btn",
                ):
                    st.session_state.employee_editor_df = append_unknown_employees(
                        st.session_state.employee_editor_df, unknown_ids,
                    )
                    save_employee_df(DB_PATH, st.session_state.employee_editor_df)
                    st.success(
                        "Unknown employees added with default 08:00–17:00 schedule. "
                        "Go to Employee Directory to update their schedule."
                    )
                    st.rerun()

            # Build employee config
            if config_file is not None:
                cfg_df = pd.read_csv(config_file)
            else:
                cfg_df = st.session_state.employee_editor_df.copy()

            employee_config_issues = validate_employee_df(cfg_df)
            if employee_config_issues:
                st.error(employee_config_issues[0])
                st.stop()

            employee_config: dict = {}
            for _, r in cfg_df.iterrows():
                if is_blank_row(r, ["employee_id", "short_name", "full_name", "schedule_in", "schedule_out"]):
                    continue
                eid = safe_int(r.get("employee_id"))
                if eid is None:
                    continue
                employee_config[eid] = {
                    "short_name":   str(r.get("short_name",  "") or "").strip(),
                    "full_name":    str(r.get("full_name",   "") or "").strip(),
                    "schedule_in":  str(r.get("schedule_in",  "08:00") or "08:00").strip(),
                    "schedule_out": str(r.get("schedule_out", "17:00") or "17:00").strip(),
                }

            # Build adjustments
            if adjust_file is not None:
                adj_source = pd.read_csv(adjust_file).fillna("")
            else:
                adj_source = st.session_state.adjustment_editor_df.fillna("")

            adjustments = parse_adjustments_table(adj_source.to_dict(orient="records"))

            # Process records
            records, employee_meta, _ = build_daily_records(
                punches, employee_config, adjustments,
            )

            st.session_state.last_processed_info = {
                "raw_logs":      len(punches),
                "daily_records": len(records),
                "timestamp":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            # ✅ Simple clean success message lang — walang info boxes or metric cards
            st.markdown(
                f'<div class="success-box">✅ Processing complete. '
                f'<b>{len(records)}</b> daily records generated from '
                f'<b>{len(punches)}</b> raw punch logs. '
                f'Ready to export.</div>',
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
                "🔍 Detailed View",
                "📊 Summary",
                "🆕 Unknown Employees",
                "💾 Finalize & Export",
            ])

            # Build preview dataframe
            preview_data = [
                {
                    "ID":               r.employee_id,
                    "Name":             r.display_name,
                    "Date":             r.work_date,
                    "In":               r.time_in,
                    "Out":              r.time_out,
                    "Late (Minutes)":   r.late_minutes,
                    "Undertime (Mins)": getattr(r, "undertime_minutes", ""),
                    "OT (Hours)":       r.overtime_hours,
                    "Remarks":          r.remarks,
                }
                for r in records
            ]
            pdf = pd.DataFrame(preview_data)

            with sub_tab1:
                search = st.text_input("🔎 Search Employee / Date / Remarks")
                filtered_pdf = pdf.copy()
                if search:
                    filtered_pdf = filtered_pdf[
                        filtered_pdf.astype(str)
                        .apply(lambda x: x.str.contains(search, case=False, na=False))
                        .any(axis=1)
                    ]
                st.dataframe(filtered_pdf, use_container_width=True, height=500, hide_index=True)

            with sub_tab2:
                if not pdf.empty:
                    summary = (
                        pdf.groupby("Name", as_index=False)
                        .agg({
                            "Late (Minutes)":   "sum",
                            "Undertime (Mins)": "sum",
                            "OT (Hours)":       "sum",
                            "ID":               "count",
                        })
                        .rename(columns={"ID": "Days Active"})
                    )
                    st.dataframe(summary, use_container_width=True, height=500, hide_index=True)
                else:
                    st.info("No summary available.")

            with sub_tab3:
                if st.session_state.unknown_ids:
                    unknown_df = pd.DataFrame({
                        "Unknown Employee ID": st.session_state.unknown_ids,
                        "Action Needed": ["Set schedule in Employee Directory"] * len(st.session_state.unknown_ids),
                    })
                    st.dataframe(unknown_df, use_container_width=True, height=300, hide_index=True)
                else:
                    st.success("✅ No unknown employees found.")

            with sub_tab4:
                st.success("Workbook is ready for download.")
                wb = build_output_workbook(
                    records,
                    employee_meta,
                    infer_cutoff_label(records),
                    infer_payroll_label(records),
                    adjustments,
                    prepared_by,
                    prepared_title,
                )
                st.download_button(
                    label="📥 Download Excel Report",
                    data=save_workbook_to_bytes(wb),
                    file_name="Attendance_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="download_professional_excel_report_btn",
                )

        except Exception as e:
            st.error(f"System Error: {str(e)}")


st.markdown('<div class="footer">POWERED BY GOCLINIC</div>', unsafe_allow_html=True)