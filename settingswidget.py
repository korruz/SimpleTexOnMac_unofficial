from PySide6.QtCore import QMetaObject, Slot, QFile, QSettings
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLabel, QDialog
from settingswidget_ui import Ui_SettingsWidget
import configparser


class SettingsWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.setWindowTitle("第二个窗口")
        self.config_file = QFile(":/config.ini")

        self.getTokenFromFile()

        QMetaObject.connectSlotsByName(self)

    def setupUi(self):
        self._ui = Ui_SettingsWidget()
        self._ui.setupUi(self)

    def getTokenFromFile(self):
        self.config_file.open(QFile.OpenModeFlag.ReadOnly)

        settings = QSettings(self.config_file.fileName(), QSettings.Format.IniFormat)

        self.token = settings.value("DEFAULT/token")
        self._ui.lineEdit.setText(self.token)

        self.config_file.close()

    @Slot()
    def on_okButton_clicked(self):
        self.config_file.open(QFile.OpenModeFlag.WriteOnly | QFile.OpenModeFlag.Text)

        settings = QSettings(self.config_file.fileName(), QSettings.Format.IniFormat)

        settings.setValue("DEFAULT/token", self._ui.lineEdit.text())

        self.config_file.close()
        self.close()
