import math
import random

from configs import CONFIGS
from point import DriftingPoint, PointABC, StaticPoint, SwayingPoint


def seed(seed: int) -> None:
    random.seed(seed)


def generate_border_points() -> list[PointABC]:
    border_points = []
    num_of_x_border_points = (
        math.floor(CONFIGS.full_width / CONFIGS.point_configs.border_configs.separation) + 1
    )
    x_dist = CONFIGS.full_width / (num_of_x_border_points - 1)
    for i in range(num_of_x_border_points):
        if CONFIGS.point_configs.border_configs.top:
            border_points.append(StaticPoint(x_dist * i, 1))
        if CONFIGS.point_configs.border_configs.bottom:
            border_points.append(StaticPoint(x_dist * i, CONFIGS.full_height - 1))
    num_of_y_border_points = (
        math.floor(CONFIGS.full_height / CONFIGS.point_configs.border_configs.separation) + 1
    )
    y_dist = CONFIGS.full_height / (num_of_y_border_points - 1)
    for i in range(num_of_y_border_points - 2):
        if CONFIGS.point_configs.border_configs.left:
            border_points.append(StaticPoint(1, y_dist * (i + 1)))
        if CONFIGS.point_configs.border_configs.right:
            border_points.append(StaticPoint(CONFIGS.full_width - 1, y_dist * (i + 1)))
    return border_points


def random_point() -> PointABC:
    global open_simplex
    if random.random() < CONFIGS.point_configs.drifting_configs.percentage:
        if CONFIGS.point_configs.drifting_configs.reflective:
            drift_x = random.uniform(
                CONFIGS.point_configs.drifting_configs.x_min,
                CONFIGS.point_configs.drifting_configs.x_max,
            )
            drift_y = random.uniform(
                CONFIGS.point_configs.drifting_configs.y_min,
                CONFIGS.point_configs.drifting_configs.y_max,
            )
        else:
            drift_x = random.randint(
                int(CONFIGS.point_configs.drifting_configs.x_min),
                int(CONFIGS.point_configs.drifting_configs.x_max),
            )
            drift_y = random.randint(
                int(CONFIGS.point_configs.drifting_configs.y_min),
                int(CONFIGS.point_configs.drifting_configs.y_max),
            )

        return DriftingPoint(
            random.uniform(0, CONFIGS.full_width),
            random.uniform(0, CONFIGS.full_height),
            None,  # type: ignore
            drift_x,
            drift_y,
            CONFIGS.point_configs.drifting_configs.reflective,
        )
    else:
        return SwayingPoint(
            random.uniform(0, CONFIGS.full_width), random.uniform(0, CONFIGS.full_height)
        )


def generate_points() -> list[PointABC]:
    global open_simplex
    # Generate evenly separated border points
    points = generate_border_points()
    # Find how many points are border points
    border_points_length = len(points)
    # Add one initial interior point
    points.append(random_point())
    # Add points while there is space to
    fails = 0
    while (
        len(points) - border_points_length < CONFIGS.point_configs.num_of_points
        and fails < CONFIGS.point_configs.max_fails
    ):
        # Create a new point
        new_point = random_point()
        failed = False
        # Check if the point can fit without being too close to other points
        for point in points:
            if (point.x - new_point.x) ** 2 + (
                point.y - new_point.y
            ) ** 2 < CONFIGS.point_configs.separation_radius**2:
                fails += 1
                failed = True
                break
        # Add new point to total points if the point is well separated from others
        if not failed:
            points.append(new_point)
            fails = 0
    return points
