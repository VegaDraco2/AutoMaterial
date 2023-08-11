bl_info = {
    "name": "MatBuilder",
    "author": "Vega Draco",
    "version": (0, 1),
    "blender": (3, 6, 1),
    "location": "3D Viewport > Right Sidebar (N-Bar)",
    "description": "Material Stuff",
    "warning": "Has not been tested on Linux or Mac!",
    "doc_url": "",
    "category": "Material",
}

import bpy
import os
import re

def _clearconsole():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
#_clearconsole(self, context)

def _remove_material_slots():
    for obj in bpy.context.selected_editable_objects:
        if not hasattr(obj.data, 'materials'):
            continue
        for i in range(len(obj.material_slots)):
            obj.data.materials.pop()
            #bpy.ops.object.material_slot_remove({'object': obj})
            
            

class AM_PROPERTIES(bpy.types.PropertyGroup):
    parent_path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="This is the parent directory for you files", default=os.getcwd())
    new_mat_name : bpy.props.StringProperty(name="", description="Name of new material", default="MyMaterial")
    
    path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="Metallic.  Right Click for options", default="Path/path/paht")
    name : bpy.props.StringProperty(subtype='NONE', name="", description="Metallic.  Right Click for options", default="Name.png")
    
    show_guide : bpy.props.BoolProperty(name="Guide", description="Show Guide", default=False)
    show_options : bpy.props.BoolProperty(name="Show Options", description="Show Options", default=False)
    show_extras : bpy.props.BoolProperty(name="Extras", description="Show Extras", default=False)
    
    albedo_name : bpy.props.StringProperty(subtype='NONE', name="", description="", default="Albedo")
    albedo_path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="Albedo, Color, Diffuse.  Right Click for options", default="Albedo")
    ao_name : bpy.props.StringProperty(subtype='NONE', name="", description="", default="Ambient Occlusion")
    ao_path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="Ambient Occlusion.  Right Click for options", default="Ambient Occlusion")
    metal_name : bpy.props.StringProperty(subtype='NONE', name="", description="", default="Metallic")
    metal_path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="Metallic.  Right Click for options", default="Metallic")
    rough_name : bpy.props.StringProperty(subtype='NONE', name="", description="", default="Roughness")
    rough_path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="Roughness.  Right Click for options", default="Roughness")
    normal_name : bpy.props.StringProperty(subtype='NONE', name="", description="", default="Normal")
    normal_path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="Normal.  Right Click for options", default="Normal")
    mask_name : bpy.props.StringProperty(subtype='NONE', name="", description="", default="Mask")
    mask_path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="Mask.  Right Click for options", default="Mask")
    bump_name : bpy.props.StringProperty(subtype='NONE', name="", description="", default="Bump")
    bump_path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="Bump.  Right Click for options", default="Bump")
    displace_name : bpy.props.StringProperty(subtype='NONE', name="", description="", default="Displace")
    displace_path : bpy.props.StringProperty(subtype='FILE_PATH', name="", description="Displace.  Right Click for options", default="Displace")
    
    sel_albedo : bpy.props.BoolProperty(name="Albedo", description="Select Albedo", default=False)
    sel_ao : bpy.props.BoolProperty(name="", description="Select AO", default=False)
    sel_metal : bpy.props.BoolProperty(name="", description="Select Metallic", default=False)
    sel_rough : bpy.props.BoolProperty(name="", description="Select Roughness", default=False)
    sel_normal : bpy.props.BoolProperty(name="", description="Select Normal", default=False)
    sel_mask : bpy.props.BoolProperty(name="", description="Select Mask", default=False)
    sel_bump : bpy.props.BoolProperty(name="", description="Select Bump", default=False)
    sel_displace : bpy.props.BoolProperty(name="", description="Select Displace", default=False)
    
    use_autoname : bpy.props.BoolProperty(name="Generate Material Name from Albedo Image", description="Generate Material Name", default=True)
    use_box_proj : bpy.props.BoolProperty(name="Set Box Projection", description="Preset for Box Projection", default=False)
    box_blend : bpy.props.FloatProperty(name="Blend:", min=0.0, max=1.0, step=1, default = 0.2, unit='NONE')
    use_mat_index : bpy.props.BoolProperty(name="Specify Material Slot", description="Specify material slot", default=False)
    mat_index_slider : bpy.props.IntProperty(name="Slot Index", min=0, soft_max=8, step=1, description="Choose material index", default=0)
    
    clear_console : bpy.props.BoolProperty(name="Clear Console", description="Clear System Console on Build/Update", default=True)
    move_split : bpy.props.FloatProperty(name="Adjust Split Window", subtype='FACTOR', unit='NONE', min=0.1, max=0.85, step=0.1, description="Adjust Split Window", default=0.36)

            
