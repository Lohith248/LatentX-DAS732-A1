"""Build the Fig 7 Tableau workbook XML from structured parts.

Not a pasted Desktop dump. Sheets, calcs, sorts, colours, and dashboard
zones are emitted from Python so validation can check each requirement.
"""
from __future__ import annotations

import hashlib
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

NS_USER = "http://www.tableausoftware.com/xml/user"
CSV_NAME = "a07_delay.csv"
DS = "federated.0a07latx732delaycsv1k9p2"
CONN = "textscan.0a07latx732delaycsvscan1"
OBJ = "a07_delay.csv_" + hashlib.sha1(b"latentx-a07-delay").hexdigest()[:32].upper()
SOURCE_BUILD = "2026.2"
VERSION = "18.1"

WS_A = "A07a Delay histogram"
WS_B = "A07b Delay by family"
WS_C = "A07c Year grid"
DASH = "A07 Report delay"

NAVY = "#1F4E79"
STEEL = "#4E79A7"
MIST = "#A8B4C0"
GREY = "#C5CBD3"
NAVY_LOW = "#E8EEF3"
TITLE_GREY = "#5B6570"

BUCKETS = ("same day", "1-7 days", "8-30 days", "31+ days")
# Regular palettes are applied in alphabetical member order if maps do not bind.
PALETTE_ASSIGN_ORDER = ("1-7 days", "31+ days", "8-30 days", "same day")
BUCKET_COLORS = {
    "same day": NAVY,
    "1-7 days": STEEL,
    "8-30 days": MIST,
    "31+ days": GREY,
}
DELAY_BIN_FORMULA = "IF [delay_days] > 60 THEN 61 ELSE [delay_days] END"
SAME_DAY_FORMULA = 'IF [delay_bucket] = "same day" THEN 1 ELSE 0 END'
REPORT_YEAR_FORMULA = "YEAR([Date Rptd])"
BUCKET_RANK_FORMULA = (
    "CASE [delay_bucket] "
    'WHEN "same day" THEN 1 '
    'WHEN "1-7 days" THEN 2 '
    'WHEN "8-30 days" THEN 3 '
    'WHEN "31+ days" THEN 4 '
    "ELSE 5 END"
)
MEDIAN_LABEL_FORMULA = (
    'IF [delay_bucket] = "31+ days" THEN '
    "{FIXED [crime_family]: MEDIAN([delay_days])} END"
)

TITLE_A = "(a) Most reports are filed the same day"
TITLE_B = "(b) Identity theft is reported late; assaults the same day"
TITLE_C = "(c) When it happened vs when it was filed"
DASH_TITLE = "Fig 7. How long before a crime is reported"
DASH_CAPTION = (
    "(a) Same-day is the mode. (b) Identity theft median 7 days; assaults median 0. "
    "(c) 94 filings have a 2025 report date; 0 crimes in this file occurred in 2025."
)


def q(name: str) -> str:
    return f"[{DS}].[{name}]"


def uid(label: str) -> str:
    return "{" + str(uuid.uuid5(uuid.NAMESPACE_URL, "latentx-a07-" + label)).upper() + "}"


def _map_color(parent: ET.Element, hex_color: str, member: str) -> None:
    mapped = ET.SubElement(parent, "map", {"to": hex_color})
    ET.SubElement(mapped, "bucket").text = f'"{member}"'


def _tableau_quote_buckets(xml: str) -> str:
    return xml.replace("<bucket>\"", "<bucket>&quot;").replace("\"</bucket>", "&quot;</bucket>")


def _col(
    parent: ET.Element,
    *,
    name: str,
    datatype: str,
    role: str,
    col_type: str,
    caption: str | None = None,
    formula: str | None = None,
    default_format: str | None = None,
    alias_61: bool = False,
) -> ET.Element:
    attrs = {
        "datatype": datatype,
        "name": f"[{name}]",
        "role": role,
        "type": col_type,
    }
    if caption:
        attrs["caption"] = caption
    if default_format:
        attrs["default-format"] = default_format
    node = ET.SubElement(parent, "column", attrs)
    if formula:
        ET.SubElement(node, "calculation", {"class": "tableau", "formula": formula})
    if alias_61:
        aliases = ET.SubElement(node, "aliases")
        ET.SubElement(aliases, "alias", {"key": "61", "value": ">60"})
    return node


