from enum import Enum
from .additional_types import Rect, Vector2
from pygenshin.modules.inputs.keybindings import KEYBINDINGS, KEY

class GAMESCREEN(Enum):
    GAME = 0

    GAME_PAIMON_OVERLAY = 1

    SHOP                = 5
    PARTY_SETUP         = 6
    FRIENDS             = 7
    ACHIEVEMENTS        = 8
    ARCHIVE             = 9
    CHARACTER_ARCHIVE   = 10
    CHARACTER           = 11
    INVENTORY           = 12
    QUESTS              = 13
    MAP                 = 14
    EVENTS              = 15
    AVENTURER_HANDBOOK  = 16
    WISH                = 17
    COOP_MODE           = 18
    SPECIAL_EVENT       = 19
    COMMUNITY           = 20
    FEEDBACK            = 21
    SURVEY              = 22

    PHOTO               = 30
    NOTICES             = 31
    MAIL                = 32
    TIME                = 33
    SETTINGS            = 34

    PROFILE             = 40
    CHANGE_AVATAR       = 41
    CHANGE_NAMECARD     = 42
    EDIT_NICKNAME       = 43
    EDIT_SIGNATURE      = 44

class UIButton:
    def __init__(self, position:Rect, leadsToMenu:GAMESCREEN = None, keybind:KEY = None) -> None:
        self.position    = position
        self.leadsToMenu = leadsToMenu
        self.keybind     = keybind

class GameScreen:
    class Buttons:
        PaimonOverlay   = UIButton(Rect(Vector2(0.01171875, 0.00694444), Vector2(0.05156250, 0.08680555)), GAMESCREEN.GAME_PAIMON_OVERLAY)
        SuperVision     = UIButton(Rect(Vector2(0.12890625, 0.01388888), Vector2(0.16015625, 0.06944444)), GAMESCREEN.GAME)
        Shop            = UIButton(Rect(Vector2(0.17656250, 0.01736111), Vector2(0.20390625, 0.06597222)), GAMESCREEN.SHOP)
        Quests          = UIButton(Rect(Vector2(0.01757812, 0.15972222), Vector2(0.04687500, 0.21527777)), GAMESCREEN.QUESTS)

        Compass         = UIButton(Rect(Vector2(0.75781250, 0.00694444), Vector2(0.79296875, 0.07638888)), GAMESCREEN.MAP) # CHECK
        Wish            = UIButton(Rect(Vector2(0.80273437, 0.00694444), Vector2(0.83789062, 0.07638888)), GAMESCREEN.WISH)
        Book            = UIButton(Rect(Vector2(0.84765625, 0.00694444), Vector2(0.89062500, 0.07638888)), GAMESCREEN.INVENTORY) # CHECK
        Bag             = UIButton(Rect(Vector2(0.89648437, 0.00694444), Vector2(0.93359375, 0.07638888)), GAMESCREEN.INVENTORY)
        Character       = UIButton(Rect(Vector2(0.94726562, 0.01388888), Vector2(0.97851562, 0.07291666)), GAMESCREEN.CHARACTER)

        MiniMap         = UIButton(Rect(Vector2(0.04882812, 0.04513888), Vector2(0.12695312, 0.19097222)), GAMESCREEN.MAP, KEY.M)

class MapScreen:
    class Buttons:
        ZoomMinus       = UIButton(Rect(Vector2(0.00519210, 0.59314179), Vector2(0.01817237, 0.616311399)))
        ZoomPlus        = UIButton(Rect(Vector2(0.00519210, 0.38461538), Vector2(0.01817237, 0.407784986)))
