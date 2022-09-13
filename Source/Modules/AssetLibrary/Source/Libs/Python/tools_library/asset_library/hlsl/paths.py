"""
:TODO? Update shader library methods to work now they're merged with asset library
"""
import os
import glob

import juniper
import juniper.engine.types.plugin
import juniper.utilities.pathing as pathing_utils


def plugin():
    """
    :return <Plugin:plugin> The plugin wrapper for this plugin
    """
    return juniper.engine.types.plugin.PluginManager().find_plugin("asset_library")


def root():
    """Returns the directory to the root of this plugin"""
    return plugin().root


def shaders_dir():
    """Root directory of the hlsl shaders folder"""
    return os.path.join(
        root(),
        "shelves\\common\\shaders"
    ).lower()


def material_templates_dir():
    """Root directory of the material templates shaders folder"""
    return os.path.join(
        root(),
        "shelves\\common\\materialtemplates"
    ).lower()


def unreal_shaders_dir():
    """Root directory of the HLSL shaders source folder for Unreal"""
    return os.path.join(
        root(),
        "shelves\\unreal\\shaders"
    )

# -----------------------------------------------------------------------------------------

def get_shader_files(ignore_abstract=False):
    """Gets the paths to all .shader files
    :param [<bool:ignore_abstract>] Should abstract (template) materials be ignored?
    :return <[str]:paths> List containing the paths to all .shader files
    """
    output = []
    for i in glob.glob(shaders_dir() + "/**/*.shader", recursive=True):
        shader_name = os.path.basename(i).lower()
        if(not (ignore_abstract and shader_name.startswith("shd.abs"))):
            output.append(i.lower())
    for i in glob.glob(material_templates_dir() + "/**/*.shader", recursive=True):
        output.append(i.lower())
    return output


def find_shader_path(shader_name):
    """Attempt to find the path to a .shader from an input shader name"""
    shader_name = shader_name.lower()
    shader_paths = get_shader_files()
    for i in shader_paths:
        if(pathing_utils.get_filename_only(i) == shader_name):
            return i
    return ""


def get_unreal_shader_paths(ignore_abstract=False):
    """Return the path to the .uasset files matching to all .shader files"""
    output = []
    shaders_dir = os.path.join(root(), "shelves\\unreal\\content")
    for i in glob.glob(shaders_dir + "/**/shd_*.uasset", recursive=True):
        if(not ("shd_abs" in i.lower() and ignore_abstract)):
            output.append(i.lower())
    for i in glob.glob(shaders_dir + "/**/mt_*.uasset", recursive=True):
        output.append(i.lower())
    return output
