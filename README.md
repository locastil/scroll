# Scroll

Scroll is a big-screen Windows app for TikTok and Instagram Reels. It opens the real websites in an Edge WebView2 window (through pywebview). You log in with your own account, and the app keeps you signed in between runs. You can switch between TikTok and Instagram with one key.

## Requirements

- Windows 10 or 11 with the Microsoft Edge WebView2 Runtime (included with current Windows)
- Python 3.11 (tested with 3.11.9)
- The `pywebview` package (see `requirements.txt`), which pulls in `pythonnet`, `bottle` and `proxy_tools`

## Install

```
cd C:\Users\YourName\TikTokDesktop
py -3.11 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Run

- Double-click `Scroll.bat`. It starts `scroll_app.py` with `.venv\Scripts\pythonw.exe` and no console window.
- Or use the **Scroll** shortcut on the Desktop or in the Start menu.
- Or press **Ctrl+Alt+S** from anywhere. The hotkey is set on the Start menu shortcut
  (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Scroll.lnk`). Windows only honours shortcut hotkeys on
  `.lnk` files in the Desktop or Start menu folders, so if you recreate that shortcut, set its
  "Shortcut key" again under Properties.

## Keys inside the app

| Key | Action |
| --- | --- |
| Ctrl+1 | TikTok |
| Ctrl+2 | Instagram Reels |
| Ctrl+Tab | Switch to the other site |
| F11 | Fullscreen on/off (Esc also leaves fullscreen) |
| F5 | Reload |
| Up / Down | Previous / next video |
| Ctrl + mouse wheel | Zoom |

The same actions are in the **Switch** and **View** menus.

## Local data (not committed)

- `browser_data/` is the WebView2 profile. It holds your logins, cookies and cache.
- `settings.json` remembers the last site you opened.
- `.venv/` is the Python environment.

All three are listed in `.gitignore`. Never commit them.
