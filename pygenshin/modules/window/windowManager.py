import win32gui
from pygenshin.modules.additional_types import Rect


def GetWindowHandle(title: str):
    return win32gui.FindWindow(None, title)


def GetWindowRect(handle) -> Rect:
    xS, yS, xE, yE = win32gui.GetWindowRect(handle)
    #x, y = win32gui.ClientToScreen(handle, (xS, yS))
    #x1, y1 = win32gui.ClientToScreen(handle, (xE, yE))
    rect = Rect.fromArray([xS+3, yS+25, xE-3, yE-5])
    return rect


def SetWindowToForeground(handle) -> None:
    win32gui.SetForegroundWindow(handle)


def GetDesktopHandle():
    return win32gui.GetDesktopWindow()
