'''
:type tool
:category Selection
:group Selection
:supported_hosts [max]
:summary Creates an instance of currently selected objects
'''
import juniper
import juniper.dcc.scene


copies = []
for node in juniper.dcc.scene.get_selection():
    copies.append(node.instance())
juniper.dcc.scene.set_selection(copies)

if(len(copies)):
    multiple = "" if len(copies) == 1 else "s"
    juniper.log.info(f"Instanced {len(copies)} object{multiple}.")