class AM_PT_AUTOMAT(bpy.types.Panel):
    bl_label = "AutoMat Material Builder"
    bl_idname = "AM_PT_AUTOMAT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoMat"
    
    def draw(self, context):
        y_ht = 1.12
        layout = self.layout  
        scene = context.scene
        am_prop = scene.am_properties 
        
        row=layout.box()
        row.prop(am_prop, 'show_guide', icon='QUESTION')
        if am_prop.show_guide:
            row=layout.box()
            row.separator()
            row.label(text="1.  Open the Image Browser. Navigate to a valid directory.  Click 'Accept'.")
            row.label(text="2.  Click the 'Load Directory' button.  AutoMat will try to sort your PBR textures.")
            row.label(text="3.  You can overide each image by using the adjacent Image Browser.")
            row.label(text="4.  Click 'Update Directories' to confirm any changes.")
            row.label(text="5.  Click 'Build Material' to finalize.")
            row.separator()
            
            row.scale_y = 0.5
            
        row=layout.box()
        row.prop(am_prop, 'parent_path', icon='BOOKMARKS')
        row.scale_y = 1.5
        #row.operator('am.tool', text="I'm a Tool", icon='FILE_REFRESH')
        row.operator('am.load', icon='FILE_REFRESH', text="Load Texture Data")
        
        split = layout.split(align=False, factor = am_prop.move_split)
        col = split.column(align = False)
        col.scale_x = 2
        col.prop(am_prop, 'albedo_name', icon='EVENT_A')
        col.prop(am_prop, 'ao_name', icon='EVENT_O')
        col.prop(am_prop, 'metal_name', icon='EVENT_M')
        col.prop(am_prop, 'rough_name', icon='EVENT_R')
        col.prop(am_prop, 'normal_name', icon='EVENT_N')
        col.prop(am_prop, 'mask_name', icon='EVENT_M')
        col.prop(am_prop, 'bump_name', icon='EVENT_B')
        col.prop(am_prop, 'displace_name', icon='EVENT_D')
        col.scale_y = y_ht
        
        col = split.column(align=False)

        if am_prop.sel_albedo:
            col.prop(am_prop, 'albedo_path', icon='SEQUENCE_COLOR_04')
        else:
            col.prop(am_prop, 'albedo_path', icon='SEQUENCE_COLOR_01')
        if am_prop.sel_ao:
            col.prop(am_prop, 'ao_path', icon='SEQUENCE_COLOR_04')
        else:    
            col.prop(am_prop, 'ao_path', icon='SEQUENCE_COLOR_01')
        if am_prop.sel_metal:
            col.prop(am_prop, 'metal_path', icon='SEQUENCE_COLOR_04')
        else:
            col.prop(am_prop, 'metal_path', icon='SEQUENCE_COLOR_01')
        if am_prop.sel_rough:
            col.prop(am_prop, 'rough_path', icon='SEQUENCE_COLOR_04')
        else:  
            col.prop(am_prop, 'rough_path', icon='SEQUENCE_COLOR_01')
        if am_prop.sel_normal:
            col.prop(am_prop, 'normal_path', icon='SEQUENCE_COLOR_04')
        else:
            col.prop(am_prop, 'normal_path', icon='SEQUENCE_COLOR_01')
        if am_prop.sel_mask:
            col.prop(am_prop, 'mask_path', icon='SEQUENCE_COLOR_04')
        else:
            col.prop(am_prop, 'mask_path', icon='SEQUENCE_COLOR_01')
        if am_prop.sel_bump:
            col.prop(am_prop, 'bump_path', icon='SEQUENCE_COLOR_04')
        else:
            col.prop(am_prop, 'bump_path', icon='SEQUENCE_COLOR_01')
        if am_prop.sel_displace:
            col.prop(am_prop, 'displace_path', icon='SEQUENCE_COLOR_04')
        else:
            col.prop(am_prop, 'displace_path', icon='SEQUENCE_COLOR_01')
            
        col.scale_y = y_ht
        row = layout.row()

        row=layout.box()
        row.operator('am.update', text="Update Changes", icon='FILE_REFRESH')
        row.scale_y = 1.5
        
        row=layout.row()
        row=layout.box()
        row.prop(am_prop, 'show_options', icon='OPTIONS')
        if am_prop.show_options:
            row=layout.row()
            row.label(text="Active Images:")
            row=layout.row()
            split = layout.split(align=True)
            col = split.column(align=True)
            
            row=layout.row()
            col.prop(am_prop, 'sel_albedo', text="Albedo")
            col.prop(am_prop, 'sel_ao', text="Ambient Occlusion")
            col.prop(am_prop, 'sel_metal', text="Metallic")
            col.prop(am_prop, 'sel_rough', text="Roughness")
            col = split.column(align=True)
            col.prop(am_prop, 'sel_normal', text="Normal")
            col.prop(am_prop, 'sel_mask', text = "Mask")
            col.prop(am_prop, 'sel_bump', text = "Bump")
            col.prop(am_prop, 'sel_displace', text = "Displace")
            row=layout.row()
            row.label(text="")
            row.scale_y = 0.1
            row=layout.row()
            row.prop(am_prop, 'use_autoname')
            row=layout.row()
            row=layout.row()
            row.prop(am_prop, 'use_box_proj', text="Use Box Projection")
            row.prop(am_prop, 'box_blend', text="Blend")
            row.scale_y = y_ht
            row=layout.row()
                
            row=layout.row()
            row.prop(am_prop, 'use_mat_index')
            row.prop(am_prop, 'mat_index_slider')
            row.scale_y = y_ht
            row=layout.row()
            row=layout.row()
            row=layout.box()
            row.prop(am_prop, 'show_extras', icon='OPTIONS')
            if am_prop.show_extras:
                row=layout.row()
                row.prop(am_prop, 'move_split')
                row=layout.row()
                row.prop(am_prop, 'clear_console', text="Clear System Console on Build/Udate")
                row=layout.row()
                row.operator('am.tog_console', icon = 'CONSOLE')
                row.operator('am.cleaner', text="Clean Unused Datablocks", icon='ERROR')
                row.scale_y = 1.1
                row=layout.row()
                row.operator('am.reset_props', text="Reset All Properties to Default", icon='ERROR')
                row.scale_y = 1.1
        row=layout.box()
        row=layout.row()
        row=layout.row()
        row.scale_x = 0.25
        row.label(text="")
        row.scale_x = 1.0
        row.prop(am_prop, 'new_mat_name', icon='MATERIAL')
        row.scale_x = 0.25
        row.label(text="")
        row.scale_y = 1.5
        
        row=layout.row()
        row=layout.box()
        row.operator('am.build_material', text="Build Material", icon='FILE_REFRESH')
        row.scale_y = 2.5
        
        
