# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause


from PySide6.QtCore import (
    QDir,
    QFile,
    QIODevice,
    QUrl,
    Qt,
    Slot,
    QTimer,
    QMetaObject,
    Signal,
)
from PySide6.QtGui import QFontDatabase
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QApplication,
)
from PySide6.QtNetwork import (
    QNetworkReply,
)

from mainwindow_ui import Ui_MainWindow
from document import Document
from previewpage import PreviewPage
from screenwidget import ScreenWidget
from settingswidget import SettingsWidget
import requests
import json


class MainWindow(QMainWindow):
    signal_test = Signal(QNetworkReply)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_file_path = ""
        self.m_content = Document()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(16)
        self._ui.editor.setFont(font)
        self._ui.preview.setContextMenuPolicy(Qt.NoContextMenu)
        self._page = PreviewPage(self)
        self._ui.preview.setPage(self._page)

        self._ui.editor.textChanged.connect(self.plainTextEditChanged)

        self._ui.splitter.setStretchFactor(0, 5)
        self._ui.splitter.setStretchFactor(1, 1)

        self._ui.captureButton.setFixedHeight(50)

        self._channel = QWebChannel(self)
        self._channel.registerObject("content", self.m_content)
        self._page.setWebChannel(self._channel)

        self._ui.preview.setUrl(QUrl("qrc:/index.html"))

        self._ui.actionNew.triggered.connect(self.onFileNew)
        self._ui.actionOpen.triggered.connect(self.onFileOpen)
        self._ui.actionSave.triggered.connect(self.onFileSave)
        self._ui.actionSaveAs.triggered.connect(self.onFileSaveAs)
        self._ui.actionExit.triggered.connect(self.close)

        self._ui.editor.document().modificationChanged.connect(
            self._ui.actionSave.setEnabled
        )

        defaultTextFile = QFile(":/default.md")
        defaultTextFile.open(QIODevice.ReadOnly)
        data = defaultTextFile.readAll()

        self._ui.editor.setPlainText(data.data().decode("utf8"))

        # self.settings_action = QAction("Settings", self)
        # self.settings_action.triggered.connect(self.open_settings)
        # self._ui.menu_File.addAction(self.settings_action)

        # self._ui.capture_button.clicked.connect(self.onCapture)
        # self._ui.copy_button.clicked.connect(self.onCopy)
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_settingsButton_clicked(self):
        # 打开设置对话框或执行其他设置操作
        self.label = SettingsWidget()
        QTimer.singleShot(100, self.label.show)

    @Slot(str)
    def requestApi(self, file_path: str):
        """Request the simpletex api."""

        # self.file_path = file_path
        # manager = QNetworkAccessManager()
        # # https://server.simpletex.cn/api/latex_ocr
        # api_url = QUrl("https://httpbingo.org/post")
        # request = QNetworkRequest(api_url)

        # multi_part = QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)

        # file_part = QHttpPart()
        # file_part.setHeader(
        #     QNetworkRequest.ContentDispositionHeader,
        #     f'form-data; name="file"; filename="{file_path}"',
        # )
        # print("binggo")
        # file = QFile(file_path)
        # file.open(QIODevice.OpenModeFlag.ReadOnly)
        # file_part.setBodyDevice(file)
        # multi_part.append(file_part)

        # params = QUrlQuery()
        # params.addQueryItem("token", str(self.label.token))

        # for param in params.queryItems():
        #     text_part = QHttpPart()
        #     text_part.setHeader(
        #         QNetworkRequest.KnownHeaders.ContentDispositionHeader,
        #         f'form-data; name="{param[0]}"',
        #     )
        #     text_part.setBody(param[1].encode())
        #     multi_part.append(text_part)

        # reply = manager.post(request, multi_part)
        # reply.finished.connect(self.handle_response)

        # # QTimer.singleShot(1000, self.handle_response)
        # self.signal_test.connect(self.handle_response)
        # self.signal_test.emit(reply)
        # print("finished")

        self.label = SettingsWidget()
        api_url = "https://server.simpletex.cn/api/latex_ocr"
        header = {"token": str(self.label.token)}
        file = [("file", (file_path, open(file_path, "rb")))]
        r = requests.post(api_url, files=file, headers=header)
        print(r.status_code)
        print(r.text)
        result_path = file_path.replace("png", "json")
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(r.json(), f, indent=4)

        self._ui.scoreSlider.setValue(eval(str(r.json()["res"]["conf"])) * 100)
        self._ui.editor.setPlainText("$${}$$".format(r.json()["res"]["latex"]))

    @Slot(QNetworkReply)
    def handle_response(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll().data().decode()
            print(data)

            # 将结果保存为json文件
            result_path = self.file_path.replace("png", "json")
            with open(result_path, "w", encoding="utf-8") as f:
                f.write(data)
        else:
            print("Error:", reply.errorString())

        # # 清理资源
        reply.deleteLater()

    @Slot()
    def on_captureButton_clicked(self):
        self.hide()
        self.capture = ScreenWidget()
        self.capture.signal_send_msg.connect(self.requestApi)
        self.capture.accepted.connect(self.show)
        QTimer.singleShot(100, self.capture.show)

    @Slot()
    def on_copyButton_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self._ui.editor.toPlainText())

    @Slot(str)
    def refresh(self, msg):
        self._ui.editor.setPlainText(msg)

    @Slot()
    def plainTextEditChanged(self):
        self.m_content.setText(self._ui.editor.toPlainText())

    @Slot(str)
    def openFile(self, path):
        f = QFile(path)
        name = QDir.toNativeSeparators(path)
        if not f.open(QIODevice.ReadOnly):
            error = f.errorString()
            QMessageBox.warning(
                self, self.windowTitle(), f"Could not open file {name}: {error}"
            )
            return
        self.m_file_path = path
        data = f.readAll()
        self._ui.editor.setPlainText(data.data().decode("utf8"))
        self.statusBar().showMessage(f"Opened {name}")

    def isModified(self):
        return self._ui.editor.document().isModified()

    @Slot()
    def onFileNew(self):
        if self.isModified():
            m = "You have unsaved changes. Do you want to create a new document anyway?"
            button = QMessageBox.question(self, self.windowTitle(), m)
            if button != QMessageBox.Yes:
                return

        self.m_file_path = ""
        self._ui.editor.setPlainText("## New document")
        self._ui.editor.document().setModified(False)

    @Slot()
    def onFileOpen(self):
        if self.isModified():
            m = "You have unsaved changes. Do you want to open a new document anyway?"
            button = QMessageBox.question(self, self.windowTitle(), m)
            if button != QMessageBox.Yes:
                return
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Open MarkDown File")
        dialog.setMimeTypeFilters(["text/markdown"])
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if dialog.exec() == QDialog.Accepted:
            self.openFile(dialog.selectedFiles()[0])

    @Slot()
    def onFileSave(self):
        if not self.m_file_path:
            self.onFileSaveAs()
        if not self.m_file_path:
            return

        f = QFile(self.m_file_path)
        name = QDir.toNativeSeparators(self.m_file_path)
        if not f.open(QIODevice.WriteOnly | QIODevice.Text):
            error = f.errorString()
            QMessageBox.warning(
                self, self.windowTitle(), f"Could not write to file {name}: {error}"
            )
            return
        text = self._ui.editor.toPlainText()
        f.write(bytes(text, encoding="utf8"))
        f.close()
        self._ui.editor.document().setModified(False)
        self.statusBar().showMessage(f"Wrote {name}")

    @Slot()
    def onFileSaveAs(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Save MarkDown File")
        dialog.setMimeTypeFilters(["text/markdown"])
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("md")
        if dialog.exec() != QDialog.Accepted:
            return
        path = dialog.selectedFiles()[0]
        self.m_file_path = path
        self.onFileSave()

    def closeEvent(self, event):
        if self.isModified():
            m = "You have unsaved changes. Do you want to exit anyway?"
            button = QMessageBox.question(self, self.windowTitle(), m)
            if button != QMessageBox.Yes:
                event.ignore()
            else:
                event.accept()
