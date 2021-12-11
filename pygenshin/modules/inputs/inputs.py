from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from pygenshin.modules.inputs.keybindings import KEY, MOUSEBUTTON
from pygenshin.modules.additional_types import Vector2
from pygenshin.modules.gamescreens import UIButton
import pygenshin.modules.window as pgWindow

import time

MOUSE = MouseController()
KEYBOARD = KeyboardController()


def SetMousePosAbsolute(position: Vector2) -> None:
    MOUSE.position = position.asTuple()


def SetMousePosRelative(position: Vector2) -> None:
    MOUSE.position = (
        pgWindow.GetGenshinImpactWindowRect().start + position
    ).asTuple()


def GetMousePosAbsolute() -> Vector2:
    return Vector2.fromTuple(MOUSE.position)


def GetMousePosRelative() -> Vector2:
    return Vector2.fromTuple(MOUSE.position) - pgWindow.GetGenshinImpactWindowRect().start


def MoveMousePosAbsolute(moveBy: Vector2) -> None:
    MOUSE.move(moveBy.x, moveBy.y)


def ClickMouse() -> None:
    MOUSE.click(MOUSEBUTTON.LEFT)


def PressMouse() -> None:
    MOUSE.press(MOUSEBUTTON.LEFT)


def ReleaseMouse() -> None:
    MOUSE.release(MOUSEBUTTON.LEFT)


def DragMouse(startPos: Vector2, endPos: Vector2, duration: float) -> None:
    PressMouse()
    draw_steps = 100  # total times to update cursor

    step_x = (endPos.x - startPos.x) / draw_steps
    step_y = (endPos.y - startPos.y) / draw_steps
    dt = duration / draw_steps

    for n in range(draw_steps):
        x = int(startPos.x + step_x * n)
        y = int(startPos.y + step_y * n)
        MOUSE.position = (x, y)
        time.sleep(dt)
    MOUSE.position = endPos.asTuple()


def PressUIButton(uiButton: UIButton) -> None:
    if (uiButton.keybind):
        TapKey(uiButton.keybind)
    else:
        PressKey('alt')
        SetMousePosRelative(uiButton.position.center)
        ClickMouse()
        ReleaseKey('alt')
    time.sleep(1)


# Keyboard stuff
def PressKey(key: KEY) -> None:
    KEYBOARD.press(key)


def ReleaseKey(key: KEY) -> None:
    KEYBOARD.press(key)


def TapKey(key: KEY) -> None:
    KEYBOARD.tap(key)
    time.sleep(0.1)
