'''
:type tool
:category Utilities|Selection
:group Selection
:supported_hosts [max]
:summary Runs a deep copy of all selected objects. Keeping data such as user properties, selection sets, and node properties.
'''
import juniper
import tools_library.jdcc.scene


copies = []
for node in tools_library.jdcc.scene.get_selection():
    copies.append(node.copy())
tools_library.jdcc.scene.set_selection(copies)

if(len(copies)):
    multiple = "" if len(copies) == 1 else "s"
    juniper.log.info(f"Copied {len(copies)} object{multiple}.")
