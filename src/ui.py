"""Loading feedback shared by data loading and chart rendering."""

from base64 import b64encode
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path

import streamlit as st


@lru_cache(maxsize=1)
def font_stylesheet() -> str:
    font = Path(__file__).resolve().parents[1] / "assets/fonts/NotoSansThai.ttf"
    encoded = b64encode(font.read_bytes()).decode("ascii")
    return (
        '@font-face {font-family: "Noto Sans Thai"; font-style: normal; '
        'font-weight: 100 900; font-display: swap; '
        f'src: url(data:font/ttf;base64,{encoded}) format("truetype");}}'
    )


@contextmanager
def loading_skeleton(label="กำลังเตรียมข้อมูล", chart=False):
    """Remove the temporary loading surface on both success and failure."""
    placeholder = st.empty()
    shape = "skeleton-chart" if chart else "skeleton-summary"
    placeholder.markdown(
        f'<div class="loading-skeleton {shape}" role="status" aria-live="polite" '
        f'aria-busy="true"><span class="loading-label">{label}</span>'
        '<div class="skeleton-line"></div><div class="skeleton-line short"></div>'
        '<div class="skeleton-body"></div></div>',
        unsafe_allow_html=True,
    )
    try:
        yield
    finally:
        placeholder.empty()


def render_chart(factory, data, *args):
    """Show an adaptive chart and equivalent text/table for nonvisual access."""
    with loading_skeleton("กำลังเตรียมกราฟ", chart=True):
        spec = factory(data, *args)
        st.write(spec["description"])
        st.vega_lite_chart(spec=spec, width="stretch", theme=None)
        with st.expander("อ่านตารางข้อมูลของกราฟนี้"):
            # HTML tables expose rows and column headers to assistive technology.
            table = data.copy()
            if "DATE_DIAG" in table.columns:
                table["DATE_DIAG"] = table["DATE_DIAG"].dt.strftime("%d/%m/%Y")
            st.table(table)
