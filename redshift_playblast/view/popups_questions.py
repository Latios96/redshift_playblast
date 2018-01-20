from Qt import QtWidgets

def movie_exists():
    return QtWidgets.QMessageBox.question(None, "Movie file already exists", "Movie File already exists. Override?")==QtWidgets.QMessageBox.StandardButton.Yes

def unsaved_changes():
    return QtWidgets.QMessageBox.question(None, "Unsaved Changes","You have unsaved changed. Do you want to save?")==QtWidgets.QMessageBox.StandardButton.Yes
