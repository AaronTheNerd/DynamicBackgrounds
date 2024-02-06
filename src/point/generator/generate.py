import logging
import math
import random

from opensimplex import OpenSimplex

from configs import CONFIGS
from log.performance import measure
from point.ABCs import PointABC
from point.generator.ABCs import MoverGeneratorABC, ZMoverGeneratorABC
from point.generator.mover_generator import get_mover_generator_object
from point.generator.zmover_generator import get_zmover_generator_object
from point.point import Moving, Static


def seed(seed: int) -> None:
    random.seed(seed)


def generate_border_points() -> list[PointABC]:
    border_points = []
    num_of_x_border_points = (
        math.floor(CONFIGS.full_width / CONFIGS.point_generation.border.separation) + 1
    )
    x_dist = CONFIGS.full_width / (num_of_x_border_points - 1)
    for i in range(num_of_x_border_points):
        if CONFIGS.point_generation.border.top:
            border_points.append(Static(x_dist * i, 1, 0))
        if CONFIGS.point_generation.border.bottom:
            border_points.append(Static(x_dist * i, CONFIGS.full_height - 1, 0))
    num_of_y_border_points = (
        math.floor(CONFIGS.full_height / CONFIGS.point_generation.border.separation) + 1
    )
    y_dist = CONFIGS.full_height / (num_of_y_border_points - 1)
    for i in range(num_of_y_border_points - 2):
        if CONFIGS.point_generation.border.left:
            border_points.append(Static(1, y_dist * (i + 1), 0))
        if CONFIGS.point_generation.border.right:
            border_points.append(Static(CONFIGS.full_width - 1, y_dist * (i + 1), 0))
    return border_points


def random_point(
    x_movers: list[MoverGeneratorABC],
    y_movers: list[MoverGeneratorABC],
    z_movers: list[ZMoverGeneratorABC],
    open_simplex: OpenSimplex,
) -> PointABC:
    return Moving(
        random.uniform(0, CONFIGS.full_width),
        random.uniform(0, CONFIGS.full_height),
        0.0,
        [mover.generate() for mover in x_movers],
        [mover.generate() for mover in y_movers],
        [mover.generate() for mover in z_movers],
        open_simplex,
    )


@measure
def generate_points(open_simplex: OpenSimplex) -> list[PointABC]:
    logger = logging.getLogger(__name__)
    logger.info("Generating Initial Points...")
    # Generate evenly separated border points
    points = generate_border_points()
    # Find how many points are border points
    border_points_length = len(points)

    x_movers = [
        get_mover_generator_object(config) for config in CONFIGS.point_movement.x
    ]
    y_movers = [
        get_mover_generator_object(config) for config in CONFIGS.point_movement.y
    ]
    z_movers = [
        get_zmover_generator_object(config) for config in CONFIGS.point_movement.z
    ]

    # Add one initial interior point
    points.append(random_point(x_movers, y_movers, z_movers, open_simplex))
    # Add points while there is space to
    fails = 0
    while (
        len(points) - border_points_length < CONFIGS.point_generation.num_of_points
        and fails < CONFIGS.point_generation.max_fails
    ):
        # Create a new point
        new_point = random_point(x_movers, y_movers, z_movers, open_simplex)
        failed = False
        # Check if the point can fit without being too close to other points
        for point in points:
            if (
                math.pow(point.x - new_point.x, 2) + math.pow(point.y - new_point.y, 2)
                < CONFIGS.point_generation.separation_radius**2
            ):
                fails += 1
                failed = True
                break
        # Add new point to total points if the point is well separated from others
        if not failed:
            points.append(new_point)
            fails = 0
    logger.info("Finished generating initial points")
    logger.info(f"Generated {len(points)} points")
    return points
