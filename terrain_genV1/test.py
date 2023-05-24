from ursina import *
from chunk_gen import Chunk
from util import *

app = Ursina()

chunk = Chunk()
chunk.gen_noise()
chunk.gen_voxel_data()
chunk.gen_octree()

octree = Octree.load_from_file('octree.dat')

voxels = Octree.touching_air_voxels(octree.root)
#print(len(voxels))

mesh_verts = []
mesh_uvs = []
mesh_triangles = []


def generate_voxel_cube(x, y, z):
    vertices = [
        # Front face
        (0 + x, 0 + y, 1 + z),
        (1 + x, 0 + y, 1 + z),
        (1 + x, 1 + y, 1 + z),
        (0 + x, 1 + y, 1 + z),
        # Back face
        (1 + x, 0 + y, 0 + z),
        (0 + x, 0 + y, 0 + z),
        (0 + x, 1 + y, 0 + z),
        (1 + x, 1 + y, 0 + z),
        # Top face
        (0 + x, 1 + y, 1 + z),
        (1 + x, 1 + y, 1 + z),
        (1 + x, 1 + y, 0 + z),
        (0 + x, 1 + y, 0 + z),
        # Bottom face
        (0 + x, 0 + y, 0 + z),
        (1 + x, 0 + y, 0 + z),
        (1 + x, 0 + y, 1 + z),
        (0 + x, 0 + y, 1 + z),
        # Left face
        (0 + x, 0 + y, 0 + z),
        (0 + x, 0 + y, 1 + z),
        (0 + x, 1 + y, 1 + z),
        (0 + x, 1 + y, 0 + z),
        # Right face
        (1 + x, 0 + y, 1 + z),
        (1 + x, 0 + y, 0 + z),
        (1 + x, 1 + y, 0 + z),
        (1 + x, 1 + y, 1 + z)
    ]

    uvs = [
        # Front face
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
        # Back face
        (1, 0),
        (0, 0),
        (0, 1),
        (1, 1),
        # Top face
        (0, 1),
        (1, 1),
        (1, 0),
        (0, 0),
        # Bottom face
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
        # Left face
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
        # Right face
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1)
    ]

    triangles = [
        # Front face
        [0, 1, 2],
        [0, 2, 3],
        # Back face
        [4, 5, 6],
        [4, 6, 7],
        # Top face
        [8, 9, 10],
        [8, 10, 11],
        # Bottom face
        [12, 13, 14],
        [12, 14, 15],
        # Left face
        [16, 17, 18],
        [16, 18, 19],
        # Right face
        [20, 21, 22],
        [20, 22, 23]
    ]

    mesh_verts.extend(vertices)
    mesh_uvs.extend(uvs)
    for tri in triangles:
        mesh_triangles.extend([i + len(mesh_verts) - 24 for i in tri])  # Adjust triangle indices


for voxel in voxels:
    x, y, z = voxel[0], voxel[2], voxel[1]
    generate_voxel_cube(x, z, y)

chunk_mesh = Mesh(vertices=mesh_verts, triangles=mesh_triangles, uvs=mesh_uvs)
chunk_entity = Entity(model=chunk_mesh, position=(0, 0, 0))
chunk_entity.model.generate()

EditorCamera()
app.run()
