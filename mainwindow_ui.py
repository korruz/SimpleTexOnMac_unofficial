# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QSlider, QSplitter, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.preview = QWebEngineView(self.splitter)
        self.preview.setObjectName(u"preview")
        self.splitter.addWidget(self.preview)
        self.editor = QPlainTextEdit(self.splitter)
        self.editor.setObjectName(u"editor")
        self.splitter.addWidget(self.editor)

        self.verticalLayout.addWidget(self.splitter)

        self.captureButton = QPushButton(self.centralwidget)
        self.captureButton.setObjectName(u"captureButton")
        self.captureButton.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.captureButton.sizePolicy().hasHeightForWidth())
        self.captureButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.captureButton)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.settingsButton = QPushButton(self.centralwidget)
        self.settingsButton.setObjectName(u"settingsButton")

        self.horizontalLayout.addWidget(self.settingsButton)

        self.copyButton = QPushButton(self.centralwidget)
        self.copyButton.setObjectName(u"copyButton")

        self.horizontalLayout.addWidget(self.copyButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.scoreSlider = QSlider(self.centralwidget)
        self.scoreSlider.setObjectName(u"scoreSlider")
        self.scoreSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.scoreSlider)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menu_File.addAction(self.actionNew)
        self.menu_File.addAction(self.actionOpen)
        self.menu_File.addAction(self.actionSave)
        self.menu_File.addAction(self.actionSaveAs)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Formula OCR", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"&Open...", None))
#if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(QCoreApplication.translate("MainWindow", u"Open document", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
#if QT_CONFIG(tooltip)
        self.actionSave.setToolTip(QCoreApplication.translate("MainWindow", u"Save current document", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
#if QT_CONFIG(tooltip)
        self.actionExit.setToolTip(QCoreApplication.translate("MainWindow", u"Exit editor", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"Save &As...", None))
#if QT_CONFIG(tooltip)
        self.actionSaveAs.setToolTip(QCoreApplication.translate("MainWindow", u"Save document under different name", None))
#endif // QT_CONFIG(tooltip)
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"&New", None))
#if QT_CONFIG(tooltip)
        self.actionNew.setToolTip(QCoreApplication.translate("MainWindow", u"Create new document", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.captureButton.setText(QCoreApplication.translate("MainWindow", u"Capture", None))
        self.settingsButton.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.copyButton.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
    # retranslateUi

