import os

import juniper
import juniper.engine.types.plugin
import juniper.utilities.string


def plugin():
    """
    :return <Plugin:plugin> The plugin wrapper for this plugin
    """
    return juniper.engine.types.plugin.PluginManager().find_plugin("asset_library")


def format_path(input_path):
    """
    Formats an input path string to match the standards
    :param <str:input_path> The path to format
    :return <str:formatted_path> The formatted path
    """
    output = input_path.replace("/", "\\")
    output = output.lower()
    output = output.rstrip("\\")
    if(output.endswith(":")):
        output += "\\"
    return output


def path():
    """Returns the path to the current Asset Library .assetlibrary file"""
    return juniper.utilities.json.get_property(
        user_settings_path(),
        "path"
    )


def root():
    """
    :return <str:root> The path to the root of the current Asset Library
    """
    return os.path.dirname(path())


def get_content_modules():
    """Returns paths to all content modules (Ie, "asset_library/content/common" """
    output = []
    for i in os.listdir(os.path.join(root(), "content")):
        dirname = os.path.join(root(), "content", i)
        if(not i[0] in [".", "_"] and os.path.isdir(dirname)):
            output.append(format_path(dirname))
    return output


# -----------------------------------------------------------------------------------------

def user_settings_path():
    return os.path.join(juniper.paths.root(), "Cached\\Plugins\\AssetLibrary\\user_settings.json")


# -----------------------------------------------------------------------------------------

def map_path(real_path):
    """Takes an input filepath and maps it to be relative to the current asset library"""
    real_path = format_path(real_path)
    output = juniper.utilities.string.remove_prefix(real_path, root())
    return output


def unmap_path(mapped_path):
    """Takes an input AssetLibrary relative filepath and returns the absolute file path"""
    mapped_path = format_path(mapped_path)
    return format_path(os.path.join(root(), mapped_path))


def resolve_path(target_path, relative_to=""):
    """Takes an input path and attempts to create a real path"""
    root_path = root()
    target_path = format_path(target_path)
    relative_to = format_path(relative_to)

    # if we've already got a real path
    if(target_path.startswith(root_path)):
        possible_output = os.path.abspath(target_path)
        if(os.path.isfile(possible_output)):
            return possible_output

    # if we're starting at a relative location then it has to be relative to something
    if(target_path.startswith("..")):
        possible_output = os.path.abspath(os.path.join(relative_to, target_path))
        return possible_output

    if(relative_to != ""):
        if(not relative_to.startswith(root_path)):
            relative_to = os.path.join(root_path, relative_to)

        # relative to current directory
        possible_path = os.path.abspath(os.path.join(relative_to, target_path))
        if(os.path.isfile(possible_path)):
            return possible_path

        # relative to asset library
        possible_path = os.path.abspath(os.path.join(root_path, target_path))
        if(os.path.isfile(possible_path)):
            return possible_path

    return ""
