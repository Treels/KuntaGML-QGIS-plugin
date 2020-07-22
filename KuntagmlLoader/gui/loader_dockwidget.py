import os
import sys

from PyQt5.QtCore import pyqtSignal, QSettings, pyqtSlot
from qgis.PyQt import QtWidgets
from qgis.PyQt import uic
from qgis.core import Qgis, QgsProject

from ..qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS = load_ui('kunta_gml_loader_dockwidget_base.ui')

class LoaderDockwidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""

        super(LoaderDockwidget, self).__init__(parent)

        self.setupUi(self)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
