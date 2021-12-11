from pygenshin.modules.additional_types import PYGenshinException, Rect, Vector2
from pygenshin.modules.map.items import MapItem
import pygenshin.modules.window as pgWindow
import pygenshin.modules.math as pgMath

# WRONG, WRONG WRONG WRONG
# you need to calculate the line using player coordinates
# then translate EITHER the line and calculate the point of intersection


def TeleportToTeleport(teleport: MapItem):
    windowRect = pgWindow.GetGenshinImpactWindowRect()
    posDragStart = windowRect.center

    xPoint = pgMath.LineIntersection(
        pgMath.Line(posDragStart, teleport.Position),
        pgMath.Line(windowRect.start, Vector2(
            windowRect.start.x, windowRect.end.y))
    )
    yPoint = pgMath.LineIntersection(
        pgMath.Line(posDragStart, teleport.Position),
        pgMath.Line(windowRect.end, Vector2(
            windowRect.start.x, windowRect.end.y)
        )
    )

    posDragEnd = min([
        pgMath.DistanceBetweenPoints(posDragStart, xPoint),
        pgMath.DistanceBetweenPoints(posDragStart, yPoint)
    ])

    print(posDragEnd)

    # Instance.INPUTS.DragMouse(posDragStart, point, 2)
