# TODO~ Juniper DCC: Replace with the class in `juniper.dcc.types.scene`
import os
import subprocess

import juniper.engine.decorators
import tools_library.jdcc.material
import tools_library.jdcc.scene.object_wrapper
import tools_library.jdcc.scene.selection_set_wrapper
import juniper.runtime.types.wrappers.type_wrapper


class SceneWrapperManager(juniper.runtime.types.wrappers.type_wrapper.TypeWrapperManager):
    pass


class SceneWrapper(juniper.runtime.types.wrappers.type_wrapper.TypeWrapper):
    """
    A wrapper class for the current scene depending on the current DCC application
    """
    __manager__ = SceneWrapperManager

    @property
    def path(self):
        """
        Get the path to the currently opened scene file respective of the current program
        :return <str:output> Path
        """
        return self.get_path().replace("/", "\\")

    @juniper.engine.decorators.virtual_method
    def get_path(self):
        raise NotImplementedError

    @get_path.override("max")
    def _get_path(self):
        import pymxs
        return os.path.join(pymxs.runtime.maxFilePath, pymxs.runtime.maxFileName)

    @get_path.override("designer")
    def _get_path(self):
        if(self.native_object):
            return self.native_object.getPackage().getFilePath()
        return None

    @get_path.override("painter")
    def _get_path(self):
        import substance_painter.project
        return substance_painter.project.file_path()

    @get_path.override("blender")
    def _get_path(self):
        import bpy
        return bpy.data.filepath

    # -------------------------------------------------------

    @property
    def name(self):
        """
        Gets the name of the current scene
        :return <str:name> The name of the current scene
        """
        return self.get_name()

    @juniper.engine.decorators.virtual_method
    def get_name(self):
        raise NotImplementedError

    @get_name.override("designer")
    def _get_name(self):
        return juniper.utilities.pathing.get_filename_only(self.get_path())

    @get_name.override("painter")
    def _get_name(self):
        import substance_painter.project
        return substance_painter.project.name()

    @get_name.override("max")
    def _get_name(self):
        import pymxs.juniper.scene
        output = pymxs.juniper.scene.name()
        if(output not in ("", None)):
            return output
        return None

    @get_name.override("blender")
    def _get_name(self):
        return os.path.basename(self.path).split(".")[0]

    # -------------------------------------------------------

    def explore(self):
        """
        Reveal the current scene file in windows explorer
        """
        subprocess.Popen(f'explorer /select,"{self.path}"')

    # -------------------------------------------------------

    @juniper.engine.decorators.virtual_method
    def save(self):
        """
        Save the current scene to disk - runs a save as if the file does not exist
        :return <bool:success> True if saved - else False
        """
        raise NotImplementedError

    @save.override("painter")
    def _save(self):
        try:
            import substance_painter.project
            if(substance_painter.project.is_open()):
                if(substance_painter.project.needs_saving()):
                    substance_painter.project.save()
                    return True
        except Exception:
            return False

    @juniper.engine.decorators.virtual_method
    def save_as(self, file_path=None):
        """
        Save the current file to disk
        :param [<str:file_path>] The path to save to - if None then a file picker will be used
        :return <bool:success> True if saved - else False
        """
        raise NotImplementedError

    # -------------------------------------------------------

    @juniper.engine.decorators.virtual_method
    def close(self, force=False):
        """
        Closes the current scene
        :param [<bool:force>] If True then the scene will be force closed without saving - else a save will be attempted
        """
        raise NotImplementedError

    @close.override("painter")
    def _close(self, force=False):
        import substance_painter.project
        if(not force):
            self.save()
        substance_painter.project.close()
        self.invalidate()

    # -------------------------------------------------------

    @property
    def materials(self):
        """
        :return <[MaterialWrapper]:materials> All materials in the current scene
        """
        return self.get_materials()

    @juniper.engine.decorators.virtual_method
    def get_materials(self):
        raise NotImplementedError

    @get_materials.override("painter")
    def _get_materials(self):
        import substance_painter.textureset
        output = []
        for i in substance_painter.textureset.all_texture_sets():
            output.append(tools_library.jdcc.material.MaterialWrapper(i))
        return output

    @get_materials.override("designer")
    def _get_materials(self):
        import sd
        import sd.juniper.package
        output = []
        current_package = sd.juniper.package.current()
        for i in sd.juniper.package.child_graphs(package=current_package):
            if(isinstance(i, sd.api.sbs.sdsbscompgraph.SDSBSCompGraph)):
                output.append(tools_library.jdcc.material.MaterialWrapper(i))
        return output

    # -------------------------------------------------------

    @property
    def objects(self):
        """
        Gets all objects in this scene
        :return <[ObjectWrapper]:objects> All objects in this scene
        """
        return self.get_objects()

    @juniper.engine.decorators.virtual_method
    def get_objects(self):
        raise NotImplementedError

    @get_objects.override("max")
    def __get_objects(self):
        import pymxs
        output = []
        for i in pymxs.runtime.objects:
            node = tools_library.jdcc.scene.object_wrapper.ObjectWrapper(i)
            output.append(node)
        return output

    # -------------------------------------------------------

    @property
    def selection_sets(self):
        return self.get_selection_sets()

    @juniper.engine.decorators.virtual_method
    def get_selection_sets(self):
        """
        :return <[SelectionSetWrapper]:selection_sets> All selection sets in the current scene
        """
        raise NotImplementedError

    @get_selection_sets.override("max")
    def __get_selection_sets(self):
        import pymxs
        output = []
        for i in pymxs.runtime.selectionSets:
            output.append(tools_library.jdcc.scene.selection_set_wrapper.SelectionSetWrapper(i))
        return output
