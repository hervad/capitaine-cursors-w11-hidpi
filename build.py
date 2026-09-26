#!/usr/bin/env python3
"""Build the Windows cursor schemes from the SVG sources in src/svg.

Usage:
    python -m pip install -r requirements.txt
    python build.py

Writes capitaine-dark/, capitaine-light/, capitaine-cursors-windows11.zip and
docs/preview.png.
On Windows, every generated file is also test-loaded with the system loader.
The SVGs are vendored from keeferrourke/capitaine-cursors at commit 06c8843.
"""

from __future__ import annotations

import io
import math
import struct
import sys
import zipfile
from pathlib import Path

import resvg_py
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SVG_DIR = ROOT / "src" / "svg"
ZIP_PATH = ROOT / "capitaine-cursors-windows11.zip"
PREVIEW_PATH = ROOT / "docs" / "preview.png"

# The SVGs are drawn on a 24-unit grid (the Linux Xcursor nominal size).
SVG_GRID = 24

# Windows picks the cursor size in steps from the display scale -- 32 (<150%),
# 48 (150-199%), 64 (200-299%), 96 (300-399%), 128 (>=400%) -- and multiplies
# it by the pointer-size slider (CursorBaseSize / 32 = 1, 1.5, 2, ... 8).
# It uses an exact match when present and otherwise shrinks the next larger
# image. Static cursors carry every size needed for slider positions 1-3.
STATIC_SIZES = (32, 48, 64, 72, 96, 128, 144, 192, 256)
# Windows silently refuses .ani files whose frames carry too much image data
# (observed around 79 KB per frame on Windows 11), so animated cursors use
# the default-slider sizes plus 192/256 and must stay under this budget.
ANIMATED_SIZES = (32, 48, 64, 96, 128, 192, 256)
ANI_FRAME_BUDGET = 56 * 1024

VARIANTS = {
    "dark": "Capitaine Cursors (Dark)",
    "light": "Capitaine Cursors (Light)",
}

# Windows cursor roles in the order the registry scheme string expects:
# (role, output file, source SVG stem, hotspot on the 24-unit grid, frames).
# Pin and Person have no Capitaine equivalent and are left empty.
ROLES = (
    ("Arrow", "arrow.cur", "default", (4, 2), 0),
    ("Help", "help.cur", "help", (4, 2), 0),
    ("AppStarting", "working.ani", "progress", (4, 2), 24),
    ("Wait", "wait.ani", "wait", (12, 12), 24),
    ("Crosshair", "crosshair.cur", "crosshair", (12, 12), 0),
    ("IBeam", "text.cur", "text", (12, 12), 0),
    ("NWPen", "pen.cur", "pencil", (3.64, 20.68), 0),  # pencil tip, not upstream's (4, 4)
    ("No", "unavailable.cur", "not-allowed", (12, 12), 0),
    ("SizeNS", "size_ns.cur", "size_ver", (12, 12), 0),
    ("SizeWE", "size_ew.cur", "size_hor", (12, 12), 0),
    ("SizeNWSE", "size_nwse.cur", "size_fdiag", (12, 12), 0),
    ("SizeNESW", "size_nesw.cur", "size_bdiag", (12, 12), 0),
    ("SizeAll", "move.cur", "fleur", (12, 12), 0),
    ("UpArrow", "up_arrow.cur", "up-arrow", (12, 4), 0),
    ("Hand", "link.cur", "pointer", (12, 6), 0),
)
EMPTY_ROLES = 2  # Pin, Person

# Frame duration in jiffies (1/60 s): 24 frames x 33 ms = one turn per 0.8 s,
# close to upstream's 30 ms per frame.
ANI_JIFFIES = 2
ANI_TITLE = "Capitaine Cursors"
ANI_ARTIST = "Keefer Rourke and contributors"

ZIP_EXTRAS = ("COPYING", "ATTRIBUTION.md")
ZIP_DATE = (2026, 1, 1, 0, 0, 0)  # fixed so the archive is reproducible


def render(svg: Path, size: int) -> bytes:
    """Render an SVG to an optimized 32-bit RGBA PNG of size x size pixels."""
    png = bytes(resvg_py.svg_to_bytes(svg_path=str(svg), width=size, height=size))
    image = Image.open(io.BytesIO(png)).convert("RGBA")
    if image.size != (size, size):
        raise ValueError(f"{svg.name} rendered at {image.size}, expected {size}")
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()


def scale_hotspot(hotspot: tuple[float, float], size: int) -> tuple[int, int]:
    """Map a hotspot from the 24-unit grid to the pixel that contains it."""
    return tuple(min(size - 1, math.floor(c * size / SVG_GRID)) for c in hotspot)


