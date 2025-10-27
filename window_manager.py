# window_manager.py
import sys, subprocess, webbrowser, re

class WindowManager:
    def __init__(self, site_aliases=None, preferred_browser=None):
        self.site_aliases = site_aliases or {}
        self.preferred_browser = preferred_browser  # e.g., "Google Chrome" (mac), "chrome" (win)

    def _to_url(self, target: str):
        t = target.strip().lower()

        # 1) Alias (e.g., "gmail" -> https://mail.google.com)
        if t in self.site_aliases:
            return self.site_aliases[t]

        # 2) Raw URL or domain
        if re.search(r'\.\w{2,}$', t) or t.startswith(("http://", "https://")):
            if not t.startswith(("http://", "https://")):
                t = "https://" + t
            return t

        # 3) Not a URL (e.g., "browser", "chrome"): treat as open-browser-only
        return None

    def open(self, target: str):
        """
        Open a site or a browser.
        - If 'target' resolves to a URL, navigate to it.
        - Otherwise, just open the browser.
        """
        print(f"[DEBUG] open() target='{target}'")  # NEW: debug
        url = self._to_url(target)
        print(f"[DEBUG] resolved url={url}")  # NEW: debug

        if url:
            self.open_url(url)
            return

        # No URL: just open the browser app
        self.open_browser()

    def open_url(self, url: str):
        """
        Cross-platform: open a URL in either preferred browser or system default.
        """
        if sys.platform == "darwin":  # macOS
            if self.preferred_browser:
                subprocess.run(["open", "-a", self.preferred_browser, url])
            else:
                subprocess.run(["open", url])
        elif sys.platform.startswith("win"):
            if self.preferred_browser and self.preferred_browser.lower() == "chrome":
                try:
                    subprocess.Popen(["chrome", url])
                except FileNotFoundError:
                    webbrowser.open(url)
            else:
                webbrowser.open(url)
        else:
            webbrowser.open(url)

        print(f"Opening URL: {url}")

    def open_browser(self):
        """
        Open just the browser (blank window).
        """
        if sys.platform == "darwin":
            app = self.preferred_browser or "Safari"
            subprocess.run(["open", "-a", app])
            print(f"Opening browser app: {app}")
        elif sys.platform.startswith("win"):
            if self.preferred_browser and self.preferred_browser.lower() == "chrome":
                try:
                    subprocess.Popen(["chrome"])
                    print("Opening browser app: chrome")
                    return
                except FileNotFoundError:
                    pass
            webbrowser.open("about:blank")
            print("Opening default browser")
        else:
            webbrowser.open("about:blank")
            print("Opening default browser")
