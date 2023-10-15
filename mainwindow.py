from PySide6.QtCore import QDir, QFile, QIODevice, QUrl, Qt, Slot, QTimer, QMetaObject
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
    QNetworkAccessManager,
    QNetworkRequest,
    QHttpMultiPart,
    QHttpPart,
)

from mainwindow_ui import Ui_MainWindow
from document import Document
from previewpage import PreviewPage
from screenwidget import ScreenWidget
from settingswidget import SettingsWidget
import json


class MainWindow(QMainWindow):
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

        self._ui.splitter.setStretchFactor(0, 10)
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

        self.token = SettingsWidget().token

        self.networkManager = QNetworkAccessManager()
        self.networkManager.finished.connect(self.on_finished)

        self.multi_part = None  # 用于存储multi_part对象，保持其生命周期
        self.file = None  # 用于存储file对象，保持其生命周期

        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_settingsButton_clicked(self):
        # 打开设置对话框或执行其他设置操作
        self.settingsLabel = SettingsWidget()
        QTimer.singleShot(100, self.settingsLabel.show)

    @Slot(str)
    def get_simpletex_data(self, file_path: str):
        """Request the simpletex api."""
        self.screen_file_path = file_path
        # 创建POST请求
        url = QUrl("https://server.simpletex.cn/api/latex_ocr")
        request = QNetworkRequest(url)

        # 将 token 添加到请求头
        self.token = SettingsWidget().token
        request.setRawHeader(b"token", str(self.token).encode())

        # 创建QHttpMultiPart对象
        self.multi_part = QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)

        # 创建文件上传部分
        file_part = QHttpPart()
        file_part.setHeader(
            QNetworkRequest.KnownHeaders.ContentDispositionHeader,
            f'form-data; name="file"; filename="{self.screen_file_path}"',
        )
        self.file = QFile(self.screen_file_path)
        self.file.open(QIODevice.OpenModeFlag.ReadOnly)
        file_part.setBodyDevice(self.file)
        self.multi_part.append(file_part)

        # 发送POST请求
        reply = self.networkManager.post(request, self.multi_part)
        # 在post请求后，保持multi_part对象的生命周期，直到请求完成
        reply.finished.connect(self.clear_multi_part)

    def clear_multi_part(self):
        """清理multi_part和file对象, 在网络请求完成后调用"""
        if self.multi_part:
            self.multi_part.setParent(None)
            self.multi_part = None
        if self.file:
            self.file.close()
            self.file = None

    def on_finished(self, response: QNetworkReply):
        # Check if the request was successful
        if response.error() == QNetworkReply.NoError:
            content = response.readAll().data().decode("utf-8")
            content = json.loads(content)
            self.result_json_path = self.screen_file_path.replace(".png", ".json")
            with open(self.result_json_path, "w") as f:
                json.dump(content, f)
            self._ui.scoreSlider.setValue(eval(str(content["res"]["conf"])) * 100)
            self._ui.editor.setPlainText("$${}$$".format(content["res"]["latex"]))
        else:
            print("Failed to fetch the web page. Error:", response.errorString())

        response.deleteLater()

    @Slot()
    def on_captureButton_clicked(self):
        self.hide()
        self.capture = ScreenWidget(self)
        self.capture.send_screen_path_signal.connect(self.get_simpletex_data)
        # 延迟100ms显示截图窗口，避免被主窗口遮挡
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
