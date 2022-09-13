'''
:type tool
:category Scene
:group Scene
:supported_hosts [max]
:summary Cleans the current max scene of all unused selection sets
'''
import pymxs


selection_sets = []
for i in pymxs.runtime.selectionSets:
    selection_sets.append(i)


for selection_set in selection_sets:
    if(selection_set.count == 0):
        pymxs.runtime.deleteItem(pymxs.runtime.selectionSets, selection_set)
