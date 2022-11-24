"""
:type tool
:category Asset Library|Export
:group Asset Library
:supported_hosts [max, designer]
:summary Exports all assets from the current scene context
"""
import juniper.decorators

import tools_library.jdcc.scene
import tools_library.jdcc.geometry
import tools_library.jdcc.material

import tools_library.asset_library
import tools_library.asset_library.asset_exporters.geometry_exporter
import tools_library.asset_library.asset_exporters.material_exporter
import tools_library.asset_library.paths


class Exporter(object):
    def __init__(self):
        pass

    @juniper.decorators.virtual_method
    def run(self):
        raise NotImplementedError

    @run.override("max")
    def _run(self):
        for i in tools_library.jdcc.scene.get_current().selection_sets:
            if(i.name.startswith("Export:")):
                target_asset = tools_library.jdcc.geometry.GeometryWrapper(i)
                exporter_instance = tools_library.asset_library.asset_exporters.geometry_exporter.GeometryExporter(target_asset)
                exporter_instance.execute()

    @run.override("designer")
    def _run(self):
        for i in tools_library.jdcc.scene.get_current().materials:
            exporter_instance = tools_library.asset_library.asset_exporters.material_exporter.MaterialExporter(i)
            exporter_instance.execute()


exporter = Exporter()
exporter.run()
