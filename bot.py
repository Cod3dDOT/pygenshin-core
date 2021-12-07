from pygenshin.pygenshin import PYGenshin, CreatePyGenshin

import time


def main():
    try:
        CreatePyGenshin()

        PYGenshin.InitializeRecording()

        PYGenshin.StartRecording()

        # First time gets location by opening map (long)
        t1 = time.perf_counter()
        loc = PYGenshin.Location.GetMyLocation()
        t2 = time.perf_counter()
        print("Full map. Location: {}. Took: {}.".format(loc, t2 - t1))

        # Gets location with minimap (must be efficient)
        loc = PYGenshin.Location.GetMyLocation()
        t1 = time.perf_counter()
        print("Minimap. Location: {}. Took: {}.".format(loc, t1 - t2))

        # Gets location with minimap (must be efficient)
        loc = PYGenshin.Location.GetMyLocation()
        t2 = time.perf_counter()
        print("Minimap x2. Location: {}. Took: {}.".format(loc, t2 - t1))

        PYGenshin.StopRecording()
    except Exception as e:
        PYGenshin.Logger.logException(e)
        PYGenshin.StopRecording()


if __name__ == "__main__":
    main()
