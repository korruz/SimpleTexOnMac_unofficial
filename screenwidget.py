from PySide6.QtCore import (
    QSize,
    QPoint,
    Slot,
    Qt,
    QDateTime,
    Signal,
)
from PySide6.QtWidgets import QMenu, QApplication, QWidget
from PySide6.QtGui import (
    QPixmap,
    QContextMenuEvent,
    QMouseEvent,
    QPaintEvent,
    QShowEvent,
    QPainter,
    QPen,
    QColor,
)
from enum import Enum

import os

basedir = os.path.dirname(__file__)


class STATUE(Enum):
    SElECT = 1
    MOV = 2
    SET_W_H = 3


class Screen:
    """截屏的屏幕"""

    def __init__(self, size: QSize):
        self.__left_up_point: QPoint
        self.__right_down_point: QPoint

        self.__mouse_start_point: QPoint
        self.__mouse_end_point: QPoint

        self.__max_width: int
        self.__max_height: int

        self.__statue: STATUE

        self.max_width = size.width()
        self.max_height = size.height()

        self.mouse_start_point = QPoint(-1, -1)
        self.mouse_end_point = QPoint(-1, -1)

        self.left_up_point = QPoint(-1, -1)
        self.right_down_point = QPoint(-1, -1)

        self.statue = STATUE.SElECT

    def cmp_point(self, left_point: QPoint, right_point: QPoint) -> (QPoint, QPoint):
        """Compare two points."""
        if left_point.x() <= right_point.x():
            if left_point.y() <= right_point.y():
                return left_point, right_point
            else:
                return QPoint(left_point.x(), right_point.y()), QPoint(
                    right_point.x(), left_point.y()
                )
        else:
            if left_point.y() <= right_point.y():
                return QPoint(right_point.x(), left_point.y()), QPoint(
                    left_point.x(), right_point.y()
                )
            else:
                return right_point, left_point

    def is_in_area(self, point: QPoint) -> bool:
        """Determine whether the point is in the area."""
        if (
            self.left_up_point.x() <= point.x() <= self.right_down_point.x()
            and self.left_up_point.y() <= point.y() <= self.right_down_point.y()
        ):
            return True
        else:
            return False

    def move(self, point: QPoint):
        """Move the area."""
        left_x = self.left_up_point.x() + point.x()
        left_y = self.left_up_point.y() + point.y()
        right_x = self.right_down_point.x() + point.x()
        right_y = self.right_down_point.y() + point.y()

        if left_x < 0:
            left_x = 0
            right_x -= point.x()

        if left_y < 0:
            left_y = 0
            right_y -= point.y()

        if right_x > self.max_width:
            right_x = self.max_width
            left_x -= point.x()

        if right_y > self.max_height:
            right_y = self.max_height
            left_y -= point.y()

        self.left_up_point = QPoint(left_x, left_y)
        self.right_down_point = QPoint(right_x, right_y)
        self.mouse_start_point = self.left_up_point
        self.mouse_end_point = self.right_down_point

    def set_end_point(self, point: QPoint):
        """Set the end point."""
        self.mouse_end_point = point
        self.left_up_point, self.right_down_point = self.cmp_point(
            self.mouse_start_point, self.mouse_end_point
        )

    @property
    def left_up_point(self) -> QPoint:
        return self.__left_up_point

    @left_up_point.setter
    def left_up_point(self, value: QPoint):
        self.__left_up_point = value

    @property
    def right_down_point(self) -> QPoint:
        return self.__right_down_point

    @right_down_point.setter
    def right_down_point(self, value: QPoint):
        self.__right_down_point = value

    @property
    def mouse_start_point(self) -> QPoint:
        return self.__mouse_start_point

    @mouse_start_point.setter
    def mouse_start_point(self, value: QPoint):
        self.__mouse_start_point = value

    @property
    def mouse_end_point(self) -> QPoint:
        return self.__mouse_end_point

    @mouse_end_point.setter
    def mouse_end_point(self, value: QPoint):
        self.__mouse_end_point = value

    @property
    def max_width(self) -> int:
        return self.__max_width

    @max_width.setter
    def max_width(self, value: int):
        self.__max_width = value

    @property
    def max_height(self) -> int:
        return self.__max_height

    @max_height.setter
    def max_height(self, value: int):
        self.__max_height = value

    @property
    def statue(self) -> STATUE:
        return self.__statue

    @statue.setter
    def statue(self, value: STATUE):
        self.__statue = value


STRDATETIME = QDateTime.currentDateTime().toString("yyyy-MM-dd-HH-mm-ss")


