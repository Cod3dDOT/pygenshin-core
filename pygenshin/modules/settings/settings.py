import json
from enum import Enum
from pygenshin.modules.additional_types import Rect

class Settings:
    WindowRect = None
    MapScreenshotRect = None

    DataFolder = None

    def Valid(self) -> bool:
        return self.WindowRect and self.ScreenshotRect

    def ToJson(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return "Settings()"

    def __str__(self):
        return self.ToJson()