def build_cur(svg: Path, hotspot: tuple[float, float], sizes: tuple[int, ...]) -> bytes:
    """Build a multi-resolution .cur file with one PNG image per size."""
    images = [(size, render(svg, size)) for size in sizes]
    header = struct.pack("<HHH", 0, 2, len(images))
    offset = len(header) + 16 * len(images)
    entries, blobs = [], []
    for size, png in images:
        hx, hy = scale_hotspot(hotspot, size)
        dim = size % 256  # 0 means 256 in the directory entry
        entries.append(struct.pack("<BBBBHHII", dim, dim, 0, 0, hx, hy, len(png), offset))
        blobs.append(png)
        offset += len(png)
    return header + b"".join(entries) + b"".join(blobs)


def riff_chunk(chunk_id: bytes, data: bytes) -> bytes:
    pad = b"\0" if len(data) % 2 else b""
    return chunk_id + struct.pack("<I", len(data)) + data + pad


def riff_list(list_type: bytes, chunks: list[bytes]) -> bytes:
    return riff_chunk(b"LIST", list_type + b"".join(chunks))


def build_ani(frames: list[bytes]) -> bytes:
    """Build an .ani file whose frames are multi-resolution .cur images."""
    info = riff_list(b"INFO", [
        riff_chunk(b"INAM", ANI_TITLE.encode("ascii") + b"\0"),
        riff_chunk(b"IART", ANI_ARTIST.encode("ascii") + b"\0"),
    ])
    # cbSize, nFrames, nSteps, cx, cy, cBitCount, cPlanes, JifRate, flags (AF_ICON)
    anih = riff_chunk(b"anih", struct.pack("<9I", 36, len(frames), len(frames),
                                           0, 0, 32, 1, ANI_JIFFIES, 1))
    fram = riff_list(b"fram", [riff_chunk(b"icon", f) for f in frames])
    body = b"ACON" + info + anih + fram
    return b"RIFF" + struct.pack("<I", len(body)) + body


def build_inf(variant: str) -> str:
    name = VARIANTS[variant]
    files = [role[1] for role in ROLES]
    paths = ",".join(f"%10%\\%CUR_DIR%\\{f}" for f in files) + "," * EMPTY_ROLES
    lines = [
        f"; {name}",
        '; Right-click this file and select "Install" (asks for administrator rights),',
        "; then choose the scheme in main.cpl > Pointers.",
        "; Uninstall: rundll32.exe setupapi.dll,InstallHinfSection DefaultUninstall 132 <path to this file>",
        "",
        "[Version]",
        'Signature = "$Windows NT$"',
        "",
        "[DefaultInstall]",
        "CopyFiles = Scheme.Cur",
        "AddReg    = Scheme.Reg",
        "",
        "[DefaultUninstall]",
        "DelFiles  = Scheme.Cur",
        "DelReg    = Scheme.DelReg",
        "",
        "[DestinationDirs]",
        'Scheme.Cur = 10,"%CUR_DIR%"',
        "",
        "[Scheme.Reg]",
        f'HKLM,"%SCHEMES_KEY%","%SCHEME_NAME%",,"{paths}"',
        "",
        "[Scheme.DelReg]",
        'HKLM,"%SCHEMES_KEY%","%SCHEME_NAME%"',
        "",
        "[Scheme.Cur]",
        *files,
        "",
        "[Strings]",
        'SCHEMES_KEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Control Panel\\Cursors\\Schemes"',
        f'CUR_DIR     = "Cursors\\{name}"',
        f'SCHEME_NAME = "{name}"',
    ]
    return "\r\n".join(lines) + "\r\n"


def verify_cur(data: bytes, hotspot: tuple[float, float], sizes: tuple[int, ...], label: str) -> None:
    """Re-parse a generated .cur and check every directory entry against its image."""
    def check(ok: bool, problem: str) -> None:
        if not ok:
            raise ValueError(f"{label}: {problem}")

    reserved, kind, count = struct.unpack_from("<HHH", data, 0)
    check((reserved, kind, count) == (0, 2, len(sizes)), f"bad header {reserved, kind, count}")
    for i, size in enumerate(sizes):
        w, h, _, _, hx, hy, length, offset = struct.unpack_from("<BBBBHHII", data, 6 + 16 * i)
        image = Image.open(io.BytesIO(data[offset:offset + length]))
        check((w or 256, h or 256) == (size, size), f"directory says {w}x{h}, expected {size}")
        check(image.size == (size, size) and image.mode == "RGBA",
              f"image is {image.size} {image.mode}, expected {size}px RGBA")
        check((hx, hy) == scale_hotspot(hotspot, size), f"wrong hotspot at {size}px")


