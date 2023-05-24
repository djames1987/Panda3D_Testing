import numpy as np
import noise
from ursina import floor
voxel_data = np.zeros((256, 64, 64))

#for i in range(0, 100):
#    for x in range(0, 64):
#        for y in range(0, 64):
#voxel_data[i][x][y] = 1.003

for i in range(0, 100):
    for x in range(0,64):
        voxel_data[i][x] = 1.003

def generate_terrain(x, y):
    scale = 100.0  # Adjust this value to change the terrain scale
    octaves = 6    # Adjust this value to change the level of detail
    persistence = 0.5  # Adjust this value to change the roughness
    lacunarity = 2.0  # Adjust this value to change the frequency

    # Generate Perlin noise value for the given (x, y) coordinates
    noise_value = noise.pnoise2(x / scale,
                               y / scale,
                               octaves=octaves,
                               persistence=persistence,
                               lacunarity=lacunarity,
                               repeatx=1024,
                               repeaty=1024,
                               base=0)

    # Map the noise value to the range [0, 1] and scale it to the desired height range
    z = noise_value * 10.0  # Adjust this value to change the height range

    return floor(z)


for i in range(100, 150):
    for x in range(0, 64):
        for y in range(0, 64):
            z = generate_terrain(x, y)
            newz = z + i
            voxel_data[newz][x][y] = 1.002
            print(x, newz, y)


