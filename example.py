import pygenshin


def main():
    pygenshin.InitializeRecording()

    pygenshin.StartRecording()

    playerLocation = pygenshin.Location.GetMyLocation()
    item = pygenshin.MapItems.GetClosestItemOfType(
        playerLocation, "Waypoints:Teleport Waypoint")
    print(item)
    pygenshin.Navigation.TeleportToItemOnMap(playerLocation, item)

    pygenshin.StopRecording()


if __name__ == "__main__":
    main()
