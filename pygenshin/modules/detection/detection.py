import mss
import numpy
import threading
import d3dshot
from enum import Enum
import cv2
import time

from pygenshin.modules.additional_types import PYGenshinException, Rect


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    Stopped = False

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pause(self):
        self.Stopped = True

    def paused(self):
        return self.Stopped


class mssDetection:
    resolution = None
    mss = None
    thread = None
    lastFrame = None
    isRecording: bool = False

    def CreateMss(self):
        self.mss = mss.mss()
        self.thread = StoppableThread(target=self._takeScreenshots)
        self.thread.daemon = True

    def SetResolution(self, res):
        self.resolution = res

    def StartRecording(self):
        if (not self.resolution):
            raise PYGenshinException("mssDetection: Resolution is not set")
        self.thread.start()
        self.isRecording = True

    def _takeScreenshots(self):
        while (not self.thread.paused()):
            self.lastFrame = numpy.array(self.mss.grab(self.resolution))

    def StopRecording(self):
        if (not self.thread.paused()):
            self.thread.pause()
            self.thread.join()
            self.thread = StoppableThread(target=self._takeScreenshots)
            self.thread.daemon = True
            self.isRecording = False

    def GetLastFrame(self):
        return self.lastFrame

    def IsRecording(self):
        return self.isRecording


class d3dshotDetection:
    d3dshot = None
    resolution = None

    def CreateD3DShot(self):
        self.d3dshot = d3dshot.create(capture_output="numpy")

    def SetResolution(self, res):
        self.resolution = res

    def StartRecording(self):
        if (not self.resolution):
            raise PYGenshinException("D3DShotDetection: Resolution is not set")
        self.d3dshot.capture(region=self.resolution)

    def StopRecording(self):
        self.d3dshot.stop()

    def GetLastFrame(self):
        return cv2.cvtColor(self.d3dshot.get_latest_frame(), cv2.COLOR_BGR2RGB)

    def IsRecording(self):
        return self.d3dshot.is_capturing()


class DETECTION_MODE(Enum):
    MSS = "mss"
    D3DSHOT = "d3dshot"


Mode: DETECTION_MODE = None
Mss: mssDetection = None
D3DShot: d3dshotDetection = None


def CreateScreenGrabber(mode: DETECTION_MODE = DETECTION_MODE.MSS) -> None:
    global Mode
    global Mss
    global D3DShot

    if (not isinstance(mode, DETECTION_MODE)):
        raise PYGenshinException("Incorrect Detection Mode")

    Mode = mode

    if (mode == DETECTION_MODE.MSS):
        Mss = mssDetection()
        Mss.CreateMss()

    if (mode == DETECTION_MODE.D3DSHOT):
        D3DShot = d3dshotDetection()
        D3DShot.CreateD3DShot()


def SetResolution(resolution: Rect):
    if (Mode == DETECTION_MODE.MSS):
        return Mss.SetResolution(resolution.asMss())

    if (Mode == DETECTION_MODE.D3DSHOT):
        return D3DShot.SetResolution(resolution.asTuple())


def StartRecording():
    if (Mode == DETECTION_MODE.MSS):
        return Mss.StartRecording()

    if (Mode == DETECTION_MODE.D3DSHOT):
        return D3DShot.StartRecording()

    time.sleep(1)


def StopRecording():
    if (Mode == DETECTION_MODE.MSS):
        return Mss.StopRecording()

    if (Mode == DETECTION_MODE.D3DSHOT):
        return D3DShot.StopRecording()


def IsRecording():
    if (Mode == DETECTION_MODE.MSS):
        return Mss.IsRecording()

    if (Mode == DETECTION_MODE.D3DSHOT):
        return D3DShot.IsRecording()


def GetLastFrame():
    if (Mode == DETECTION_MODE.MSS):
        return Mss.GetLastFrame()

    if (Mode == DETECTION_MODE.D3DSHOT):
        return D3DShot.GetLastFrame()
