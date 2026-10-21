from pathlib import Path

import pandas as pd
import pytest

from src.data_loader import load_diagnosis_data, load_hypertension_data


def test_hypertension_loader_converts_number_columns(tmp_path: Path):
    csv_path = tmp_path / "hypertension.csv"
    csv_path.write_text(
        "เขตบริการสุขภาพ,จังหวัด,2559,2560,2561,ประชากรกลางปี\n"
        "1,จังหวัดตัวอย่าง,100,110,120,50000\n",
        encoding="utf-8",
    )

    result = load_hypertension_data(csv_path)

    assert result.loc[0, "2559"] == 100
    assert result.loc[0, "ประชากรกลางปี"] == 50000
    assert pd.api.types.is_numeric_dtype(result["2561"])


def test_hypertension_loader_reports_missing_column(tmp_path: Path):
    csv_path = tmp_path / "missing.csv"
    csv_path.write_text(
        "เขตบริการสุขภาพ,จังหวัด,2559,2560,ประชากรกลางปี\n"
        "1,จังหวัดตัวอย่าง,100,110,50000\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="2561"):
        load_hypertension_data(csv_path)


def test_diagnosis_loader_parses_date(tmp_path: Path):
    csv_path = tmp_path / "diagnosis.csv"
    csv_path.write_text("DATE_DIAG,A,B\n2016-01-02,3,4\n", encoding="utf-8")

    result = load_diagnosis_data(csv_path)

    assert result.loc[0, "DATE_DIAG"] == pd.Timestamp("2016-01-02")
    assert result.loc[0, "A"] == 3
