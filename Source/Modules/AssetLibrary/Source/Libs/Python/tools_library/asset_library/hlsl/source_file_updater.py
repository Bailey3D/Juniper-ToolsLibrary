import os
import shutil
import glob

import tools_library.asset_library
import tools_library.asset_library.hlsl.paths


def update_shaders():
    """Copy all source .hlsl files from the shader library to the unreal/shaders folder
    and conver them from ".hlsl" to ".ush" as required by Unreal
    """
    shaders_dir = tools_library.asset_library.hlsl.paths.shaders_dir()
    unreal_shaders_dir = os.path.join(tools_library.asset_library.hlsl.paths.root(), "shelves\\unreal\\shaders")

    if(os.path.isdir(unreal_shaders_dir)):
        os.system('rmdir /S /Q "{}"'.format(unreal_shaders_dir))

    shutil.copytree(shaders_dir, unreal_shaders_dir)

    for i in glob.glob(unreal_shaders_dir + "/**", recursive=True):
        if(i.endswith(".hlsl")):
            new_path = i.replace(".hlsl", ".ush")
            os.rename(i, new_path)
            with open(new_path, "r") as f:
                old_lines = f.readlines()
                for i in range(len(old_lines)):
                    old_lines[i] = old_lines[i].replace(".hlsl", ".ush")
            with open(new_path, "w") as f:
                f.writelines(old_lines)

    tools_library.asset_library.log.info("Updated shader source HLSL files.")
