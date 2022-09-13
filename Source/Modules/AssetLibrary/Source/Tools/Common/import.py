"""
:type tool
:category Import
:group Import
:supported_hosts [unreal, max, designer, painter]
:summary Imports an asset to the current host application
"""
import os

import juniper.decorators
import juniper.utilities.filemgr

import tools_library.asset_library.paths
import tools_library.asset_library.asset_importers.geometry_importer


class Importer(object):
    def __init__(self):
        pass

    @juniper.decorators.virtual_method
    def run(self):
        raise NotImplementedError

    @run.override("max")
    def _run(self):
        raise NotImplementedError

    @run.override("designer")
    def _run(self):
        self.__import_material()

    @run.override("painter")
    def _run(self):
        self.__import_material()

    @run.override("unreal")
    def _run(self):
        import unreal.juniper
        target_asset = juniper.utilities.filemgr.pick_file(
            title="Pick File to Import..",
            file_types="Geometry (*.geometry)",
            start=unreal.juniper.unreal_project_dir()
        )
        if(target_asset and os.path.isfile(target_asset)):
            importer = tools_library.asset_library.asset_importers.geometry_importer.GeometryImporter(target_asset)
            importer.execute()

    # ------------------------------------------------------------------

    def __import_material(self):
        target_asset = juniper.utilities.filemgr.pick_file(
            title="Pick Target Material",
            file_types="Material Metadata (*.material)",
            start=tools_library.asset_library.paths.root()
        )
        if(target_asset and os.path.isfile(target_asset)):
            importer = tools_library.asset_library.asset_importers.material_importer.MaterialImporter(
                target_asset
            )
            importer.execute()


importer = Importer()
importer.run()