def _inst(
    parent: ET.Element,
    *,
    column: str,
    derivation: str,
    name: str,
    inst_type: str,
    table_calc: dict[str, str] | None = None,
    order_fields: tuple[str, ...] = (),
) -> ET.Element:
    node = ET.SubElement(
        parent,
        "column-instance",
        {
            "column": f"[{column}]",
            "derivation": derivation,
            "name": f"[{name}]",
            "pivot": "key",
            "type": inst_type,
        },
    )
    if table_calc:
        tc = ET.SubElement(node, "table-calc", table_calc)
        for field in order_fields:
            ET.SubElement(tc, "order", {"field": field})
    return node


def _title_block(parent: ET.Element, title: str, subtitle: str | None = None) -> None:
    layout = ET.SubElement(parent, "layout-options")
    title_el = ET.SubElement(layout, "title")
    text = ET.SubElement(title_el, "formatted-text")
    ET.SubElement(
        text, "run", {"fontname": "Tableau Bold", "fontsize": "15"}
    ).text = title
    if subtitle:
        ET.SubElement(text, "run").text = "\n"
        ET.SubElement(
            text, "run", {"fontcolor": TITLE_GREY, "fontsize": "10"}
        ).text = subtitle


def _sheet_deps(view: ET.Element) -> ET.Element:
    deps = ET.SubElement(view, "datasource-dependencies", {"datasource": DS})
    _col(deps, name="DR_NO", datatype="string", role="dimension", col_type="nominal")
    _col(deps, name="Date Rptd", datatype="date", role="dimension", col_type="ordinal")
    _col(
        deps,
        name="delay_days",
        datatype="integer",
        role="measure",
        col_type="quantitative",
        default_format="n#,##0",
    )
    _col(deps, name="delay_bucket", datatype="string", role="dimension", col_type="nominal")
    _col(
        deps,
        name="crime_family",
        datatype="string",
        role="dimension",
        col_type="nominal",
        caption="Crime Family",
    )
    _col(deps, name="year_occ", datatype="integer", role="dimension", col_type="ordinal")
    _col(
        deps,
        name="Delay bin",
        datatype="integer",
        role="dimension",
        col_type="ordinal",
        caption="Delay bin",
        formula=DELAY_BIN_FORMULA,
        alias_61=True,
    )
    _col(
        deps,
        name="Same day flag",
        datatype="integer",
        role="measure",
        col_type="quantitative",
        caption="Same day flag",
        formula=SAME_DAY_FORMULA,
    )
    _col(
        deps,
        name="Report year",
        datatype="integer",
        role="dimension",
        col_type="ordinal",
        caption="Report year",
        formula=REPORT_YEAR_FORMULA,
    )
    _col(
        deps,
        name="Delay bucket rank",
        datatype="integer",
        role="dimension",
        col_type="ordinal",
        caption="Delay bucket rank",
        formula=BUCKET_RANK_FORMULA,
    )
    _inst(deps, column="DR_NO", derivation="Count", name="cnt:DR_NO:qk", inst_type="quantitative")
    _inst(
        deps,
        column="DR_NO",
        derivation="Count",
        name="pcto:cnt:DR_NO:qk",
        inst_type="quantitative",
        table_calc={"ordering-type": "Rows", "type": "PctTotal"},
    )
    _inst(
        deps,
        column="delay_days",
        derivation="Median",
        name="med:delay_days:qk",
        inst_type="quantitative",
    )
    _col(
        deps,
        name="Family median label",
        datatype="real",
        role="measure",
        col_type="quantitative",
        caption="Family median label",
        formula=MEDIAN_LABEL_FORMULA,
        default_format='n0" d median"',
    )
    _inst(
        deps,
        column="Family median label",
        derivation="Min",
        name="min:Family median label:qk",
        inst_type="quantitative",
    )
    _inst(
        deps,
        column="Same day flag",
        derivation="Avg",
        name="avg:Same day flag:qk",
        inst_type="quantitative",
    )
    _inst(
        deps,
        column="Delay bucket rank",
        derivation="None",
        name="none:Delay bucket rank:ok",
        inst_type="ordinal",
    )
    _inst(deps, column="Delay bin", derivation="None", name="none:Delay bin:ok", inst_type="ordinal")
    _inst(
        deps,
        column="crime_family",
        derivation="None",
        name="none:crime_family:nk",
        inst_type="nominal",
    )
    _inst(
        deps,
        column="delay_bucket",
        derivation="None",
        name="none:delay_bucket:nk",
        inst_type="nominal",
    )
    _inst(deps, column="year_occ", derivation="None", name="none:year_occ:ok", inst_type="ordinal")
    _inst(
        deps,
        column="Report year",
        derivation="None",
        name="none:Report year:ok",
        inst_type="ordinal",
    )
    return deps


