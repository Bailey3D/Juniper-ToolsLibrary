"""
Importer class for geometry assets
"""
import os

import juniper.decorators
import jdcc.types.assets.asset_importer_template


class GeometryImporter(jdcc.types.assets.asset_importer_template.AssetImporterTemplate):
    def __init__(self, asset_path):
        super().__init__(asset_path)

    def validate(self):
        if(os.path.isfile(self.asset_path) and os.path.isfile(self.fbx_path)):
            return True
        return False

    @property
    def unreal_geometry_path(self):
        """
        :return <str:path> The unreal relative path to this asset
        """
        import unreal.juniper.content_browser as cb
        return cb.map_path(self.asset_path)

    @property
    def fbx_path(self):
        """
        :return <str:path> The path to the .fbx file for this geometry
        """
        # TODO? Should meshes be stored in the metadata file? So we can have nested folders?
        return self.asset_path.replace(".geometry", ".fbx")

    # -------------------------------------------------------------------------

    def do_import(self):
        pass

    @juniper.decorators.virtual_method
    def on_do_import(self):
        pass

    @on_do_import.override("unreal")
    def __on_do_import(self):
        # 1) TODO~: Import all materials
        # ..

        # 2) Import geometry w/ settings
        import unreal.juniper.static_mesh
        import unreal.juniper.content_browser
        imported_asset = unreal.juniper.static_mesh.import_static_mesh(
            self.fbx_path,
            unreal.juniper.content_browser.map_path(self.fbx_path)
        )

        # 3) TODO~: Set materials
        # ..

        # 4) Save asset ..
        unreal.juniper.content_browser.save_asset(imported_asset)

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
