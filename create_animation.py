
# This script makes a sphere.

import os
import bpy
import bmesh

def make_collections():
    if 'Beads' not in bpy.data.collections:
        bpy.data.collections.new('Beads')
    if 'Rods' not in bpy.data.collections:
        bpy.data.collections.new('Rods')
    if 'Beads' not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(bpy.data.collections['Beads'])
    if 'Rods' not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(bpy.data.collections['Rods'])
        
def make_materials():
    bead_material = bpy.data.materials.new('Bead Material')
    bead_material.metallic = 1.0
    bead_material.roughness = 0.4
    bead_material.diffuse_color = (0.15, 0.40, 0.80, 1.00)
    rod_material = bpy.data.materials.new('Rod Material')
    rod_material.metallic = 1.0
    rod_material.roughness = 0.8
    rod_material.diffuse_color = (0.35, 0.35, 0.35, 1.00)

def make_bead_mesh():
    sphere = bmesh.new()

    # Add a icosphere
    bmesh.ops.create_icosphere(sphere, subdivisions=3, radius=1.4)
    for face in sphere.faces:
        face.smooth = True

    # Finish up, write the bmesh into a new mesh
    bead_mesh = bpy.data.meshes.new("BeadMesh")
    sphere.to_mesh(bead_mesh)
    sphere.free()
    return bead_mesh
        

def get_pos(values, bead_num):
    index = bead_num * 3
    return (float(values[index]), float(values[index+1]), float(values[index+2]))

def make_bead(num, mesh, pos):
    obj = bpy.data.objects.new(f'Bead{num}', mesh)
    obj.location = pos
    obj.data.materials.append(bpy.data.materials['Bead Material'])
    bpy.data.collections['Beads'].objects.link(obj)
    return obj
    
def make_rod(num, pos_from, pos_to):
    rod = bpy.data.meshes.new(f'LineMesh{num}')
    rod.vertices.add(2)
    rod.vertices[0].co = pos_from
    rod.vertices[1].co = pos_to
    rod.edges.add(1)
    rod.edges[0].vertices = (0, 1)
    obj = bpy.data.objects.new(f'Rod{num}', rod)
    obj.modifiers.new("Skin", 'SKIN')
    obj.modifiers['Skin'].use_smooth_shade = True
    obj.modifiers.new("Subsurf", 'SUBSURF')
    obj.data.skin_vertices[0].data[0].radius = (0.5, 0.5)
    obj.data.skin_vertices[0].data[1].radius = (0.5, 0.5)
    obj.data.materials.append(bpy.data.materials['Rod Material'])
    bpy.data.collections['Rods'].objects.link(obj)
    return rod.vertices

make_collections()    
make_materials()    

beads = []
tick = 0

input_file = open("./Development/BeadAnimation/data/net_dt01.dat", "r")
for time_line in input_file:
    print(tick)
    values = time_line.split()
    if not beads:
        bead_mesh = make_bead_mesh()
        for num in range(0, len(values) // 3):
            beads.append({"bead": make_bead(num, bead_mesh, get_pos(values, num)), "rod_ends": []})
            if num > 0:
                rod_ends = make_rod(num, get_pos(values, num - 1), get_pos(values, num))
                beads[num - 1]['rod_ends'].append(rod_ends[0])
                beads[num]['rod_ends'].append(rod_ends[1])
    for num in range(len(beads)):
        beads[num]['bead'].location = get_pos(values, num)
        beads[num]['bead'].keyframe_insert(data_path='location', frame = tick * 5)
        for rod_end in beads[num]['rod_ends']:
            rod_end.co = get_pos(values, num)
            rod_end.keyframe_insert(data_path='co', frame = tick * 5)
    tick += 1

bpy.context.scene.frame_end = tick * 5





