#  Gispo Ltd., hereby disclaims all copyright interest in the program KuntaGML-QGIS-plugin
#  Copyright (C) 2020 Gispo Ltd (https://www.gispo.fi/).
#
#
#  This file is part of KuntaGML-QGIS-plugin.
#
#  KuntaGML-QGIS-plugin is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  KuntaGML-QGIS-plugin is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with KuntaGML-QGIS-plugin.  If not, see <https://www.gnu.org/licenses/>.

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
