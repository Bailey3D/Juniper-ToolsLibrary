"""
:type tool
:category Export
:group Export
:supported_hosts [max, designer]
:summary Exports all assets from the current scene context
"""
import juniper.decorators

import jdcc.scene
import jdcc.geometry
import jdcc.material

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
        for i in jdcc.scene.get_current().selection_sets:
            if(i.name.startswith("Export:")):
                target_asset = jdcc.geometry.GeometryWrapper(i)
                exporter_instance = tools_library.asset_library.asset_exporters.geometry_exporter.GeometryExporter(target_asset)
                exporter_instance.execute()

    @run.override("designer")
    def _run(self):
        for i in jdcc.scene.get_current().materials:
            exporter_instance = tools_library.asset_library.asset_exporters.material_exporter.MaterialExporter(i)
            exporter_instance.execute()


exporter = Exporter()
exporter.run()
