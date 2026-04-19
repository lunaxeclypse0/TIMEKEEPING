# Timekeeping Detail Builder

This mini system converts a raw biometric/exported timekeeping file into a clean workbook with:

- **TIME IN & TIME OUT** sheet
  - employee-by-employee detailed rows
  - daily time in / time out
  - late, undertime, overtime, half day, remarks
  - total row under every employee block

- **SUMMARY** sheet
  - one row per employee
  - pulls totals from the detailed sheet
  - paid leave / holidays / remarks support

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files to upload

### 1. Raw timekeeping export
Supported:
- `.xls`
- `.xlsx`

Expected columns from the raw export:
- `Department`
- `Name`
- `No.`
- `Date/Time`
- `Location ID`
- `ID Number`
- `VerifyCode`
- `CardNo`

### 2. Optional employee config CSV
Use this if you want exact names and exact schedule rules.

Required columns:
- `employee_id`
- `short_name`
- `full_name`
- `schedule_in`
- `schedule_out`

Example:

```csv
employee_id,short_name,full_name,schedule_in,schedule_out
7,Kazz,Pavia, Kazzela Aira C.,09:00,18:00
8,Janneth,Duran, Janneth B.,06:00,15:00
```

### 3. Optional adjustments CSV
Use this for paid leave, holidays, and special manual fixes.

Columns:
- `date`
- `employee_id`
- `type`
- `value`
- `label`
- `remarks`

Supported `type` values:
- `paid_leave`
- `regular_holiday`
- `special_holiday`
- `adjustment_days`
- `half_day`

## Notes

- Raw punches are grouped by **employee + date**.
- Earliest punch becomes **time in**.
- Latest punch becomes **time out**.
- Totals are placed below each employee section.
- The workbook is built to stay close to your attached sample layout.
