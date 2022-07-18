class Vector2D:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)
    def __truediv__(self, other):
        return Vector2D(self.x / other, self.y / other)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    def __neg__(self):
        return Vector2D(-self.x, -self.y)
    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Index out of range")
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Index out of range")
    def __iter__(self):
        return self
    def __next__(self):
        if self.x == 0 and self.y == 0:
            raise StopIteration
        else:
            self.x -= 1
            self.y -= 1
            return self
    def __copy__(self):
        return Vector2D(self.x, self.y)
    def __deepcopy__(self, memo):
        return Vector2D(self.x, self.y)
    def __getstate__(self):
        return (self.x, self.y)
    def __setstate__(self, state):
        self.x, self.y = state
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
    def __repr__(self):
        return "Vector2D(" + str(self.x) + ", " + str(self.y) + ")"

class Vector3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, other):
        return Vector3D(self.x * other, self.y * other, self.z * other)
    def __truediv__(self, other):
        return Vector3D(self.x / other, self.y / other, self.z / other)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.z != other.z
    def __neg__(self):
        return Vector3D(-self.x, -self.y, -self.z)
    def __abs__(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise IndexError("Index out of range")
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError("Index out of range")
    def __iter__(self):
        return self
    def __next__(self):
        if self.x == 0 and self.y == 0 and self.z == 0:
            raise StopIteration
        else:
            self.x -= 1
            self.y -= 1
            self.z -= 1
            return self
    def __copy__(self):
        return Vector3D(self.x, self.y, self.z)
    def __deepcopy__(self, memo):
        return Vector3D(self.x, self.y, self.z)
    def __getstate__(self):
        return (self.x, self.y, self.z)
    def __setstate__(self, state):
        self.x, self.y, self.z = state
    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.z)
    def __repr__(self):
        return "Vector3D(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
