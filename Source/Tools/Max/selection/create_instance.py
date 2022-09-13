'''
:type tool
:category Selection
:group Selection
:supported_hosts [max]
:summary Creates an instance of currently selected objects
'''
import juniper
import jdcc.scene


copies = []
for node in jdcc.scene.get_selection():
    copies.append(node.instance())
jdcc.scene.set_selection(copies)

if(len(copies)):
    multiple = "" if len(copies) == 1 else "s"
    juniper.log.info(f"Instanced {len(copies)} object{multiple}.")
