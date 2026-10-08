# Installation guide

## Install

1. Download `capitaine-dark-w11-hidpi-v….zip` or `capitaine-light-w11-hidpi-v….zip` from the
   [latest release](https://github.com/hervad/capitaine-cursors-w11-hidpi/releases/latest) and extract it anywhere.
2. Open the extracted `Capitaine Dark W11 HiDPI` or `Capitaine Light W11 HiDPI` folder.
3. Right-click `install.inf` and choose **Install**. On Windows 11, choose **Show more options** first.
4. Approve the administrator prompt. The installer copies the cursors to `C:\Windows\Cursors\Capitaine Dark W11 HiDPI`
   or `Capitaine Light W11 HiDPI`, adds the scheme for your account and applies it. Mouse Properties may open.
5. If the cursors don't change right away, press <kbd>Win</kbd>+<kbd>R</kbd>, run `main.cpl`, open the **Pointers** tab,
   pick **Capitaine Dark W11 HiDPI** or **Capitaine Light W11 HiDPI** and click **OK**.

You can also reach the Pointers tab from **Settings › Bluetooth & devices › Mouse › Additional mouse settings**.
The extracted folder isn't needed after installation, except for `uninstall.cmd` (see below).

## Change the pointer size

Go to **Settings › Accessibility › Mouse pointer and touch › Size**. The README lists which image size Windows uses for
each pointer size and display scale; every one of them is in the files.

Choosing a different **Mouse pointer style** on that page (white, black, inverted or custom colors) switches back to
Windows' own cursors. To get Capitaine back, select it again in `main.cpl`.

## Switch variants

Install both variants and switch between them in `main.cpl › Pointers`.

## Upgrading

**From 3.0 or 2.0:** both used the scheme names *Capitaine Cursors (Dark)* and *(Light)* - 2.0 registered them for all
users (`HKLM`), 3.0 for your account (`HKCU`). Since 3.1 the schemes are called *Capitaine Dark/Light W11 HiDPI*, so the
old ones would stay in the list. Choose another scheme in `main.cpl` (e.g. **Windows Default**), then run this in an
administrator PowerShell (it covers both versions):

```powershell
foreach ($key in 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Control Panel\Cursors\Schemes', 'HKCU:\Control Panel\Cursors\Schemes') {
    Remove-ItemProperty $key -Name 'Capitaine Cursors (Dark)', 'Capitaine Cursors (Light)' -ErrorAction SilentlyContinue
}
Remove-Item "$env:WINDIR\Cursors\Capitaine Cursors (Dark)", "$env:WINDIR\Cursors\Capitaine Cursors (Light)" -Recurse -ErrorAction SilentlyContinue
```

**From 1.0:** 1.0 registered its schemes as **Capitaine HiDPI** (light) and **Capitaine Dark HiDPI**. Remove them the
same way:

```powershell
$schemes = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Control Panel\Cursors\Schemes'
Remove-ItemProperty $schemes -Name 'Capitaine HiDPI', 'Capitaine Dark HiDPI' -ErrorAction SilentlyContinue
Remove-Item "$env:WINDIR\Cursors\Capitaine HiDPI", "$env:WINDIR\Cursors\Capitaine Dark HiDPI" -Recurse -ErrorAction SilentlyContinue
```

## Uninstall

1. Run `uninstall.cmd` from the extracted folder. It removes the scheme entry and opens Mouse Properties.
2. Choose another scheme, such as **Windows Default (system scheme)**, and click **OK**.
3. Delete the cursor files from an administrator PowerShell:

   ```powershell
   Remove-Item "$env:WINDIR\Cursors\Capitaine Dark W11 HiDPI" -Recurse
   ```

## Troubleshooting

**There's no "Install" when I right-click `install.inf`.**
On Windows 11, choose **Show more options** or press <kbd>Shift</kbd>+<kbd>F10</kbd>. Make sure you extracted the zip
first; Windows can't install from inside it.

**The scheme appears twice.**
An older version (3.0, 2.0 or 1.0) is still registered. See [Upgrading](#upgrading).

**The cursors look blurry.**
Make sure a Capitaine scheme is selected in `main.cpl › Pointers`, not only installed. If you changed the display
scale or pointer size, click **OK** in `main.cpl` again to reload the cursors. At 125 % and 175 % display scale some
softness is normal (the README explains why).

**Some apps show different cursors.**
Browsers (for CSS cursors), games, and some creative tools draw their own cursors. Only the system cursors change.
