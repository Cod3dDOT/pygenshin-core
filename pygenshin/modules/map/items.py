import json
import numpy
from pygenshin.modules.additional_types import Vector2


class MapItems:
    data = None

    def __init__(self, datafolder) -> None:
        with open(datafolder + "json/map/items/map_data.json") as file:
            self.data = json.load(file)

    def GetCategory(self, category: str):
        return self.data["points"][category]

    def GetItemsOfType(self, category: str, type: str):
        return self.data["points"][category][type]

    def GetDomainByName(self, name: str):
        items = [t for t in self.data["points"]["Waypoints"]
                 ["Domain"] if t["content"] == name]
        if (len(items) > 0):
            return items[0]

    def GetClosestItemOfType(self, position: Vector2, category: str, type: str):
        position = self.GetClosestItemPositionOfType(position, category, type)
        return [item for item in self.GetItemsOfType(category, type) if (item["x"], item["y"]) == position.asTuple()][0]

    def GetClosestItemPositionOfType(self, position: Vector2, category: str, type: str):
        points = self.GetItemsOfType(category, type)
        nodes = numpy.asarray([[p["x"], p["y"]] for p in points])
        dist_2 = numpy.sum((nodes - position.asTuple())**2, axis=1)
        return Vector2.fromTuple(nodes[numpy.argmin(dist_2)])
