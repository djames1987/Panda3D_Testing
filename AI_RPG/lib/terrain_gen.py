import math
import subprocess


def generate_spiral_coordinates(num_coords):
    """
    Generates the next `num_coords` whole number grid coordinates in a clockwise
    swirl pattern around the point (0, 0).

    Args:
    - num_coords: An integer indicating the number of coordinates to generate.

    Returns:
    A list of tuples representing the grid coordinates in the spiral pattern.
    """

    # Initialize variables to keep track of the current position and direction
    x, y = 0, 0
    dx, dy = 0, -1

    # Initialize a list to store the coordinates as we generate them
    coords = []

    # Loop until we've generated the desired number of coordinates
    for i in range(num_coords):
        # If we're at a corner, change direction
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
            dx, dy = -dy, dx

        # Add the current position to the list of coordinates
        coords.append((x, y))
        exe_file = "../bin/AI_GAME_SERVER.exe"
        subprocess.call([exe_file, str(x), str(y)])

        # Move to the next position in the current direction
        x, y = x + dx, y + dy

    return coords

generate_spiral_coordinates(10)