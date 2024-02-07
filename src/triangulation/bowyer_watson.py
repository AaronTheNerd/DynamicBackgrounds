###############################################################################
# Copyright 2021                                                              #
# Written by Aaron Barge                                                      #
# Idea from: https://necessarydisorder.wordpress.com/2017/11/15/drawing-from-noise-and-then-making-animated-loopy-gifs-from-there/
###############################################################################

################################### Imports ###################################
import math

from configs import CONFIGS
from log.performance import measure
from point.ABCs import PointABC
from point.point import Static
from triangle.triangle import Edge, Triangle

################################### Methods ###################################


def isInside(t: Triangle, p: PointABC) -> bool:
    if t.circumcenter.x == math.inf or t.circumcenter.y == math.inf:
        return True
    dist_sq = math.pow(t.circumcenter.x - p.x, 2) + math.pow(t.circumcenter.y - p.y, 2)
    return dist_sq < t.radius_sq


############################# Start Triangulation #############################
# https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm#/media/File:Bowyer-Watson_6.png
# Super Triangle Math                                                         #
# Point b: (-WIDTH / 2, HEIGHT)                                               #
# Point c: (3 * WIDTH / 2, HEIGHT)                                            #
# Solving for point a                                                         #
#    Set point a.x to the center of canvas = WIDTH / 2                        #
#    Find angle of left angle of super triangle                               #
#        theta = atan(HEIGHT / (WIDTH / 2))                                   #
#              = atan(2 * HEIGHT / WIDTH)                                     #
#    Find distance from bottom of canvas (HEIGHT) to the point a.y            #
#        tan(theta) = dist / WIDTH =>                                         #
#              dist = WIDTH * tan(theta)                                      #
#    Solve for a.y                                                            #
#    a.y = HEIGHT - dist                                                      #
#        = HEIGHT - WIDTH * tan(theta)                                        #
#        = HEIGHT - WIDTH                                                     #
#             * tan(atan(2 * HEIGHT / WIDTH))                                 #
#        = HEIGHT - WIDTH * 2                                                 #
#             * HEIGHT / WIDTH                                                #
#        = HEIGHT - 2 * HEIGHT                                                #
#        = -HEIGHT                                                            #
#    Point a: (WIDTH / 2, -HEIGHT)                                            #
###############################################################################
@measure
def BowyerWatson(points: list[PointABC]) -> list[Triangle]:
    super_a = Static(CONFIGS.full_width / 2, -CONFIGS.full_height, 0)
    super_b = Static(-CONFIGS.full_width / 2, CONFIGS.full_height, 0)
    super_c = Static(3 * CONFIGS.full_width / 2, CONFIGS.full_height, 0)
    triangles = [Triangle(super_a, super_b, super_c)]
    points = sorted(points, key=lambda x: [x.x, x.y])
    for curr_point in points:
        bad_triangles = [
            triangle for triangle in triangles if isInside(triangle, curr_point)
        ]
        polygon: list[Edge] = []
        for triangle in bad_triangles:
            edges = triangle.edges()
            for edge in edges:
                shared = False
                for triangle2 in bad_triangles:
                    if triangle != triangle2:
                        edges2 = triangle2.edges()
                        for edge2 in edges2:
                            if edge.a == edge2.a and edge.b == edge2.b:
                                shared = True
                                break
                    if shared:
                        break
                if not shared:
                    polygon.append(edge)
        for bad_triangle in bad_triangles:
            triangles = [triangle for triangle in triangles if triangle != bad_triangle]
        for edge in polygon:
            triangles.append(Triangle(edge.a, edge.b, curr_point))

    for triangle in triangles:
        triangles = [
            triangle2
            for triangle2 in triangles
            if not (
                triangle2.has_point(super_a)
                or triangle2.has_point(super_b)
                or triangle2.has_point(super_c)
            )
        ]
    return triangles


############################## End Triangulation ##############################
