import json

class MapItems:
    data = None

    def __init__(self, datafolder) -> None:
        with open(datafolder + "json/map/items/map_data.json") as file:
            self.data = json.load(file)

    def GetCategory(self, category:str):
        return self.data[category]
    
    def GetItems(self, category:str, name:str):
        return self.data[category][name]

    def GetTeleportByName(self, name:str):
        items = [t for t in self.data["Waypoints"]["Teleport"] if t["content"] == name]
        if (len(items) > 0): return items[0]

    def GetDomainByName(self, name:str):
        items = [t for t in self.data["Waypoints"]["Domain"] if t["content"] == name]
        if (len(items) > 0): return items[0]