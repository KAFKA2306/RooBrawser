from pydantic import BaseModel
import toml
import json

class SettingsConfig(BaseModel):
    api_url: str
    browser_type: str = "firefox"
    headless_mode: bool = False

class SelectorsConfig(BaseModel):
    pass  # Selectors will be defined later

class PerplexityConfig(BaseModel):
    settings: SettingsConfig
    selectors: SelectorsConfig

    @classmethod
    def load_config(cls):
        settings_path = "config/settings.toml"
        selectors_path = "config/selectors.json"
        settings = toml.load(settings_path)
        selectors = json.load(open(selectors_path, "r"))
        return cls(
            settings=SettingsConfig(**settings),
            selectors=SelectorsConfig(**selectors)
        )