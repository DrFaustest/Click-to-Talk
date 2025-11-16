# window_manager.py
import os
import sys
import shlex
import subprocess
import webbrowser
import re

class WindowManager:
    def __init__(self, site_aliases=None, preferred_browser=None, browser_open_target="about:blank"):
        self.site_aliases = site_aliases or {}
        self.preferred_browser = preferred_browser  # e.g., "/Applications/Brave Browser.app"
        self.browser_open_target = browser_open_target or "about:blank"

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
        url = self._to_url(target)

        if url:
            self.open_url(url)
            return

        # No URL: just open the browser app
        self.open_browser()

    def open_url(self, url: str):
        """
        Cross-platform: open a URL in either preferred browser or system default.
        """
        handled = False
        if self.preferred_browser:
            handled = self._launch_preferred_browser(url)

        if not handled:
            handled = self._open_with_system_default(url)

        if not handled:
            webbrowser.open(url)

        print(f"Opening URL: {url}")

    def open_browser(self):
        """
        Open just the browser (blank window).
        """
        target = self.browser_open_target or "about:blank"

        handled = False
        if self.preferred_browser:
            handled = self._launch_preferred_browser(target if target != "about:blank" else None)

        if not handled:
            # For about:blank on Windows, just use webbrowser module
            # which handles it properly
            webbrowser.open(target)
            handled = True

        print("Opening browser")

    def _launch_preferred_browser(self, url=None):
        """
        Attempt to launch the preferred browser/application with optional URL.
        Returns True if the launch command was dispatched successfully.
        """
        if not self.preferred_browser:
            return False

        try:
            if sys.platform == "darwin":
                args = ["open", "-a", self.preferred_browser]
                if url:
                    args.append(url)
                subprocess.run(args, check=False)
                return True

            # Windows or Linux: treat preferred_browser as command / path.
            if isinstance(self.preferred_browser, (list, tuple)):
                cmd = list(self.preferred_browser)
            else:
                if sys.platform.startswith("win"):
                    cmd = shlex.split(self.preferred_browser, posix=False)
                else:
                    cmd = shlex.split(self.preferred_browser)
            if url:
                cmd.append(url)
            subprocess.Popen(cmd)
            return True
        except FileNotFoundError:
            print(f"Preferred browser '{self.preferred_browser}' was not found; falling back to system default.")
        except OSError as exc:
            print(f"Unable to launch preferred browser '{self.preferred_browser}': {exc}")

        return False

    def _open_with_system_default(self, target):
        """
        Use the OS default handler (e.g., default browser) for a URL/URI/shortcut.
        Returns True on best-effort dispatch.
        """
        if not target:
            return False

        try:
            if sys.platform == "darwin":
                subprocess.run(["open", target], check=False)
                return True
            if sys.platform.startswith("win"):
                os.startfile(target)
                return True

            subprocess.run(["xdg-open", target], check=False)
            return True
        except FileNotFoundError:
            # xdg-open missing -> fallback later
            pass
        except OSError as exc:
            print(f"OS default open failed for '{target}': {exc}")

        return False
