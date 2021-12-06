import cv2
import pygenshin.modules.inputs as pgInputs
import pygenshin.modules.detection.opencvUtils as opencvUtils
from   pygenshin.modules.additional_types import Rect, Vector2
import pygenshin.modules.low_level.gamescreens as pgScreens

class MapLocation:
    X_SCALE = 0.44392523364
    Y_SCALE = 21.7047817048
    DomainMarker = None
    TeleportMarker = None

    def __init__(self, datafolder) -> None:
        self.DomainMarker = cv2.imread(datafolder + "images/map/location/domainMarker.png")
        self.TeleportMarker = cv2.imread(datafolder + "images/map/location/teleportMarker.png")

    def ZoomOut(self, resolution:Vector2, inputs:pgInputs.Inputs):
        inputs.SetMousePos(pgScreens.MapScreen.Buttons.ZoomPlus.position.center.toPixels(resolution.asTuple()))
        for i in range(5):
            inputs.ClickMouse()

    def GetMyLocation(self, inputs, screenshot, windowrect):
        self.ZoomOut(windowrect.GetDimensions(), inputs)
        domain, teleport = opencvUtils.bestMatches(screenshot, [self.DomainMarker, self.TeleportMarker])

        if (domain): inputs.SetMousePos(Vector2.fromTuple(domain))
        if (teleport): inputs.SetMousePos(Vector2.fromTuple(teleport))

    def ConvertScreenLocationToMap(self, location:Vector2):
        return location / Vector2(self.X_SCALE, self.Y_SCALE)