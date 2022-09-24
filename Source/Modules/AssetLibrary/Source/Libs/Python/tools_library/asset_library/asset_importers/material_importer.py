"""
Importer class for material assets
"""
import os

import jdcc.material
import juniper.decorators
import jdcc.types.assets.asset_importer_template
import unreal.juniper
import unreal.juniper.content_browser as cb

import tools_library.asset_library.paths
import tools_library.asset_library.framework.types.texture_types


class MaterialImporter(jdcc.types.assets.asset_importer_template.AssetImporterTemplate):
    def __init__(self, asset_path):
        super().__init__(asset_path)

    def validate(self):
        if(os.path.isfile(self.asset_path)):
            return True
        return False

    @property
    def unreal_material_path(self):
        """
        :return <str:path> The unreal relative path to this asset
        """
        return cb.map_path(self.asset_path)

    def unmap_texture_path(self, path):
        if(os.path.isfile(path)):
            return path

        # map to asset library
        texture_path = os.path.join(tools_library.asset_library.paths.root(), "content", path)
        if(os.path.isfile(texture_path)):
            return texture_path

        # map to unreal project
        texture_path = os.path.join(unreal.juniper.unreal_project_dir(), "content", path)
        if(os.path.isfile(texture_path)):
            return texture_path

        return None

    # -------------------------------------------------------------------------

    def do_import(self):
        pass

    @juniper.decorators.virtual_method
    def on_do_import(self):
        pass

    @on_do_import.override("unreal")
    def __on_do_import(self):
        import unreal.juniper.materials.material as material
        import unreal.juniper.textures.texture as utexture

        unreal_parent_material_path = "/AssetLibrary/MaterialTemplates/Surface_Standard/MT_Surface_Standard"

        # 1) Create the base material
        material_asset = material.create_material_instance(
            self.unreal_material_path,
            unreal_parent_material_path,
            save=True
        )
        material_wrapper = jdcc.material.MaterialWrapper(material_asset)
        material_wrapper.load_asset_interface(self.asset_path)

        # 2) Loop all parameters and set them
        for i in material_wrapper.asset_interface.get_key_names("parameters"):
            param = material_wrapper.asset_interface.get_key(i, "parameters")

            if(hasattr(param, "__iter__") and not isinstance(param, str)):
                if(len(param) == 2):
                    param = juniper.types.math.vector.Vector2(param[0], param[1])
                if(len(param) == 3):
                    param = juniper.types.math.vector.Vector3(param[0], param[1], param[2])
                else:
                    param = juniper.types.math.vector.Vector4(param[0], param[1], param[2], param[3])
            material.set_parameter(material_asset, i, param)

        # 3) Loop set all texture parameters, import the asset if it doesn't exist
        for i in material_wrapper.asset_interface.get_group_data("textures"):
            v = material_wrapper.asset_interface.get_key(i, "textures")
            texture_path = self.unmap_texture_path(v)
            if(texture_path and os.path.isfile(texture_path)):
                texture_upath = cb.map_path(texture_path)
                texture_type_data = tools_library.asset_library.framework.types.texture_types.TextureTypes().find_from_path(texture_path)
                utexture.import_texture(
                    texture_path,
                    texture_upath,
                    save=True,
                    texture_compression_method=texture_type_data.unreal_compression_method,
                    srgb=texture_type_data.use_srgb
                )
                material.set_texture_parameter_value(material_asset, texture_type_data.parameter_name, texture_upath)
            else:
                tools_library.asset_library.log.error(f"Failed to import texture: {v}")

        # 4) Set all properties (Ie, "two_sided")
        if(material_wrapper.asset_interface.get_key("two_sided", "properties") is not None):
            material.set_two_sided(
                material_asset,
                material_wrapper.asset_interface.get_key("two_sided", "properties")
            )

        # 5) Save asset
        material.save_material(material_asset)

        return True

    # -------------------------------------------------------------------------

    def pre_import(self):
        pass

    def on_pre_import(self):
        pass

    # -------------------------------------------------------------------------

    def post_import(self):
        pass

    def on_post_import(self):
        pass

    # ----------------------------------------------------------------

    def success(self):
        pass

    def on_success(self):
        pass

    def failure(self):
        pass

    def on_failure(self):
        pass