def _base_view(table: ET.Element, *, report_years: tuple[int, ...] | None = None) -> ET.Element:
    view = ET.SubElement(table, "view")
    ET.SubElement(view, "datasources")
    ET.SubElement(view.find("datasources"), "datasource", {"caption": "LAPD clean", "name": DS})
    _sheet_deps(view)
    if report_years:
        filt = ET.SubElement(
            view,
            "filter",
            {"class": "categorical", "column": q("none:Report year:ok")},
        )
        union = ET.SubElement(filt, "groupfilter", {"function": "union"})
        for year in report_years:
            ET.SubElement(
                union,
                "groupfilter",
                {
                    "function": "member",
                    "level": "[none:Report year:ok]",
                    "member": str(year),
                },
            )
    else:
        filt = ET.SubElement(
            view,
            "filter",
            {"class": "categorical", "column": q("none:crime_family:nk")},
        )
        ET.SubElement(filt, "groupfilter", {"function": "level-members", "level": "[crime_family]"})
    return view


def _finish_view(view: ET.Element) -> None:
    ET.SubElement(view, "aggregation", {"value": "true"})


def _pane(parent: ET.Element, mark: str) -> ET.Element:
    pane = ET.SubElement(
        parent, "pane", {"selection-relaxation-option": "selection-relaxation-allow"}
    )
    ET.SubElement(ET.SubElement(pane, "view"), "breakdown", {"value": "auto"})
    ET.SubElement(pane, "mark", {"class": mark})
    return pane


def _worksheet_a() -> ET.Element:
    ws = ET.Element("worksheet", {"name": WS_A})
    _title_block(ws, TITLE_A)
    table = ET.SubElement(ws, "table")
    view = _base_view(table)
    ET.SubElement(
        view,
        "sort",
        {
            "class": "computed",
            "column": q("none:Delay bin:ok"),
            "direction": "ASC",
            "using": q("none:Delay bin:ok"),
        },
    )
    _finish_view(view)
    style = ET.SubElement(table, "style")
    axis = ET.SubElement(style, "style-rule", {"element": "axis"})
    ET.SubElement(
        axis,
        "format",
        {
            "attr": "title",
            "class": "0",
            "field": q("cnt:DR_NO:qk"),
            "scope": "rows",
            "value": "Reports",
        },
    )
    ET.SubElement(
        axis,
        "format",
        {
            "attr": "title",
            "class": "0",
            "field": q("none:Delay bin:ok"),
            "scope": "cols",
            "value": "Days from occurrence to report",
        },
    )
    sheet = ET.SubElement(style, "style-rule", {"element": "worksheet"})
    for scope in ("cols", "rows"):
        ET.SubElement(
            sheet,
            "format",
            {"attr": "display-field-labels", "scope": scope, "value": "false"},
        )
    panes = ET.SubElement(table, "panes")
    pane = _pane(panes, "Bar")
    pane_style = ET.SubElement(pane, "style")
    mark_rule = ET.SubElement(pane_style, "style-rule", {"element": "mark"})
    ET.SubElement(mark_rule, "format", {"attr": "mark-color", "value": NAVY})
    ET.SubElement(mark_rule, "format", {"attr": "mark-labels-show", "value": "false"})
    ET.SubElement(table, "rows").text = q("cnt:DR_NO:qk")
    ET.SubElement(table, "cols").text = q("none:Delay bin:ok")
    ET.SubElement(ws, "simple-id", {"uuid": uid("ws-a")})
    return ws


