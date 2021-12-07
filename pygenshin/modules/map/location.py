import cv2
import pygenshin.modules.inputs as pgInputs
import pygenshin.modules.detection.opencvUtils as opencvUtils
from pygenshin.modules.additional_types import Rect, Vector2
import pygenshin.modules.gamescreens as pgScreens
import time


class MapLocation:
    Inputs: pgInputs.Inputs = None

    DomainMarker = None
    TeleportMarker = None
    FullMap = None

    WindowRect: Rect = None

    ResizedMapIsSet = False
    ResizedMap = None
    ResizedMapPosition: Rect = None

    CurrentPosition: Vector2 = None

    def __init__(self, datafolder, windowrect: Rect, inputs: pgInputs.Inputs) -> None:
        self.DomainMarker = cv2.imread(
            datafolder + "images/map/location/domainMarker.png", cv2.IMREAD_GRAYSCALE)
        self.TeleportMarker = cv2.imread(
            datafolder + "images/map/location/teleportMarker.png", cv2.IMREAD_GRAYSCALE)
        self.FullMap = cv2.imread(
            datafolder + "images/map/full_cropped.jpg", cv2.IMREAD_GRAYSCALE)

        self.WindowRect = windowrect
        self.Inputs = inputs

    def ZoomIn(self):
        self.Inputs.SetMousePos(pgScreens.MapScreen.Buttons.ZoomPlus.position.center.toPixels(
            self.WindowRect.GetDimensions().asTuple()))
        for _ in range(5):
            self.Inputs.ClickMouse()
            time.sleep(0.1)

    def GetMyLocationOnFullMap(self, screenshot) -> Vector2:
        self.ZoomIn()
        rect = opencvUtils.featureMatching(
            self.FullMap, cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY))
        rect = Rect.fromTuples(rect[0], rect[1])

        self.ResizedMapIsSet = True
        self.ResizedMapPosition = round(rect)
        self.ResizedMap = opencvUtils.cropImage(self.FullMap, rect)
        self.CurrentPosition = round(rect.center)
        return self.CurrentPosition

        # domain, teleport = opencvUtils.bestMatches(
        #     screenshot, [self.DomainMarker, self.TeleportMarker])

        # if (domain):
        #     inputs.SetMousePos(Vector2.fromTuple(domain))
        # if (teleport):
        #     inputs.SetMousePos(Vector2.fromTuple(teleport))

    def CanScreenMinimap(self):
        return self.ResizedMapIsSet

    def GetMyLocationOnMinimap(self, minimap):
        if (not self.CanScreenMinimap()):
            return

        minimap = opencvUtils.cropImage(
            minimap,
            pgScreens.GameScreen.Buttons.MiniMap.position.toPixels(
                self.WindowRect.GetDimensions()
            )
        )

        rect = opencvUtils.featureMatching(
            self.ResizedMap, cv2.cvtColor(minimap, cv2.COLOR_RGB2GRAY))
        rect = round(Rect.fromTuples(rect[0], rect[1]))
        self.CurrentPosition = self.ResizedMapPosition.start + rect.center
        #                                                       pgScreens.GameScreen.rect):
        if (self.DistanceToBounds(self.CurrentPosition, rect) < 100):
            dims = self.WindowRect.GetDimensions()
            resize_rect = Rect(
                Vector2(self.CurrentPosition.x - dims.x / 2,
                        self.CurrentPosition.y - dims.y / 2),
                Vector2(self.CurrentPosition.x + dims.x / 2,
                        self.CurrentPosition.y + dims.y / 2))
            self.ResizedMap = opencvUtils.cropImage(self.FullMap, resize_rect)

        return self.CurrentPosition

    def ConvertScreenLocationToMap(self, location: Vector2):
        return location / Vector2(self.X_SCALE, self.Y_SCALE)

    def DistanceToBounds(self, point: Vector2, bounds: Rect):
        distTop = abs(point.y - bounds.start.y)
        distBottom = abs(point.y - bounds.end.y)
        distLeft = abs(point.x - bounds.start.x)
        distRight = abs(point.y - bounds.end.x)
        return min([distTop, distBottom, distLeft, distRight])
