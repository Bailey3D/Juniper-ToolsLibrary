"""
Exporter class for geometry assets
"""
import os

import jdcc.types.assets.asset_exporter_template
import jdcc.scene
import juniper.decorators
import juniper.utilities.string as string_utils

import tools_library.asset_library.paths


class GeometryExporter(jdcc.types.assets.asset_exporter_template.AssetExporterTemplate):
    def __init__(self, target_asset):
        super().__init__(target_asset)

    # ----------------------------------------------------------

    def validate(self):
        if(self.target_asset):
            return True
        return False

    def get_asset_name(self):
        return string_utils.remove_prefix(self.target_asset.name_only, "Export:")

    def get_export_dir(self):
        """
        Gets the export directory for the data for this geometry.
        """
        scene = jdcc.scene.get_current()
        scene_dir = os.path.dirname(scene.path)
        if(os.path.basename(scene_dir) == ".source"):
            output = os.path.join(os.path.dirname(scene.path), "..")
        else:
            # for files not directly in the .source folder we export to an "exported" directory
            # as we cannot logically predict how these should be treated
            output = os.path.join(os.path.dirname(scene.path), "exported")
        return os.path.abspath(output)

    # ----------------------------------------------------------

    def export(self):
        pass

    @juniper.decorators.virtual_method
    def on_export(self):
        pass

    @on_export.override("max")
    def __on_export(self):
        scene = self.scene
        if(scene):
            self.target_asset.export(
                self.export_dir,
                #meshes_subdir="meshes",
                #relative_to=tools_library.asset_library.paths.root(),
                filename_override=self.asset_name,
                export_asset_data=True
            )
            self.exported_file_paths.append(self.target_asset.asset_interface.asset_path)
            return True
        return False

    # ----------------------------------------------------------

    def pre_export(self):
        metadata_file_path = os.path.join(self.export_dir, self.asset_name + ".geometry")
        self.target_asset.load_asset_interface(metadata_file_path)
        return True

    # ----------------------------------------------------------

    def post_export(self):
        pass

    # ----------------------------------------------------------

    def success(self):
        for i in self.exported_file_paths:
            tools_library.asset_library.log.info(f"Exported File: {i}")

    def failure(self):
        pass

    # ----------------------------------------------------------

    @property
    def scene(self):
        return jdcc.scene.get_current()