def _worksheet_b() -> ET.Element:
    ws = ET.Element("worksheet", {"name": WS_B})
    _title_block(ws, TITLE_B)
    table = ET.SubElement(ws, "table")
    view = _base_view(table)
    ET.SubElement(
        view,
        "sort",
        {
            "class": "computed",
            "column": q("none:crime_family:nk"),
            "direction": "DESC",
            "using": q("avg:Same day flag:qk"),
        },
    )
    ET.SubElement(
        view,
        "sort",
        {
            "class": "computed",
            "column": q("none:delay_bucket:nk"),
            "direction": "ASC",
            "using": q("none:Delay bucket rank:ok"),
        },
    )
    _finish_view(view)
    style = ET.SubElement(table, "style")
    axis = ET.SubElement(style, "style-rule", {"element": "axis"})
    ET.SubElement(
        axis,
        "format",
        {
            "attr": "title",
            "class": "0",
            "field": q("pcto:cnt:DR_NO:qk"),
            "scope": "cols",
            "value": "Share of that family's reports",
        },
    )
    cell = ET.SubElement(style, "style-rule", {"element": "cell"})
    ET.SubElement(
        cell,
        "format",
        {"attr": "text-format", "field": q("pcto:cnt:DR_NO:qk"), "value": "p0%"},
    )
    ET.SubElement(
        cell,
        "format",
        {
            "attr": "text-format",
            "field": q("min:Family median label:qk"),
            "value": 'n0" d median"',
        },
    )
    legend_title = ET.SubElement(style, "style-rule", {"element": "legend-title-text"})
    legend_fmt = ET.SubElement(
        legend_title,
        "format",
        {
            "attr": "color",
            "field": q("none:delay_bucket:nk"),
            "value": "Report delay",
        },
    )
    legend_text = ET.SubElement(legend_fmt, "formatted-text")
    ET.SubElement(legend_text, "run").text = "Report delay"
    sheet = ET.SubElement(style, "style-rule", {"element": "worksheet"})
    ET.SubElement(
        sheet,
        "format",
        {"attr": "display-field-labels", "scope": "cols", "value": "false"},
    )
    panes = ET.SubElement(table, "panes")
    pane = _pane(panes, "Bar")
    encodings = ET.SubElement(pane, "encodings")
    ET.SubElement(encodings, "color", {"column": q("none:delay_bucket:nk")})
    ET.SubElement(encodings, "text", {"column": q("min:Family median label:qk")})
    pane_style = ET.SubElement(pane, "style")
    label_rule = ET.SubElement(pane_style, "style-rule", {"element": "datalabel"})
    ET.SubElement(label_rule, "format", {"attr": "font-size", "value": "9"})
    ET.SubElement(label_rule, "format", {"attr": "color", "value": "#1A1D21"})
    mark_rule = ET.SubElement(pane_style, "style-rule", {"element": "mark"})
    ET.SubElement(mark_rule, "format", {"attr": "mark-labels-show", "value": "true"})
    ET.SubElement(mark_rule, "format", {"attr": "mark-labels-cull", "value": "true"})
    ET.SubElement(table, "rows").text = q("none:crime_family:nk")
    ET.SubElement(table, "cols").text = q("pcto:cnt:DR_NO:qk")
    ET.SubElement(ws, "simple-id", {"uuid": uid("ws-b")})
    return ws


def _worksheet_c() -> ET.Element:
    ws = ET.Element("worksheet", {"name": WS_C})
    _title_block(ws, TITLE_C)
    table = ET.SubElement(ws, "table")
    view = _base_view(table, report_years=(2020, 2021, 2022, 2023, 2024, 2025))
    ET.SubElement(
        view,
        "sort",
        {
            "class": "computed",
            "column": q("none:year_occ:ok"),
            "direction": "ASC",
            "using": q("none:year_occ:ok"),
        },
    )
    ET.SubElement(
        view,
        "sort",
        {
            "class": "computed",
            "column": q("none:Report year:ok"),
            "direction": "ASC",
            "using": q("none:Report year:ok"),
        },
    )
    _finish_view(view)
    style = ET.SubElement(table, "style")
    color_rule = ET.SubElement(style, "style-rule", {"element": "mark"})
    encoding = ET.SubElement(
        color_rule,
        "encoding",
        {
            "attr": "color",
            "field": q("cnt:DR_NO:qk"),
            "num-steps": "5",
            "palette": "A07_navy_sequential",
            "type": "interpolated",
        },
    )
    cell = ET.SubElement(style, "style-rule", {"element": "cell"})
    ET.SubElement(
        cell,
        "format",
        {"attr": "text-format", "field": q("cnt:DR_NO:qk"), "value": "n#,##0"},
    )
    panes = ET.SubElement(table, "panes")
    pane = _pane(panes, "Square")
    encodings = ET.SubElement(pane, "encodings")
    ET.SubElement(encodings, "color", {"column": q("cnt:DR_NO:qk")})
    ET.SubElement(encodings, "text", {"column": q("cnt:DR_NO:qk")})
    pane_style = ET.SubElement(pane, "style")
    mark_rule = ET.SubElement(pane_style, "style-rule", {"element": "mark"})
    ET.SubElement(mark_rule, "format", {"attr": "size", "value": "1.5"})
    ET.SubElement(mark_rule, "format", {"attr": "mark-labels-show", "value": "true"})
    ET.SubElement(table, "rows").text = q("none:year_occ:ok")
    ET.SubElement(table, "cols").text = q("none:Report year:ok")
    ET.SubElement(ws, "simple-id", {"uuid": uid("ws-c")})
    return ws


