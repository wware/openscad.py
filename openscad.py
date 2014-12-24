# Python things for OpenSCAD things

from math import sqrt, atan2, pi


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


def flatten(lst):
    result = []
    for x in lst:
        if isinstance(x, list):
            result += flatten(x)
        else:
            result += [x]
    return result


def union(*args):
    return list(args)


def translate(offset):
    def func(*objects):
        lst = []
        for obj in objects:
            if isinstance(obj, list):
                lst += [func(subobj) for subobj in obj if subobj]
            else:
                lst.append("translate({}){{\n{}\n}}".format(offset, obj))
        return lst
    return func


def rotate(*args):
    def func(*objects):
        lst = []
        for obj in objects:
            if isinstance(obj, list):
                lst += [func(subobj) for subobj in obj if subobj]
            else:
                lst.append("rotate{}{{\n{}\n}}".format(args, obj))
        return lst
    return func


def cube(xyz=[1, 1, 1]):
    return "cube({});".format(xyz)


def sphere(r=1):
    return "sphere(r={});".format(r)


def cylinder(r=1, h=1):
    return "cylinder(r={}, h={});".format(r, h)


#############################


#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()

print "$fn = 30;"

def bar(v1, v2, r):
    p = v2 - v1
    R = sqrt(p.x * p.x + p.y * p.y)
    L = sqrt(R * R + p.z * p.z)
    return translate(v1)(
        rotate((180.0 / pi) * atan2(R, p.z),
               [-p.y, p.x, 0])(
            cylinder(h=L, r=r)))

Aa = Vector(1, 0, 0)
Ba = Vector(-0.5, sqrt(3) / 2, 0)
Ca = Vector(-0.5, -sqrt(3) / 2, 0)
Da = Vector(0, 0, sqrt(2))
center = 0.25 * (Aa + Ba + Ca + Da)
A = Aa - center
B = Ba - center
C = Ca - center
D = Da - center

def tetrahedron(S, r):
    v1 = S * A
    v2 = S * B
    v3 = S * C
    v4 = S * D
    return union(
        bar(v1, v2, r),
        bar(v1, v3, r),
        bar(v1, v4, r),
        bar(v2, v3, r),
        bar(v2, v4, r),
        bar(v3, v4, r)
    )

S = 120
r = 0.05 * S

def recurse(S, r, depth):
    lst = []
    if depth > 0:
        lst += [ tetrahedron(S, r) ]
        S, r = 0.5 * S, 0.7 * r
        lst += [
            translate(S * A)(recurse(S, r, depth - 1)),
            translate(S * B)(recurse(S, r, depth - 1)),
            translate(S * C)(recurse(S, r, depth - 1)),
            translate(S * D)(recurse(S, r, depth - 1))
        ]
    return lst

for x in flatten([
    translate(S * A)(sphere(r=r)),
    translate(S * B)(sphere(r=r)),
    translate(S * C)(sphere(r=r)),
    translate(S * D)(sphere(r=r)),
    recurse(S, r, 4)
]):
    print x
