"""Streamlit dashboard for the Thai Health Analytics portfolio project."""

from pathlib import Path

import streamlit as st

from src.analysis import (
    diagnosis_daily_summary,
    province_summary,
    province_trend,
    region_summary,
)
from src.charts import (
    diagnosis_trend_chart,
    province_trend_chart,
    region_chart,
    top_provinces_chart,
)
from src.data_loader import load_diagnosis_data, load_hypertension_data
from src.data_quality import (
    column_quality_table,
    data_quality_overview,
    prepare_csv_download,
)


PROJECT_ROOT = Path(__file__).resolve().parent
HYPERTENSION_PATH = PROJECT_ROOT / "data" / "raw" / "hypertension_all.csv"
DIAGNOSIS_PATH = PROJECT_ROOT / "data" / "raw" / "diag_code_2016.csv"


st.set_page_config(
    page_title="Health Data Explorer",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem;}
    [data-testid="stMetric"] {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px;
    }
    [data-testid="stMetricLabel"] {color: #475569 !important;}
    [data-testid="stMetricValue"] {color: #0F172A !important;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data():
    hypertension = load_hypertension_data(HYPERTENSION_PATH)
    diagnosis = load_diagnosis_data(DIAGNOSIS_PATH)
    return hypertension, diagnosis


hypertension_data, diagnosis_data = get_data()

st.title("ข้อมูลสุขภาพรายจังหวัด")
st.caption("เปรียบเทียบอัตราผู้ป่วยความดันโลหิตสูงและดูแนวโน้มการวินิจฉัย")

with st.sidebar:
    st.header("ตัวกรองข้อมูล")
    selected_year = st.selectbox("เลือกปี พ.ศ.", ["2561", "2560", "2559"])

    region_values = sorted(hypertension_data["เขตบริการสุขภาพ"].unique().tolist())
    selected_region = st.selectbox("เลือกเขตบริการสุขภาพ", ["ทุกเขต", *region_values])

    st.divider()
    st.caption("ข้อมูลสรุปรวมสำหรับการศึกษา ไม่มีข้อมูลรายบุคคล")

filtered_data = hypertension_data.copy()
if selected_region != "ทุกเขต":
    filtered_data = filtered_data[
        filtered_data["เขตบริการสุขภาพ"] == selected_region
    ]

total_cases = int(filtered_data[selected_year].sum())
total_population = int(filtered_data["ประชากรกลางปี"].sum())
overall_rate = total_cases * 100_000 / total_population

metric_one, metric_two, metric_three, metric_four = st.columns(4)
metric_one.metric("ปีที่เลือก", selected_year)
metric_two.metric("จำนวนผู้ป่วย", f"{total_cases:,.0f}")
metric_three.metric("ประชากร", f"{total_population:,.0f}")
metric_four.metric("อัตราต่อแสนคน", f"{overall_rate:,.2f}")

st.caption("อัตราต่อแสนคน = จำนวนผู้ป่วย × 100,000 ÷ ประชากรกลางปี")

overview_tab, diagnosis_tab, quality_tab = st.tabs(
    ["ภาพรวม", "แนวโน้มการวินิจฉัย", "คุณภาพข้อมูล"]
)

with overview_tab:
    left_column, right_column = st.columns(2)
    with left_column:
        top_provinces = province_summary(filtered_data, selected_year, top_n=10)
        st.pyplot(top_provinces_chart(top_provinces, selected_year), clear_figure=True)

    with right_column:
        province_options = sorted(filtered_data["จังหวัด"].unique().tolist())
        selected_province = st.selectbox("เลือกจังหวัดเพื่อดูแนวโน้ม", province_options)
        trend = province_trend(hypertension_data, selected_province)
        st.pyplot(
            province_trend_chart(trend, selected_province),
            clear_figure=True,
        )

    st.subheader("เปรียบเทียบเขตบริการสุขภาพ")
    all_regions = region_summary(hypertension_data, selected_year)
    st.pyplot(region_chart(all_regions, selected_year), clear_figure=True)

    filtered_summary = province_summary(filtered_data, selected_year, top_n=None)
    with st.expander("ตารางข้อมูลที่ใช้ในกราฟ"):
        st.dataframe(
            filtered_summary,
            width="stretch",
            hide_index=True,
        )
        region_name = "all" if selected_region == "ทุกเขต" else selected_region
        st.download_button(
            "ดาวน์โหลดตารางที่กรองแล้ว (.csv)",
            data=prepare_csv_download(filtered_summary),
            file_name=f"hypertension_{selected_year}_region_{region_name}.csv",
            mime="text/csv",
        )

with diagnosis_tab:
    st.subheader("จำนวนการวินิจฉัยรายวัน")
    diagnosis_codes = [
        column for column in diagnosis_data.columns if column != "DATE_DIAG"
    ]
    selected_code = st.selectbox("เลือกหมวดรหัสการวินิจฉัย", diagnosis_codes)
    diagnosis_trend = diagnosis_daily_summary(diagnosis_data, selected_code)
    st.pyplot(
        diagnosis_trend_chart(diagnosis_trend, selected_code),
        clear_figure=True,
    )
    st.download_button(
        "ดาวน์โหลดข้อมูลของรหัสที่เลือก (.csv)",
        data=prepare_csv_download(diagnosis_trend),
        file_name=f"diagnosis_{selected_code}_daily.csv",
        mime="text/csv",
    )

with quality_tab:
    st.subheader("ตรวจสอบข้อมูลก่อนวิเคราะห์")
    quality_dataset_name = st.selectbox(
        "เลือกชุดข้อมูล",
        ["ข้อมูลความดันโลหิตสูง", "ข้อมูลการวินิจฉัยรายวัน"],
    )
    quality_data = (
        hypertension_data
        if quality_dataset_name == "ข้อมูลความดันโลหิตสูง"
        else diagnosis_data
    )
    quality = data_quality_overview(quality_data)

    quality_one, quality_two, quality_three, quality_four = st.columns(4)
    quality_one.metric("จำนวนแถว", f"{quality['row_count']:,}")
    quality_two.metric("จำนวนคอลัมน์", quality["column_count"])
    quality_three.metric("ค่าว่าง", f"{quality['missing_count']:,}")
    quality_four.metric("แถวซ้ำ", f"{quality['duplicate_count']:,}")

    if quality["missing_count"] == 0 and quality["duplicate_count"] == 0:
        st.success("ไม่พบค่าว่างหรือแถวซ้ำในชุดข้อมูลนี้")

    st.dataframe(
        column_quality_table(quality_data),
        width="stretch",
        hide_index=True,
    )

    download_name = (
        "hypertension_all.csv"
        if quality_dataset_name == "ข้อมูลความดันโลหิตสูง"
        else "diag_code_2016.csv"
    )
    st.download_button(
        "ดาวน์โหลดชุดข้อมูลนี้ (.csv)",
        data=prepare_csv_download(quality_data),
        file_name=download_name,
        mime="text/csv",
    )

    st.caption(
        "การตรวจนี้ดูค่าว่างและแถวซ้ำเบื้องต้น "
        "ไม่ได้ยืนยันว่าค่าทุกค่าถูกต้องตามแหล่งข้อมูลต้นทาง"
    )
