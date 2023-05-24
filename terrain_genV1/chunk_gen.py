# Generate a New chunk Octree

import noise
from util import *
from ursina import floor

TYPES = [
    'GRASS',
    'STONE',
    'AIR',
]


class Chunk:
    def __init__(self):
        self.max_height = 150
        self.voxel_data = []

    def gen_noise(self):
        base_height = 50
        for x in range(64):
            for z in range(64):
                noise_value = floor(int(noise.snoise2(x / 64, z / 64) * self.max_height) + base_height)
                self.voxel_data.append((x, z, noise_value))

    def gen_voxel_data(self):
        new_voxel_data = []
        for voxel in self.voxel_data:
            x, z, y, *_ = voxel
            touching_air = self.is_touching_air(x, z, y)
            if z > 125:
                new_voxel_data.append((x, z, y, 'AIR', touching_air))
            elif z >= 100:
                new_voxel_data.append((x, z, y, 'GRASS', touching_air))
            else:
                new_voxel_data.append((x, z, y, 'STONE', touching_air))
        self.voxel_data = new_voxel_data

    def is_touching_air(self, x, z, y):
        # Check if the voxel at (x, z, y) is touching air on any of its sides
        if x == 0 or x == 63 or z == 0 or z == 63:
            return True
        for dx, dz in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, nz = x + dx, z + dz
            if nx >= 0 and nx < 64 and nz >= 0 and nz < 64:
                if self.get_voxel_type(nx, nz, y) == 'AIR':
                    return True
        return False

    def get_voxel_type(self, x, z, y):
        # Get the type of voxel at position (x, z, y)
        if z >= 100:
            return 'GRASS'
        elif z < 95:
            return 'STONE'

    def create_voxel_data(self, x, z, y, voxel_type, touching_air):
        # Create voxel data for the voxel at position (x, z, y) with the given properties
        self.voxel_data.append((x, z, y, voxel_type, touching_air))

    def gen_octree(self):
        # Create the Octree and bitmask the data using the functions from util.py
        octree = Octree()
        for voxel in self.voxel_data:
            x, z, y, voxel_type, touching_air = voxel
            bitmask = octree.bitmask_data(x, z, y, voxel_type, touching_air)
            octree.add_data(x, z, y, voxel)

        # Save the Octree
        octree.save_to_file('octree.dat')


# Run the chunk generation
#chunk = Chunk()
#chunk.gen_noise()
#chunk.gen_voxel_data()
#chunk.gen_octree()


#octree = Octree.load_from_file('octree.dat')
#with open('octree.txt', 'w') as file:
#    file.write(str(octree.root))


#test = Octree()

#test.print_grass_voxels(octree.root)