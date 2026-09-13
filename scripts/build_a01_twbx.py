"""Build LatentX_A01.twbx — Member A Fig 1 (daily reports + 28-day average)."""
from __future__ import annotations

import csv
import hashlib
import zipfile
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "lapd_a1_clean.csv"
OUT_DIR = ROOT / "tableau" / "A01"
CSV_NAME = "a01_daily.csv"
TWB_NAME = "LatentX_A01.twb"
TWBX = ROOT / "LatentX_A01.twbx"

DS = "federated.0a01latx732dailycsv1k9p2"
CONN = "textscan.0a01latx732dailycsvscan1"
OBJ = "a01_daily.csv_" + hashlib.sha1(b"latentx-a01").hexdigest()[:32].upper()
WS = "A01 Five years day by day"


def parse_occ(value: str) -> date | None:
    text = (value or "").strip()[:10]
    if len(text) < 10:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def daily_counts() -> list[tuple[date, int, int, str, str]]:
    counts: Counter[date] = Counter()
    with SRC.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            occ = parse_occ(row.get("DATE OCC") or "")
            if occ:
                counts[occ] += 1
    start = date(2020, 1, 1)
    end = date(2024, 12, 30)
    days: list[date] = []
    d = start
    while d <= end:
        days.append(d)
        d += timedelta(days=1)
    series: list[int] = [counts[d] for d in days]
    out = []
    window: list[int] = []
    events = {
        date(2020, 3, 19): "COVID stay-at-home order",
        date(2024, 3, 7): "LAPD left this records system",
    }
    for i, day in enumerate(days):
        window.append(series[i])
        if len(window) > 28:
            window.pop(0)
        ma = round(sum(window) / len(window))
        coverage = (
            "2024 (partial - system change)"
            if day.year == 2024
            else "2020-2023 (full years)"
        )
        out.append((day, series[i], ma, coverage, events.get(day, "")))
    return out


