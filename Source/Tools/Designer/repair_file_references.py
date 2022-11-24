"""
Attempts to search for missing texture resources.
Initially searches down from the target directory recursively for files matching the name.
Falls back to searching directories up recursively for name matches.

:type tool
:group Utilities
:category Utilities|Scene
:supported_hosts [designer]
"""
import os
import shutil
import pathlib
import sd


context = sd.getContext()
application = context.getSDApplication()
package_manager = application.getPackageMgr()
ui_manager = application.getQtForPythonUIMgr()


MAX_UPPER_RECURSION_DIRS = 2


def GetCurrentGraph():
    return ui_manager.getCurrentGraph()


def GetCurrentPackage():
    return GetCurrentGraph().getPackage()


def FindFileRecursive(root_dir, file_name):
    files_down = pathlib.Path(root_dir).glob("**/*" + file_name)
    for file_down in files_down:
        file_down_name = os.path.basename(file_down).replace("XXXXXX-", "")
        if(file_name == file_down_name):
            return file_down
    return ""


if(GetCurrentGraph()):
    package = GetCurrentPackage()
    package_dependencies = package.getDependencies()
    package_resources = package.getChildrenResources(True)
    
    for i in package_resources:
        # bitmaps
        if(type(i) == sd.api.sdresourcebitmap.SDResourceBitmap):
            if(not os.path.isfile(i.getFilePath())):
                root_dir = os.path.dirname(i.getFilePath())
                file_name = os.path.basename(i.getFilePath()).replace("XXXXXX-", "")
                possible_file = FindFileRecursive(root_dir, file_name)
                if(len(possible_file)):
                    shutil.copyfile(possible_file, i.getFilePath())
                else:
                    target_dir = root_dir
                    for j in range(MAX_UPPER_RECURSION_DIRS):
                        target_dir = os.path.dirname(target_dir)
                    possible_file = FindFileRecursive(target_dir, file_name)
                    if(possible_file != ""):
                        shutil.copyfile(possible_file, i.getFilePath())
