import mss
import numpy
import threading
import d3dshot
from enum import Enum
import cv2

from pygenshin.modules.additional_types import PYGenshinException, Rect

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class mssDetection:
    resolution = None
    mss = None
    thread = None
    lastFrame = None

    def CreateMss(self):
        self.mss = mss.mss()
        self.thread = StoppableThread(target=self._takeScreenshots)

    def SetResolution(self, res):
        self.resolution = res

    def StartRecording(self):
        if (not self.resolution): raise PYGenshinException("mssDetection: Resolution is not set")
        self.thread.start()

    def _takeScreenshots(self):
        while (not self.thread.stopped()):
            self.lastFrame = numpy.array(self.mss.grab(self.resolution))

    def StopRecording(self):
        if (not self.thread.stopped()):
            self.thread.stop()

    def GetLastFrame(self):
        return self.lastFrame

class d3dshotDetection:
    d3dshot = None
    resolution = None

    def CreateD3DShot(self):
        self.d3dshot = d3dshot.create(capture_output="numpy")

    def SetResolution(self, res):
        self.resolution = res

    def StartRecording(self):
        if (not self.resolution): raise PYGenshinException("D3DShotDetection: Resolution is not set")
        self.d3dshot.capture(region = self.resolution)
        

    def StopRecording(self):
        self.d3dshot.stop()

    def GetLastFrame(self):
        return cv2.cvtColor(self.d3dshot.get_latest_frame(), cv2.COLOR_BGR2RGB)

class DETECTION_MODE(Enum):
    D3DSHOT = 0
    MSS     = 1

class Detection:
    Mode = None

    Mss = None
    D3DShot = None

    def __init__(self, mode:DETECTION_MODE = DETECTION_MODE.D3DSHOT) -> None:
        if (not isinstance(mode, DETECTION_MODE)): raise PYGenshinException("Incorrect Detection Mode")
        self.Mode = mode
        
        if (mode == DETECTION_MODE.MSS):
            self.mss = mssDetection()
            self.mss.CreateMss()

        if (mode == DETECTION_MODE.D3DSHOT):
            self.D3DShot = d3dshotDetection()
            self.D3DShot.CreateD3DShot()
            
    def SetResolution(self, resolution:Rect):
        if (self.Mode == DETECTION_MODE.MSS):
            return self.mss.SetResolution(resolution.asMss())

        if (self.Mode == DETECTION_MODE.D3DSHOT):
            return self.D3DShot.SetResolution(resolution.asTuple())

    def StartRecording(self):
        if (self.Mode == DETECTION_MODE.MSS):
            return self.mss.StartRecording()

        if (self.Mode == DETECTION_MODE.D3DSHOT):
            return self.D3DShot.StartRecording()

    def StopRecording(self):
        if (self.Mode == DETECTION_MODE.MSS):
            return self.mss.StopRecording()

        if (self.Mode == DETECTION_MODE.D3DSHOT):
            return self.D3DShot.StopRecording()

    def GetLastFrame(self):
        if (self.Mode == DETECTION_MODE.MSS):
            return self.mss.GetLastFrame()

        if (self.Mode == DETECTION_MODE.D3DSHOT):
            return self.D3DShot.GetLastFrame()