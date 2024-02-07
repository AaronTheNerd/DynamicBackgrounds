from log.performance import measure
from point.ABCs import PointABC
from triangle.triangle import Triangle
import numpy
from scipy.spatial import Delaunay


@measure
def SciPy(points: list[PointABC]) -> list[Triangle]:
    scipy_points = convert_to_scipy_inputs(points)
    scipy_triangulation = Delaunay(scipy_points)
    return convert_scipy_triangulation(scipy_triangulation, points)

def convert_to_scipy_inputs(points: list[PointABC]) -> numpy.ndarray:
    return numpy.array([scipy_point(point) for point in points])

def scipy_point(point: PointABC) -> list[float]:
    return [point.x, point.y]

def convert_scipy_triangulation(delaunay: Delaunay, points: list[PointABC]) -> list[Triangle]:
    indicies = delaunay.simplices
    triangles = []
    for triangle_indicies in indicies:
        triangle_points = [points[index] for index in triangle_indicies]
        triangles.append(Triangle(*triangle_points))
    return triangles
