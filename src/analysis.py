"""Straightforward Pandas calculations used by the notebook and dashboard."""

import pandas as pd


YEARS = ["2559", "2560", "2561"]


def _check_year(year: str) -> None:
    if year not in YEARS:
        raise ValueError(f"ปีต้องเป็นหนึ่งใน {', '.join(YEARS)}")


def add_incidence_rates(data: pd.DataFrame) -> pd.DataFrame:
    """Add hypertension rates per 100,000 people for all available years."""
    result = data.copy()

    for year in YEARS:
        result[f"อัตรา_{year}"] = (
            result[year] * 100_000 / result["ประชากรกลางปี"]
        ).round(2)

    return result


def province_summary(
    data: pd.DataFrame,
    year: str,
    top_n: int | None = 10,
) -> pd.DataFrame:
    """Return provinces ordered by the rate for the selected year."""
    _check_year(year)
    data_with_rates = add_incidence_rates(data)

    result = data_with_rates[
        ["เขตบริการสุขภาพ", "จังหวัด", year, "ประชากรกลางปี", f"อัตรา_{year}"]
    ].copy()
    result = result.rename(
        columns={
            year: "จำนวนผู้ป่วย",
            f"อัตรา_{year}": "อัตราต่อแสนคน",
        }
    )
    result = result.sort_values("อัตราต่อแสนคน", ascending=False)

    if top_n is not None:
        result = result.head(top_n)

    return result.reset_index(drop=True)


def region_summary(data: pd.DataFrame, year: str) -> pd.DataFrame:
    """Aggregate cases and population first, then calculate each region's rate."""
    _check_year(year)

    result = (
        data.groupby("เขตบริการสุขภาพ", as_index=False)[[year, "ประชากรกลางปี"]]
        .sum()
        .rename(columns={year: "จำนวนผู้ป่วย"})
    )
    result["อัตราต่อแสนคน"] = (
        result["จำนวนผู้ป่วย"] * 100_000 / result["ประชากรกลางปี"]
    ).round(2)

    return result.sort_values("เขตบริการสุขภาพ").reset_index(drop=True)


def province_trend(data: pd.DataFrame, province: str) -> pd.DataFrame:
    """Convert one province's three year values into a chart-friendly long table."""
    selected_rows = data[data["จังหวัด"] == province]
    if selected_rows.empty:
        raise ValueError(f"ไม่พบจังหวัด: {province}")

    row = selected_rows.iloc[0]
    records = []
    for year in YEARS:
        rate = round(row[year] * 100_000 / row["ประชากรกลางปี"], 2)
        records.append(
            {
                "ปี": year,
                "จำนวนผู้ป่วย": row[year],
                "อัตราต่อแสนคน": rate,
            }
        )

    return pd.DataFrame(records)


def diagnosis_daily_summary(data: pd.DataFrame, diagnosis_code: str) -> pd.DataFrame:
    """Sum a diagnosis code by date and return a two-column time series."""
    if diagnosis_code not in data.columns or diagnosis_code == "DATE_DIAG":
        raise ValueError(f"ไม่พบรหัสการวินิจฉัย: {diagnosis_code}")

    result = (
        data.groupby("DATE_DIAG", as_index=False)[diagnosis_code]
        .sum()
        .rename(columns={diagnosis_code: "จำนวนการวินิจฉัย"})
        .sort_values("DATE_DIAG")
        .reset_index(drop=True)
    )
    return result
