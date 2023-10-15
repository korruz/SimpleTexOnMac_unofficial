import os
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QMetaObject, Slot, QSettings, Signal
from settingswidget_ui import Ui_SettingsWight

basedir = os.path.dirname(__file__)


class SettingsWidget(QWidget):
    """用于配置 token"""

    tokenUpdateSignal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.setWindowTitle("Settings")

        self.token: str = ""

        os.makedirs(os.path.join(basedir, "data"), exist_ok=True)
        os.makedirs(os.path.join(basedir, "data/config"), exist_ok=True)
        os.makedirs(os.path.join(basedir, "data/screen"), exist_ok=True)
        self.config_file_path = os.path.join(basedir, "data/config/config.ini")

        self.setToken()
        self.getToken()

        QMetaObject.connectSlotsByName(self)

    def setupUi(self):
        self._ui = Ui_SettingsWight()
        self._ui.setupUi(self)

    def getToken(self):
        settings = QSettings(self.config_file_path, QSettings.Format.IniFormat)
        self.token = settings.value("DEFAULT/token")
        self._ui.lineEdit.setText(self.token)

    def setToken(self):
        settings = QSettings(self.config_file_path, QSettings.Format.IniFormat)
        settings.setValue(
            "DEFAULT/token",
            "s3zeiSf6oV4C8qqTvil28fs8zgkysDPRJUp1KGqDdDjosVyeeKr7rTeaE8EznWtf",
        )
        settings.sync()

    @Slot()
    def on_okButton_clicked(self):
        settings = QSettings(self.config_file_path, QSettings.Format.IniFormat)
        settings.setValue("DEFAULT/token", self._ui.lineEdit.text())
        settings.sync()

        # token 更新
        self.token = self._ui.lineEdit.text()

        self.close()
