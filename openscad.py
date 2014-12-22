# Python things for OpenSCAD things

def sqrt(x):
    return x ** .5


class Vector:
    """
    >>> a = Vector(5, 3, 1)
    >>> b = Vector(3, 2, 1)
    >>> c = a - b
    >>> assert c == Vector(2, 1, 0)
    """
    def __init__(self, *xyz):
        for x in xyz:
            assert type(x) in (int, float)
        self.x, self.y, self.z = xyz

    def __repr__(self):
        """
        >>> Vector(5, 3, 1)
        [5, 3, 1]
        """
        return "[{0}, {1}, {2}]".format(self.x, self.y, self.z)

    def __add__(self, other):
        """
        >>> Vector(5, 3, 1) + Vector(3, 2, 1)
        [8, 5, 2]
        """
        return Vector(self.x + other.x,
                      self.y + other.y,
                      self.z + other.z)

    def __neg__(self):
        """
        >>> -Vector(3, 2, 1)
        [-3, -2, -1]
        """
        return Vector(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        """
        >>> Vector(5, 3, 1) - Vector(3, 2, 1)
        [2, 1, 0]
        """
        return self + (-other)

    def __rmul__(self, k):
        return Vector(k * self.x, k * self.y, k * self.z)

    def __eq__(self, other):
        """
        >>> Vector(2, 1, 0) == Vector(2, 1, 0)
        True
        """
        return self.x == other.x and self.y == other.y \
            and self.z == other.z



def translate(offset):
    def func(*x):
        pass
    return func


def rotate(arg1, *args):
    def func(*x):
        pass
    return func


def cube(**kwargs):
    def func(*x):
        pass
    return func


def sphere(**kwargs):
    def func(*x):
        pass
    return func


def cylinder(**kwargs):
    def func(*x):
        pass
    return func

#############################


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    def bar(v1, v2, r):
        p = v2 - v1
        R = sqrt(p.x * p.x + p.y * p.y)
        L = sqrt(R * R + p.z * p.z)
        return translate(v1)(
            rotate(atan2(R, p.z), [-p.y, p.x, 0])(
                cylinder(h=L, r=r)))

Aa = Vector(1, 0, 0)
Ba = Vector(-1/2, sqrt(3) / 2, 0)
Ca = Vector(-1/2, -sqrt(3) / 2, 0)
Da = Vector(0, 0, sqrt(2))
center = 0.25 * (Aa + Ba + Ca + Da)
A = Aa - center
B = Ba - center
C = Ca - center
D = Da - center

print A, B, C, D

def tetrahedron(S, r):
    v1 = S * A
    v2 = S * B
    v3 = S * C
    v4 = S * D
    bar(v1, v2, r)
    bar(v1, v3, r)
    bar(v1, v4, r)
    bar(v2, v3, r)
    bar(v2, v4, r)
    bar(v3, v4, r)

S = 120
r = 0.05 * S

translate(S * A)(sphere(r=r))
translate(S * B)(sphere(r=r))
translate(S * C)(sphere(r=r))
translate(S * D)(sphere(r=r))

def recurse(S, r, depth):
    if depth > 0:
        S, r = 0.5 * S, 0.7 * r
        translate(S * A)(recurse(S, r, depth - 1))
        translate(S * B)(recurse(S, r, depth - 1))
        translate(S * C)(recurse(S, r, depth - 1))
        translate(S * D)(recurse(S, r, depth - 1))

recurse(S, r, 4)
