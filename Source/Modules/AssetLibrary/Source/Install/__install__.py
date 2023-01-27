"""
:type install
:desc Prompts the user to pick a valid .assetlibrary file and initializes the paths
"""
import os
import json

import juniper.utilities.filemgr
import juniper.utilities.json as json_utils
import juniper.runtime.widgets

import tools_library.asset_library.paths


asset_library_path = juniper.utilities.filemgr.pick_file(
    title="Select Asset Library",
    file_types="Asset Library (*.assetlibrary)",
    start=tools_library.asset_library.paths.root())


asset_library_path = asset_library_path.replace("/", "\\")


if(os.path.isfile(asset_library_path)):
    user_config_path = tools_library.asset_library.paths.user_settings_path()
    if(not os.path.isfile(user_config_path)):
        if(not os.path.isdir(os.path.dirname(user_config_path))):
            os.makedirs(os.path.dirname(user_config_path))
        with open(user_config_path, "w") as f:
            json.dump({}, f)

    json_utils.set_file_property(
        user_config_path,
        "path",
        asset_library_path.lower(),
        local=True
    )
