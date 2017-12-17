"""This uses a Qt binding of "any" kind, thanks to the Qt.py module,
to produce an UI. First, one .ui file is loaded and then attaches
another .ui file onto the first. Think of it as creating a modular UI.
More on Qt.py:
https://github.com/mottosso/Qt.py
"""

import sys
import os
import platform

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
from Qt import QtCompat



# Debug
# print('Using' + QtCompat.__binding__)


class Boilerplate(QtWidgets.QMainWindow):
    """Example showing how UI files can be loaded using the same script
    when taking advantage of the Qt.py module and build-in methods
    from PySide/PySide2/PyQt4/PyQt5."""

    def __init__(self, parent=None):
        super(Boilerplate, self).__init__(parent)

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
        self.main_widget = QtCompat.load_ui(main_window_file)  # Main window UI

        # Set the main widget
        self.setCentralWidget(self.main_widget)

        # Define minimum size of UI
        self.setMinimumSize(380, 356)

        # Signals

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
    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')

# ----------------------------------------------------------------------
# Run functions
# ----------------------------------------------------------------------

def run_maya():
    """Run in Maya"""
    _maya_delete_ui()  # Delete any existing existing UI
    boil = Boilerplate(parent=_maya_main_window())

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