"""Chart helpers shared by the Streamlit dashboard."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PRIMARY_COLOR = "#2563EB"
SECONDARY_COLOR = "#0F766E"
ACCENT_COLOR = "#F59E0B"


def set_chart_style() -> None:
    """Apply one readable style to every chart."""
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.family"] = ["Tahoma", "DejaVu Sans"]
    plt.rcParams["axes.titleweight"] = "bold"


def top_provinces_chart(summary: pd.DataFrame, year: str):
    set_chart_style()
    chart_data = summary.sort_values("อัตราต่อแสนคน", ascending=True)

    figure, axis = plt.subplots(figsize=(9, 5.5))
    sns.barplot(
        data=chart_data,
        x="อัตราต่อแสนคน",
        y="จังหวัด",
        color=PRIMARY_COLOR,
        ax=axis,
    )
    axis.set_title(f"10 จังหวัดที่มีอัตราสูงสุด ปี {year}")
    axis.set_xlabel("อัตราต่อประชากร 100,000 คน")
    axis.set_ylabel("")
    sns.despine(left=True, bottom=True)
    figure.tight_layout()
    return figure


def province_trend_chart(trend: pd.DataFrame, province: str):
    set_chart_style()

    figure, axis = plt.subplots(figsize=(8, 4.5))
    sns.lineplot(
        data=trend,
        x="ปี",
        y="อัตราต่อแสนคน",
        marker="o",
        linewidth=3,
        markersize=8,
        color=SECONDARY_COLOR,
        ax=axis,
    )
    axis.set_title(f"แนวโน้มอัตราผู้ป่วย: {province}")
    axis.set_xlabel("ปี พ.ศ.")
    axis.set_ylabel("อัตราต่อประชากร 100,000 คน")
    figure.tight_layout()
    return figure


def region_chart(summary: pd.DataFrame, year: str):
    set_chart_style()

    figure, axis = plt.subplots(figsize=(9, 4.5))
    sns.barplot(
        data=summary,
        x="เขตบริการสุขภาพ",
        y="อัตราต่อแสนคน",
        color=SECONDARY_COLOR,
        ax=axis,
    )
    axis.set_title(f"อัตราผู้ป่วยแยกตามเขตบริการสุขภาพ ปี {year}")
    axis.set_xlabel("เขตบริการสุขภาพ")
    axis.set_ylabel("อัตราต่อประชากร 100,000 คน")
    figure.tight_layout()
    return figure


def diagnosis_trend_chart(summary: pd.DataFrame, diagnosis_code: str):
    set_chart_style()

    figure, axis = plt.subplots(figsize=(10, 4.5))
    sns.lineplot(
        data=summary,
        x="DATE_DIAG",
        y="จำนวนการวินิจฉัย",
        color=ACCENT_COLOR,
        linewidth=2,
        ax=axis,
    )
    axis.set_title(f"แนวโน้มการวินิจฉัยหมวด {diagnosis_code} รายวัน")
    axis.set_xlabel("วันที่")
    axis.set_ylabel("จำนวนการวินิจฉัย")
    figure.autofmt_xdate()
    figure.tight_layout()
    return figure