def verify_with_windows(paths: list[Path]) -> None:
    """Load every file with the Windows cursor loader at each target size."""
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.LoadImageW.restype = wintypes.HANDLE
    user32.LoadImageW.argtypes = (wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT,
                                  ctypes.c_int, ctypes.c_int, wintypes.UINT)
    user32.DestroyCursor.argtypes = (wintypes.HANDLE,)
    IMAGE_CURSOR, LR_LOADFROMFILE = 2, 0x10
    for path in paths:
        for size in STATIC_SIZES:
            handle = user32.LoadImageW(None, str(path), IMAGE_CURSOR, size, size, LR_LOADFROMFILE)
            if not handle:
                raise RuntimeError(f"Windows failed to load {path.relative_to(ROOT)} at {size}px")
            user32.DestroyCursor(handle)


def write_preview() -> None:
    """Draw every cursor of both variants at 48 px, doubled for HiDPI screens."""
    size, gap, pad, scale = 48, 20, 28, 2
    panels = (("dark", (243, 243, 243)), ("light", (32, 32, 32)))
    width = pad * 2 + len(ROLES) * size + (len(ROLES) - 1) * gap
    height = len(panels) * (size + pad * 2)
    canvas = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    for row, (variant, background) in enumerate(panels):
        top = row * (size + pad * 2) * scale
        corners = (row == 0, row == 0, row == len(panels) - 1, row == len(panels) - 1)
        draw.rounded_rectangle((0, top, width * scale - 1, top + (size + pad * 2) * scale - 1),
                               radius=16 * scale, fill=background, corners=corners)
        for col, (_, _, stem, _, frames) in enumerate(ROLES):
            svg = SVG_DIR / variant / (f"{stem}-00.svg" if frames else f"{stem}.svg")
            icon = Image.open(io.BytesIO(render(svg, size * scale)))
            canvas.alpha_composite(icon, ((pad + col * (size + gap)) * scale, top + pad * scale))
    PREVIEW_PATH.parent.mkdir(exist_ok=True)
    canvas.save(PREVIEW_PATH, optimize=True)


def build_variant(variant: str) -> dict[str, bytes]:
    src = SVG_DIR / variant
    outputs = {}
    for _, filename, stem, hotspot, frames in ROLES:
        print(f"  {variant}/{filename}", flush=True)
        if frames:
            curs = []
            for i in range(frames):
                cur = build_cur(src / f"{stem}-{i:02d}.svg", hotspot, ANIMATED_SIZES)
                verify_cur(cur, hotspot, ANIMATED_SIZES, f"{variant}/{filename} frame {i}")
                if len(cur) > ANI_FRAME_BUDGET:
                    raise RuntimeError(f"{variant}/{filename} frame {i} is {len(cur)} bytes, "
                                       f"over the {ANI_FRAME_BUDGET}-byte budget")
                curs.append(cur)
            outputs[filename] = build_ani(curs)
        else:
            cur = build_cur(src / f"{stem}.svg", hotspot, STATIC_SIZES)
            verify_cur(cur, hotspot, STATIC_SIZES, f"{variant}/{filename}")
            outputs[filename] = cur
    outputs["install.inf"] = build_inf(variant).encode("ascii")
    return outputs


def main() -> int:
    archive, cursor_files = [], []
    for variant in VARIANTS:
        out_dir = ROOT / f"capitaine-{variant}"
        out_dir.mkdir(exist_ok=True)
        for filename, data in build_variant(variant).items():
            (out_dir / filename).write_bytes(data)
            archive.append((f"capitaine-{variant}/{filename}", data))
            if filename != "install.inf":
                cursor_files.append(out_dir / filename)
    # Text files go in with CRLF line endings so they read well in Notepad.
    for name in ZIP_EXTRAS:
        text = (ROOT / name).read_text(encoding="utf-8")  # universal newlines -> "\n"
        archive.append((name, text.replace("\n", "\r\n").encode("utf-8")))

    if sys.platform == "win32":
        verify_with_windows(cursor_files)
        print(f"Windows loaded all {len(cursor_files)} cursors at every size")

    with zipfile.ZipFile(ZIP_PATH, "w") as zf:
        for name, data in sorted(archive):
            info = zipfile.ZipInfo(name, ZIP_DATE)
            info.external_attr = 0o644 << 16  # rw-r--r-- when extracted on Unix
            zf.writestr(info, data, zipfile.ZIP_DEFLATED, compresslevel=9)
    print(f"Wrote {ZIP_PATH.name} ({ZIP_PATH.stat().st_size / 1e6:.1f} MB)")
    write_preview()
    print(f"Wrote {PREVIEW_PATH.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
