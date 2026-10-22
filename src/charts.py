"""Static charts used by the exploratory notebook."""

from functools import lru_cache
from pathlib import Path

from matplotlib import font_manager
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PRIMARY_COLOR = "#2563EB"
ACCENT_COLOR = "#F59E0B"


@lru_cache(maxsize=1)
def _register_thai_font():
    font = Path(__file__).resolve().parents[1] / "assets/fonts/NotoSansThai.ttf"
    font_manager.fontManager.addfont(str(font))
    return font_manager.FontProperties(fname=str(font)).get_name()


def set_chart_style() -> None:
    """Apply one readable style to every chart."""
    sns.set_theme(style="whitegrid", rc={
        "axes.edgecolor": "#DCE2EB",
        "grid.color": "#E8EDF3",
        "grid.linewidth": 0.7,
        "text.color": "#253247",
        "axes.labelcolor": "#526176",
        "xtick.color": "#526176",
        "ytick.color": "#526176",
        "figure.facecolor": "#FFFFFF",
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    plt.rcParams["font.family"] = [_register_thai_font()]
    plt.rcParams["axes.titleweight"] = "bold"


def top_provinces_chart(summary: pd.DataFrame, year: str):
    set_chart_style()
    chart_data = summary.sort_values("อัตราต่อแสนคน", ascending=False)

    figure, axis = plt.subplots(figsize=(9, 5.5))
    sns.barplot(
        data=chart_data,
        x="อัตราต่อแสนคน",
        y="จังหวัด",
        color=PRIMARY_COLOR,
        ax=axis,
    )
    axis.set_title(f"{len(summary)} จังหวัดที่มีอัตราสูงสุด ปี {year}", loc="left", pad=18)
    axis.set_xlabel("อัตราต่อประชากร 100,000 คน")
    axis.set_ylabel("")
    axis.grid(axis="y", visible=False)
    sns.despine(left=True, bottom=True)
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
