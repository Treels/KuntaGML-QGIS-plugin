# -*- coding: utf-8 -*-
import os

from PyQt5.QtCore import pyqtSlot, Qt
from qgis.PyQt import QtWidgets
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QListWidgetItem

from ..core.kuntagml2layers import KuntaGML2Layers
from ..core.utils import logger

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'kunta_gml_loader_dialog.ui'))


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
        logger.info("CLicked")
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
