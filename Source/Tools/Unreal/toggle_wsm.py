'''
:type tool
:group Selection
:category Selection
:supported_hosts [unreal]
'''
import unreal


selection = unreal.EditorLevelLibrary.get_selected_level_actors()

for i in selection:
    custom_primitive_data = i.static_mesh_component.get_editor_property("custom_primitive_data")
    current_data = custom_primitive_data.get_editor_property("Data")
    if(len(current_data)):
        current_data[0] = 1.0 if current_data[0] == 0.0 else 0.0
    else:
        current_data.append(1.0)
    custom_primitive_data.set_editor_property("Data", current_data, unreal.PropertyAccessChangeNotifyMode.ALWAYS)
    i.static_mesh_component.set_editor_property("custom_primitive_data", custom_primitive_data, unreal.PropertyAccessChangeNotifyMode.ALWAYS)
