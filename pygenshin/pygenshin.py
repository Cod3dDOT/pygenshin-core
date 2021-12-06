from pygenshin.modules import detection as pgDetectionModule
from pygenshin.modules import inputs as pgInputsModule
from pygenshin.modules import map as pgMapModule
from pygenshin.modules import settings as pgSettingsModule
from pygenshin.modules import window as pgWindowModule
from pygenshin.modules import gamescreens as pgGamescreens

import os
import time
import cv2

from pygenshin.modules.additional_types import PYGenshinException
from pygenshin.modules.detection import opencvUtils

import logging

Instance = None


class PYGenshin:
    INPUTS: pgInputsModule.Inputs = None
    SETTINGS: pgSettingsModule.Settings = None
    DETECTION: pgDetectionModule.Detection = None
    GAMEWINDOW: pgWindowModule.GenshinWindow = None
    MAPITEMS: pgMapModule.MapItems = None
    MAPLOCATION: pgMapModule.MapLocation = None

    LOGGER = None

    INITIALIZED_RECORDING = False

    def __init__(self) -> None:
        self.SETTINGS = pgSettingsModule.Settings()

        path, filename = os.path.split(os.path.realpath(__file__))
        path = path.replace("\\", "/")
        self.SETTINGS.DataFolder = path + "/data/"

        self.MAPITEMS = pgMapModule.MapItems(self.SETTINGS.DataFolder)

        logging.basicConfig(level=logging.DEBUG)
        self.LOGGER = logging.getLogger(__name__)

    def InitializeRecording(detection_mode: str = "mss"):
        if ((detection_mode and not isinstance(detection_mode, str)) or (detection_mode and detection_mode not in ["d3dshot", "mss"])):
            raise PYGenshinException("Incorrect Detection Mode")
        mode = pgDetectionModule.DETECTION_MODE.D3DSHOT if(
            detection_mode == "d3dshot") else pgDetectionModule.DETECTION_MODE.MSS

        Instance.GAMEWINDOW = pgWindowModule.GenshinWindow()
        if (not Instance.GAMEWINDOW.IsGenshinRunning()):
            raise PYGenshinException("Genshin Impact is not running")
        Instance.GAMEWINDOW.BringToForeground()

        Instance.SETTINGS.WindowRect = Instance.GAMEWINDOW.GetWindowRect()
        Instance.SETTINGS.MapScreenshotRect = Instance.GAMEWINDOW.GetWindowRect()

        Instance.INPUTS = pgInputsModule.Inputs(
            Instance.GAMEWINDOW.GetWindowRect())

        Instance.DETECTION = pgDetectionModule.Detection(mode)
        Instance.DETECTION.SetResolution(Instance.SETTINGS.WindowRect)
        print(Instance.GAMEWINDOW.GetWindowRect().GetDimensions())

        Instance.MAPLOCATION = pgMapModule.MapLocation(
            Instance.SETTINGS.DataFolder, Instance.GAMEWINDOW.GetWindowRect(), Instance.INPUTS)

        Instance.INITIALIZED_RECORDING = True

    def StartRecording():
        if (not Instance.INITIALIZED_RECORDING):
            return
        Instance.DETECTION.StartRecording()
        time.sleep(1)

    def StopRecording():
        if (not Instance.INITIALIZED_RECORDING):
            return
        Instance.DETECTION.StopRecording()

    def SaveScreenshot():
        if (not Instance.INITIALIZED_RECORDING):
            return
        cv2.imwrite("test.png", Instance.DETECTION.GetLastFrame())

    class Location:
        def GetMyLocation():
            if (not Instance.INITIALIZED_RECORDING):
                return
            Instance.INPUTS.PressUIButton(
                pgGamescreens.GameScreen.Buttons.MiniMap)
            time.sleep(1)
            frame = Instance.DETECTION.GetLastFrame()
            if (Instance.MAPLOCATION.ResizedMap):
                # frame = opencvUtils.cropImage(frame, pgGamescreens.MapScreen.)
                return Instance.MAPLOCATION.GetMyLocationOnMinimap()
            else:
                return Instance.MAPLOCATION.GetMyLocationOnFullMap(frame)

    class Logger:
        def logException(exception: PYGenshinException):
            Instance.LOGGER.exception(exception)


def CreatePyGenshin():
    global Instance
    Instance = PYGenshin()
