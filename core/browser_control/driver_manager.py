from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any, Callable, Mapping

from core.browser_control.browser_state import BrowserState

DriverFactory = Callable[[], Any]


class PerplexityBrowser:
    """Own a Selenium WebDriver and release it deterministically."""

    def __init__(
        self,
        *,
        config_dir: str | Path | None = None,
        config: Mapping[str, Any] | None = None,
        driver_factory: DriverFactory | None = None,
        auto_start: bool = True,
    ) -> None:
        self.state = BrowserState.INITIALIZING
        self.driver: Any | None = None
        self._driver_factory = driver_factory
        self._config_dir = (
            Path(config_dir).expanduser().resolve()
            if config_dir is not None
            else Path(__file__).resolve().parents[2] / "config"
        )

        try:
            self.config = dict(config) if config is not None else self._load_config()
            if auto_start:
                self.start()
        except BaseException:
            self.state = BrowserState.ERROR
            self._discard_driver()
            raise

    def _load_config(self) -> dict[str, Any]:
        settings_path = self._config_dir / "settings.toml"
        selectors_path = self._config_dir / "selectors.json"

        with settings_path.open("rb") as settings_file:
            settings = tomllib.load(settings_file)
        with selectors_path.open("r", encoding="utf-8") as selectors_file:
            selectors = json.load(selectors_file)
        return {"settings": settings, "selectors": selectors}

    def _default_driver_factory(self) -> Any:
        browser_type = self.config["settings"].get("browser_type", "firefox").lower()
        if browser_type != "firefox":
            raise ValueError(f"Unsupported browser type: {browser_type}")

        from selenium import webdriver

        return webdriver.Firefox()

    def start(self) -> Any:
        """Start the configured driver once and transition to READY."""
        if self.state == BrowserState.CLOSED:
            raise RuntimeError("Cannot restart a closed browser")
        if self.driver is not None:
            return self.driver

        self.state = BrowserState.INITIALIZING
        try:
            factory = self._driver_factory or self._default_driver_factory
            self.driver = factory()
            self.state = BrowserState.READY
            return self.driver
        except BaseException:
            self.state = BrowserState.ERROR
            self._discard_driver()
            raise

    def _discard_driver(self) -> None:
        driver, self.driver = self.driver, None
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass

    def close(self) -> None:
        """Quit the owned driver at most once; repeated calls are safe."""
        if self.state == BrowserState.CLOSED:
            return

        driver, self.driver = self.driver, None
        try:
            if driver is not None:
                driver.quit()
        finally:
            self.state = BrowserState.CLOSED

    def __enter__(self) -> "PerplexityBrowser":
        if self.driver is None:
            self.start()
        return self

    def __exit__(self, exc_type: object, exc: BaseException | None, traceback: object) -> bool:
        self.close()
        return False
