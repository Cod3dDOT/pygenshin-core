import win32gui

from pygenshin.modules.additional_types import Rect

def getWindowHandle(title:str):
    return win32gui.FindWindow(None, title)

def getWindowRect(handle):
    xS, yS, xE, yE = win32gui.GetWindowRect(handle)
    #x, y = win32gui.ClientToScreen(handle, (xS, yS))
    #x1, y1 = win32gui.ClientToScreen(handle, (xE, yE))
    rect = Rect.fromRect([xS+3, yS+25, xE-3, yE-5])
    print(rect)
    return rect

def setForeground(handle):
    win32gui.SetForegroundWindow(handle)