'''
:type tool
:category Scene
:group Scene
:summary Reveals the current max scene in explorer
:supported_hosts [max, unreal, designer, painter, blender]
'''
import jdcc.scene


scene = jdcc.scene.get_current()

if(scene):
    scene.explore()