def _zone_attrs(zone_id: str, x: int, y: int, w: int, h: int, extra: dict | None = None) -> dict:
    attrs = {
        "h": str(h),
        "id": zone_id,
        "w": str(w),
        "x": str(x),
        "y": str(y),
    }
    if extra:
        attrs.update(extra)
    return attrs


def _dashboard() -> ET.Element:
    dash = ET.Element("dashboard", {"enable-sort-zone-taborder": "true", "name": DASH})
    layout = ET.SubElement(dash, "layout-options")
    title = ET.SubElement(layout, "title")
    text = ET.SubElement(title, "formatted-text")
    ET.SubElement(
        text, "run", {"fontname": "Tableau Bold", "fontsize": "18"}
    ).text = DASH_TITLE
    ET.SubElement(dash, "size", {
        "maxheight": "1200",
        "maxwidth": "1600",
        "minheight": "1200",
        "minwidth": "1600",
    })
    zones = ET.SubElement(dash, "zones")
    root = ET.SubElement(
        zones,
        "zone",
        _zone_attrs("1", 0, 0, 100000, 100000, {"type-v2": "layout-basic"}),
    )
    title_zone = ET.SubElement(
        root,
        "zone",
        _zone_attrs("2", 0, 0, 100000, 4000, {"type-v2": "title"}),
    )
    _zone_style(title_zone)
    cap = ET.SubElement(
        root,
        "zone",
        _zone_attrs("3", 0, 4000, 100000, 3500, {"type-v2": "text"}),
    )
    cap_text = ET.SubElement(cap, "formatted-text")
    ET.SubElement(
        cap_text, "run", {"fontcolor": TITLE_GREY, "fontsize": "11"}
    ).text = DASH_CAPTION
    _zone_style(cap)
    a = ET.SubElement(
        root,
        "zone",
        _zone_attrs("4", 0, 7500, 100000, 22000, {"name": WS_A, "show-title": "true"}),
    )
    _zone_style(a)
    b_wrap = ET.SubElement(
        root,
        "zone",
        _zone_attrs("5", 0, 29500, 100000, 40500, {"type-v2": "layout-basic"}),
    )
    b = ET.SubElement(
        b_wrap,
        "zone",
        _zone_attrs("6", 0, 0, 100000, 88000, {"name": WS_B, "show-title": "true"}),
    )
    _zone_style(b)
    legend = ET.SubElement(
        b_wrap,
        "zone",
        _zone_attrs(
            "7",
            0,
            88000,
            100000,
            12000,
            {
                "name": "Report delay",
                "pane-specification-id": "0",
                "param": q("none:delay_bucket:nk"),
                "type-v2": "color",
                "show-title": "true",
            },
        ),
    )
    _zone_style(legend)
    c_wrap = ET.SubElement(
        root,
        "zone",
        _zone_attrs("8", 0, 70000, 100000, 30000, {"type-v2": "layout-basic"}),
    )
    c = ET.SubElement(
        c_wrap,
        "zone",
        _zone_attrs("9", 0, 0, 88000, 100000, {"name": WS_C, "show-title": "true"}),
    )
    _zone_style(c)
    c_leg = ET.SubElement(
        c_wrap,
        "zone",
        _zone_attrs(
            "10",
            88000,
            0,
            12000,
            100000,
            {
                "pane-specification-id": "0",
                "param": q("cnt:DR_NO:qk"),
                "type-v2": "color",
                "show-title": "true",
            },
        ),
    )
    _zone_style(c_leg)
    ET.SubElement(dash, "simple-id", {"uuid": uid("dash")})
    return dash


def _zone_style(zone: ET.Element) -> None:
    style = ET.SubElement(zone, "zone-style")
    ET.SubElement(style, "format", {"attr": "border-color", "value": "#000000"})
    ET.SubElement(style, "format", {"attr": "border-style", "value": "none"})
    ET.SubElement(style, "format", {"attr": "border-width", "value": "0"})
    ET.SubElement(style, "format", {"attr": "margin", "value": "4"})


