<div align="center">

# Capitaine Cursors for Windows

**Crisp, macOS-inspired cursors for Windows 10 and 11, rendered natively for every display scale.**

[![Download](https://img.shields.io/github/v/release/hervad/capitaine-cursors-w11-hidpi?label=download&style=flat-square&color=2ea44f)](https://github.com/hervad/capitaine-cursors-w11-hidpi/releases/latest)
[![Windows 10 | 11](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D4?style=flat-square)](#install)
[![License: LGPL-3.0-or-later](https://img.shields.io/badge/license-LGPL--3.0--or--later-blue?style=flat-square)](COPYING)

<img src="docs/preview.png" alt="All 15 cursors: the Dark variant on a light background, and the Light variant on a dark background" width="100%">

</div>

## Install

1. **Download** `capitaine-cursors-windows11.zip` from the [latest release](https://github.com/hervad/capitaine-cursors-w11-hidpi/releases/latest) and extract it.
2. **Right-click** `install.inf` in `capitaine-dark` or `capitaine-light` and choose **Install**, then approve the administrator prompt.
   On Windows 11, **Install** is under **Show more options**.
3. **Apply:** press <kbd>Win</kbd>+<kbd>R</kbd>, run `main.cpl`, open the **Pointers** tab, pick the scheme and click **OK**.

That's it. Having trouble, or upgrading from 1.0? See the [installation guide](INSTALL.md).

## Pick a variant

| | Dark | Light |
| --- | --- | --- |
| **Look** | Black pointer, white outline | White pointer, black outline |
| **Scheme name** | Capitaine Cursors (Dark) | Capitaine Cursors (Light) |
| **Folder** | `capitaine-dark` | `capitaine-light` |

Both are outlined, so either one stays visible on any background. Install both and switch whenever you like.

## Why they stay sharp

Windows doesn't scale cursors smoothly. It picks a cursor size in steps from your display scale, then multiplies it by the pointer size in **Settings › Accessibility › Mouse pointer and touch**. If a cursor file doesn't contain that exact size, Windows resamples the nearest one, and resampling blurs.

Every cursor here is rendered from the original vector artwork at the exact sizes Windows asks for:

| Display scale | Pointer size 1 | Size 2 | Size 3 |
| --- | :-: | :-: | :-: |
| 100–149% | 32 px | 48 px | 64 px |
| 150–199% | 48 px | 72 px | 96 px |
| 200–299% | 64 px | 96 px | 128 px |
| 300–399% | 96 px | 144 px | 192 px |
| 400%+ | 128 px | 192 px | 256 px |

Every size in the table is exact for static cursors. The two animated cursors (busy and working) are exact for pointer sizes 1 and 3. At size 2 they use the next larger image, scaled down slightly. Larger pointer sizes use the next larger image, up to Windows' 256 px maximum.

**No performance cost.** Windows decodes only the image it displays. A cursor loads in about 1 ms and an animated cursor in about 8 ms, the same as before. Each file is also test-loaded with the Windows cursor loader at every size during the build.

## What's included

- **15 cursors:** normal, help, working in background, busy, precision, text, handwriting, unavailable, 4 resize directions, move, alternate and link. Busy and working are animated, with 24 frames at 30 fps.
- Every hotspot is placed on the tip or center at every size.
- An `install.inf` for each variant, with uninstall support.

## Uninstall

In **main.cpl › Pointers**, switch to another scheme first. Then run this from an administrator terminal, using the path to the `install.inf` you installed:

```powershell
rundll32.exe setupapi.dll,InstallHinfSection DefaultUninstall 132 C:\path\to\capitaine-dark\install.inf
```

## Build from source

The cursors are generated from the SVGs in [`src/svg`](src/svg) by [`build.py`](build.py) (Python 3.10+):

```powershell
python -m pip install -r requirements.txt
python build.py
```

This rebuilds both variant folders, the release zip and `docs/preview.png`. [TECHNICAL.md](TECHNICAL.md) explains how the size ladder, hotspots and animation limits were chosen.

## Credits

The artwork is [Capitaine Cursors](https://github.com/keeferrourke/capitaine-cursors) by [Keefer Rourke](https://krourke.org) and contributors, based on [KDE Breeze](https://invent.kde.org/plasma/breeze). This project packages it for Windows. See [ATTRIBUTION.md](ATTRIBUTION.md).

Licensed under the [GNU LGPL v3.0 or later](COPYING).
