'''
:type tool
:category Utilities|Transform
:group Selection
:supported_hosts [max]
:summary 
'''
import pymxs


if(pymxs.runtime.selection.count > 0):
    target = pymxs.runtime.pickObject()
    if(target):
        for i in pymxs.runtime.selection:
            i.position = target.position
            i.rotation = target.rotation
