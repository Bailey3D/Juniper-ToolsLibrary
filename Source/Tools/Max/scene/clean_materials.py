'''
:type tool
:category Utilities|Scene
:group Scene
:supported_hosts [max]
:summary Cleans the current max scene of all unused materials
'''
import pymxs


all_materials = []
for i in pymxs.runtime.mEditMaterials:
    all_materials.append(i)
used_materials = []

for i in pymxs.runtime.objects:
    current_material = None
    try:
        current_material = i.material
    except:
        pass
    else:
        if(current_material not in used_materials):
            used_materials.append(current_material)

i = 1
for mat in pymxs.runtime.mEditMaterials:
    if(mat not in used_materials):
        pymxs.runtime.setMeditMaterial(
            i,
            pymxs.runtime.standardMaterial()
        )
        pymxs.runtime.mEditMaterials[i - 1].name = ""
        i += 1
