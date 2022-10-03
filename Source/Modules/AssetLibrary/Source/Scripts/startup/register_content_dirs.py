"""
:type script
:desc Registers the Asset Library content directories as unreal content directories
:desc to ensure we can map / unmap file paths
:callbacks [startup]
:supported_hosts [unreal]
"""
import os

import juniper
import juniper.engine.types.plugin

import unreal.juniper.content_browser


'''asset_library_plugin_ref = juniper.engine.types.plugin.PluginManager().find_plugin("asset_library")
unreal.juniper.content_browser.register_unreal_content_dir(
    os.path.join(asset_library_plugin_ref.root, "content"),
    "/AssetLibrary/"
)
'''
