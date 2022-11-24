'''
:type tool
:category Utilities|Selection
:group Selection
:supported_hosts [max]
:summary Merges all selected poly objects
'''
import pymxs

import tools_library


copies = []

for i in pymxs.runtime.selection:
    if(pymxs.runtime.superClassOf(i) == pymxs.runtime.geometryClass):
        copy = pymxs.runtime.copy(i)
        pymxs.runtime.convertToPoly(copy)
        copies.append(copy)

if(len(copies) <= 1):
    for i in copies:
        pymxs.runtime.delete(i)
else:
    num_merged = len(copies)
    final_obj = copies[0]
    for i in copies:
        s = pymxs.runtime.polyOp.attach(final_obj, i)
    pymxs.runtime.select(final_obj)
    final_obj.name = pymxs.runtime.uniqueName("merged_scene_objects_")
    tools_library.log.info(f"Merged {num_merged} objects.")
