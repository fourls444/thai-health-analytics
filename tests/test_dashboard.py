import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import streamlit as st
from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "app.py"


def test_missing_dataset_shows_recovery_message(monkeypatch):
    def missing_file(*args, **kwargs):
        raise FileNotFoundError("Missing CSV")

    st.cache_data.clear()
    monkeypatch.setattr("src.data_loader.load_hypertension_data", missing_file)
    try:
        app = AppTest.from_file(APP_PATH, default_timeout=30).run()
        assert not app.exception
        assert len(app.error) == 1
        assert "data/raw" in app.error[0].value
        assert not app.metric
    finally:
        st.cache_data.clear()


def test_overview_does_not_calculate_hidden_diagnosis(monkeypatch):
    def unexpected_calculation(*args, **kwargs):
        raise AssertionError("Inactive diagnosis tab was calculated")

    monkeypatch.setattr("src.analysis.diagnosis_daily_summary", unexpected_calculation)
    app = AppTest.from_file(APP_PATH, default_timeout=30).run()
    assert not app.exception


def test_each_overview_chart_has_description_and_html_data_table():
    app = AppTest.from_file(APP_PATH, default_timeout=30).run()
    assert not app.exception
    charts = app.get("vega_lite_chart")
    assert len(charts) == 3
    assert all(json.loads(chart.proto.spec)["description"] for chart in charts)
    assert len(app.table) == 3


def test_switching_tabs_keeps_filters_and_only_renders_active_charts():
    app = AppTest.from_file(APP_PATH, default_timeout=30).run()
    app.sidebar.selectbox[0].set_value("2559")
    app.sidebar.selectbox[1].set_value(1)
    app.run()
    assert not app.exception
    assert app.metric[1].value == "124,236"

    app.session_state["active_view"] = "แนวโน้มการวินิจฉัย"
    app.run()
    assert not app.exception
    assert len(app.get("vega_lite_chart")) == 1
    assert len(app.table) == 1
    assert app.sidebar.selectbox[0].value == "2559"
    assert app.sidebar.selectbox[1].value == 1

    app.session_state["active_view"] = "คุณภาพข้อมูล"
    app.run()
    assert not app.exception
    assert len(app.get("vega_lite_chart")) == 0
    assert app.sidebar.selectbox[1].value == 1


def test_notebook_chart_uses_bundled_thai_font():
    from src.charts import top_provinces_chart
    from src.analysis import province_summary
    from src.data_loader import load_hypertension_data

    data = load_hypertension_data(PROJECT_ROOT / "data/raw/hypertension_all.csv")
    figure = top_provinces_chart(province_summary(data, "2561"), "2561")
    try:
        assert "Noto Sans Thai" in figure.axes[0].title.get_fontfamily()
        resolved = Path(font_manager.findfont(figure.axes[0].title.get_fontproperties()))
        assert resolved == PROJECT_ROOT / "assets/fonts/NotoSansThai.ttf"
    finally:
        plt.close(figure)
