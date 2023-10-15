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

class Ui_SettingsWight(object):
    def setupUi(self, SettingsWight):
        if not SettingsWight.objectName():
            SettingsWight.setObjectName(u"SettingsWight")
        SettingsWight.resize(351, 203)
        self.okButton = QPushButton(SettingsWight)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setGeometry(QRect(90, 120, 181, 41))
        self.lineEdit = QLineEdit(SettingsWight)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(30, 40, 301, 31))

        self.retranslateUi(SettingsWight)

        QMetaObject.connectSlotsByName(SettingsWight)
    # setupUi

    def retranslateUi(self, SettingsWight):
        SettingsWight.setWindowTitle(QCoreApplication.translate("SettingsWight", u"Settings", None))
        self.okButton.setText(QCoreApplication.translate("SettingsWight", u"Ok", None))
    # retranslateUi

