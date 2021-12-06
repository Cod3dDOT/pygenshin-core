class Vector2:
    x: float = 0
    y: float = 0
    tuple = ()

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y
        self.tuple = (x, y)

    @classmethod
    def fromTuple(cls, coords):
        return cls(coords[0], coords[1])

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            if (other.x == 0):
                raise ValueError("x: Can not divide by 0")
            if (other.y == 0):
                raise ValueError("y: Can not divide by 0")
            return Vector2(self.x / other.x, self.y / other.x)

        if isinstance(other, int) or isinstance(other, float):
            if (other == 0):
                raise ValueError("other: Can not divide by 0")
            return Vector2(self.x / other, self.y / other)

    def __round__(self):
        return Vector2(int(self.x), int(self.y))

    def toPixels(self, resolution: tuple):
        if isinstance(resolution, tuple):
            return Vector2(int(self.x * float(resolution[0])), int(self.y * float(resolution[1])))

    def __repr__(self):
        return "Vector2()"

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

    def asTuple(self):
        return self.tuple


class Rect:
    start = Vector2()
    end = Vector2()
    center = Vector2()

    tuple = ()
    mss = {}

    def __init__(self, startLocation: Vector2, endLocation: Vector2) -> None:
        self.start = startLocation
        self.end = endLocation
        self.center = (startLocation + endLocation) / 2

        self.tuple = (self.start.x, self.start.y, self.end.x, self.end.y)
        self.mss = {"left": self.start.x, "top": self.start.y,
                    "width": self.end.x - self.start.x, "height": self.end.y - self.start.y}

    @classmethod
    def fromTuples(cls, startLocation, endLocation):
        return cls(Vector2.fromTuple(startLocation), Vector2.fromTuple(endLocation))

    @classmethod
    def fromArray(cls, rect=(0, 0, 0, 0)):
        return cls(Vector2(rect[0], rect[1]), Vector2(rect[2], rect[3]))

    def GetDimensions(self) -> Vector2:
        return Vector2(self.tuple[2] - self.tuple[0], self.tuple[3] - self.tuple[1])

    def toPixels(self, resolution: Vector2):
        if isinstance(resolution, Vector2):
            return Rect(self.start.toPixels(resolution.asTuple()), self.end.toPixels(resolution.asTuple()))
        else:
            raise ValueError("resolution must be of type Vector2")

    def __repr__(self):
        return "Rect()"

    def __str__(self):
        return f"Start: {self.start} | End: {self.end}"

    def asMss(self):
        return self.mss

    def asTuple(self):
        return self.tuple


class PYGenshinException(Exception):
    pass
