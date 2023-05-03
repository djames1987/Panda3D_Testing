from ursina import *

app = Ursina()

# Load the model
model_entity = Entity(model='data/chunk_0_0.obj')

# Create and apply the shader
vertex_shader_path = 'Shaders/vertex_color.vert'
fragment_shader_path = 'Shaders/vertex_color.frag'

with open(vertex_shader_path, 'r') as f:
    vertex_shader_code = f.read()

with open(fragment_shader_path, 'r') as f:
    fragment_shader_code = f.read()

model_shader = Shader(language=Shader.GLSL, vertex=vertex_shader_code, fragment=fragment_shader_code)
model_entity.shader = model_shader
EditorCamera()
app.run()