"""This uses a Qt binding of "any" kind, thanks to the Qt.py module,
to produce an UI. First, one .ui file is loaded and then attaches
another .ui file onto the first. Think of it as creating a modular UI.
More on Qt.py:
https://github.com/mottosso/Qt.py
"""

import sys
import os
import platform

from redshift_playblast.model.shader_override_types import Shader_Override_Type

sys.dont_write_bytecode = True  # Avoid writing .pyc files

# ----------------------------------------------------------------------
# Environment detection
# ----------------------------------------------------------------------

try:
    import maya.cmds as cmds
    MAYA = True
except ImportError:
    MAYA = False

try:
    import nuke
    import nukescripts
    NUKE = True
except ImportError:
    NUKE = False

STANDALONE = False
if not MAYA and not NUKE:
    STANDALONE = True


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# Window title and object names
WINDOW_TITLE = 'Redshift Playblast'
WINDOW_OBJECT = 'RedshiftPlayblast'

# Maya-specific
DOCK_WITH_MAYA_UI = False

# Nuke-specific
DOCK_WITH_NUKE_UI = False

# Repository path
REPO_PATH = os.path.dirname(__file__)

# Full path to where .ui files are stored
UI_PATH = REPO_PATH

# Qt.py option: Set up preffered binding
# os.environ['QT_PREFERRED_BINDING'] = 'PyQt4'
# os.environ['QT_PREFERRED_BINDING'] = 'PySide'
# os.environ['QT_PREFERRED_BINDING'] = 'PyQt5'
# os.environ['QT_PREFERRED_BINDING'] = 'PySide2'
if NUKE:
    # Avoid loading site-wide PyQt4/PyQt5 inside of Nuke
    os.environ['QT_PREFERRED_BINDING'] = 'PySide'


# ----------------------------------------------------------------------
# Set up Python modules access
# ----------------------------------------------------------------------

# Enable access to boilerlib (Qt.py, mayapalette)
if REPO_PATH not in sys.path:
    sys.path.append(REPO_PATH)

# ----------------------------------------------------------------------
# Main script
# ----------------------------------------------------------------------

from Qt import QtWidgets  # pylint: disable=E0611
from Qt import QtCore  # pylint: disable=E0611
from Qt import QtUiTools
from redshift_playblast.logic import maya_manager

# Debug
# print('Using' + QtCompat.__binding__)


class Redshift_Playblast_View(QtWidgets.QMainWindow):
    """Example showing how UI files can be loaded using the same script
    when taking advantage of the Qt.py module and build-in methods
    from PySide/PySide2/PyQt4/PyQt5."""

    def __init__(self, parent=None):
        super(Redshift_Playblast_View, self).__init__(parent)

        # Set object name and window title
        self.setObjectName(WINDOW_OBJECT)
        self.setWindowTitle(WINDOW_TITLE)

        # Window type
        self.setWindowFlags(QtCore.Qt.Window)

        if MAYA:
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
        self._ui.chBxMotionBlur.stateChanged.connect(lambda x: self.maya_manager.set_job_value('motion_blur', x))
        self._ui.chBxDof.stateChanged.connect(lambda x: self.maya_manager.set_job_value('dof', x))

        self._ui.cmbxQuality.currentIndexChanged.connect(lambda x: self.maya_manager.set_job_value('quality', self._ui.cmbxQuality.currentText()))

        self._ui.cmbxShaderOverride.currentIndexChanged.connect(lambda x: self.maya_manager.set_job_value('shader_override_type', Shader_Override_Type.value(self._ui.cmbxShaderOverride.currentText())))

        self._ui.btnSubmit.clicked.connect(self.maya_manager.submit)
        self.update_view()

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
        print old_shader_override
        self._ui.cmbxShaderOverride.clear()

        for number, nice_name in Shader_Override_Type.nice_names.iteritems():
            self._ui.cmbxShaderOverride.addItem(nice_name)
        self._ui.cmbxShaderOverride.setCurrentIndex(self._ui.cmbxShaderOverride.findText(Shader_Override_Type.nice_name(old_shader_override)))

        self._ui.cmBxCamera.setCurrentIndex(self._ui.cmBxCamera.findText(old_cam))

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
    boil = Redshift_Playblast_View(parent=_maya_main_window())

    # Makes Maya perform magic which makes the window stay
    # on top in OS X and Linux. As an added bonus, it'll
    # make Maya remember the window position
    boil.setProperty("saveWindowPref", True)

    if not DOCK_WITH_MAYA_UI:
        boil.show()  # Show the UI
    elif DOCK_WITH_MAYA_UI:
        allowed_areas = ['right', 'left']
        cmds.dockControl(WINDOW_TITLE, label=WINDOW_TITLE, area='left',
                         content=WINDOW_OBJECT, allowedArea=allowed_areas)


def run_standalone():
    """Run standalone
    Note:
        Styling the UI with the Maya palette on OS X when using the
        PySide/PyQt4 bindings result in various issues, which is why
        it is disabled by default when you're running this combo.
    .. _Issue #9:
       https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/9
    """
    app = QtWidgets.QApplication(sys.argv)
    boil = Boilerplate()

    boil.show()  # Show the UI
    sys.exit(app.exec_())


if __name__ == "__main__":
    if MAYA:
        run_maya()
    else:
        run_standalone()