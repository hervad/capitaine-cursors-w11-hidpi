# Installation guide

## Install

1. Download `capitaine-cursors-windows11.zip` from the [latest release](https://github.com/hervad/capitaine-cursors-w11-hidpi/releases/latest) and extract it anywhere.
2. Open `capitaine-dark` or `capitaine-light`.
3. Right-click `install.inf` and choose **Install**. On Windows 11, choose **Show more options** first.
4. Approve the administrator prompt. The installer copies the cursors to `C:\Windows\Cursors\Capitaine Cursors (Dark)` or `(Light)` and registers the scheme for all users.
5. Press <kbd>Win</kbd>+<kbd>R</kbd>, run `main.cpl`, and open the **Pointers** tab.
6. Under **Scheme**, pick **Capitaine Cursors (Dark)** or **Capitaine Cursors (Light)**, then click **OK**.

You can also reach the Pointers tab from **Settings › Bluetooth & devices › Mouse › Additional mouse settings**.

The extracted folder isn't needed after installation.

## Change the pointer size

Go to **Settings › Accessibility › Mouse pointer and touch › Size**. Sizes 1–3 are rendered pixel-exact at every display scale. Larger sizes are scaled down from a larger image, so they stay sharp too.

Choosing a different **Mouse pointer style** on that page (white, black, inverted or custom colors) switches back to Windows' own cursors. To get Capitaine back, select it again in `main.cpl`.

## Switch variants

Install both variants and switch between them in `main.cpl › Pointers`.

## Upgrading from 1.0

Version 1.0 registered its schemes as **Capitaine HiDPI** (light) and **Capitaine Dark HiDPI**, and didn't include an uninstaller. Install the new version as described above and select the new scheme. To remove the old entries, run this in an administrator PowerShell:

```powershell
$schemes = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Control Panel\Cursors\Schemes'
Remove-ItemProperty $schemes -Name 'Capitaine HiDPI', 'Capitaine Dark HiDPI' -ErrorAction SilentlyContinue
Remove-Item "$env:WINDIR\Cursors\Capitaine HiDPI", "$env:WINDIR\Cursors\Capitaine Dark HiDPI" -Recurse -ErrorAction SilentlyContinue
```

## Uninstall

1. In `main.cpl › Pointers`, choose another scheme, such as **Windows Default (system scheme)**, and click **OK**.
2. In an administrator terminal, run the uninstall section of the `install.inf` you installed:

   ```powershell
   rundll32.exe setupapi.dll,InstallHinfSection DefaultUninstall 132 C:\path\to\capitaine-dark\install.inf
   ```

   This removes the cursor files and the scheme entry. Windows may leave an empty folder under `C:\Windows\Cursors`, which you can delete.

## Troubleshooting

**There's no "Install" when I right-click `install.inf`.**
On Windows 11, choose **Show more options** or press <kbd>Shift</kbd>+<kbd>F10</kbd>. Make sure you extracted the zip first; Windows can't install from inside it.

**The scheme isn't in the list.**
Close and reopen `main.cpl` after installing. The scheme is registered for all users, so the installer needs administrator rights. If you declined the prompt, run the installer again.

**The cursors look blurry.**
Make sure a Capitaine scheme is selected in `main.cpl › Pointers`, not only installed. If you changed the display scale or pointer size, click **OK** in `main.cpl` again to reload the cursors.

**Some apps show different cursors.**
Browsers (for CSS cursors), games, and some creative tools draw their own cursors. Only the system cursors change.

**Upgrading doesn't change anything.**
Version 1.0 used different scheme names. Select **Capitaine Cursors (Dark)** or **(Light)** instead of **Capitaine HiDPI** (see [Upgrading from 1.0](#upgrading-from-10)).
