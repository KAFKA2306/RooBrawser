import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from core.browser_control.browser_state import BrowserState
from core.browser_control.driver_manager import PerplexityBrowser


@pytest.fixture
def config_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "config"
    directory.mkdir()
    (directory / "settings.toml").write_text('browser_type = "firefox"\n', encoding="utf-8")
    (directory / "selectors.json").write_text(json.dumps({"answer": ".result"}), encoding="utf-8")
    return directory


def test_successful_start_transitions_to_ready(config_dir: Path) -> None:
    driver = Mock()
    browser = PerplexityBrowser(config_dir=config_dir, driver_factory=lambda: driver)

    assert browser.state is BrowserState.READY
    assert browser.driver is driver

    browser.close()
    driver.quit.assert_called_once_with()
    assert browser.state is BrowserState.CLOSED


def test_close_is_idempotent(config_dir: Path) -> None:
    driver = Mock()
    browser = PerplexityBrowser(config_dir=config_dir, driver_factory=lambda: driver)

    browser.close()
    browser.close()

    driver.quit.assert_called_once_with()
    assert browser.state is BrowserState.CLOSED


def test_driver_start_failure_transitions_to_error(config_dir: Path) -> None:
    def fail() -> object:
        raise RuntimeError("driver unavailable")

    with pytest.raises(RuntimeError, match="driver unavailable"):
        PerplexityBrowser(config_dir=config_dir, driver_factory=fail)


def test_invalid_config_transitions_to_error_without_starting_driver(tmp_path: Path) -> None:
    factory = Mock()

    with pytest.raises(FileNotFoundError):
        PerplexityBrowser(config_dir=tmp_path / "missing", driver_factory=factory)

    factory.assert_not_called()


def test_context_manager_closes_on_normal_exit(config_dir: Path) -> None:
    driver = Mock()

    with PerplexityBrowser(config_dir=config_dir, driver_factory=lambda: driver) as browser:
        assert browser.state is BrowserState.READY

    driver.quit.assert_called_once_with()
    assert browser.state is BrowserState.CLOSED


def test_context_manager_closes_on_exception(config_dir: Path) -> None:
    driver = Mock()

    with pytest.raises(ValueError, match="boom"):
        with PerplexityBrowser(config_dir=config_dir, driver_factory=lambda: driver):
            raise ValueError("boom")

    driver.quit.assert_called_once_with()


def test_context_manager_closes_on_keyboard_interrupt(config_dir: Path) -> None:
    driver = Mock()

    with pytest.raises(KeyboardInterrupt):
        with PerplexityBrowser(config_dir=config_dir, driver_factory=lambda: driver):
            raise KeyboardInterrupt

    driver.quit.assert_called_once_with()


def test_explicit_start_supports_dependency_injection(config_dir: Path) -> None:
    driver = Mock()
    browser = PerplexityBrowser(
        config_dir=config_dir,
        driver_factory=lambda: driver,
        auto_start=False,
    )

    assert browser.state is BrowserState.INITIALIZING
    assert browser.driver is None
    assert browser.start() is driver
    assert browser.state is BrowserState.READY
    browser.close()


def test_default_config_path_is_independent_of_current_working_directory(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    driver = Mock()
    monkeypatch.chdir(tmp_path)

    browser = PerplexityBrowser(driver_factory=lambda: driver)

    assert browser.config["settings"]["browser_type"] == "firefox"
    browser.close()
