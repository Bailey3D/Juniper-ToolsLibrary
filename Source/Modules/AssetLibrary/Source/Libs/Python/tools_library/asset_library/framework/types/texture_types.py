"""
Library containing wrappers for the texture_types.json.
Used to programatically load in settings for different texture types depending on their suffixes.
See "/AssetLibrary/config/common/texture_types.json"
"""
import json
import os

from juniper.runtime.types.framework.singleton import Singleton
import juniper.engine.paths


class TextureType(object):
    def __init__(self, name, data):
        """
        Wrapper for the texture_types.json file
        Used to get information on how a texture asset should be set up from its suffix.
        :param <str:name> The suffix name (Ie, "d", "n")
        :param <{}:data> The data as stored in the texture_types.json
        """
        self._name = name.lower()
        self._data = data

    @property
    def use_srgb(self):
        """
        :return <bool:state> True if SRGB should be used - else False (If undefined, None will be returned)
        """
        if("srgb" in self._data):
            return self._data["srgb"]
        return None

    @property
    def name(self):
        """
        :return <str:name> The name of this texture type (Ie, "d", "n")
        """
        return self._name

    @property
    def identifier(self):
        """
        :return <str:identifier> The friendly name of this texture type
        """
        if("identifier" in self._data):
            return self._data["identifier"]
        return None

    @property
    def unreal_compression_method(self):
        """
        :return <CompressionMethod:compression_method> The unreal based compression method - None if not found
        """
        import unreal.juniper.textures.compression
        if("unreal_compression_method" in self._data):
            return unreal.juniper.textures.compression.get_unreal_compression_method(
                self._data["unreal_compression_method"]
            )
        return None

    @property
    def parameter_name(self):
        """
        :param <str:name> The name of the parameter a texture of this type should target (Ie, "NormalMap")
        """
        if("parameter_name" in self._data):
            return self._data["parameter_name"]
        return None


class TextureTypes(object, metaclass=Singleton):
    def __init__(self):
        """
        Wrapper for the texture_types.json file.
        """
        self.texture_types_config_path = juniper.engine.paths.get_config("texture_types.json", plugin="AssetLibrary")
        with open(self.texture_types_config_path, "r") as f:
            self._data = json.load(f)

        self.items = []
        for i in self._data:
            self.items.append(TextureType(i, self._data[i]))

    def find(self, texture_type):
        """
        Finds the data on a given texture type
        :param <str:texture_type> The texture type to find data on (Ie, "da", "n")
        :return <TextureType:texture_type> The texture type if found - else None
        """
        texture_type = texture_type.lower()
        if(texture_type in self._data):
            for i in self.items:
                if(i.name == texture_type):
                    return i
        return None

    def find_from_path(self, texture_path):
        filename = os.path.basename(texture_path)
        filename = filename.split(".")[0]
        filename = filename.split("_")[-1]
        return self.find(filename)
