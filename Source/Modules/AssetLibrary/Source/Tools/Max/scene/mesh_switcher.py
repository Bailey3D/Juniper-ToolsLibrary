"""
:type tool
:category Asset Library|Geometry
:group Scene
:supported_hosts [max]
:summary Switches between individual meshes stored in the scene under "Export:" selection sets
"""
import pymxs
from qtpy import QtWidgets

import juniper
import tools_library.jdcc.scene
import juniper.mxs
import juniper.tooling
import juniper.tooling.tool_window


class MeshSwitcher(juniper.tooling.tool_window.ToolWindow):
    def __init__(self):
        super(MeshSwitcher, self).__init__(title="Mesh Switcher", uic=False)

        self.__init_ui()
        self.__refresh_ui()

        self.setFixedWidth(300)
        self.setFixedHeight(200)

    def __init_ui(self):
        self.q_selection_sets_list = QtWidgets.QListWidget()
        self.q_selection_sets_list.itemClicked.connect(self.on_switch)
        self.addWidget(self.q_selection_sets_list)

        self.q_btn_refresh = QtWidgets.QPushButton("Refresh..")
        self.addWidget(self.q_btn_refresh)
        self.q_btn_refresh.clicked.connect(self.__refresh_ui)

    def __refresh_ui(self):
        self.q_selection_sets_list.clear()

        for i in tools_library.jdcc.scene.get_current().selection_sets:
            if(i.name.startswith("Export:")):
                self.q_selection_sets_list.addItem(i.name.lstrip("Export:"))

    def on_switch(self, index):
        selection_set_name = "Export:" + index.text()

        for i in pymxs.runtime.objects:
            pymxs.runtime.hide(i)

        for i in tools_library.jdcc.scene.get_current().selection_sets:
            if(i.name == selection_set_name):
                i.show()

        pymxs.runtime.actionMan.executeAction(0, "310")  # Tools: Zoom Extents Selected
        pymxs.runtime.redrawViews()


dialog = juniper.tooling.run_standalone(MeshSwitcher, title="Mesh Switcher")
