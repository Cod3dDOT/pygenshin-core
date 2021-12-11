import pygenshin


def main():
    pygenshin.InitializeRecording()

    pygenshin.StartRecording()

    playerLocation = pygenshin.Map.Location.GetMyLocation()
    item = pygenshin.Map.Items.GetClosestItemOfType(
        playerLocation, "Waypoints:Teleport Waypoint")
    print(item)
    pygenshin.Map.Navigation.TeleportToItemOnMap(playerLocation, item)

    pygenshin.StopRecording()


if __name__ == "__main__":
    main()
