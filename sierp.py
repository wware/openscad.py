print """$fn = 30;

module bar(v1, v2, r) {
    p = v2 - v1;
    R = sqrt(p.x * p.x + p.y * p.y);
    L = sqrt(R * R + p.z * p.z);
    translate(v1)
        rotate(atan2(R, p.z), [-p.y, p.x, 0])
            cylinder(h=L, r=r);
}

Aa = [1, 0, 0];
Ba = [-1/2, sqrt(3) / 2, 0];
Ca = [-1/2, -sqrt(3) / 2, 0];
Da = [0, 0, sqrt(2)];
center = 0.25 * (Aa + Ba + Ca + Da);
A = Aa - center;
B = Ba - center;
C = Ca - center;
D = Da - center;


module tetrahedron(S, r) {
    v1 = S * A;
    v2 = S * B;
    v3 = S * C;
    v4 = S * D;
    bar(v1, v2, r);
    bar(v1, v3, r);
    bar(v1, v4, r);
    bar(v2, v3, r);
    bar(v2, v4, r);
    bar(v3, v4, r);
}
"""

S = 120
r = 0.05 * S

print """
    translate({0} * A) sphere(r={1});
    translate({0} * B) sphere(r={1});
    translate({0} * C) sphere(r={1});
    translate({0} * D) sphere(r={1});
""".format(S, r)

def recurse(S, r, depth): 
    print "tetrahedron({0}, {1});".format(S, r)
    if depth > 0:
        S, r = 0.5 * S, 0.7 * r
        print "translate({0} * A) {{".format(S)
        recurse(S, r, depth - 1)
        print "}"
        print "translate({0} * B) {{".format(S)
        recurse(S, r, depth - 1)
        print "}"
        print "translate({0} * C) {{".format(S)
        recurse(S, r, depth - 1)
        print "}"
        print "translate({0} * D) {{".format(S)
        recurse(S, r, depth - 1)
        print "}"

recurse(S, r, 4)
