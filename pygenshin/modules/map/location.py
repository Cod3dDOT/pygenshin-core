import pygenshin.modules.inputs as pgInputs
import pygenshin.modules.gamescreens as pgScreens
import pygenshin.modules.detection.opencvUtils as opencvUtils
import pygenshin.modules.math as pgMath
import pygenshin.modules.settings as pgSettings
import pygenshin.modules.window as pgWindow
from pygenshin.modules.additional_types import PYGenshinException, Rect, Vector2

import cv2
import time
import os
import numpy

DOMAIN_MARKER_IMAGE = None
TELEPORT_MARKER_IMAGE = None
FULL_MAP_IMAGE = None

FULL_MAP_INFO = None

CAN_USE_MINIMAP = False
RESIZED_MAP = None
RESIZED_MAP_POSITION: Rect = None

CurrentPosition: Vector2 = None


def ZoomIn():
    pgInputs.SetMousePosRelative(pgScreens.MapScreen.Buttons.ZoomPlus.position.center.toPixels(
        pgWindow.GetGenshinImpactWindowRect().GetDimensions().asTuple()))
    for _ in range(5):
        pgInputs.ClickMouse()
        time.sleep(0.1)


def LoadMapDescriptors(kpts_path, desc_path):
    global FULL_MAP_INFO

    if os.path.getsize(kpts_path) <= 0 or os.path.getsize(desc_path) <= 0:
        raise PYGenshinException("Failed loading descriptors")

    kpts = numpy.load(kpts_path)
    desc = numpy.load(desc_path)
    if kpts.size == 0 or desc.size == 0:
        raise PYGenshinException("Failed loading descriptors")

    try:
        keypoints = [cv2.KeyPoint(x, y, _size, _angle, _response, int(_octave), int(_class_id))
                     for x, y, _size, _angle, _response, _octave, _class_id in list(kpts)]
        FULL_MAP_INFO = (keypoints, numpy.array(desc))
    except(IndexError):
        raise PYGenshinException("Failed loading descriptors")


def GetMyLocationOnFullMap(screenshot) -> Vector2:
    global CAN_USE_MINIMAP
    global RESIZED_MAP_POSITION
    global RESIZED_MAP

    ZoomIn()

    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    rect = None
    rect = opencvUtils.FeatureMatch(
        FULL_MAP_IMAGE, screenshot, 0.7, FULL_MAP_INFO
    )

    CAN_USE_MINIMAP = True
    RESIZED_MAP_POSITION = round(rect)
    RESIZED_MAP = opencvUtils.CropImage(FULL_MAP_IMAGE, rect)
    # self.CurrentPosition = round(rect.center)
    return round(rect.center)


def CanScreenMinimap():
    return CAN_USE_MINIMAP


def GetMyLocationOnMinimap(screenshot):
    global RESIZED_MAP
    global RESIZED_MAP_POSITION

    if (not CanScreenMinimap()):
        return

    minimap = opencvUtils.CropImage(
        screenshot,
        pgScreens.GameScreen.Buttons.MiniMap.position.toPixels(
            pgWindow.GetGenshinImpactWindowRect().GetDimensions()
        )
    )

    minimap_h = opencvUtils.ImageSize(minimap).y

    rect = opencvUtils.FeatureMatch(
        RESIZED_MAP, cv2.cvtColor(minimap, cv2.COLOR_RGB2GRAY)
    )
    CurrentPosition = RESIZED_MAP_POSITION.start + rect.center

    distanceToBounds = pgMath.MinPointDistanceToBounds(
        CurrentPosition, rect
    )
    # its a square so we can check only height
    if (distanceToBounds < minimap_h*2):
        dims = pgWindow.GetGenshinImpactWindowRect().GetDimensions()
        resize_rect = Rect(
            Vector2(CurrentPosition.x - dims.x / 2,
                    CurrentPosition.y - dims.y / 2),
            Vector2(CurrentPosition.x + dims.x / 2,
                    CurrentPosition.y + dims.y / 2)
        )
        RESIZED_MAP = opencvUtils.CropImage(FULL_MAP_IMAGE, resize_rect)
        RESIZED_MAP_POSITION = resize_rect
        print("Cropping")

    return CurrentPosition


def main():
    global DOMAIN_MARKER_IMAGE
    global TELEPORT_MARKER_IMAGE
    global FULL_MAP_IMAGE

    DOMAIN_MARKER_IMAGE = cv2.imread(
        pgSettings.GetDataFolder() + "images/map/location/domainMarker.png", cv2.IMREAD_GRAYSCALE
    )
    TELEPORT_MARKER_IMAGE = cv2.imread(
        pgSettings.GetDataFolder() + "images/map/location/teleportMarker.png", cv2.IMREAD_GRAYSCALE
    )
    FULL_MAP_IMAGE = cv2.imread(
        pgSettings.GetDataFolder() + "images/map/full_cropped.jpg", cv2.IMREAD_GRAYSCALE
    )

    LoadMapDescriptors(
        pgSettings.GetDataFolder() + "computed/map_computed_kpts.npy",
        pgSettings.GetDataFolder() + "computed/map_computed_desc.npy"
    )


main()
