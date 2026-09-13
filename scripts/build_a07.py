"""Build tableau/A07/A07 Report delay.twbx and export images/Fig7.png."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from a07_extract import OUT_DIR, build_extract  # noqa: E402
from a07_tableau import PNG, export_dashboard_png, open_twbx  # noqa: E402
from a07_validate import TWBX, TWB_NAME, validate_twbx, write_report  # noqa: E402
from a07_workbook import write_twb  # noqa: E402

ROOT = SCRIPTS.parent
LOCKED = (
    ROOT / "Crime_Data_from_2020_to_2024.csv",
    ROOT / "tableau" / "A01" / "LatentX_A01.twb",
    ROOT / "tableau" / "A01" / "a01_daily.csv",
)


def _package(csv_path: Path, twb_path: Path) -> Path:
    if TWBX.exists():
        TWBX.unlink()
    with zipfile.ZipFile(TWBX, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(twb_path, arcname=TWB_NAME)
        zf.write(csv_path, arcname=f"Data/A07/{csv_path.name}")
    return TWBX


def _assert_locked_untouched(before: dict[Path, tuple[int, int]]) -> None:
    for path, (mtime, size) in before.items():
        if not path.exists():
            continue
        now = (path.stat().st_mtime_ns, path.stat().st_size)
        if now != (mtime, size):
            raise AssertionError(f"locked file changed: {path}")


def _snapshot(paths: tuple[Path, ...]) -> dict[Path, tuple[int, int]]:
    out: dict[Path, tuple[int, int]] = {}
    for path in paths:
        if path.exists():
            out[path] = (path.stat().st_mtime_ns, path.stat().st_size)
    return out


def _export_png_via_tableau(twbx: Path) -> tuple[bool, str]:
    pid, open_msg = open_twbx(twbx)
    opened = "rk=ok" in open_msg or "window open" in open_msg
    if not opened:
        return False, f"Tableau open failed pid={pid} {open_msg}"
    ok, png_msg = export_dashboard_png(PNG)
    return ok, f"pid={pid} {open_msg}; {png_msg}"


def main() -> None:
    locked = _snapshot(LOCKED)
    csv_path = OUT_DIR / "a07_delay.csv"
    if csv_path.exists() and csv_path.stat().st_size > 1_000_000:
        pass
    else:
        csv_path = build_extract()
    twb_path = write_twb(OUT_DIR / TWB_NAME)
    twbx = _package(csv_path, twb_path)
    notes = validate_twbx(twbx)
    png_ok, png_msg = _export_png_via_tableau(twbx)
    extra = [
        f"twbx {twbx} bytes {twbx.stat().st_size}",
        f"twb {twb_path}",
        f"png {PNG} ok={png_ok} {png_msg}",
        "source CSV and Fig 1 artifacts were not rewritten",
        "Fig 8 was not started",
    ]
    report = write_report(notes, extra)
    _assert_locked_untouched(locked)
    print(f"extract {csv_path}")
    print(f"twbx {twbx}")
    print(f"report {report}")
    print(f"png {png_ok} {png_msg}")
    if not png_ok:
        raise SystemExit("workbook built and validated; dashboard PNG export did not finish")


if __name__ == "__main__":
    main()
