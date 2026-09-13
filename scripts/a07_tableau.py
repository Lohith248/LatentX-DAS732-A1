"""Open the Fig 7 twbx in Tableau Desktop, wait until it renders, export Fig7.png."""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLEAU_EXE = Path(r"C:\Program Files\Tableau\Tableau 2026.2\bin\tableau.exe")
TWBX = ROOT / "tableau" / "A07" / "A07 Report delay.twbx"
PNG = ROOT / "images" / "Fig7.png"
LOG_DIR = Path(r"C:\Users\jagat\Documents\My Tableau Repository\Logs")
TITLE_NEEDLE = "A07 Report delay"
PROTECTED_TITLE = "A01_Six_Figures"


def _ps(script: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def tableau_windows() -> list[tuple[int, str]]:
    out = _ps(
        "Get-Process tableau -ErrorAction SilentlyContinue | "
        "ForEach-Object { '{0}|{1}' -f $_.Id, $_.MainWindowTitle }"
    )
    rows: list[tuple[int, str]] = []
    for line in (out.stdout or "").splitlines():
        if "|" not in line:
            continue
        pid_s, title = line.split("|", 1)
        try:
            rows.append((int(pid_s), title.strip()))
        except ValueError:
            continue
    return rows


def _clear_a07_recovery() -> None:
    a07 = ROOT / "tableau" / "A07"
    for path in a07.glob("~A07*"):
        try:
            path.unlink()
        except OSError:
            pass


def close_a07_windows() -> None:
    for pid, title in tableau_windows():
        if PROTECTED_TITLE in title:
            continue
        if TITLE_NEEDLE not in title and "A07" not in title:
            continue
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/F"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    deadline = time.time() + 20
    while time.time() < deadline:
        leftover = [
            (pid, title)
            for pid, title in tableau_windows()
            if TITLE_NEEDLE in title and PROTECTED_TITLE not in title
        ]
        if not leftover:
            _clear_a07_recovery()
            return
        time.sleep(1)
    raise TimeoutError("A07 Tableau window did not close")


def _newest_logs() -> list[Path]:
    if not LOG_DIR.exists():
        return []
    return sorted(LOG_DIR.glob("log_*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)[:4]


def _log_sizes() -> dict[Path, int]:
    if not LOG_DIR.exists():
        return {}
    return {p: p.stat().st_size for p in LOG_DIR.glob("log_*.txt") if "_bk" not in p.name}


def _new_log_text(before: dict[Path, int]) -> str:
    chunks: list[str] = []
    now = _log_sizes()
    for path, size in now.items():
        old = before.get(path, 0)
        if size < old:
            old = 0
        if size <= old:
            continue
        with path.open("rb") as fh:
            fh.seek(old)
            chunks.append(fh.read().decode("utf-8", errors="replace"))
    return "\n".join(chunks)


def parse_open_status(payload: str) -> tuple[bool, str]:
    errors: list[str] = []
    opened = False
    for line in payload.splitlines():
        if "A07" not in line and "error" not in line.lower() and "workbook-dom" not in line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        a = obj.get("a") or {}
        name = a.get("name") or ""
        if name == "workbook-dom-loader.load-workbook-dom":
            if a.get("rk") == "ok":
                opened = True
            elif a.get("rk"):
                errors.append(f"load-workbook-dom rk={a.get('rk')}")
        if obj.get("k") == "detailed-error-msg":
            msg = str(obj.get("v"))
            if "Error(" in msg:
                errors.append(msg[:800])
    if opened and not errors:
        return True, "load-workbook-dom rk=ok"
    if errors:
        return False, " | ".join(errors[:3])
    return False, "no A07 load-workbook-dom line yet"


def open_twbx(twbx: Path = TWBX) -> tuple[int, str]:
    if not TABLEAU_EXE.exists():
        raise FileNotFoundError(TABLEAU_EXE)
    if not twbx.exists():
        raise FileNotFoundError(twbx)
    close_a07_windows()
    before = _log_sizes()
    proc = subprocess.Popen(
        [str(TABLEAU_EXE), str(twbx)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 120
    last = "waiting"
    while time.time() < deadline:
        titles = [title for _, title in tableau_windows()]
        ok, last = parse_open_status(_new_log_text(before))
        if "Error(" in last or "early-termination" in last:
            if "Error(" not in last:
                time.sleep(8)
                ok, last = parse_open_status(_new_log_text(before))
            subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/F"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return proc.pid, last
        a07_open = any(TITLE_NEEDLE in t and PROTECTED_TITLE not in t for t in titles)
        if a07_open:
            time.sleep(12)
            if ok:
                return proc.pid, last
            return proc.pid, last + "; window open"
        time.sleep(2)
    return proc.pid, last


def export_dashboard_png(png: Path = PNG) -> tuple[bool, str]:
    png.parent.mkdir(parents=True, exist_ok=True)
    if png.exists():
        png.unlink()
    png_lit = str(png).replace("'", "''")
    ps = r"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
public class A07Win {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdcBlt, uint nFlags);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr ins, int X, int Y, int cx, int cy, uint flags);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L; public int T; public int R; public int B; }
  public static string Capture(IntPtr h, string path) {
    ShowWindow(h, 9);
    SetWindowPos(h, new IntPtr(-1), 8, 8, 1760, 1040, 0x0040);
    SetForegroundWindow(h);
    System.Threading.Thread.Sleep(1200);
    RECT r; GetWindowRect(h, out r);
    int w = Math.Max(200, r.R - r.L);
    int ht = Math.Max(200, r.B - r.T);
    Bitmap bmp = new Bitmap(w, ht, PixelFormat.Format32bppArgb);
    Graphics g = Graphics.FromImage(bmp);
    IntPtr hdc = g.GetHdc();
    PrintWindow(h, hdc, 2);
    g.ReleaseHdc(hdc);
    g.Dispose();
    bmp.Save(path, ImageFormat.Png);
    string msg = string.Format("printwindow {0}x{1} bytes={2}", w, ht, new System.IO.FileInfo(path).Length);
    bmp.Dispose();
    return msg;
  }
}
"@ -ReferencedAssemblies System.Drawing

$p = Get-Process tableau | Where-Object { $_.MainWindowTitle -like '*A07 Report delay*' } | Select-Object -First 1
if (-not $p) { Write-Output 'NO_A07_WINDOW'; exit 2 }
[A07Win]::ShowWindow($p.MainWindowHandle, 9) | Out-Null
[A07Win]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 800
try {
  Add-Type -AssemblyName UIAutomationClient | Out-Null
  Add-Type -AssemblyName UIAutomationTypes | Out-Null
  $root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
  $nameCond = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::NameProperty, 'A07 Report delay')
  $tabs = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $nameCond)
  foreach ($el in $tabs) {
    if ($el.Current.ControlType.ProgrammaticName -match 'Tab') {
      $el.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
      break
    }
  }
} catch {}
Start-Sleep -Seconds 2
[A07Win]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 300
[System.Windows.Forms.SendKeys]::SendWait('{F7}')
Start-Sleep -Seconds 2
$msg = [A07Win]::Capture($p.MainWindowHandle, '__PNG__')
[System.Windows.Forms.SendKeys]::SendWait('{ESC}')
Write-Output ($msg + ' presentation title=' + $p.MainWindowTitle)
"""
    ps = ps.replace("__PNG__", png_lit)
    cap = _ps(ps, timeout=90)
    detail = ((cap.stdout or "") + " " + (cap.stderr or "")).strip()
    if png.exists() and png.stat().st_size > 20_000:
        return True, detail
    return False, detail or f"exit {cap.returncode}"
