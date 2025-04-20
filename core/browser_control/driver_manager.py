import toml
import json
from core.browser_control.browser_state import BrowserState
from selenium import webdriver

class PerplexityBrowser:
    def __init__(self):
        self.config = self._load_config()
        self.state = BrowserState.INITIALIZING
        self.driver = self._init_webdriver()

    def _load_config(self):
        settings_path = "config/settings.toml"
        selectors_path = "config/selectors.json"
        settings = toml.load(settings_path)
        selectors = json.load(open(selectors_path, "r"))
        return {"settings": settings, "selectors": selectors}

    def _init_webdriver(self):
        browser_type = self.config['settings'].get('browser_type', 'firefox').lower()
        if browser_type == 'firefox':
            driver = webdriver.Firefox()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        return driver