class AM_OT_LOAD_DATA(bpy.types.Operator):
    bl_label = "Load Data"
    bl_idname = 'am.load'
    bl_description="Load Texture Data from File"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        am_prop = bpy.context.scene.am_properties
        if am_prop.clear_console:
            _clearconsole()
        print("Loading Texture Data from File...\n")
        if am_prop.use_autoname:
            print("Use Autoname = {}".format(am_prop.use_autoname))
            name_split = str(os.path.splitext(am_prop.albedo_name)[0])
            name = re.split('_', name_split)[0]
            am_prop.new_mat_name = name

        am_prop.albedo_path = ""
        am_prop.ao_path = ""
        am_prop.metal_path = ""
        am_prop.rough_path = ""
        am_prop.normal_path = ""
        am_prop.mask_path = ""
        am_prop.bump_path = ""
        am_prop.displace_path = ""
        
        am_prop.albedo_name = ""
        am_prop.ao_name = ""
        am_prop.metal_name = ""
        am_prop.rough_name = ""
        am_prop.normal_name = ""
        am_prop.mask_name = ""
        am_prop.bump_name = ""
        am_prop.displace_name = ""
        
        am_prop.sel_albedo = False
        am_prop.sel_ao = False
        am_prop.sel_metal = False
        am_prop.sel_rough = False
        am_prop.sel_normal = False
        am_prop.sel_mask = False
        am_prop.sel_bump = False
        am_prop.sel_displace = False
        
        
        #d_path = os.path.dirname(bpy.data.filepath)
        #search_path = d_path + am_prop.parent_path
        exts = [".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".tga", ".exr"]
        lst_albedo_sort = ["_a.", "_albedo", "_d.", "_dif.", "_diffuse", "_c.", "_col", "_color"]
        lst_ao_sort = ["_ao.", "_o.", "_occ.", "ambientocclusion"]
        lst_metal_sort = ["_m.", "_met", "_metal", "_metallic", "_metalness"]
        lst_rough_sort = ["_r.", "_rgh", "_rough", "_roughness"]
        lst_normal_sort = ["_n.", "_nm.", "_nrm.", "_nor.", "_norm", "_normal"]
        lst_mask_sort = ["_ma.", "_msk.", "_mask", "_op.", "_om.", "_opacity", "_opmask."]
        lst_bump_sort = ["_b.", "_bmp.", "_bump.", "_bmap.", "_bm."]
        lst_displace_sort = ["_di.", "_dis.", "_disp.", "_displace", "_displacement"]
        valid_exts = []
        
        is_file = os.path.isfile(am_prop.parent_path)
        if is_file:
            head, tail = os.path.split(am_prop.parent_path)
            am_prop.parent_path = head
            print("Head: {}\nTail: {}".format(head, tail))
            
        if os.path.exists(am_prop.parent_path):
            for file in os.listdir(am_prop.parent_path):
                if any (file.lower().endswith(s) for s in exts):
                    valid_exts.append(file)
                    
            print("Found {} Valid Images: ".format(len(valid_exts)), valid_exts, "\n")
                
            for e in valid_exts:
                for t in lst_albedo_sort:
                    if t in e.lower():               
                        am_prop.albedo_path = os.path.join(am_prop.parent_path, e)
                        am_prop.albedo_name = e
                        am_prop.sel_albedo = True
                        print("Albedo File: ", e)
                        print("Albedo Path: ", am_prop.albedo_path, "\n")

            for e in valid_exts:
                for t in lst_ao_sort:
                    if t in e.lower():     
                        am_prop.ao_path = os.path.join(am_prop.parent_path, e)
                        am_prop.ao_name = e
                        am_prop.sel_ao = True
                        print("AO File: ", e)
                        print("AO Path: ", am_prop.ao_path, "\n")

            for e in valid_exts:
                for t in lst_metal_sort:
                    if t in e.lower():     
                        am_prop.metal_path = os.path.join(am_prop.parent_path, e)
                        am_prop.metal_name = e
                        am_prop.sel_metal = True
                        print("Metallic File: ", e)
                        print("Metallic Path: ", am_prop.metal_path, "\n")

            for e in valid_exts:
                for t in lst_rough_sort:
                    if t in e.lower():     
                        am_prop.rough_path = os.path.join(am_prop.parent_path, e)
                        am_prop.rough_name = e
                        am_prop.sel_rough = True
                        print("Roughness File: ", e)
                        print("Roughness Path: ", am_prop.rough_path, "\n")                        
        
            for e in valid_exts:
                for t in lst_normal_sort:
                    if t in e.lower():     
                        am_prop.normal_path = os.path.join(am_prop.parent_path, e)
                        am_prop.normal_name = e
                        am_prop.sel_normal = True
                        print("Normal File: ", e)
                        print("Normal Path: ", am_prop.normal_path, "\n")
                  
            for e in valid_exts:
                for t in lst_mask_sort:
                    if t in e.lower():     
                        am_prop.mask_path = os.path.join(am_prop.parent_path, e)
                        am_prop.mask_name = e
                        am_prop.sel_mask = True
                        print("Mask File: ", e)
                        print("Mask Path: ", am_prop.normal_path, "\n")
                          
            for e in valid_exts:
                for t in lst_bump_sort:
                    if t in e.lower():     
                        am_prop.bump_path = os.path.join(am_prop.parent_path, e)
                        am_prop.bump_name = e
                        am_prop.sel_bump = True
                        print("Bump File: ", e)
                        print("Bump Path: ", am_prop.normal_path, "\n")
                        
            for e in valid_exts:
                for t in lst_displace_sort:
                    if t in e.lower():     
                        am_prop.displace_path = os.path.join(am_prop.parent_path, e)
                        am_prop.displace_name = e
                        am_prop.sel_displace = True
                        print("Displacement File: ", e)
                        print("Displacement Path: ", am_prop.displace_path, "\n")
                        
            if not am_prop.albedo_name:
                am_prop.albedo_path = am_prop.parent_path                
            if not am_prop.ao_path:
                am_prop.ao_path = am_prop.parent_path
            if not am_prop.metal_path:
                am_prop.metal_path = am_prop.parent_path
            if not am_prop.rough_name:
                am_prop.rough_path = am_prop.parent_path
            if not am_prop.normal_path:
                am_prop.normal_path = am_prop.parent_path
            if not am_prop.mask_path:
                am_prop.mask_path = am_prop.parent_path
            if not am_prop.bump_path:
                am_prop.bump_path = am_prop.parent_path
            if not am_prop.displace_path:
                am_prop.displace_path = am_prop.parent_path
            
        else:
            print("Failed to find path '{}'".format(am_prop.parent_path))
        return {'FINISHED'}
    
    
class AM_OT_UPDATE(bpy.types.Operator):
    bl_label = "Update Changes"
    bl_idname = 'am.update'
    bl_description="Update Changes"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        print("Updating Changes")
        am_prop = bpy.context.scene.am_properties
        if am_prop.clear_console:
            _clearconsole()
        if am_prop.use_autoname:
            print("Use Autoname = {}".format(am_prop.use_autoname))
            name_split = str(os.path.splitext(am_prop.albedo_name)[0])
            name = re.split('_', name_split)[0]
            am_prop.new_mat_name = name
        exts = [".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".tga", ".exr"]
        
        if os.path.isfile(am_prop.albedo_path):
            head, tail = os.path.split(am_prop.albedo_path)
            if any (tail.lower().endswith(s) for s in exts):
                am_prop.albedo_name = tail
                am_prop.sel_albedo = True
            else:
                am_prop.albedo_name = ""
                am_prop.sel_albedo = False
        else:
            am_prop.sel_albedo = False
            
        if os.path.isfile(am_prop.ao_path):
            head, tail = os.path.split(am_prop.ao_path)
            if any (tail.lower().endswith(s) for s in exts):
                am_prop.ao_name = tail
                am_prop.sel_ao = True
            else:
                am_prop.ao_name = ""
                am_prop.sel_ao = False
        else:
            am_prop.sel_ao = False
            
        if os.path.isfile(am_prop.metal_path):
            head, tail = os.path.split(am_prop.metal_path)
            if any (tail.lower().endswith(s) for s in exts):
                am_prop.metal_name = tail
                am_prop.sel_metal = True
            else:
                am_prop.metal_name = ""
                am_prop.sel_metal = False
        else:
            am_prop.sel_metal = False
                
        if os.path.isfile(am_prop.rough_path):
            head, tail = os.path.split(am_prop.rough_path)
            if any (tail.lower().endswith(s) for s in exts):
                am_prop.rough_name = tail
                am_prop.sel_rough = True
            else:
                am_prop.rough_name = ""
                am_prop.sel_rough = False
        else:
            am_prop.sel_rough = False
                
        if os.path.isfile(am_prop.normal_path):
            head, tail = os.path.split(am_prop.normal_path)
            if any (tail.lower().endswith(s) for s in exts):
                am_prop.normal_name = tail
                am_prop.sel_normal = True
            else:
                am_prop.normal_name = ""
                am_prop.sel_normal = False
        else:
            am_prop.sel_normal = False
            
        if os.path.isfile(am_prop.mask_path):
            head, tail = os.path.split(am_prop.mask_path)
            if any (tail.lower().endswith(s) for s in exts):
                am_prop.mask_name = tail
                am_prop.sel_mask = True
            else:
                am_prop.mask_name = ""
                am_prop.sel_mask = False
        else:
            am_prop.sel_mask = False
            
        if os.path.isfile(am_prop.bump_path):
            head, tail = os.path.split(am_prop.bump_path)
            if any (tail.lower().endswith(s) for s in exts):
                am_prop.bump_name = tail
                am_prop.sel_bump = True
            else:
                am_prop.bump_name = ""
                am_prop.sel_bump = False
        else:
            am_prop.sel_bump = False
                
        if os.path.isfile(am_prop.rough_path):
            head, tail = os.path.split(am_prop.displace_path)
            if any (tail.lower().endswith(s) for s in exts):
                am_prop.displace_name = tail
                am_prop.sel_displace = True
            else:
                am_prop.displace_name = ""
                am_prop.sel_displace = False
        else:
            am_prop.sel_displace = False
              
        return {'FINISHED'}
    
class AM_OT_TOGGLE_CONSOLE(bpy.types.Operator):
    bl_label = "Toggle System Console"
    bl_idname = 'am.tog_console'
    bl_description="Toggle System Console"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        print("Toggle System Console")
        bpy.ops.wm.console_toggle()
  
        return {'FINISHED'}
    
class AM_OT_CLEANER(bpy.types.Operator):
    bl_label = "Delete Unused Data Blocks"
    bl_idname = 'am.cleaner'
    bl_description="Clean ALL unused data-blocks.  Use with Caution!"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        print("Purge Orphan Data")
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
  
        return {'FINISHED'}
    
class AM_OT_RESETPROPS(bpy.types.Operator):
    bl_label = "Reset All to Default"
    bl_idname = 'am.reset_props'
    bl_description="Reset all AutoMat Properties.  Use with Caution!"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        print("Reset AutoMat Properties")
        bpy.context.scene.property_unset("am_properties")
  
        return {'FINISHED'}

class AM_OT_BUILDMATERIAL(bpy.types.Operator):
    bl_label = "Batch Rename"
    bl_idname = 'am.build_material'
    bl_description="Build Material"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):        
        am_prop = bpy.context.scene.am_properties
        if am_prop.clear_console:
            _clearconsole()
        print("Building Material...\n")
#        if am_prop.use_autoname:
#            print("Use Autoname = {}".format(am_prop.use_autoname))
#            name_split = str(os.path.splitext(am_prop.albedo_name)[0])
#            name = re.split('_', name_split)[0]
#        am_prop.new_mat_name = name
        mat_name = am_prop.new_mat_name
        use_proj = am_prop.use_box_proj
        proj_blend = am_prop.box_blend
        
        img_list = []
        for img in bpy.data.images:
            img_list.append(img.name)
        img_set = set(img_list)
        print("LIST OF LOADED IMAGES:  ", img_set, "\n")
        
        mat_list = []
        for mat in bpy.data.materials:
            mat_list.append(mat.name)
        mat_set = set(mat_list)
        print("LIST OF LOADED MATERIALS:  ", mat_set, "\n")
        
        proj = 'FLAT'
        if use_proj:
            proj = 'BOX'
        else:
            proj = 'FLAT'
        print("Material Name: ", mat_name)
        print("Projection Mode: ", proj)
        print("Projection Blend: ", round(am_prop.box_blend, 2), "\n")

        #so = bpy.context.selected_objects
                 
        obj = bpy.context.view_layer.objects.active
        print("Active Object: ", obj.name, "\n")
           
        #for obj in so:
        new_mat = bpy.data.materials.new(name=mat_name)
        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes
        links = new_mat.node_tree.links
        img = bpy.data.materials
        
        shader = nodes["Principled BSDF"]
        shader.location = (0, 0)
        mat_output = nodes["Material Output"]
        mat_output.location = ( 400, 0)
        shader.inputs[0].default_value = (1.0,0.25,0.0,1.0)
        #if am_prop.sel_mask:
            #shader.
        
        if am_prop.new_mat_name not in mat_set:
            
            if am_prop.sel_albedo:
                img_albedo = nodes.new('ShaderNodeTexImage')
                img_albedo.location = (-700, 200)
                img_albedo.label = "Albedo"
                img_albedo.projection = proj
                img_albedo.projection_blend = proj_blend
                
                if am_prop.albedo_name not in img_set:
                    try:
                        img_albedo.image = bpy.data.images.load(am_prop.albedo_path)
                        img_albedo.image.colorspace_settings.name = 'sRGB'
                    except:
                        ph = "PLACEHOLDER_albedo"
                        if ph not in img_set:
                            print("Could not find Albedo image PATH")
                            img_albedo.image = bpy.data.images.new(name=ph, width=32, height=32)
                            img_albedo.image.generated_color = (1,1,1,1)     
                        else:
                              img_albedo.image = bpy.data.images[ph]
                else:
                    try:
                        img_albedo.image = bpy.data.images[am_prop.albedo_name]
                    except:
                        print("Could not load albedo image NAME") 
                                
            if am_prop.sel_ao:
                img_ao = nodes.new('ShaderNodeTexImage')
                img_ao.location = (-700, 500)
                img_ao.label = "Ambient Occlusion"
                ao_mix = nodes.new('ShaderNodeMixRGB')
                ao_mix.location = (-400, 300)
                ao_mix.label = "AO-Mix"
                ao_mix.blend_type = 'MULTIPLY'
                ao_mix.inputs[0].default_value = 1.0
                                           
                if am_prop.ao_name not in img_set:
                    try:
                        img_ao.image = bpy.data.images.load(am_prop.ao_path)
                        img_ao.image.colorspace_settings.name = 'sRGB'
                    except:
                        ph = "PLACEHOLDER_ao"
                        if ph not in img_set:
                            print("Could not find AO image PATH")
                            img_ao.image = bpy.data.images.new(name=ph, width=32, height=32)
                            img_ao.image.generated_color = (1,1,1,1)     
                        else:
                              img_ao.image = bpy.data.images[ph]
                else:
                    try:
                        img_ao.image = bpy.data.images[am_prop.ao_name]
                    except:
                        print("Could not load AO image NAME")       

            if am_prop.sel_metal:
                img_metal = nodes.new('ShaderNodeTexImage')
                img_metal.location = (-700, -100)
                img_metal.label = "Metallic"
                img_metal.projection = proj
                img_metal.projection_blend = proj_blend
                
                if am_prop.metal_name not in img_set:
                    try:
                        img_metal.image = bpy.data.images.load(am_prop.metal_path)
                        img_metal.image.colorspace_settings.name = 'Non-Color'
                    except:
                        ph = "PLACEHOLDER_metal"
                        if ph not in img_set:
                            print("Could not find METALLIC image PATH")
                            img_metal.image = bpy.data.images.new(name=ph, width=32, height=32)
                            img_metal.image.generated_color = (0,0,0,1)
                            img_metal.image.colorspace_settings.name = 'Non-Color'    
                        else:
                              img_metal.image = bpy.data.images[ph]
                else:
                    try:
                        img_metal.image = bpy.data.images[am_prop.metal_name]
                    except:
                        print("Could not load METAL image NAME")   
                

                
            if am_prop.sel_rough:
                img_rough = nodes.new('ShaderNodeTexImage')
                img_rough.location = (-700, -400)
                img_rough.label = "Roughness"
                img_rough.projection = proj
                img_rough.projection_blend = proj_blend

                if am_prop.rough_name not in img_set:
                    try:
                        img_rough.image = bpy.data.images.load(am_prop.rough_path)
                        img_rough.image.colorspace_settings.name = 'Non-Color'
                    except:
                        ph = "PLACEHOLDER_rough"
                        if ph not in img_set:
                            print("Could not find Roughness image PATH")
                            img_rough.image = bpy.data.images.new(name=ph, width=32, height=32)
                            img_rough.image.generated_color = (1,1,1,1) 
                        else:
                              img_rough.image = bpy.data.images[ph]
                else:
                    try:
                        img_rough.image = bpy.data.images[am_prop.rough_name]
                    except:
                        print("Could not load Roughness image NAME")    
                
            if am_prop.sel_normal:
            
                img_normal = nodes.new('ShaderNodeTexImage')
                img_normal.location = (-700, -700)
                img_normal.label = "Normal Map"
                img_normal.projection = proj
                img_normal.projection_blend = proj_blend
                nor_map = nodes.new("ShaderNodeNormalMap")
                nor_map.location = (-400, -700)

                if am_prop.normal_name not in img_set:
                    try:
                        img_normal.image = bpy.data.images.load(am_prop.normal_path)
                        img_normal.image.colorspace_settings.name = 'Non-Color'
                    except:
                        ph = "PLACEHOLDER_normal"
                        if ph not in img_set:
                            print("Could not find Normal Map image PATH")
                            img_normal.image = bpy.data.images.new(name=ph, width=32, height=32)
                            img_normal.image.generated_color = (0.5,0.5,1,1) 
                        else:
                              img_normal.image = bpy.data.images[ph]
                else:
                    try:
                        img_normal.image = bpy.data.images[am_prop.normal_name]
                    except:
                        print("Could not load Normal Map image NAME")
                        
            if am_prop.sel_mask:
            
                img_mask = nodes.new('ShaderNodeTexImage')
                img_mask.location = (-700, -1000)
                img_mask.label = "Opacity Mask"
                img_mask.projection = proj
                img_mask.projection_blend = proj_blend
                #new_mat.diffuse_color = (1,0,0,1)
                new_mat.blend_method = 'CLIP'
                new_mat.shadow_method = 'CLIP'

                if am_prop.mask_name not in img_set:
                    try:
                        img_mask.image = bpy.data.images.load(am_prop.mask_path)
                        img_mask.image.colorspace_settings.name = 'Non-Color'
                    except:
                        ph = "PLACEHOLDER_mask"
                        if ph not in img_set:
                            print("Could not find mask Map image PATH")
                            img_mask.image = bpy.data.images.new(name=ph, width=32, height=32)
                            img_mask.image.generated_color = (1,1,1,1)
                            img_mask.image.colorspace_settings.name = 'Non-Color' 
                        else:
                              img_mask.image = bpy.data.images[ph]
                              img_mask.image.colorspace_settings.name = 'Non-Color'
                else:
                    try:
                        img_mask.image = bpy.data.images[am_prop.mask_name]
                        img_mask.image.colorspace_settings.name = 'Non-Color'
                    except:
                        print("Could not load Opacity Mask image NAME")
                        
            if am_prop.sel_bump:
            
                img_bump = nodes.new('ShaderNodeTexImage')
                img_bump.location = (-1000, -700)
                img_bump.label = "Bump Map"
                img_bump.projection = proj
                img_bump.projection_blend = proj_blend
                #new_mat.diffuse_color = (1,0,0,1)
                #new_mat.blend_method = 'BLEND'
                #new_mat.shadow_method = 'CLIP'
                bmp_map = nodes.new("ShaderNodeBump")
                bmp_map.location = (-300, -500)
                bmp_map.inputs[0].default_value = 0.1

                if am_prop.bump_name not in img_set:
                    try:
                        img_bump.image = bpy.data.images.load(am_prop.bump_path)
                        img_bump.image.colorspace_settings.name = 'Non-Color'
                    except:
                        ph = "PLACEHOLDER_bump"
                        if ph not in img_set:
                            print("Could not find Bump Map image PATH")
                            img_bump.image = bpy.data.images.new(name=ph, width=32, height=32)
                            img_bump.image.generated_color = (0,0,0,1)
                            img_bump.image.colorspace_settings.name = 'Non-Color' 
                        else:
                              img_bump.image = bpy.data.images[ph]
                              img_bump.image.colorspace_settings.name = 'Non-Color'
                else:
                    try:
                        img_bump.image = bpy.data.images[am_prop.bump_name]
                        img_bump.image.colorspace_settings.name = 'Non-Color'
                    except:
                        print("Could not load Bump Map image NAME")
                        
            if am_prop.sel_displace:
            
                img_displace = nodes.new('ShaderNodeTexImage')
                img_displace.location = (300, -700)
                img_displace.label = "Displacement Map"
                img_displace.projection = proj
                img_displace.projection_blend = proj_blend

                if am_prop.displace_name not in img_set:
                    try:
                        img_displace.image = bpy.data.images.load(am_prop.displace_path)
                        img_displace.image.colorspace_settings.name = 'Non-Color'
                    except:
                        ph = "PLACEHOLDER_displace"
                        if ph not in img_set:
                            print("Could not find Displacement Map image PATH")
                            img_displace.image = bpy.data.images.new(name=ph, width=32, height=32)
                            img_displace.image.generated_color = (0,0,0,1)
                            img_displace.image.colorspace_settings.name = 'Non-Color' 
                        else:
                              img_displace.image = bpy.data.images[ph]
                              img_displace.image.colorspace_settings.name = 'Non-Color'
                else:
                    try:
                        img_displace.image = bpy.data.images[am_prop.displace_name]
                        img_displace.image.colorspace_settings.name = 'Non-Color'
                    except:
                        print("Could not load Displacement Map image NAME")
                        
            mapping = nodes.new('ShaderNodeMapping')
            mapping.location = (-1000, -150)
            
            if am_prop.use_box_proj:
                tex_coord = nodes.new('ShaderNodeTexCoord')
                tex_coord.location = (-1200, -150)
            
            else:        
                uv_map = nodes.new('ShaderNodeUVMap')
                uv_map.location = (-1200, -200)
                #uv_map.uv_map = "UV0"
                uv_map.uv_map = obj.data.uv_layers[0].name
            
            tiling = nodes.new('ShaderNodeValue')
            tiling.location = (-1200, -400)
            tiling.outputs[0].default_value = 1.0
            
            if am_prop.sel_albedo:
                links.new(img_albedo.outputs[0], shader.inputs[0])
                links.new(mapping.outputs[0], img_albedo.inputs[0])
            if am_prop.sel_ao:
                links.new(img_ao.outputs[0], ao_mix.inputs[2])
                links.new(img_albedo.outputs[0], ao_mix.inputs[1])
                links.new(ao_mix.outputs[0], shader.inputs[0])
                links.new(mapping.outputs[0], img_ao.inputs[0])
                
            if am_prop.sel_metal:
                links.new(img_metal.outputs[0], shader.inputs[6])
                links.new(mapping.outputs[0], img_metal.inputs[0])
            if am_prop.sel_rough:
                links.new(img_rough.outputs[0], shader.inputs[9])
                links.new(mapping.outputs[0], img_rough.inputs[0])
            if am_prop.sel_normal:
                links.new(nor_map.outputs[0], shader.inputs[22])
                links.new(img_normal.outputs[0], nor_map.inputs[1])
                links.new(mapping.outputs[0], img_normal.inputs[0])
                
            if am_prop.sel_mask:
                links.new(img_mask.outputs[0], shader.inputs[21])
                links.new(mapping.outputs[0], img_mask.inputs[0])
                
            if am_prop.sel_bump:
                links.new(img_bump.inputs[0], mapping.outputs[0])
                links.new(img_bump.outputs[0], bmp_map.inputs[2])
                links.new(bmp_map.outputs[0], shader.inputs[22])
                links.new(nor_map.outputs[0], bmp_map.inputs[3])
                links.new(bmp_map.inputs['Normal'], nor_map.outputs[0])
                
            if am_prop.sel_displace:
                links.new(img_displace.inputs[0], mapping.outputs[0])
                
            if am_prop.use_box_proj:
                links.new(tex_coord.outputs[3], mapping.inputs[0])
                links.new(tiling.outputs[0], mapping.inputs[3])
            if not am_prop.use_box_proj:
                links.new(uv_map.outputs[0], mapping.inputs[0])
                links.new(tiling.outputs[0], mapping.inputs[3])
                
            obj.data.materials.append(new_mat)
            obj.active_material_index = len(obj.data.materials) - 1
        
        else:
            print("Material '{}' already exists.".format(am_prop.new_mat_name))
            mat = bpy.data.materials.get(am_prop.new_mat_name)
            obj.data.materials.append(mat)
            
        so = bpy.context.selected_objects
        share_mat = bpy.data.materials.get(am_prop.new_mat_name)
        
        for o in so:
            if o.data.materials.get(share_mat.name) is None:
                print(o)
                print("tick")
                o.data.materials.append(share_mat)
                
        return {'FINISHED'}
        
classes = [AM_PROPERTIES,
            AM_OT_LOAD_DATA,
            AM_OT_UPDATE,
            AM_PT_AUTOMAT,
            AM_OT_TOGGLE_CONSOLE,
            AM_OT_CLEANER,
            AM_OT_RESETPROPS,
            AM_OT_BUILDMATERIAL,
            ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)        
    bpy.types.Scene.am_properties = bpy.props.PointerProperty(type = AM_PROPERTIES)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mt_properties
        
if __name__ == '__main__':
    register()
