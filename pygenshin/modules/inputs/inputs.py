from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from pygenshin.modules.inputs.keybindings import KEY, MOUSEBUTTONS
from pygenshin.modules.additional_types import Rect, Vector2
from pygenshin.modules.gamescreens import UIButton

import time


class Inputs:
    Mouse = None
    Keyboard = None
    WindowRect = None

    def __init__(self, windowRect: Rect) -> None:
        self.Mouse = MouseController()
        self.Keyboard = KeyboardController()
        self.WindowRect = windowRect

    def SetAbsolutesMousePos(self, pos: Vector2):
        self.Mouse.position = pos.asTuple()

    def SetMousePos(self, pos: Vector2):
        self.Mouse.position = (self.WindowRect.start + pos).asTuple()

    def PressKey(self, key: KEY):
        self.Keyboard.press(key)

    def ReleaseKey(self, key: KEY):
        self.Keyboard.press(key)

    def TapKey(self, key: KEY):
        self.Keyboard.tap(key)
        time.sleep(0.1)

    def ClickMouse(self):
        self.Mouse.click(MOUSEBUTTONS.LEFT)

    def PressUIButton(self, uiButton: UIButton):
        if (uiButton.keybind):
            self.TapKey(uiButton.keybind)
        else:
            self.PressKey('alt')
            self.SetMousePos(uiButton.position.center)
            self.ClickMouse()
            self.ReleaseKey('alt')
        time.sleep(1)

    def TapEscKey(self):
        self.TapKey(KEY.ESCAPE)
