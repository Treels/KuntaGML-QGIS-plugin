# -*- coding: utf-8 -*-

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

import logging

from PyQt5.QtCore import pyqtSlot, Qt
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QListWidgetItem

from ..core.kuntagml2layers import KuntaGML2Layers
# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
from ..qgis_plugin_tools.tools.resources import load_ui, plugin_name

FORM_CLASS = load_ui('kunta_gml_loader_dialog.ui')

LOGGER = logging.getLogger(plugin_name())


class LoaderDialog(QtWidgets.QDialog, FORM_CLASS):
    onCloseHandler = None

    def __init__(self, parent=None):
        """Constructor."""

        super(LoaderDialog, self).__init__(parent)

        self.setupUi(self)

        self.converter = None

    def get_converter(self):
        return self.converter

    @pyqtSlot()
    def on_loadTypesPushButton_clicked(self):
        LOGGER.info("CLicked")
        self.listWidget.clear()

        wfs = self.wfsPathLineEdit.text()
        self.converter = KuntaGML2Layers(wfs, '2.1.6', '2.1.1', '1.1.0')
        self.converter.populate_features()

        for f_type in self.converter.feature_types:
            item = QListWidgetItem(f_type)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            self.listWidget.addItem(item)

    def get_feature_types(self):
        return [item.text() for item in self.listWidget.selectedItems()]

    def get_max_features(self):
        txt = self.maxFeaturesLineEdit.text()
        try:
            return int(txt)
        except ValueError:
            return 100
