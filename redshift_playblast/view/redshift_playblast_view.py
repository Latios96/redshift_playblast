"""
Based on pyvfx-boilerplate https://github.com/fredrikaverpil/pyvfx-boilerplate
The MIT License (MIT)

Copyright (c) 2016 Fredrik Averpil

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import sys

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# Window title and object names
WINDOW_TITLE = 'Redshift Playblast'
WINDOW_OBJECT = 'RedshiftPlayblast'

# Repository path
UI_PATH = os.path.dirname(__file__)


# ----------------------------------------------------------------------
# Main script
# ----------------------------------------------------------------------

from Qt import QtWidgets  # pylint: disable=E0611
from Qt import QtCore  # pylint: disable=E0611
try:
    from Qt import QtUiTools
except:
    from PySide2 import QtUiTools

import maya.cmds as cmds
from redshift_playblast.logic import maya_manager
from redshift_playblast.model.shader_override_types import Shader_Override_Type


class Redshift_Playblast_View(QtWidgets.QMainWindow):
    """
    Redshift playblast view
    """

    def __init__(self, parent=None):
        super(Redshift_Playblast_View, self).__init__(parent)

        # Set object name and window title
        self.setObjectName(WINDOW_OBJECT)
        self.setWindowTitle(WINDOW_TITLE)

        # Window type
        self.setWindowFlags(QtCore.Qt.Window)

        # Makes Maya perform magic which makes the window stay
        # on top in OS X and Linux. As an added bonus, it'll
        # make Maya remember the window position
        self.setProperty("saveWindowPref", True)

        # Filepaths
        main_window_file = os.path.join(UI_PATH, 'view_maya.ui')

        # Load UIs
        self.loadUiWidget(main_window_file)  # Main window UI

        # Set the main widget
        self.setCentralWidget(self._ui)

        # Define minimum size of UI
        self.setMinimumSize(380, 457)

        self.maya_manager=maya_manager.Maya_Manager()
        # Signals
        self.maya_manager.job.data_changed.connect(self.update_view)
        self._ui.txtStartFrame.textChanged.connect(lambda x: self.maya_manager.set_job_value('start_frame', x))
        self._ui.txtEndFrame.textChanged.connect(lambda x: self.maya_manager.set_job_value('end_frame', x))
        self._ui.txtWidth.textChanged.connect(lambda x: self.maya_manager.set_job_value('width', x))
        self._ui.txtHeight.textChanged.connect(lambda x: self.maya_manager.set_job_value('height', x))

        self._ui.cmBxCamera.currentIndexChanged.connect(lambda x: self.maya_manager.set_job_value('camera', self._ui.cmBxCamera.currentText()))
        self._ui.chBxMotionBlur.stateChanged.connect(lambda x: self.maya_manager.set_job_value('motion_blur', x==QtCore.Qt.CheckState.Checked))
        self._ui.chBxDof.stateChanged.connect(lambda x: self.maya_manager.set_job_value('dof', x==QtCore.Qt.CheckState.Checked))

        self._ui.cmbxQuality.currentIndexChanged.connect(lambda x: self.maya_manager.set_job_value('quality', self._ui.cmbxQuality.currentText()))

        self._ui.cmbxShaderOverride.currentIndexChanged.connect(lambda x: self.maya_manager.set_job_value('shader_override_type', Shader_Override_Type.value(self._ui.cmbxShaderOverride.currentText())))

        self._ui.radioRunInMaya.toggled.connect(lambda x: self.maya_manager.set_job_value('local_mode', self._ui.radioRunInMaya.isChecked()))
        self._ui.radioRunOnRenderFarm.toggled.connect(lambda x: self.maya_manager.set_job_value('local_mode', self._ui.radioRunInMaya.isChecked()))

        self._ui.btnCreatePlayblast.clicked.connect(self.maya_manager.create_playblast)

        self._ui.btnSceneRange.clicked.connect(lambda: self.maya_manager.apply_scene_range())
        self._ui.btnRenderSettings.clicked.connect(lambda: self.maya_manager.apply_render_settings_resolution())
        self.update_view()

        #tab order
        self.setTabOrder(self._ui.txtStartFrame, self._ui.txtEndFrame)
        self.setTabOrder(self._ui.txtEndFrame, self._ui.txtWidth)
        self.setTabOrder(self._ui.txtWidth, self._ui.txtHeight)
        self.setTabOrder(self._ui.txtHeight, self._ui.txtOutput)
        self.setTabOrder(self._ui.txtOutput, self._ui.btnCreatePlayblast)
        self.setTabOrder(self._ui.btnCreatePlayblast, self._ui.txtStartFrame)


    def loadUiWidget(self, uifilename, parent=None):
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(uifilename)
        uifile.open(QtCore.QFile.ReadOnly)
        self._ui = loader.load(uifile, self)
        uifile.close()

    def update_view(self):
        job=self.maya_manager.job

        #start end frame
        self._ui.txtStartFrame.setText(str(job.start_frame))
        self._ui.txtEndFrame.setText(str(job.end_frame))

        #resolution
        self._ui.txtWidth.setText(str(job.width))
        self._ui.txtHeight.setText(str(job.height))

        #camera
        self._ui.cmBxCamera.clear()
        old_cam=job.camera.name()
        for camera in job.avaible_cameras:
            self._ui.cmBxCamera.addItem(camera.name())
        self._ui.cmBxCamera.setCurrentIndex(self._ui.cmBxCamera.findText(old_cam))

        self._ui.chBxMotionBlur.setCheckState(QtCore.Qt.CheckState.Checked if job.motion_blur else QtCore.Qt.CheckState.Unchecked)
        self._ui.chBxDof.setCheckState(QtCore.Qt.CheckState.Checked if job.dof else QtCore.Qt.CheckState.Unchecked)

        #output
        self._ui.cmbxQuality.setCurrentIndex(self._ui.cmbxQuality.findText(job.quality))
        self._ui.txtOutput.setText(job.frame_path)

        #shader override
        old_shader_override=job.shader_override_type

        self._ui.cmbxShaderOverride.clear()

        for number, nice_name in Shader_Override_Type.nice_names.iteritems():
            self._ui.cmbxShaderOverride.addItem(nice_name)
        self._ui.cmbxShaderOverride.setCurrentIndex(self._ui.cmbxShaderOverride.findText(Shader_Override_Type.nice_name(old_shader_override)))

        self._ui.cmBxCamera.setCurrentIndex(self._ui.cmBxCamera.findText(old_cam))

        self._ui.radioRunInMaya.setChecked(job.local_mode)
        self._ui.radioRunOnRenderFarm.setChecked(False if job.local_mode else True)


# ----------------------------------------------------------------------
# DCC application helper functions
# ----------------------------------------------------------------------

def _maya_delete_ui():
    """Delete existing UI in Maya"""
    if cmds.window(WINDOW_OBJECT, q=True, exists=True):
        cmds.deleteUI(WINDOW_OBJECT)  # Delete window
    if cmds.dockControl('MayaWindow|' + WINDOW_TITLE, q=True, ex=True):
        cmds.deleteUI('MayaWindow|' + WINDOW_TITLE)  # Delete docked window


def _maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')

# ----------------------------------------------------------------------
# Run functions
# ----------------------------------------------------------------------

def run_maya():
    """Run in Maya"""
    _maya_delete_ui()  # Delete any existing existing UI
    view = Redshift_Playblast_View(parent=_maya_main_window())

    # Makes Maya perform magic which makes the window stay
    # on top in OS X and Linux. As an added bonus, it'll
    # make Maya remember the window position
    view.setProperty("saveWindowPref", True)

    view.show()  # Show the UI



if __name__ == "__main__":
    run_maya()