"""Scroll - a big-screen desktop window for TikTok and Instagram Reels.

It opens the real websites in an Edge (WebView2) window, so you log in
with your own account and everything works like the site, just bigger.

Keys:
  Ctrl+1        TikTok
  Ctrl+2        Instagram Reels
  Ctrl+Tab      switch to the other one
  F11           fullscreen on/off   (Esc also leaves fullscreen)
  F5            reload
  Up / Down     previous / next video (the sites' own keys)
  Ctrl + wheel  zoom
"""
import json
import os

import webview
from webview.menu import Menu, MenuAction, MenuSeparator

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "browser_data")      # logins/cookies live here
SETTINGS_FILE = os.path.join(HERE, "settings.json")

SITES = {
    "tiktok": ("TikTok", "https://www.tiktok.com/foryou"),
    "instagram": ("Instagram Reels", "https://www.instagram.com/reels/"),
}

# Let videos start with sound without clicking first.
os.environ.setdefault(
    "WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS",
    "--autoplay-policy=no-user-gesture-required",
)

window = None
state = {"site": "tiktok", "fullscreen": False}


def load_settings():
    try:
        with open(SETTINGS_FILE, encoding="utf-8") as f:
            saved = json.load(f)
        if saved.get("site") in SITES:
            state["site"] = saved["site"]
    except (OSError, ValueError):
        pass


def save_settings():
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"site": state["site"]}, f)
    except OSError:
        pass


def go(site):
    state["site"] = site
    save_settings()
    name, url = SITES[site]
    window.title = f"Scroll - {name}"
    window.load_url(url)


def toggle_site():
    go("instagram" if state["site"] == "tiktok" else "tiktok")


def toggle_fullscreen():
    state["fullscreen"] = not state["fullscreen"]
    window.toggle_fullscreen()


def reload_page():
    window.evaluate_js("location.reload()")


class Api:
    """Called from the page's keyboard shortcuts."""

    def switch(self, site):
        if site == "other":
            toggle_site()
        elif site in SITES:
            go(site)

    def fullscreen(self):
        toggle_fullscreen()

    def leave_fullscreen(self):
        if state["fullscreen"]:
            toggle_fullscreen()

    def reload(self):
        reload_page()


KEYS_JS = r"""
(function () {
  if (window.__scrollKeys) return;
  window.__scrollKeys = true;
  function api() { return window.pywebview && window.pywebview.api; }
  document.addEventListener('keydown', function (e) {
    var a = api(); if (!a) return;
    var hit = true;
    if (e.key === 'F11') a.fullscreen();
    else if (e.key === 'F5') a.reload();
    else if (e.key === 'Escape') { a.leave_fullscreen(); hit = false; }
    else if (e.ctrlKey && e.key === '1') a.switch('tiktok');
    else if (e.ctrlKey && e.key === '2') a.switch('instagram');
    else if (e.ctrlKey && e.key === 'Tab') a.switch('other');
    else hit = false;
    if (hit) { e.preventDefault(); e.stopPropagation(); }
  }, true);
})();
"""


def on_loaded():
    try:
        window.evaluate_js(KEYS_JS)
    except Exception:
        pass


def main():
    global window
    load_settings()
    name, url = SITES[state["site"]]

    menu = [
        Menu("Switch", [
            MenuAction("TikTok    (Ctrl+1)", lambda: go("tiktok")),
            MenuAction("Instagram Reels    (Ctrl+2)", lambda: go("instagram")),
            MenuSeparator(),
            MenuAction("Other one    (Ctrl+Tab)", toggle_site),
        ]),
        Menu("View", [
            MenuAction("Fullscreen    (F11)", toggle_fullscreen),
            MenuAction("Reload    (F5)", reload_page),
        ]),
    ]

    window = webview.create_window(
        f"Scroll - {name}",
        url,
        js_api=Api(),
        width=1600,
        height=1000,
        maximized=True,
        min_size=(600, 500),
        background_color="#000000",
        text_select=True,
        zoomable=True,
    )
    window.events.loaded += on_loaded

    os.makedirs(DATA_DIR, exist_ok=True)
    webview.start(
        gui="edgechromium",
        private_mode=False,          # keep you logged in between runs
        storage_path=DATA_DIR,
        menu=menu,
    )


if __name__ == "__main__":
    main()
