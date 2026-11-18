# Scroll

A big-screen Windows window for TikTok and Instagram Reels. It opens the real sites in Edge WebView2 (pywebview), so you stay logged in with your own account.

## Run

```
python -m venv .venv
.venv\Scripts\pip install pywebview
Scroll.bat
```

## Keys

- Ctrl+1 TikTok, Ctrl+2 Instagram Reels, Ctrl+Tab switch
- F11 fullscreen (Esc leaves), F5 reload
- Up / Down previous / next video, Ctrl + wheel zoom

Logins are stored in `browser_data/`, which is not committed.
