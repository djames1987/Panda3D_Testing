import noise
from ursina import floor
from util import *

TYPES = [
    'GRASS',
    'STONE',
    'AIR',
]

class Chunk:
    def __init__(self):
        self.voxel_data = [
            [
                [
                    {'position': (x, y, z), 'type': 'AIR', 'touching_air': True}
                    for y in range(256)
                ]
                for z in range(64)
            ]
            for x in range(64)
        ]

    def gen_noise(self):
        base_height = 50
        for x in range(64):
            for z in range(64):
                height = floor(int(noise.snoise2(x / 64, z / 64) * base_height) + base_height)
                for y in range(height):
                    self.voxel_data[x][z][y]['type'] = 'STONE' if y < 95 else 'GRASS'
                    if y == height - 1 and y < 94:
                        self.voxel_data[x][z][y]['touching_air'] = True
                    elif y < 94:
                        self.voxel_data[x][z][y + 1]['touching_air'] = True

    def is_touching_air(self, x, z, y):
        if x == 0 or x == 63 or z == 0 or z == 63:
            return True
        for dx, dz in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, nz = x + dx, z + dz
            if nx >= 0 and nx < 64 and nz >= 0 and nz < 64:
                if self.get_voxel(nx, nz, y)['type'] == 'AIR':
                    return True
        return False

    def get_voxel(self, x, z, y):
        return self.voxel_data[x][z][y]

    def gen_octree(self):
        octree = Octree()
        for x in range(64):
            for z in range(64):
                for y in range(256):
                    voxel = self.voxel_data[x][z][y]
                    if voxel['type'] != 'AIR' or voxel['touching_air']:
                        octree.add_data(voxel)
        octree.save_to_file('octree.dat')


chunk = Chunk()
chunk.gen_noise()
chunk.gen_octree()
