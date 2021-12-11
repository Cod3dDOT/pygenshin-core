from pygenshin.modules.additional_types import Rect
from . import windowManager as pgWindowManager
import pygenshin.modules.math as pgMath


WINDOW_RECT = None
HANDLE = None


def GetGenshinImpactHandle() -> None:
    global HANDLE
    HANDLE = pgWindowManager.GetWindowHandle("Genshin Impact")
    return HANDLE


def IsGenshinImpactRunning() -> bool:
    window = GetGenshinImpactHandle()
    desktop = pgWindowManager.GetDesktopHandle()
    if (not window or not desktop):
        return False

    windowRect = pgWindowManager.GetWindowRect(window)
    desktopRect = pgWindowManager.GetWindowRect(desktop)

    # or not pgMath.IsRectInsideBounds(windowRect, desktopRect)):
    if (not windowRect or not desktopRect):
        return False

    return True


def GetGenshinImpactWindowRect() -> Rect:
    global WINDOW_RECT
    window = GetGenshinImpactHandle()
    # if (not window):
    #     return False

    WINDOW_RECT = pgWindowManager.GetWindowRect(window)
    return WINDOW_RECT


def BringGenshinImpactToFront() -> None:
    pgWindowManager.SetWindowToForeground(HANDLE)
