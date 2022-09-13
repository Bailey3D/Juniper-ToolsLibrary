'''
:type tool
:category Selection
:group Selection
:supported_hosts [max]
:summary Splits an Editable Poly / Editable Mesh out into individual nodes for each of the sub-elements
'''
import pymxs

import pymxs.juniper.selection


split_objects = []
targets = pymxs.juniper.selection.get_or_pick_selection()

if(targets.count):
    for node in targets:
        node_class = pymxs.runtime.classOf(node)
        node_superclass = pymxs.runtime.superClassOf(node)

        # editable poly/mesh
        if(node_class in [pymxs.runtime.editable_mesh, pymxs.runtime.editable_poly]):
            temp_copy = pymxs.runtime.copy(node)
            temp_copy_name = node.name
            pymxs.runtime.convertToPoly(temp_copy)

            for i in range(temp_copy.getNumFaces()):
                if(temp_copy.getNumFaces() != 0):
                    pymxs.runtime.polyOp.setFaceSelection(temp_copy, pymxs.runtime.array(1))
                    temp_copy.selectElement()
                    elem = pymxs.runtime.polyOp.getFaceSelection(temp_copy)
                    elem_name = pymxs.runtime.uniqueName(temp_copy_name + "_elem_")
                    pymxs.runtime.polyOp.detachFaces(
                        temp_copy,
                        elem,
                        asNode=True,
                        name=elem_name
                    )
                    geo = pymxs.runtime.getNodeByName(elem_name)
                    split_objects.append(geo)

                    pymxs.runtime.convertToPoly(geo)
                    pymxs.runtime.resetXForm(geo)
                    pymxs.runtime.resetTransform(geo)
                    pymxs.runtime.resetScale(geo)
                    pymxs.runtime.resetPivot(geo)
                    pymxs.runtime.centerPivot(geo)
                else:
                    break

            pymxs.runtime.delete(temp_copy)


    split_objects_mxs_array = pymxs.runtime.array()
    for i in split_objects:
        pymxs.runtime.append(split_objects_mxs_array, i)
    pymxs.runtime.select(split_objects_mxs_array)
