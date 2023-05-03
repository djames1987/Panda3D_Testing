from ursina import *
import os
import subprocess


class ChunkManager:
    def __init__(self):
        # Settings for Chunk view and buffer distance
        self.view_radius = 3
        self.buffer_radius = 6

        # Lists of stored chunk
        self.loaded_chunks = []
        self.buffered_chunks = []
        self.unloaded_chunks = []

        self.chunk_path = 'data/chunk_'
        self.model_type = '.obj'

    def load_chunk(self, **kwargs):
        x = kwargs['x']
        y = kwargs['y']
        chunk_name = f"data/chunk_{x}_{y}.obj"
        if not os.path.exists(chunk_name):
            exe_path = "../bin/AI_GAME_SERVER.exe"
            subprocess.run([exe_path, str(x), str(y)])

    def buffer_chunk(self, **kwargs):
        pass

    def unload_chunk(self, **kwargs):
        pass

    def update_chunks(self, **kwargs):
        pass

