'''
:type tool
:category Utilities|Scene
:group Scene
:summary Reveals the current max scene in explorer
:supported_hosts [max, unreal, designer, painter, blender]
'''
import tools_library.jdcc.scene


scene = tools_library.jdcc.scene.get_current()

if(scene):
    scene.explore()
