# Credits

## Artwork

**Capitaine Cursors** by [Keefer Rourke](https://krourke.org) and contributors.

- Source: [keeferrourke/capitaine-cursors](https://github.com/keeferrourke/capitaine-cursors), pinned as the `upstream/`
  git submodule at commit `06c8843` (its latest)
- Based on the [KDE Breeze](https://invent.kde.org/plasma/breeze) cursor theme
- License: GNU LGPL v3.0 or later. [COPYING](COPYING) is upstream's licence file, unchanged.

## Colour variants (since 3.2)

Every variant is the same Capitaine artwork with colours replaced in the SVG source (see [TECHNICAL.md](TECHNICAL.md)).
Only colour values are taken from the projects below; no files from them are included.

- **Nord, Gruvbox, Palenight:** the colour maps of
  [sainnhe/capitaine-cursors](https://github.com/sainnhe/capitaine-cursors) by Sainnhe Park, as in its release r5
  (`patch.sh`, including its outline colour), listed on [gnome-look](https://www.gnome-look.org/p/1818760). The fork has
  no licence file; its gnome-look page is tagged LGPLv3 and it modifies the LGPL-3.0 Capitaine artwork. The palettes
  themselves: [Nord](https://github.com/nordtheme/nord) (MIT), [Gruvbox](https://github.com/morhetz/gruvbox) by Pavel
  Pertsev (MIT/X11), Palenight from Material Theme ([material.vim](https://github.com/kaicataldo/material.vim), MIT).
- **Catppuccin Mocha:** [catppuccin/palette](https://github.com/catppuccin/palette) (MIT).
- **Dracula:** [dracula-theme](https://github.com/dracula/dracula-theme) (MIT).
- **Rosé Pine:** [rose-pine/palette](https://github.com/rose-pine/palette) (MIT).
- **Tokyo Night:** the Night palette as in [folke/tokyonight.nvim](https://github.com/folke/tokyonight.nvim)
  (Apache-2.0).
- **Solarized:** [Solarized](https://github.com/altercation/solarized) by Ethan Schoonover (MIT).
- **Blue, Red, Green, Amber, Purple:** the Material Design colour palette (Google).
- **Ideas:** colouring the whole pointer with a palette accent follows
  [catppuccin/cursors](https://github.com/catppuccin/cursors); describing colours by role follows
  [Simp1e](https://gitlab.com/cursors/simp1e). Neither project's files are used.

## Windows adaptation

By [hervad](https://github.com/hervad), © 2026, released under the same license (GNU LGPL v3.0 or later).
Source: <https://github.com/hervad/capitaine-cursors-w11-hidpi>.

- Since 3.0, [w11-cursor-toolkit](https://github.com/hervad/w11-cursor-toolkit) renders the SVGs at the sizes Windows
  requests, from 32 to 256 px, assembles the multi-size `.cur` and `.ani` files and writes the installer
  ([`theme.toml`](theme.toml) holds the roles, hotspots and sizes)
- The pen cursor's hotspot is moved to the pencil tip
- Location and person select (new in 3.0) use the pointing hand
- 16 colour variants (new in 3.2); their colour maps are in [`theme.toml`](theme.toml)
- Windows-specific documentation

## License

The artwork and this adaptation are both licensed under the **GNU Lesser General Public License v3.0 or later**. You
may use, modify and redistribute them, provided you keep the license and credits and license your changes under the
same terms. The full text is in [COPYING](COPYING).
