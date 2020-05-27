# -*- coding: utf-8 -*-
import os

from PyQt5 import QtWidgets
from PyQt5 import uic

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'kunta_gml_loader_dialog.ui'))


class LoaderDialog(QtWidgets.QDialog, FORM_CLASS):
    onCloseHandler = None

    def __init__(self, parent=None):
        """Constructor."""

        super(LoaderDialog, self).__init__(parent)

        self.setupUi(self)
