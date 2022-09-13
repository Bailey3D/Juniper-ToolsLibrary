'''
:type tool
:category Selection
:group Selection
:supported_hosts [max]
:summary Runs a deep copy of all selected objects. Keeping data such as user properties, selection sets, and node properties.
'''
import juniper
import jdcc.scene


copies = []
for node in jdcc.scene.get_selection():
    copies.append(node.copy())
jdcc.scene.set_selection(copies)

if(len(copies)):
    multiple = "" if len(copies) == 1 else "s"
    juniper.log.info(f"Copied {len(copies)} object{multiple}.")
