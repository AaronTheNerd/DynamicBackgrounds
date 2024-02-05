import math

from point.ABCs import PointABC
from point.point import Static

########################## Start GeeksForGeeks Code ###########################
# https://www.geeksforgeeks.org/find-if-a-point-lies-inside-outside-or-on-the-circumcircle-of-three-points-a-b-c/
# Python3 program to find the points which lies inside, outside or on the     #
# circle                                                                      #
###############################################################################


# Function to find the line given
# two points
def lineFromPoints(P: PointABC, Q: PointABC) -> tuple[float, float, float]:
    a = Q.y - P.y
    b = P.x - Q.x
    c = a * (P.x) + b * (P.y)
    return a, b, c


# Function which converts the
# input line to its perpendicular
# bisector. It also inputs the
# points whose mid-lies o
# on the bisector
def perpenBisectorFromLine(
    P: PointABC, Q: PointABC, a: float, b: float, c: float
) -> tuple[float, float, float]:
    # Find the mid point
    mid_point = Static((P.x + Q.x) / 2, (P.y + Q.y) / 2, 0)
    # c = -bx + ay
    c = -b * (mid_point.x) + a * (mid_point.y)
    # Assign the coefficient of
    # a and b
    a, b = -b, a
    return a, b, c


# Returns the intersection of
# two lines
def LineInterX(
    a1: float, b1: float, c1: float, a2: float, b2: float, c2: float
) -> float:
    # Find determinant
    determ = a1 * b2 - a2 * b1
    x = b2 * c1 - b1 * c2
    try:
        x /= determ
    except ZeroDivisionError:
        x = math.inf
    return x


# Returns the intersection of
# two lines
def LineInterY(
    a1: float, b1: float, c1: float, a2: float, b2: float, c2: float
) -> float:
    # Find determinant
    determ = a1 * b2 - a2 * b1
    y = a1 * c2 - a2 * c1
    try:
        y /= determ
    except ZeroDivisionError:
        y = math.inf
    return y


########################### End GeeksForGeeks Code ############################