def write_csv(rows: list[tuple[date, int, int, str, str]]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / CSV_NAME
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Date Occ", "Daily reports", "28-day average", "Coverage", "Event"])
        for day, n, ma, coverage, event in rows:
            w.writerow([day.isoformat(), n, ma, coverage, event])
    return path


def twb_xml() -> str:
    ds, conn, obj, ws = DS, CONN, OBJ, WS
    title = escape("Fig 1. Reported crime by day, Los Angeles, 2020-2024")
    subtitle = escape(
        "Grey line: daily reports. Navy line: 28-day average. "
        "2024 after 7 March is a records-system change, not a fall in crime."
    )
    return f"""<?xml version='1.0' encoding='utf-8' ?>

<!-- build LatentX A01 Fig 1 -->
<workbook source-build='2026.2' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <document-format-change-manifest>
    <_.fcp.AccessibleZoneTabOrder.true...AccessibleZoneTabOrder />
    <_.fcp.AnimationOnByDefault.true...AnimationOnByDefault />
    <AutoCreateAndUpdateDSDPhoneLayouts />
    <_.fcp.MarkAnimation.true...MarkAnimation />
    <_.fcp.ObjectModelEncapsulateLegacy.true...ObjectModelEncapsulateLegacy />
    <_.fcp.ObjectModelTableType.true...ObjectModelTableType />
    <_.fcp.SchemaViewerObjectModel.true...SchemaViewerObjectModel />
    <SetMembershipControl />
    <SheetIdentifierTracking />
    <WindowsPersistSimpleIdentifiers />
    <ZoneFriendlyName />
  </document-format-change-manifest>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
    <datasource caption='A01 daily reports' inline='true' name='{ds}' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='A01 daily reports' name='{conn}'>
            <connection class='textscan' directory='Data/A01' filename='{CSV_NAME}' password='' server='' />
          </named-connection>
        </named-connections>
        <_.fcp.ObjectModelEncapsulateLegacy.false...relation connection='{conn}' name='{CSV_NAME}' table='[a01_daily#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>
            <column datatype='date' name='Date Occ' ordinal='0' />
            <column datatype='integer' name='Daily reports' ordinal='1' />
            <column datatype='integer' name='28-day average' ordinal='2' />
            <column datatype='string' name='Coverage' ordinal='3' />
            <column datatype='string' name='Event' ordinal='4' />
          </columns>
        </_.fcp.ObjectModelEncapsulateLegacy.false...relation>
        <_.fcp.ObjectModelEncapsulateLegacy.true...relation connection='{conn}' name='{CSV_NAME}' table='[a01_daily#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>
            <column datatype='date' name='Date Occ' ordinal='0' />
            <column datatype='integer' name='Daily reports' ordinal='1' />
            <column datatype='integer' name='28-day average' ordinal='2' />
            <column datatype='string' name='Coverage' ordinal='3' />
            <column datatype='string' name='Event' ordinal='4' />
          </columns>
        </_.fcp.ObjectModelEncapsulateLegacy.true...relation>
        <metadata-records>
          <metadata-record class='capability'>
            <remote-name />
            <remote-type>0</remote-type>
            <parent-name>[{CSV_NAME}]</parent-name>
            <remote-alias />
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
            <attributes>
              <attribute datatype='string' name='character-set'>&quot;UTF-8&quot;</attribute>
              <attribute datatype='string' name='collation'>&quot;en_US&quot;</attribute>
              <attribute datatype='string' name='field-delimiter'>&quot;,&quot;</attribute>
              <attribute datatype='string' name='header-row'>&quot;true&quot;</attribute>
              <attribute datatype='string' name='locale'>&quot;en_US&quot;</attribute>
              <attribute datatype='string' name='single-char'>&quot;&quot;</attribute>
            </attributes>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Date Occ</remote-name>
            <remote-type>133</remote-type>
            <local-name>[Date Occ]</local-name>
            <parent-name>[{CSV_NAME}]</parent-name>
            <remote-alias>Date Occ</remote-alias>
            <ordinal>0</ordinal>
            <local-type>date</local-type>
            <aggregation>Year</aggregation>
            <contains-null>true</contains-null>
            <_.fcp.ObjectModelEncapsulateLegacy.true...object-id>[{obj}]</_.fcp.ObjectModelEncapsulateLegacy.true...object-id>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Daily reports</remote-name>
            <remote-type>20</remote-type>
            <local-name>[Daily reports]</local-name>
            <parent-name>[{CSV_NAME}]</parent-name>
            <remote-alias>Daily reports</remote-alias>
            <ordinal>1</ordinal>
            <local-type>integer</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
            <_.fcp.ObjectModelEncapsulateLegacy.true...object-id>[{obj}]</_.fcp.ObjectModelEncapsulateLegacy.true...object-id>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>28-day average</remote-name>
            <remote-type>20</remote-type>
            <local-name>[28-day average]</local-name>
            <parent-name>[{CSV_NAME}]</parent-name>
            <remote-alias>28-day average</remote-alias>
            <ordinal>2</ordinal>
            <local-type>integer</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
            <_.fcp.ObjectModelEncapsulateLegacy.true...object-id>[{obj}]</_.fcp.ObjectModelEncapsulateLegacy.true...object-id>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Coverage</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Coverage]</local-name>
            <parent-name>[{CSV_NAME}]</parent-name>
            <remote-alias>Coverage</remote-alias>
            <ordinal>3</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <scale>1</scale>
            <width>1073741823</width>
            <contains-null>true</contains-null>
            <collation flag='0' name='LEN_RUS' />
            <_.fcp.ObjectModelEncapsulateLegacy.true...object-id>[{obj}]</_.fcp.ObjectModelEncapsulateLegacy.true...object-id>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Event</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Event]</local-name>
            <parent-name>[{CSV_NAME}]</parent-name>
            <remote-alias>Event</remote-alias>
            <ordinal>4</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <scale>1</scale>
            <width>1073741823</width>
            <contains-null>true</contains-null>
            <collation flag='0' name='LEN_RUS' />
            <_.fcp.ObjectModelEncapsulateLegacy.true...object-id>[{obj}]</_.fcp.ObjectModelEncapsulateLegacy.true...object-id>
          </metadata-record>
        </metadata-records>
      </connection>
      <aliases enabled='yes' />
      <column datatype='date' name='[Date Occ]' role='dimension' type='ordinal' />
      <column datatype='integer' default-format='n#,##0' name='[Daily reports]' role='measure' type='quantitative' />
      <column datatype='integer' default-format='n#,##0' name='[28-day average]' role='measure' type='quantitative' />
      <column datatype='string' name='[Coverage]' role='dimension' type='nominal' />
      <column datatype='string' name='[Event]' role='dimension' type='nominal' />
      <_.fcp.ObjectModelTableType.true...column caption='A01 daily reports' datatype='table' name='[__tableau_internal_object_id__].[{obj}]' role='measure' type='quantitative' />
      <column-instance column='[Daily reports]' derivation='Sum' name='[sum:Daily reports:qk]' pivot='key' type='quantitative' />
      <column-instance column='[28-day average]' derivation='Sum' name='[sum:28-day average:qk]' pivot='key' type='quantitative' />
      <layout _.fcp.SchemaViewerObjectModel.true...common-percentage='0.7' dim-ordering='alphabetic' measure-ordering='alphabetic' show-structure='true' />
      <style>
        <style-rule element='mark'>
          <encoding attr='color' field='[:Measure Names]' type='palette'>
            <map to='#B7BDC9'>
              <bucket>&quot;[{ds}].[sum:Daily reports:qk]&quot;</bucket>
            </map>
            <map to='#1F4E79'>
              <bucket>&quot;[{ds}].[sum:28-day average:qk]&quot;</bucket>
            </map>
          </encoding>
        </style-rule>
      </style>
      <_.fcp.ObjectModelEncapsulateLegacy.true...object-graph>
        <objects>
          <object caption='A01 daily reports' id='{obj}'>
            <properties context=''>
              <relation connection='{conn}' name='{CSV_NAME}' table='[a01_daily#csv]' type='table'>
                <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>
                  <column datatype='date' name='Date Occ' ordinal='0' />
                  <column datatype='integer' name='Daily reports' ordinal='1' />
                  <column datatype='integer' name='28-day average' ordinal='2' />
                  <column datatype='string' name='Coverage' ordinal='3' />
                  <column datatype='string' name='Event' ordinal='4' />
                </columns>
              </relation>
            </properties>
          </object>
        </objects>
      </_.fcp.ObjectModelEncapsulateLegacy.true...object-graph>
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name='{ws}'>
      <layout-options>
        <title>
          <formatted-text>
            <run fontname='Tableau Bold' fontsize='15'>{title}</run>
            <run>&#10;</run>
            <run fontcolor='#5B6570' fontsize='10'>{subtitle}</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='A01 daily reports' name='{ds}' />
          </datasources>
          <datasource-dependencies datasource='{ds}'>
            <column datatype='date' name='[Date Occ]' role='dimension' type='ordinal' />
            <column datatype='integer' default-format='n#,##0' name='[Daily reports]' role='measure' type='quantitative' />
            <column datatype='integer' default-format='n#,##0' name='[28-day average]' role='measure' type='quantitative' />
            <column datatype='string' name='[Coverage]' role='dimension' type='nominal' />
            <column-instance column='[Date Occ]' derivation='None' name='[none:Date Occ:qk]' pivot='key' type='quantitative' />
            <column-instance column='[Daily reports]' derivation='Sum' name='[sum:Daily reports:qk]' pivot='key' type='quantitative' />
            <column-instance column='[28-day average]' derivation='Sum' name='[sum:28-day average:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <filter class='categorical' column='[{ds}].[:Measure Names]'>
            <groupfilter function='union' user:op='manual'>
              <groupfilter function='member' level='[:Measure Names]' member='&quot;[{ds}].[sum:Daily reports:qk]&quot;' />
              <groupfilter function='member' level='[:Measure Names]' member='&quot;[{ds}].[sum:28-day average:qk]&quot;' />
            </groupfilter>
          </filter>
          <slices>
            <column>[{ds}].[:Measure Names]</column>
          </slices>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='axis'>
            <format attr='title' class='0' field='[{ds}].[Multiple Values]' scope='rows' value='Reports per day' />
            <format attr='title' class='0' field='[{ds}].[none:Date Occ:qk]' scope='cols' value='Date occurred' />
          </style-rule>
          <style-rule element='worksheet'>
            <format attr='display-field-labels' scope='cols' value='false' />
            <format attr='display-field-labels' scope='rows' value='false' />
          </style-rule>
          <_.fcp.MarkAnimation.true...style-rule element='animation'>
            <format attr='animation-on' value='ao-off' />
          </_.fcp.MarkAnimation.true...style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Line' />
            <encodings>
              <color column='[{ds}].[:Measure Names]' />
            </encodings>
            <customized-tooltip>
              <formatted-text>
                <run fontcolor='#1F4E79' fontname='Tableau Bold' fontsize='12'><![CDATA[<[{ds}].[none:Date Occ:qk]>]]></run>
                <run>&#10;</run>
                <run fontcolor='#5B6570'><![CDATA[<[{ds}].[:Measure Names]>: ]]></run>
                <run fontname='Tableau Medium'><![CDATA[<[{ds}].[Multiple Values]>]]></run>
              </formatted-text>
            </customized-tooltip>
            <style>
              <style-rule element='mark'>
                <format attr='mark-labels-show' value='false' />
                <format attr='size' value='0.16' />
              </style-rule>
            </style>
          </pane>
        </panes>
        <rows>[{ds}].[Multiple Values]</rows>
        <cols>[{ds}].[none:Date Occ:qk]</cols>
      </table>
      <simple-id uuid='{{A01E7320-0001-4C11-8A01-A1B2C3D4E5F6}}' />
    </worksheet>
  </worksheets>
  <windows>
    <window class='worksheet' maximized='true' name='{ws}'>
      <cards>
        <edge name='left'>
          <strip size='160'>
            <card type='pages' />
            <card type='filters' />
            <card type='marks' />
          </strip>
        </edge>
        <edge name='top'>
          <strip size='2147483647'>
            <card type='columns' />
          </strip>
          <strip size='2147483647'>
            <card type='rows' />
          </strip>
          <strip size='90'>
            <card type='title' />
          </strip>
        </edge>
        <edge name='right'>
          <strip size='200'>
            <card pane-specification-id='0' param='[{ds}].[:Measure Names]' type='color' />
          </strip>
        </edge>
      </cards>
      <simple-id uuid='{{A01E7320-0002-4C11-8A01-A1B2C3D4E5F7}}' />
    </window>
  </windows>
</workbook>
"""


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}")
    rows = daily_counts()
    csv_path = write_csv(rows)
    twb_path = OUT_DIR / TWB_NAME
    twb_path.write_text(twb_xml(), encoding="utf-8")
    if TWBX.exists():
        TWBX.unlink()
    with zipfile.ZipFile(TWBX, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(twb_path, arcname=TWB_NAME)
        zf.write(csv_path, arcname=f"Data/A01/{CSV_NAME}")
    n2020 = sum(n for d, n, *_ in rows if d.year == 2020)
    n2024 = sum(n for d, n, *_ in rows if d.year == 2024)
    assert n2020 == 199847, n2020
    assert n2024 == 127567, n2024
    print(f"rows {len(rows)}")
    print(f"csv {csv_path} ({csv_path.stat().st_size} bytes)")
    print(f"twb {twb_path}")
    print(f"twbx {TWBX} ({TWBX.stat().st_size} bytes)")
    print("ok")


if __name__ == "__main__":
    main()