def _cards(window: ET.Element, legends: list[tuple[str, str]] | None = None) -> None:
    cards = ET.SubElement(window, "cards")
    left = ET.SubElement(cards, "edge", {"name": "left"})
    left_strip = ET.SubElement(left, "strip", {"size": "160"})
    for card_type in ("pages", "filters", "marks"):
        ET.SubElement(left_strip, "card", {"type": card_type})
    top = ET.SubElement(cards, "edge", {"name": "top"})
    for card_type, size in (("columns", "2147483647"), ("rows", "2147483647"), ("title", "90")):
        ET.SubElement(
            ET.SubElement(top, "strip", {"size": size}), "card", {"type": card_type}
        )
    if legends:
        right = ET.SubElement(cards, "edge", {"name": "right"})
        strip = ET.SubElement(right, "strip", {"size": "160"})
        for card_type, param in legends:
            ET.SubElement(
                strip,
                "card",
                {"pane-specification-id": "0", "param": param, "type": card_type},
            )


def _windows() -> ET.Element:
    windows = ET.Element("windows", {"source-height": "30"})
    for name, legends in (
        (WS_A, None),
        (WS_B, [("color", q("none:delay_bucket:nk"))]),
        (WS_C, [("color", q("cnt:DR_NO:qk"))]),
    ):
        win = ET.SubElement(windows, "window", {"class": "worksheet", "name": name})
        _cards(win, legends)
        viewpoint = ET.SubElement(win, "viewpoint")
        ET.SubElement(viewpoint, "zoom", {"type": "entire-view"})
        ET.SubElement(win, "simple-id", {"uuid": uid("win-" + name)})
    dash_win = ET.SubElement(
        windows,
        "window",
        {"class": "dashboard", "maximized": "true", "name": DASH},
    )
    viewpoints = ET.SubElement(dash_win, "viewpoints")
    for name in (WS_A, WS_B, WS_C):
        vp = ET.SubElement(viewpoints, "viewpoint", {"name": name})
        ET.SubElement(vp, "zoom", {"type": "entire-view"})
    ET.SubElement(dash_win, "active", {"id": "1"})
    ET.SubElement(dash_win, "simple-id", {"uuid": uid("win-dash")})
    return windows


