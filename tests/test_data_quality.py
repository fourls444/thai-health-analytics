import pandas as pd

from src.data_quality import (
    column_quality_table,
    data_quality_overview,
    prepare_csv_download,
)


def sample_data():
    return pd.DataFrame(
        {
            "จังหวัด": ["Alpha", "Alpha", None],
            "ผู้ป่วย": [10, 10, 20],
        }
    )


def test_data_quality_overview_counts_rows_missing_values_and_duplicates():
    result = data_quality_overview(sample_data())

    assert result == {
        "row_count": 3,
        "column_count": 2,
        "missing_count": 1,
        "duplicate_count": 1,
    }


def test_column_quality_table_reports_each_column():
    result = column_quality_table(sample_data())
    province = result[result["คอลัมน์"] == "จังหวัด"].iloc[0]

    assert province["ค่าว่าง"] == 1
    assert province["ค่าที่ไม่ซ้ำ"] == 1


def test_prepare_csv_download_includes_utf8_bom_for_excel():
    result = prepare_csv_download(sample_data())

    assert result.startswith(b"\xef\xbb\xbf")
    assert "จังหวัด" in result.decode("utf-8-sig")
