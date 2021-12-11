from pygenshin.modules import detection as pgDetection
from pygenshin.modules import inputs as pgInputs
from pygenshin.modules import map as pgMap
from pygenshin.modules import settings as pgSettings
from pygenshin.modules import window as pgWindow
from pygenshin.modules import gamescreens as pgGamescreens
from pygenshin.modules import math as pgMath

import time
import cv2

from pygenshin.modules.additional_types import PYGenshinException, Vector2


INITIALIZED_RECORDING: bool = False


def InitializeRecording(detection_mode: str = "mss"):
    global INITIALIZED_RECORDING

    if (
        detection_mode and not isinstance(detection_mode, str) or
        detection_mode and detection_mode not in ["d3dshot", "mss"]
    ):
        raise PYGenshinException("Incorrect Detection Mode")

    mode = pgDetection.DETECTION_MODE.D3DSHOT \
        if (detection_mode == "d3dshot") \
        else pgDetection.DETECTION_MODE.MSS

    if (not pgWindow.IsGenshinImpactRunning()):
        raise PYGenshinException("Genshin Impact is not running")

    pgWindow.BringGenshinImpactToFront()

    pgDetection.CreateScreenGrabber(mode)

    pgDetection.SetResolution(
        pgWindow.GetGenshinImpactWindowRect()
    )

    INITIALIZED_RECORDING = True


def StartRecording():
    '''Starts background recording of game window.
    Is required by almost any function.\n
    Make sure you have called InitializeRecording() before.'''

    if (not INITIALIZED_RECORDING):
        raise PYGenshinException(
            "Please call InitializeRecording() BEFORE any StartRecording() calls"
        )
    pgDetection.StartRecording()


def StopRecording():
    '''Stops background recording of game window.\n
    Make sure you have called InitializeRecording() before.'''

    if (not INITIALIZED_RECORDING):
        raise PYGenshinException(
            "Please call InitializeRecording() BEFORE any StopRecording() calls"
        )

    if (IsRecording()):
        pgDetection.StopRecording()


def IsGenshinImpactRunning():
    return pgWindow.IsGenshinImpactRunning()


def IsRecording():
    return INITIALIZED_RECORDING and pgDetection.IsRecording()


def SaveScreenshot():
    if (not INITIALIZED_RECORDING):
        raise PYGenshinException(
            "Please call InitializeRecording() BEFORE any SaveScreenshot() calls"
        )
    cv2.imwrite("test.png", pgDetection.GetLastFrame())


class Location:
    def CanUseMinimapForLocation():
        '''Check if you can use GetMyLocationWithMinimap().\n
        Returns True if you have used GetMyLocationWithFullMap() atleast once.'''

        return pgMap.location.CanScreenMinimap()

    def GetMyLocationWithFullMap():
        '''Slower, more accurate. Opens full map. (Total time: 5 seconds.)'''

        if (not INITIALIZED_RECORDING):
            raise PYGenshinException(
                "Please call InitializeRecording() BEFORE any GetMyLocationWithFullMap() calls"
            )

        pgInputs.PressUIButton(
            pgGamescreens.GameScreen.Buttons.MiniMap
        )
        time.sleep(1)
        frame = pgDetection.GetLastFrame()

        StopRecording()

        location = pgMap.location.GetMyLocationOnFullMap(frame)
        pgInputs.TapKey(pgInputs.KEY.ESCAPE)

        StartRecording()
        return location

    def GetMyLocationWithMinimap():
        '''Fast, less accurate. (Total time: 0.15 seconds). Can only be used if you called GetMyLocationWithFullMap() before.'''

        if (not INITIALIZED_RECORDING):
            raise PYGenshinException(
                "Please call InitializeRecording() BEFORE any GetMyLocationWithMinimap() calls"
            )

        if (not Location.CanUseMinimapForLocation()):
            raise PYGenshinException(
                "Can't get location with minmap: make sure you have called \
                GetMyLocationWithFullMap() before and CanUseMinimapForLocation() returns True"
            )
        frame = pgDetection.GetLastFrame()
        return pgMap.location.GetMyLocationOnMinimap(frame)

    def GetMyLocation():
        '''General function to get player location.
        Will automatically decide whether to use GetMyLocationWithFullMap() or GetMyLocationWithMinimap()'''

        if (Location.CanUseMinimapForLocation()):
            return Location.GetMyLocationWithMinimap()
        else:
            return Location.GetMyLocationWithFullMap()


class MapItems:
    def GetClosestItemOfType(position: Vector2, type: str):
        '''Gets closest item on map of type.\nType must be string separated by ':' \n Example: 'Waypoints:Teleport Waypoints\''''
        if (not isinstance(position, Vector2)):
            raise PYGenshinException(
                "position needs to be of type Vector2"
            )
        if (not isinstance(type, str) or not ":" in type or not len(type.split(":")) == 2):
            raise PYGenshinException(
                "type needs to be 'category:type'\n \
                Example: 'Waypoints:Teleport Waypoints'"
            )
        category, type = type.split(":")
        return pgMap.items.GetClosestItemOfType(position, category, type)


class Navigation:
    def TeleportToItemOnMap(playerPosition: Vector2, item: pgMap.MapItem):
        if (not INITIALIZED_RECORDING):
            raise PYGenshinException(
                "Please call InitializeRecording() BEFORE any TeleportToItemOnMap() calls"
            )
        teleport = MapItems.GetClosestItemOfType(
            item.Position, "Waypoints:Teleport Waypoint"
        )
        if (
            pgMath.DistanceBetweenPoints(teleport.Position, playerPosition) >
            pgMath.DistanceBetweenPoints(teleport.Position, item.Position)
        ):
            pgMap.navigation.TeleportToTeleport(teleport)
        else:
            print("Its faster to go by foot")