def _datasource() -> ET.Element:
    ds = ET.Element(
        "datasource",
        {"caption": "LAPD clean", "inline": "true", "name": DS, "version": VERSION},
    )
    connection = ET.SubElement(ds, "connection", {"class": "federated"})
    named = ET.SubElement(connection, "named-connections")
    named_conn = ET.SubElement(
        named, "named-connection", {"caption": "LAPD clean", "name": CONN}
    )
    ET.SubElement(
        named_conn,
        "connection",
        {
            "class": "textscan",
            "directory": "Data/A07",
            "filename": CSV_NAME,
            "password": "",
            "server": "",
        },
    )
    for flag in ("false", "true"):
        tag = f"_.fcp.ObjectModelEncapsulateLegacy.{flag}...relation"
        rel = ET.SubElement(
            connection,
            tag,
            {"connection": CONN, "name": CSV_NAME, "table": "[a07_delay#csv]", "type": "table"},
        )
        cols = ET.SubElement(
            rel,
            "columns",
            {"character-set": "UTF-8", "header": "yes", "locale": "en_US", "separator": ","},
        )
        ET.SubElement(cols, "column", {"datatype": "string", "name": "DR_NO", "ordinal": "0"})
        ET.SubElement(cols, "column", {"datatype": "date", "name": "Date Rptd", "ordinal": "1"})
        ET.SubElement(
            cols, "column", {"datatype": "integer", "name": "delay_days", "ordinal": "2"}
        )
        ET.SubElement(
            cols, "column", {"datatype": "string", "name": "delay_bucket", "ordinal": "3"}
        )
        ET.SubElement(
            cols, "column", {"datatype": "string", "name": "crime_family", "ordinal": "4"}
        )
        ET.SubElement(
            cols, "column", {"datatype": "integer", "name": "year_occ", "ordinal": "5"}
        )
    meta = ET.SubElement(connection, "metadata-records")
    cap = ET.SubElement(meta, "metadata-record", {"class": "capability"})
    ET.SubElement(cap, "remote-name")
    ET.SubElement(cap, "remote-type").text = "0"
    ET.SubElement(cap, "parent-name").text = f"[{CSV_NAME}]"
    ET.SubElement(cap, "remote-alias")
    ET.SubElement(cap, "aggregation").text = "Count"
    ET.SubElement(cap, "contains-null").text = "true"
    specs = (
        ("DR_NO", "129", "string", "Count"),
        ("Date Rptd", "133", "date", "Year"),
        ("delay_days", "20", "integer", "Sum"),
        ("delay_bucket", "129", "string", "Count"),
        ("crime_family", "129", "string", "Count"),
        ("year_occ", "20", "integer", "Sum"),
    )
    for i, (name, remote_type, local_type, agg) in enumerate(specs):
        rec = ET.SubElement(meta, "metadata-record", {"class": "column"})
        ET.SubElement(rec, "remote-name").text = name
        ET.SubElement(rec, "remote-type").text = remote_type
        ET.SubElement(rec, "local-name").text = f"[{name}]"
        ET.SubElement(rec, "parent-name").text = f"[{CSV_NAME}]"
        ET.SubElement(rec, "remote-alias").text = name
        ET.SubElement(rec, "ordinal").text = str(i)
        ET.SubElement(rec, "local-type").text = local_type
        ET.SubElement(rec, "aggregation").text = agg
        ET.SubElement(rec, "contains-null").text = "true"
        obj = ET.SubElement(
            rec, "_.fcp.ObjectModelEncapsulateLegacy.true...object-id"
        )
        obj.text = f"[{OBJ}]"
    ET.SubElement(ds, "aliases", {"enabled": "yes"})
    _col(ds, name="DR_NO", datatype="string", role="dimension", col_type="nominal")
    _col(ds, name="Date Rptd", datatype="date", role="dimension", col_type="ordinal")
    _col(
        ds,
        name="delay_days",
        datatype="integer",
        role="measure",
        col_type="quantitative",
        default_format="n#,##0",
    )
    _col(ds, name="delay_bucket", datatype="string", role="dimension", col_type="nominal")
    _col(
        ds,
        name="crime_family",
        datatype="string",
        role="dimension",
        col_type="nominal",
        caption="Crime Family",
    )
    _col(ds, name="year_occ", datatype="integer", role="dimension", col_type="ordinal")
    _col(
        ds,
        name="Delay bin",
        datatype="integer",
        role="dimension",
        col_type="ordinal",
        caption="Delay bin",
        formula=DELAY_BIN_FORMULA,
        alias_61=True,
    )
    _col(
        ds,
        name="Same day flag",
        datatype="integer",
        role="measure",
        col_type="quantitative",
        caption="Same day flag",
        formula=SAME_DAY_FORMULA,
    )
    _col(
        ds,
        name="Report year",
        datatype="integer",
        role="dimension",
        col_type="ordinal",
        caption="Report year",
        formula=REPORT_YEAR_FORMULA,
    )
    _col(
        ds,
        name="Delay bucket rank",
        datatype="integer",
        role="dimension",
        col_type="ordinal",
        caption="Delay bucket rank",
        formula=BUCKET_RANK_FORMULA,
    )
    _col(
        ds,
        name="Family median label",
        datatype="real",
        role="measure",
        col_type="quantitative",
        caption="Family median label",
        formula=MEDIAN_LABEL_FORMULA,
        default_format='n0" d median"',
    )
    ET.SubElement(
        ds,
        "_.fcp.ObjectModelTableType.true...column",
        {
            "caption": "LAPD clean",
            "datatype": "table",
            "name": f"[__tableau_internal_object_id__].[{OBJ}]",
            "role": "measure",
            "type": "quantitative",
        },
    )
    _inst(ds, column="DR_NO", derivation="Count", name="cnt:DR_NO:qk", inst_type="quantitative")
    _inst(
        ds,
        column="DR_NO",
        derivation="Count",
        name="pcto:cnt:DR_NO:qk",
        inst_type="quantitative",
        table_calc={"ordering-type": "Rows", "type": "PctTotal"},
    )
    _inst(
        ds,
        column="delay_bucket",
        derivation="None",
        name="none:delay_bucket:nk",
        inst_type="nominal",
    )
    _inst(
        ds,
        column="Family median label",
        derivation="Min",
        name="min:Family median label:qk",
        inst_type="quantitative",
    )
    ds_style = ET.SubElement(ds, "style")
    mark_rule = ET.SubElement(ds_style, "style-rule", {"element": "mark"})
    bucket_enc = ET.SubElement(
        mark_rule,
        "encoding",
        {
            "attr": "color",
            "field": "[none:delay_bucket:nk]",
            "type": "palette",
        },
    )
    for bucket in BUCKETS:
        _map_color(bucket_enc, BUCKET_COLORS[bucket], bucket)
    seq_enc = ET.SubElement(
        mark_rule,
        "encoding",
        {
            "attr": "color",
            "field": "[cnt:DR_NO:qk]",
            "num-steps": "5",
            "palette": "A07_navy_sequential",
            "type": "interpolated",
        },
    )
    graph = ET.SubElement(ds, "_.fcp.ObjectModelEncapsulateLegacy.true...object-graph")
    objects = ET.SubElement(graph, "objects")
    obj = ET.SubElement(objects, "object", {"caption": "LAPD clean", "id": OBJ})
    props = ET.SubElement(obj, "properties", {"context": ""})
    rel = ET.SubElement(
        props,
        "relation",
        {"connection": CONN, "name": CSV_NAME, "table": "[a07_delay#csv]", "type": "table"},
    )
    cols = ET.SubElement(
        rel,
        "columns",
        {"character-set": "UTF-8", "header": "yes", "locale": "en_US", "separator": ","},
    )
    ET.SubElement(cols, "column", {"datatype": "string", "name": "DR_NO", "ordinal": "0"})
    ET.SubElement(cols, "column", {"datatype": "date", "name": "Date Rptd", "ordinal": "1"})
    ET.SubElement(cols, "column", {"datatype": "integer", "name": "delay_days", "ordinal": "2"})
    ET.SubElement(cols, "column", {"datatype": "string", "name": "delay_bucket", "ordinal": "3"})
    ET.SubElement(cols, "column", {"datatype": "string", "name": "crime_family", "ordinal": "4"})
    ET.SubElement(cols, "column", {"datatype": "integer", "name": "year_occ", "ordinal": "5"})
    return ds


