import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow

import rc_markdowneditor


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QCoreApplication.setOrganizationName("Formula OCR App")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
