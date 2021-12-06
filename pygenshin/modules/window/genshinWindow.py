from pygenshin.modules.additional_types import Rect
from .windowManager import getWindowHandle, getWindowRect, setForeground

class GenshinWindow:
    WINDOW_RECT = None
    HANDLE = None

    def __init__(self) -> None:
        self.HANDLE = getWindowHandle("Genshin Impact")

    def IsGenshinRunning(self) -> bool:
        handle = getWindowHandle("Genshin Impact")
        if (not self.HANDLE): return False

        w_r = getWindowRect(self.HANDLE)
        if (not w_r or not self.IsInBounds(w_r)): return False
        self.HANDLE = handle
        self.WINDOW_RECT = w_r
        return True

    def IsInBounds(self, rect:Rect, bounds:Rect = None):
        if (not bounds):
            return rect.start.asTuple() > (0, 0)
        else:
            return rect.start.asTuple() > (0, 0) # TODO
    
    def UpdateWindowRect(self):
        self.WINDOW_RECT = getWindowRect(self.HANDLE)
        return self.WINDOW_RECT

    def GetWindowRect(self):
        return self.WINDOW_RECT

    def BringToForeground(self):
        setForeground(self.HANDLE)