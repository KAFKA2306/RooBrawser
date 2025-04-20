import pytest
import sys
sys.path.append('.')  # Add project root to Python path
from core.browser_control.driver_manager import PerplexityBrowser
from core.browser_control.browser_state import BrowserState
from unittest.mock import patch

def test_initialize_perplexity_browser():
    browser = PerplexityBrowser()
    assert isinstance(browser, PerplexityBrowser)
    assert browser.config is not None
    assert browser.state == BrowserState.INITIALIZING
    from selenium.webdriver.firefox.webdriver import WebDriver
    assert isinstance(browser.driver, WebDriver)