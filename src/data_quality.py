"""Small, reusable checks that explain the condition of a dataset."""

import pandas as pd


def data_quality_overview(data: pd.DataFrame) -> dict[str, int]:
    """Return the four checks shown at the top of the Data Quality section."""
    return {
        "row_count": len(data),
        "column_count": len(data.columns),
        "missing_count": int(data.isna().sum().sum()),
        "duplicate_count": int(data.duplicated().sum()),
    }


def column_quality_table(data: pd.DataFrame) -> pd.DataFrame:
    """Describe type, missing values, and unique values for every column."""
    rows = []
    for column in data.columns:
        rows.append(
            {
                "คอลัมน์": column,
                "ชนิดข้อมูล": str(data[column].dtype),
                "ค่าว่าง": int(data[column].isna().sum()),
                "ค่าที่ไม่ซ้ำ": int(data[column].nunique(dropna=True)),
            }
        )

    return pd.DataFrame(rows)


def prepare_csv_download(data: pd.DataFrame) -> bytes:
    """Create an Excel-friendly UTF-8 CSV without a DataFrame index column."""
    csv_text = data.to_csv(index=False)
    return csv_text.encode("utf-8-sig")
