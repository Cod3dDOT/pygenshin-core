from pygenshin.modules.additional_types import PYGenshinException, Vector2, Rect
import math


def IsPointInsideBounds(point: Vector2, bounds: Rect) -> bool:
    return not (point.x < bounds.start.x or
                point.x > bounds.end.x or
                point.y < bounds.start.y or
                point.y > bounds.end.y)


def DistanceBetweenPoints(start: Vector2, end: Vector2) -> float:
    return math.sqrt((end.x-start.x)**2 + (end.y-start.y)**2)


def IsRectInsideBounds(rect: Rect, bounds: Rect) -> bool:
    raise NotImplementedError()


def MinPointDistanceToBounds(point: Vector2, bounds: Rect) -> float:
    distTop = abs(point.y - bounds.start.y)
    distBottom = abs(point.y - bounds.end.y)
    distLeft = abs(point.x - bounds.start.x)
    distRight = abs(point.y - bounds.end.x)
    return min([distTop, distBottom, distLeft, distRight])


def ClosestBoundsAxis(point: Vector2, bounds: Rect):
    distTop = abs(point.y - bounds.start.y)
    distBottom = abs(point.y - bounds.end.y)
    distLeft = abs(point.x - bounds.start.x)
    distRight = abs(point.y - bounds.end.x)
    min_dist = min([distTop, distBottom, distLeft, distRight])
    if min_dist == distTop or min_dist == distBottom:
        return "y"
    if min_dist == distLeft or min_dist == distRight:
        return "x"
    raise PYGenshinException("Error on ClosestBoundsAxis()")


def MinRectDistanceToBounds(rect: Rect, bounds: Rect) -> float:
    distLeftDown = MinPointDistanceToBounds(rect.start, bounds)
    distRightUp = MinPointDistanceToBounds(rect.end, bounds)
    distLeftUp = MinPointDistanceToBounds(
        Vector2(rect.start.x, rect.end.y), bounds
    )
    distRightDown = MinPointDistanceToBounds(
        Vector2(rect.end.x, rect.start.y), bounds
    )
    return min([distLeftDown, distLeftUp, distRightUp, distRightDown])


def DivideLineSegmentByCount(start: Vector2, end: Vector2, segments: int) -> list[Vector2]:
    x_delta = (end.x - start.x) / float(segments)
    y_delta = (end.y - start.y) / float(segments)
    points = []
    for i in range(1, segments):
        points.append(Vector2(start.x + i * x_delta, start.y + i * y_delta))
    return [start] + points + [end]


def DivideLineSegmentByLength(start: Vector2, end: Vector2, length: float) -> list[Vector2]:
    delta = math.sqrt(length**length / 2)

    segments = math.floor(DistanceBetweenPoints(start, end) / length)

    points = []
    for i in range(1, segments - 1):
        points.append(
            Vector2(start.x + i * delta, start.y + i * delta)
        )
    return [start] + points + [end]


class Line:
    A: float = None
    B: float = None
    C: float = None

    def __init__(self, start: Vector2, direction: Vector2) -> None:
        self.A = (start.y - direction.y)
        self.B = (direction.x - start.x)
        self.C = -(start.x*direction.y - direction.x*start.y)

    def AsTuple(self):
        return self.A, self.B, self.C


def LineIntersection(line1: Line, line2: Line):
    D = line1.A * line2.B - line1.B * line2.A
    Dx = line1.C * line2.B - line1.B * line2.C
    Dy = line1.A * line2.C - line1.C * line2.A
    if D != 0:
        x = Dx / D
        y = Dy / D
        return Vector2(x, y)
