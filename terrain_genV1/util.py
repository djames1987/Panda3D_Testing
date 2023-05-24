# Classes and functions for the Octree Data Storage

import pickle
total = 0

class OctreeNode:
    def __init__(self, level, bounds):
        self.level = level
        self.bounds = bounds
        self.children = [None] * 8
        self.data = None

    def __repr__(self):
        return f"OctreeNode(level={self.level}, bounds={self.bounds}, data={self.data})"

    def __str__(self):
        children_str = ', '.join(
            str(child) if child is not None else 'None'
            for child in self.children
        )
        return f"OctreeNode(level={self.level}, bounds={self.bounds}, data={self.data}, children=[{children_str}])"


class Octree:
    def __init__(self):
        self.max_level = 6
        self.root = OctreeNode(0, (0, 0, 0, 64, 64, 256))
        self.position_bits = 8 # 8 bits for position data
        self.type_bits = 2 # 2 bits for type data
        self.position_mask = ((1 << self.type_bits) - 1) << self.position_bits # Bitmask for type bits



    def add_data(self, x, y, z, data):
        node = self.root
        for level in range(1, self.max_level + 1):
            octant = self.get_octant(x, y, z, level)
            if node.children[octant] is None:
                node.children[octant] = OctreeNode(level, self.get_octant_bounds(node.bounds, octant))
            node = node.children[octant]
        node.data = (x, z, y, data)  # Update the voxel data with x, y, z

    def remove_data(self, x, y, z):
        node = self.root
        for level in range(1, self.max_level + 1):
            octant = self.get_octant(x, y, z, level)
            if node.children[octant] is None:
                node.children[octant] = OctreeNode(level, self.get_octant_bounds(node.bounds, octant))
            node = node.children[octant]
        node.data = None

    def search_data(self, x, y, z):
        node = self.root
        for level in range(1, self.max_level + 1):
            octant = self.get_octant(x, z, y, level)
            node = node.children[octant]
            if node is None:
                return None
        if node.data is None:
            return None
        return node.data[3]  # Return only the data value

    @staticmethod
    def get_octant(x, z, y, level):
        return ((z >> level) & 1) << 2 | ((y >> level) & 1) << 1 | ((x >> level) & 1)

    @staticmethod
    def get_octant_bounds(bounds, octant):
        x_min, y_min, z_min, x_max, y_max, z_max = bounds
        x_mid = (x_min + x_max) // 2
        y_mid = (y_min + y_max) // 2
        z_mid = (z_min + z_max) // 2
        if octant & 1:
            x_min = x_mid
        else:
            x_max = x_mid
        if octant & 2:
            z_min = z_mid
        else:
            z_max = z_mid
        if octant & 4:
            y_min = y_mid
        else:
            y_max = y_mid
        return x_min, y_min, z_min, x_max, y_max, z_max

    def bitmask_data(self, x, y, z, voxel_type, touching_air):
        # Pack position, type, and touching_air into a bitmask
        # Define the offsets for each piece of data
        voxel_type_offset = 24
        x_offset = 16
        z_offset = 8
        y_offset = 0

        # Define the voxel types as binary values
        voxel_types = {'GRASS': 0b00, 'STONE': 0b01, 'AIR': 0b10}

        # Create the bitmask
        bitmask = (
                (voxel_types[voxel_type] << voxel_type_offset) |
                (x << x_offset) |
                (y << y_offset) |
                (z << z_offset) |
                int(touching_air)
        )
        #print(bitmask)

        return bitmask

    def extract_data(self, bitmask):
        # Define the offsets for each piece of data
        voxel_type_offset = 24
        x_offset = 16
        y_offset = 8
        z_offset = 0

        # Define the voxel types as binary values
        #voxel_types = {0b00: 'GRASS', 0b01: 'STONE', 0b10: 'AIR'}
        voxel_types = {'GRASS': 0b00, 'STONE': 0b01, 'AIR': 0b10}

        # Extract each piece of data from the bitmask
        voxel_type = voxel_types[(bitmask >> voxel_type_offset) & 0b11]
        x = (bitmask >> x_offset) & 0xFF
        y = (bitmask >> y_offset) & 0xFF
        z = (bitmask >> z_offset) & 0xFF
        touching_air = bool(bitmask & 1)

        return x, y, z, voxel_type, touching_air

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.root, file)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as file:
            root = pickle.load(file)

        max_level = root.level
        octree = Octree()
        octree.root = root
        return octree

    @staticmethod
    def touching_air_voxels(node):
        voxels = []
        global total

        if node is None:
            return voxels

        if node.data is not None:
            x, y, z, data = node.data
            data_x, data_z, data_y, voxel_type, touching_air = data
            if touching_air:
                voxels.append((x, y, z))
                total = total + 1

        for child in node.children:
            voxels.extend(Octree.touching_air_voxels(child))

        #print(total)

        return voxels
