'''
:type tool
:category Utilities|Selection
:group Selection
:supported_hosts [max]
:summary Creates an instance of currently selected objects
'''
import juniper
import tools_library.jdcc.scene


copies = []
for node in tools_library.jdcc.scene.get_selection():
    copies.append(node.instance())
tools_library.jdcc.scene.set_selection(copies)

if(len(copies)):
    multiple = "" if len(copies) == 1 else "s"
    juniper.log.info(f"Instanced {len(copies)} object{multiple}.")
