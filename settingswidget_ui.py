# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingswidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_SettingsWidget(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(351, 203)
        self.okButton = QPushButton(Settings)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setGeometry(QRect(90, 120, 181, 41))
        self.lineEdit = QLineEdit(Settings)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(30, 30, 301, 41))

        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("SettingsWidget", u"Settings", None))
        self.okButton.setText(QCoreApplication.translate("SettingsWidget", u"Ok", None))
    # retranslateUi

