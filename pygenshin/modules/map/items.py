import json
import numpy
from pygenshin.modules.additional_types import PYGenshinException, Vector2
import pygenshin.modules.settings as pgSettings

JSON_DATA: dict = None
with open(pgSettings.GetDataFolder() + "json/map/items/map_data.json") as file:
    JSON_DATA = json.load(file)


class MapItem:
    Category: str = None
    Type: str = None
    Position: Vector2 = None

    def __init__(self, category, type, position) -> None:
        self.Category = category
        self.Type = type
        self.Position = position

    @classmethod
    def FromJson(cls, category, type, jsonDict):
        return cls(category, type, Vector2(jsonDict["x"], jsonDict["y"]))

    def __str__(self) -> str:
        return f"MapItem('{self.Category}', '{self.Type}', {self.Position})"


def GetCategory(category: str):
    return JSON_DATA["points"][category]


def GetItemsOfType(category: str, type: str):
    return JSON_DATA["points"][category][type]


def GetDomainByName(name: str):
    items = [t for t in JSON_DATA["points"]["Waypoints"]
             ["Domain"] if t["content"] == name]
    if (len(items) > 0):
        return items[0]


def GetClosestItemOfType(position: Vector2, category: str, type: str):
    points = GetItemsOfType(category, type)
    nodes = numpy.asarray([[p["x"], p["y"]] for p in points])
    dist_2 = numpy.sum((nodes - position.asTuple())**2, axis=1)
    position = Vector2.fromTuple(nodes[numpy.argmin(dist_2)])
    itemJson = [item for item in GetItemsOfType(category, type) if (
        item["x"], item["y"]) == position.asTuple()][0]
    return MapItem.FromJson(category, type, itemJson)
