"""
:type tool
:category Asset Library
:group Asset Library
:icon icons\\standard\\folder.png
:desc Open a new explorer window at the current asset library root directory
"""
import os

import tools_library.asset_library


os.startfile(tools_library.asset_library.paths.root())
