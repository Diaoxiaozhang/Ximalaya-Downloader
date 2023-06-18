# coding:utf-8
import sys
from typing import Optional
from enum import Enum
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont, QAction
from PySide6.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QHeaderView, QTableWidgetItem, QLabel

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            Theme, FluentIconBase, RoundMenu, Action, MenuAnimationType)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar

from view.DecryptPage_ui import Ui_decryptPageFrame
from view.DownloadPage_ui import Ui_downloadPageFrame
from view.FrontPage_ui import Ui_frontPageFrame
from view.SettingPage_ui import Ui_settingPageFrame
import resource.resource_rc


class FrontPageFrame(QFrame, Ui_frontPageFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.initTable()
        self.TableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.TableWidget.customContextMenuRequested.connect(self.contextMenuEvent_)
    
    def initTable(self):
        self.TableWidget.verticalHeader().setVisible(False)
        column_widths = [1, 4, 4, 2]
        total_width = sum(column_widths)
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_width = self.TableWidget.width()
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        for col, width in enumerate(column_widths):
            relative_width = width / total_width
            self.TableWidget.horizontalHeader().resizeSection(col, relative_width * table_width)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.initTable()
    
    def contextMenuEvent_(self, e):
        row = self.TableWidget.rowAt(e.y())
        self.TableWidget.selectRow(row)
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FIF.DOWNLOAD, '下载'))
        menu.exec_(self.mapToGlobal(e) + QPoint(10, 95), aniType=MenuAnimationType.FADE_IN_PULL_UP)


class DownloadPageFrame(QFrame, Ui_downloadPageFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.initTable()
        self.TableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.TableWidget.customContextMenuRequested.connect(self.contextMenuEvent_)
    
    def initTable(self):
        self.TableWidget.verticalHeader().setVisible(False)
        column_widths = [2, 2, 1, 1, 1]
        total_width = sum(column_widths)
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_width = self.TableWidget.width()
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        for col, width in enumerate(column_widths):
            relative_width = width / total_width
            self.TableWidget.horizontalHeader().resizeSection(col, relative_width * table_width)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.initTable()
    
    def contextMenuEvent_(self, e):
        row = self.TableWidget.rowAt(e.y())
        self.TableWidget.selectRow(row)
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FIF.DOCUMENT, '打开'))
        menu.addAction(Action(FIF.FOLDER, '在资源管理器中打开'))
        menu.exec_(self.mapToGlobal(e) + QPoint(10, 55), aniType=MenuAnimationType.FADE_IN_PULL_UP)


class DecryptPageFrame(QFrame, Ui_decryptPageFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class SettingPageFrame(QFrame, Ui_settingPageFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class Icon(FluentIconBase, Enum):
    LOCK = "lock"

    def path(self, theme=Theme.AUTO):
        return f":/{self.value}.svg"


class AvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage(':/shoko.png').scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw background
        if self.isEnter:
            painter.setBrush(QColor(0, 0, 0, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # draw avatar
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.black)
            font = QFont('Segoe UI')
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, 'BrandNewMe')


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.frontPageInterface = FrontPageFrame(self)
        self.downloadPageInterface = DownloadPageFrame(self)
        self.decryptPageInterface = DecryptPageFrame(self)
        self.settingPageInterface = SettingPageFrame(self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(self.frontPageInterface, FIF.HOME, '首页')
        self.addSubInterface(self.downloadPageInterface, FIF.DOWNLOAD, '下载列表')
        self.addSubInterface(self.decryptPageInterface, Icon.LOCK, 'XM解密')

        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget(),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        self.addSubInterface(self.settingPageInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

        #!IMPORTANT: don't forget to set the default route key if you enable the return button
        # qrouter.setDefaultRouteKey(self.stackWidget, self.musicInterface.objectName())

        # set the maximum width
        self.navigationInterface.setExpandWidth(250)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(1)
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/icon.png'))
        self.setWindowTitle('Ximalaya-Downloader')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)


    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, parent=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
            parentRouteKey=parent.objectName() if parent else None
        )

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

        #!IMPORTANT: This line of code needs to be uncommented if the return button is enabled
        # qrouter.push(self.stackWidget, widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            'This is a help message',
            'You clicked a customized navigation widget. You can add more custom widgets by calling `NavigationInterface.addWidget()` 😉',
            self
        )
        w.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
