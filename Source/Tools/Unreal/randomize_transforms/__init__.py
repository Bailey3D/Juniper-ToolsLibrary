'''
:type tool
:group Selection
:category Selection
:supported_hosts [unreal]
'''
import random
from qtpy import QtWidgets

import juniper
import juniper.tooling.tool_window
import juniper.widgets as qt_utils


class RandomizeTransforms(juniper.tooling.tool_window.ToolWindow):
    def __init__(self):

        self.translation_x = False
        self.translation_y = False
        self.translation_z = False

        self.rotation_x = False
        self.rotation_y = False
        self.rotation_z = False

        self.scale_uniform = True
        self.scale_x = False
        self.scale_y = False
        self.scale_z = False

        self.transforms_cache = {

        }


        super(RandomizeTransforms, self).__init__(title="Randomize Transforms", uic=False)

    # ---------------------------------------------------------------------------------

    def __add_spinners(self, title, parent, min, max, bind_checked=None, checked=False, default=0.0):

        q_spinner_layout = QtWidgets.QHBoxLayout()
        q_chk_state = QtWidgets.QCheckBox(title)
        parent.addLayout(q_spinner_layout)
        q_chk_state.setChecked(checked)

        q_spn_min = QtWidgets.QDoubleSpinBox()
        q_spn_min.setPrefix("Min: ")
        q_spn_min.setMinimum(min)
        q_spn_min.setMaximum(max)
        q_spn_min.setValue(default)

        q_spn_max = QtWidgets.QDoubleSpinBox()
        q_spn_max.setPrefix("Max: ")
        q_spn_max.setMinimum(min)
        q_spn_max.setMaximum(max)
        q_spn_max.setValue(default)

        q_spinner_layout.addWidget(q_chk_state)
        q_spinner_layout.addStretch()
        q_spinner_layout.addWidget(q_spn_min)
        q_spinner_layout.addWidget(q_spn_max)

        spinners_data = {
            "layout": q_spinner_layout,
            "checkbox": q_chk_state,
            "spinner_min": q_spn_min,
            "spinner_max": q_spn_max
        }

        if(bind_checked):
            q_chk_state.clicked.connect(bind_checked)

        return spinners_data

    def initialize_ui(self):
        """"""

        self.q_main_layout = QtWidgets.QVBoxLayout()
        self.addLayout(self.q_main_layout)

        def __add_group_widget(title):
            q_group_widget = QtWidgets.QGroupBox(title)
            q_group_layout = QtWidgets.QVBoxLayout(q_group_widget)
            self.q_main_layout.addWidget(q_group_widget)
            return q_group_layout

        # translation
        q_trans_group_widget = __add_group_widget("Translation:")
        self.translation_widgets = {
            "x": self.__add_spinners("X", q_trans_group_widget, -9999, 9999, bind_checked=self.__update_ui_translation),
            "y": self.__add_spinners("Y", q_trans_group_widget, -9999, 9999, bind_checked=self.__update_ui_translation),
            "z": self.__add_spinners("Z", q_trans_group_widget, -9999, 9999, bind_checked=self.__update_ui_translation)
        }
        self.__update_ui_translation()

        # rotation
        q_rot_group_widget = __add_group_widget("Rotation:")
        self.rotation_widgets = {
            "x": self.__add_spinners("X", q_rot_group_widget, -9999, 9999, bind_checked=self.__update_ui_rotation),
            "y": self.__add_spinners("Y", q_rot_group_widget, -9999, 9999, bind_checked=self.__update_ui_rotation),
            "z": self.__add_spinners("Z", q_rot_group_widget, -9999, 9999, bind_checked=self.__update_ui_rotation)
        }
        self.__update_ui_rotation()

        # scale
        q_scale_group_widget = __add_group_widget("Scale:")
        self.scale_widgets = {
            "uniform": self.__add_spinners("Uniform:", q_scale_group_widget, -9999, 9999, bind_checked=self.__update_ui_scale, checked=True, default=1.0),
            "x": self.__add_spinners("X", q_scale_group_widget, -9999, 9999, bind_checked=self.__update_ui_scale, default=1.0),
            "y": self.__add_spinners("Y", q_scale_group_widget, -9999, 9999, bind_checked=self.__update_ui_scale, default=1.0),
            "z": self.__add_spinners("Z", q_scale_group_widget, -9999, 9999, bind_checked=self.__update_ui_scale, default=1.0)
        }
        self.__update_ui_scale()

        # buttons
        q_btn_apply = QtWidgets.QPushButton("Randomize")
        q_btn_revert = QtWidgets.QPushButton("Reset")

        q_btn_apply.clicked.connect(self.randomize)
        q_btn_revert.clicked.connect(self.reset_transforms)

        self.addWidget(q_btn_apply)
        self.addWidget(q_btn_revert)

        self.addStretch()

    # ---------------------------------------------------------------------------------

    def __update_ui_translation(self):
        new_translation_x = self.translation_widgets["x"]["checkbox"].isChecked()
        new_translation_y = self.translation_widgets["y"]["checkbox"].isChecked()
        new_translation_z = self.translation_widgets["z"]["checkbox"].isChecked()

        stats = {"x": new_translation_x, "y": new_translation_y, "z": new_translation_z}
        for i in stats:
            self.translation_widgets[i]["spinner_min"].setEnabled(stats[i])
            self.translation_widgets[i]["spinner_max"].setEnabled(stats[i])

        self.translation_x = new_translation_x
        self.translation_y = new_translation_y
        self.translation_z = new_translation_z

    def __update_ui_rotation(self):
        new_rotation_x = self.rotation_widgets["x"]["checkbox"].isChecked()
        new_rotation_y = self.rotation_widgets["y"]["checkbox"].isChecked()
        new_rotation_z = self.rotation_widgets["z"]["checkbox"].isChecked()

        stats = {"x": new_rotation_x, "y": new_rotation_y, "z": new_rotation_z}
        for i in stats:
            self.rotation_widgets[i]["spinner_min"].setEnabled(stats[i])
            self.rotation_widgets[i]["spinner_max"].setEnabled(stats[i])

        self.rotation_x = new_rotation_x
        self.rotation_y = new_rotation_y
        self.rotation_z = new_rotation_z

    def __update_ui_scale(self):
        new_scale_uniform = self.scale_widgets["uniform"]["checkbox"].isChecked()
        new_scale_x = self.scale_widgets["x"]["checkbox"].isChecked()
        new_scale_y = self.scale_widgets["y"]["checkbox"].isChecked()
        new_scale_z = self.scale_widgets["z"]["checkbox"].isChecked()

        if(
            new_scale_x != self.scale_x or
            new_scale_y != self.scale_y or
            new_scale_z != self.scale_z
        ):
            new_scale_uniform = not any((new_scale_x, new_scale_y, new_scale_z))

        if(new_scale_uniform):
            for i in ("x", "y", "z"):
                self.scale_widgets[i]["checkbox"].setChecked(False)
                self.scale_widgets[i]["spinner_min"].setEnabled(False)
                self.scale_widgets[i]["spinner_max"].setEnabled(False)
            self.scale_widgets["uniform"]["spinner_min"].setEnabled(True)
            self.scale_widgets["uniform"]["spinner_max"].setEnabled(True)

        elif(any((new_scale_x, new_scale_y, new_scale_z))):
            self.scale_widgets["uniform"]["checkbox"].setChecked(False)
            self.scale_widgets["uniform"]["spinner_min"].setEnabled(False)
            self.scale_widgets["uniform"]["spinner_max"].setEnabled(False)

            stats = {"x": new_scale_x, "y": new_scale_y, "z": new_scale_z}
            for i in stats:
                self.scale_widgets[i]["spinner_min"].setEnabled(stats[i])
                self.scale_widgets[i]["spinner_max"].setEnabled(stats[i])

        self.scale_uniform = new_scale_uniform
        self.scale_x = new_scale_x
        self.scale_y = new_scale_y
        self.scale_z = new_scale_z

    # ---------------------------------------------------------------------------------

    @property
    def translation_min(self):
        return (
            self.translation_widgets["x"]["spinner_min"].value(),
            self.translation_widgets["y"]["spinner_min"].value(),
            self.translation_widgets["z"]["spinner_min"].value()
        )

    @property
    def translation_max(self):
        return (
            self.translation_widgets["x"]["spinner_max"].value(),
            self.translation_widgets["y"]["spinner_max"].value(),
            self.translation_widgets["z"]["spinner_max"].value()
        )

    # ---------------------------------------------------------------------------------

    @property
    def rotation_min(self):
        return (
            self.rotation_widgets["x"]["spinner_min"].value(),
            self.rotation_widgets["y"]["spinner_min"].value(),
            self.rotation_widgets["z"]["spinner_min"].value()
        )

    @property
    def rotation_max(self):
        return (
            self.rotation_widgets["x"]["spinner_max"].value(),
            self.rotation_widgets["y"]["spinner_max"].value(),
            self.rotation_widgets["z"]["spinner_max"].value()
        )

    # ---------------------------------------------------------------------------------

    @property
    def scale_min(self):
        return (
            self.scale_widgets["x"]["spinner_min"].value(),
            self.scale_widgets["y"]["spinner_min"].value(),
            self.scale_widgets["z"]["spinner_min"].value(),
            self.scale_widgets["uniform"]["spinner_min"].value()
        )

    @property
    def scale_max(self):
        return (
            self.scale_widgets["x"]["spinner_max"].value(),
            self.scale_widgets["y"]["spinner_max"].value(),
            self.scale_widgets["z"]["spinner_max"].value(),
            self.scale_widgets["uniform"]["spinner_max"].value()
        )

    # ---------------------------------------------------------------------------------

    def randomize(self):
        for i in self.selection:

            if(i not in self.transforms_cache):
                self.transforms_cache[i] = unreal.Transform(
                    i.get_actor_location(),
                    i.get_actor_rotation(),
                    i.get_actor_scale3d()
                )

            current_transform = self.transforms_cache[i]
            final_transform = unreal.Matrix.IDENTITY.transform()

            if(any((self.translation_x, self.translation_y, self.translation_z))):
                final_translation = current_transform.translation

                if(self.translation_x):
                    final_translation.x += random.uniform(self.translation_min[0], self.translation_max[0])
                if(self.translation_y):
                    final_translation.y += random.uniform(self.translation_min[1], self.translation_max[1])
                if(self.translation_z):
                    final_translation.z += random.uniform(self.translation_min[2], self.translation_max[2])

                final_transform.translation = unreal.Vector(final_translation.x, final_translation.y, final_translation.z)

            if(any((self.rotation_x, self.rotation_y, self.rotation_z))):
                final_rotation = current_transform.euler()

                if(self.rotation_x):
                    final_rotation[0] += random.uniform(self.rotation_min[0], self.rotation_max[0])
                if(self.rotation_y):
                    final_rotation[1] += random.uniform(self.rotation_min[1], self.rotation_max[1])
                if(self.rotation_z):
                    final_rotation[2] += random.uniform(self.rotation_min[2], self.rotation_max[2])

                final_transform.rotation = unreal.Rotator(final_rotation[0], final_rotation[1], final_rotation[2]).quaternion()

            if(any((self.scale_x, self.scale_y, self.scale_z, self.scale_uniform))):
                final_scale = current_transform.scale3d

                if(self.scale_uniform):
                    val = random.uniform(self.scale_min[3], self.scale_max[3])
                    final_scale = unreal.Vector(final_scale.x * val, final_scale.y * val, final_scale.z * val)
                else:
                    if(self.scale_x):
                        final_scale.x *= random.uniform(self.scale_min[0], self.scale_max[0])
                    if(self.scale_y):
                        final_scale.y *= random.uniform(self.scale_min[1], self.scale_max[1])
                    if(self.scale_z):
                        final_scale.z *= random.uniform(self.scale_min[2], self.scale_max[2])

                final_transform.scale3d = unreal.Vector(final_scale.x, final_scale.y, final_scale.z)

            i.set_actor_transform(final_transform, False, True)

    def __cache_selection_transforms(self):
        pass

    def reset_transforms(self):
        for i in self.transforms_cache:
            i.set_actor_transform(self.transforms_cache[i], False, True)

    @property
    def selection(self):
        return unreal.EditorLevelLibrary.get_selected_level_actors()
     

if(__name__ == "__main__" and juniper.program_context != "unreal"):

    app = qt_utils.get_application()
    a = RandomizeTransforms()
    a.show()
    app.exec_()

else:
    a = RandomizeTransforms()
