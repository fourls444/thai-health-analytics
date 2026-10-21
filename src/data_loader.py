"""Functions for reading and validating the two CSV datasets."""

from pathlib import Path

import pandas as pd


HYPERTENSION_REQUIRED_COLUMNS = {
    "เขตบริการสุขภาพ",
    "จังหวัด",
    "2559",
    "2560",
    "2561",
    "ประชากรกลางปี",
}


def _read_csv(csv_path: str | Path) -> pd.DataFrame:
    """Read a UTF-8 CSV and give a clear message when the file is missing."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"ไม่พบไฟล์ข้อมูล: {path}")

    return pd.read_csv(path, encoding="utf-8-sig")


def _check_required_columns(
    data: pd.DataFrame,
    required_columns: set[str],
    dataset_name: str,
) -> None:
    missing_columns = sorted(required_columns - set(data.columns))
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"{dataset_name} ขาดคอลัมน์ที่จำเป็น: {missing_text}")


def load_hypertension_data(csv_path: str | Path) -> pd.DataFrame:
    """Load province hypertension data and convert calculation columns to numbers."""
    data = _read_csv(csv_path)
    _check_required_columns(
        data,
        HYPERTENSION_REQUIRED_COLUMNS,
        "ข้อมูลความดันโลหิตสูง",
    )

    number_columns = [
        "เขตบริการสุขภาพ",
        "2559",
        "2560",
        "2561",
        "ประชากรกลางปี",
    ]
    for column in number_columns:
        data[column] = pd.to_numeric(data[column], errors="raise")

    data["จังหวัด"] = data["จังหวัด"].astype(str).str.strip()
    return data


def load_diagnosis_data(csv_path: str | Path) -> pd.DataFrame:
    """Load diagnosis counts, parse dates, and convert code columns to numbers."""
    data = _read_csv(csv_path)
    _check_required_columns(data, {"DATE_DIAG"}, "ข้อมูลการวินิจฉัย")

    data["DATE_DIAG"] = pd.to_datetime(data["DATE_DIAG"], errors="raise")
    diagnosis_columns = [column for column in data.columns if column != "DATE_DIAG"]

    if not diagnosis_columns:
        raise ValueError("ข้อมูลการวินิจฉัยต้องมีคอลัมน์รหัสโรคอย่างน้อย 1 คอลัมน์")

    for column in diagnosis_columns:
        data[column] = pd.to_numeric(data[column], errors="raise").fillna(0)

    return data.sort_values("DATE_DIAG").reset_index(drop=True)
