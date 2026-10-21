import pandas as pd

from src.analysis import (
    add_incidence_rates,
    diagnosis_daily_summary,
    province_summary,
    province_trend,
    region_summary,
)


def sample_hypertension_data():
    return pd.DataFrame(
        {
            "เขตบริการสุขภาพ": [1, 1, 2],
            "จังหวัด": ["Alpha", "Beta", "Gamma"],
            "2559": [100, 80, 40],
            "2560": [120, 100, 50],
            "2561": [150, 110, 60],
            "ประชากรกลางปี": [100_000, 50_000, 200_000],
        }
    )


def test_add_incidence_rates_uses_cases_per_100000_people():
    result = add_incidence_rates(sample_hypertension_data())

    assert result.loc[0, "อัตรา_2559"] == 100.0
    assert result.loc[1, "อัตรา_2559"] == 160.0


def test_region_summary_calculates_rate_from_group_totals():
    result = region_summary(sample_hypertension_data(), "2559")
    region_one = result[result["เขตบริการสุขภาพ"] == 1].iloc[0]

    assert region_one["จำนวนผู้ป่วย"] == 180
    assert region_one["ประชากรกลางปี"] == 150_000
    assert region_one["อัตราต่อแสนคน"] == 120.0


def test_province_summary_sorts_highest_rate_first():
    result = province_summary(sample_hypertension_data(), "2559", top_n=2)

    assert result["จังหวัด"].tolist() == ["Beta", "Alpha"]


def test_province_trend_returns_three_years_in_order():
    result = province_trend(sample_hypertension_data(), "Alpha")

    assert result["ปี"].tolist() == ["2559", "2560", "2561"]
    assert result["จำนวนผู้ป่วย"].tolist() == [100, 120, 150]


def test_diagnosis_daily_summary_groups_same_date():
    data = pd.DataFrame(
        {
            "DATE_DIAG": pd.to_datetime(["2016-01-01", "2016-01-01", "2016-01-02"]),
            "A": [2, 3, 7],
        }
    )

    result = diagnosis_daily_summary(data, "A")

    assert result["จำนวนการวินิจฉัย"].tolist() == [5, 7]