class ScreenWidget(QWidget):
    """Screen widget class."""

    send_screen_path_signal = Signal(str)

    def __init__(self, parent):
        super().__init__()

        # 保存对主窗口的引用
        self.main_window = parent

        self.__menu: QMenu
        self.__screen: Screen
        self.__full_screen: QPixmap
        self.__bg_screen: QPixmap
        self.__move_point: QPoint

        self.move_point = QPoint(-1, -1)

        self.menu = QMenu(self)
        self.menu.addAction("Start OCR", self.saveScreen)
        self.menu.addAction("Exit", self.close)

        desktop_geometry = QApplication.primaryScreen().geometry()

        self.setGeometry(desktop_geometry)
        self.screen = Screen(desktop_geometry.size())
        self.full_screen = QPixmap()

    def closeEvent(self, event):
        # 重写窗口关闭事件，在此事件中使主窗口重新显示
        self.main_window.show()
        super().closeEvent(event)

    @property
    def menu(self) -> QMenu:
        return self.__menu

    @menu.setter
    def menu(self, value: QMenu):
        self.__menu = value

    @property
    def screen(self) -> Screen:
        return self.__screen

    @screen.setter
    def screen(self, value: Screen):
        self.__screen = value

    @property
    def full_screen(self) -> QPixmap:
        return self.__full_screen

    @full_screen.setter
    def full_screen(self, value: QPixmap):
        self.__full_screen = value

    @property
    def bg_screen(self) -> QPixmap:
        return self.__bg_screen

    @bg_screen.setter
    def bg_screen(self, value: QPixmap):
        self.__bg_screen = value

    @property
    def move_point(self) -> QPoint:
        return self.__move_point

    @move_point.setter
    def move_point(self, value: QPoint):
        self.__move_point = value

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.menu.exec(self.cursor().pos())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        status = self.screen.statue
        if status == STATUE.SElECT:
            self.screen.mouse_start_point = event.pos()
        elif status == STATUE.MOV:
            if self.screen.is_in_area(event.pos()) is False:
                self.screen.statue = STATUE.SElECT
                self.screen.mouse_start_point = event.pos()
            else:
                self.move_point = event.pos()
                self.setCursor(Qt.CursorShape.SizeAllCursor)

        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.screen.statue == STATUE.SElECT:
            self.screen.set_end_point(event.pos())
        elif self.screen.statue == STATUE.MOV:
            self.screen.move(event.pos() - self.move_point)
            self.move_point = event.pos()

        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.screen.statue == STATUE.SElECT:
            self.screen.statue = STATUE.MOV
        elif self.screen.statue == STATUE.MOV:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the screen."""
        painter = QPainter(self)

        x = self.screen.left_up_point.x()
        y = self.screen.left_up_point.y()
        w = self.screen.right_down_point.x() - x
        h = self.screen.right_down_point.y() - y

        pen = QPen()
        pen.setColor(Qt.GlobalColor.red)
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.DotLine)

        painter.setPen(pen)
        painter.drawPixmap(0, 0, self.bg_screen)

        if w != 0 and h != 0:
            painter.drawPixmap(x, y, self.full_screen.copy(x, y, w, h))

        painter.drawRect(x, y, w, h)

        pen.setColor(Qt.GlobalColor.yellow)
        painter.setPen(pen)
        painter.drawText(
            x + 2,
            y - 8,
            f"(截图范围：( {x} x {y} ) - ( {x + w} x {y + h} )  图片大小：( {w} x {h} ))",
        )

    def showEvent(self, event: QShowEvent) -> None:
        """Show the screen."""
        point = QPoint(-1, -1)
        self.screen.mouse_start_point = point
        self.screen.mouse_end_point = point

        primary_screen = QApplication.primaryScreen()
        self.full_screen = primary_screen.grabWindow(
            0, 0, 0, self.screen.max_width, self.screen.max_height
        )

        # Set transparency to blur the background
        pixmap = QPixmap(self.screen.max_width, self.screen.max_height)
        pixmap.fill((QColor(160, 160, 160, 200)))
        self.bg_screen = QPixmap(self.full_screen)
        p = QPainter(self.bg_screen)
        p.drawPixmap(0, 0, pixmap)

    @Slot()
    def saveScreen(self):
        """Save the screen."""
        x = self.screen.left_up_point.x()
        y = self.screen.left_up_point.y()
        w = self.screen.right_down_point.x() - x
        h = self.screen.right_down_point.y() - y

        os.makedirs(os.path.join(basedir, "data"), exist_ok=True)
        file_path = f"data/screen/screen_{STRDATETIME}.png"
        file_path = os.path.join(basedir, file_path)
        self.full_screen.copy(x, y, w, h).save(file_path, "png")
        self.send_screen_path_signal.emit(file_path)
        self.close()
