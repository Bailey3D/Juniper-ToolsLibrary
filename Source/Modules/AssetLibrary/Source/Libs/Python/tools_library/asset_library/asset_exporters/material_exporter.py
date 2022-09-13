"""
Exporter class for material assets
"""
import os

import jdcc.types.assets.asset_exporter_template
import jdcc.scene
import juniper.decorators

import tools_library.asset_library.paths


class MaterialExporter(jdcc.types.assets.asset_exporter_template.AssetExporterTemplate):
    def __init__(self, target_asset):
        super().__init__(target_asset)

    # ------------------------------------------------------------

    def validate(self):
        if(self.scene is None):
            return False
        if(self.target_asset is None):
            return False
        return True

    def get_asset_name(self):
        raise NotImplementedError

    def get_export_dir(self):
        """
        Gets the export directory for this material
        :return <str:dir> The directory to export to
        """
        scene = self.scene
        scene_dir = os.path.dirname(scene.path)
        if(os.path.basename(scene_dir) == ".source"):
            output = os.path.join(os.path.dirname(scene.path), "..")
            # if we're exporting geometry, then segment this off into a "materials"
            # folder to avoid cluttering the root directory, as this will contain .geometry / .fbx data
            if(self.is_geometry_material):
                output = os.path.join(output, "materials")
        else:
            # for files not directly in the .source folder we export to an "exported" directory
            # as we cannot logically predict how these should be treated
            output = os.path.join(os.path.dirname(scene.path), "exported")
        return os.path.abspath(output)

    # ------------------------------------------------------------

    def export(self):
        textures_subdir = "textures"
        relative_to = os.path.join(tools_library.asset_library.paths.root(), "content")
        export_metadata = True
        success = self.target_asset.export(
            self.export_dir,
            textures_subdir=textures_subdir,
            relative_to=relative_to,
            export_metadata=export_metadata
        )
        if(success):
            self.exported_file_paths.append(self.target_asset.asset_interface.asset_path)
        return success

    def on_export(self):
        pass

    # ------------------------------------------------------------

    def pre_export(self):
        metadata_file_path = os.path.join(self.export_dir, self.target_asset.name + ".material")
        self.target_asset.load_asset_interface(metadata_file_path)
        return True

    @juniper.decorators.virtual_method
    def on_pre_export(self):
        pass

    @on_pre_export.override("painter")
    def __on_pre_export(self):
        # TODO~: We should have a way to programatically pick the right export preset
        # this should be asset library specific, and include logic for things such as
        # Alpha channel, thickness maps, subsurface maps, etc, when required.
        self.target_asset.asset_interface.set_metadata_key(
            "export:preset",
            "Asset Library - Surface Opaque",
            subgroup="painter"
        )

    # ------------------------------------------------------------

    def post_export(self):
        return True

    @juniper.decorators.virtual_method
    def on_post_export(self):
        pass

    @on_post_export.override("designer")
    def __on_post_export(self):
        import sd.juniper.package
        if(not self.is_geometry_material):
            # Only non-geometry materials should generate an SBSAR as they
            # can be used inside of shelves.
            package = sd.juniper.package.current()
            sbsar_path = sd.juniper.package.export_sbsar(package)
            sbsar_path = sbsar_path.replace("/", "\\")
            if(os.path.isfile(sbsar_path)):
                self.exported_file_paths.append(sbsar_path)

    # ------------------------------------------------------------

    def success(self):
        for i in self.exported_file_paths:
            tools_library.asset_library.log.info(f"Exported File: {i}")

    def on_success(self):
        pass

    def failure(self):
        tools_library.asset_library.log.error("Asset export failed!")

    def on_failure(self):
        pass

    # ------------------------------------------------------------

    @property
    def scene(self):
        return jdcc.scene.get_current()

    @property
    def is_geometry_material(self):
        """
        :return <bool:state> True if this is a geometry material (inside a "geometry" folder) - else False
        """
        return "\\geometry\\" in self.scene.path.lower()
