import bpy
import sys

# Get command-line arguments
argv = sys.argv
argv = argv[argv.index("--") + 1 :]  # Skip Blender arguments

# Debug: Print the received arguments
print("Arguments passed to the script:", argv)

# Parse arguments
obj_path = argv[0]
ply_path = argv[1]

# Debug: Print the parsed paths
print("OBJ Path:", obj_path)
print("PLY Path:", ply_path)

# Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import OBJ
bpy.ops.import_scene.obj(filepath=obj_path)

# Export to PLY
bpy.ops.export_mesh.ply(filepath=ply_path)

# Exit Blender
bpy.ops.wm.quit_blender()