def _manifest() -> ET.Element:
    man = ET.Element("document-format-change-manifest")
    for tag in (
        "_.fcp.AccessibleZoneTabOrder.true...AccessibleZoneTabOrder",
        "_.fcp.AnimationOnByDefault.true...AnimationOnByDefault",
        "AutoCreateAndUpdateDSDPhoneLayouts",
        "_.fcp.MarkAnimation.true...MarkAnimation",
        "_.fcp.ObjectModelEncapsulateLegacy.true...ObjectModelEncapsulateLegacy",
        "_.fcp.ObjectModelTableType.true...ObjectModelTableType",
        "_.fcp.SchemaViewerObjectModel.true...SchemaViewerObjectModel",
        "SetMembershipControl",
        "SheetIdentifierTracking",
        "WindowsPersistSimpleIdentifiers",
        "ZoneFriendlyName",
    ):
        ET.SubElement(man, tag)
    return man


def build_twb_xml() -> str:
    ET.register_namespace("user", NS_USER)
    wb = ET.Element(
        "workbook",
        {
            "source-build": SOURCE_BUILD,
            "source-platform": "win",
            "version": VERSION,
            "xmlns:user": NS_USER,
        },
    )
    wb.append(_manifest())
    prefs = ET.SubElement(wb, "preferences")
    ET.SubElement(prefs, "preference", {"name": "ui.encoding.shelf.height", "value": "24"})
    ET.SubElement(prefs, "preference", {"name": "ui.shelf.height", "value": "26"})
    ET.SubElement(prefs, "preference", {"name": "show-data-guide", "value": "0"})
    pal = ET.SubElement(
        prefs,
        "color-palette",
        {"custom": "true", "name": "A07_navy_sequential", "type": "ordered-sequential"},
    )
    ET.SubElement(pal, "color").text = NAVY_LOW
    ET.SubElement(pal, "color").text = NAVY
    delay_pal = ET.SubElement(
        prefs,
        "color-palette",
        {"custom": "true", "name": "A07_delay_buckets", "type": "regular"},
    )
    for bucket in PALETTE_ASSIGN_ORDER:
        ET.SubElement(delay_pal, "color").text = BUCKET_COLORS[bucket]
    datasources = ET.SubElement(wb, "datasources")
    datasources.append(_datasource())
    worksheets = ET.SubElement(wb, "worksheets")
    worksheets.append(_worksheet_a())
    worksheets.append(_worksheet_b())
    worksheets.append(_worksheet_c())
    dashboards = ET.SubElement(wb, "dashboards")
    dashboards.append(_dashboard())
    wb.append(_windows())
    xml = _tableau_quote_buckets(ET.tostring(wb, encoding="unicode"))
    return "<?xml version='1.0' encoding='utf-8' ?>\n" + xml + "\n"


def write_twb(path: Path) -> Path:
    path.write_text(build_twb_xml(), encoding="utf-8")
    return path
