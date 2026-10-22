"""Responsive chart specifications with summaries independent of visual marks."""

import json

import pandas as pd


def _base(data: pd.DataFrame, description: str, height=320):
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
        "description": description,
        "data": {"values": json.loads(data.to_json(orient="records", date_format="iso"))},
        "width": "container",
        "height": height,
        "autosize": {"type": "fit", "contains": "padding", "resize": True},
        "config": {
            "font": "Noto Sans Thai",
            "view": {"stroke": None},
            "axis": {
                "labelFontSize": 12, "titleFontSize": 12,
                "labelColor": "#526176", "titleColor": "#253247",
                "gridColor": "#E8EDF3", "domain": False,
                "labelLimit": 120, "labelOverlap": "greedy", "titlePadding": 12,
            },
        },
    }


def top_provinces_chart(summary: pd.DataFrame, year: str):
    leading = summary.sort_values("อัตราต่อแสนคน", ascending=False).iloc[0]
    description = (
        f"ปี {year} ในกลุ่มจังหวัดที่เลือก {leading['จังหวัด']} มีอัตราสูงสุด "
        f"{leading['อัตราต่อแสนคน']:,.2f} ต่อแสนคน แสดง {len(summary)} จังหวัดเรียงจากมากไปน้อย"
    )
    spec = _base(summary, description, max(260, len(summary) * 32 + 60))
    spec.update({
        "mark": {"type": "bar", "color": "#2563EB", "cornerRadiusEnd": 3},
        "encoding": {
            "y": {"field": "จังหวัด", "type": "nominal", "sort": "-x", "title": None, "axis": {"grid": False}},
            "x": {"field": "อัตราต่อแสนคน", "type": "quantitative", "title": "อัตราต่อแสนคน", "axis": {"tickCount": 3, "format": ",.0f"}},
            "tooltip": [{"field": "จังหวัด"}, {"field": "จำนวนผู้ป่วย", "format": ",.0f"}, {"field": "อัตราต่อแสนคน", "format": ",.2f"}],
        },
    })
    return spec


def province_trend_chart(trend: pd.DataFrame, province: str):
    first, last = trend.iloc[0], trend.iloc[-1]
    description = (
        f"{province}: อัตราต่อแสนคนจาก {first['อัตราต่อแสนคน']:,.2f} ในปี {first['ปี']} "
        f"เป็น {last['อัตราต่อแสนคน']:,.2f} ในปี {last['ปี']} ใช้ประชากรฐานเดียวกันทั้ง 3 ปี"
    )
    spec = _base(trend, description)
    spec.update({
        "mark": {"type": "line", "point": True, "color": "#0F766E", "strokeWidth": 3},
        "encoding": {
            "x": {"field": "ปี", "type": "ordinal", "title": "ปี พ.ศ.", "axis": {"labelAngle": 0}},
            "y": {"field": "อัตราต่อแสนคน", "type": "quantitative", "title": "อัตราต่อแสนคน", "axis": {"tickCount": 4}},
            "tooltip": [{"field": "ปี"}, {"field": "จำนวนผู้ป่วย", "format": ",.0f"}, {"field": "อัตราต่อแสนคน", "format": ",.2f"}],
        },
    })
    return spec


def region_chart(summary: pd.DataFrame, year: str):
    leading = summary.loc[summary["อัตราต่อแสนคน"].idxmax()]
    description = (
        f"เปรียบเทียบ {len(summary)} เขตในปี {year} เขต {int(leading['เขตบริการสุขภาพ'])} "
        f"มีอัตราสูงสุด {leading['อัตราต่อแสนคน']:,.2f} ต่อแสนคน คำนวณจากยอดรวมผู้ป่วยและประชากรของแต่ละเขต"
    )
    spec = _base(summary, description, max(320, len(summary) * 28 + 60))
    spec.update({
        "mark": {"type": "bar", "color": "#0F766E", "cornerRadiusEnd": 3},
        "encoding": {
            "y": {"field": "เขตบริการสุขภาพ", "type": "ordinal", "title": "เขต", "axis": {"grid": False}},
            "x": {"field": "อัตราต่อแสนคน", "type": "quantitative", "title": "อัตราต่อแสนคน", "axis": {"tickCount": 3, "format": ",.0f"}},
            "tooltip": [{"field": "เขตบริการสุขภาพ"}, {"field": "จำนวนผู้ป่วย", "format": ",.0f"}, {"field": "อัตราต่อแสนคน", "format": ",.2f"}],
        },
    })
    return spec


def diagnosis_trend_chart(summary: pd.DataFrame, diagnosis_code: str):
    peak = summary.loc[summary["จำนวนการวินิจฉัย"].idxmax()]
    description = (
        f"หมวด {diagnosis_code}: รวม {summary['จำนวนการวินิจฉัย'].sum():,.0f} ครั้ง "
        f"ใน {len(summary)} วันที่มีข้อมูล สูงสุด {peak['จำนวนการวินิจฉัย']:,.0f} ครั้ง "
        f"วันที่ {peak['DATE_DIAG']:%d/%m/%Y} จำนวนนี้เป็นการวินิจฉัย ไม่ใช่จำนวนบุคคลที่ไม่ซ้ำกัน"
    )
    spec = _base(summary, description)
    spec.update({
        "mark": {"type": "line", "color": "#B45309", "strokeWidth": 2},
        "encoding": {
            "x": {"field": "DATE_DIAG", "type": "temporal", "title": "วันที่ (ค.ศ.)", "axis": {"tickCount": 4, "format": "%m/%Y", "labelAngle": 0}},
            "y": {"field": "จำนวนการวินิจฉัย", "type": "quantitative", "title": "จำนวนครั้ง", "axis": {"tickCount": 4}},
            "tooltip": [{"field": "DATE_DIAG", "type": "temporal", "format": "%d/%m/%Y"}, {"field": "จำนวนการวินิจฉัย", "format": ",.0f"}],
        },
    })
    return spec
