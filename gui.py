# coding:utf-8
'''
这是一个使用PySide6库编写的Python应用程序，用于创建一个具有侧边导航栏和多个可切换页面的无边框窗口。代码的主要部分包括：
 1. 导入所需的库和模块。
2. 定义不同的子界面（如 FrontPageFrame, DownloadPageFrame, DecryptPageFrame, SettingPageFrame），这些子界面都继承自 QFrame。
3. 创建 AvatarWidget 类，绘制带有头像的自定义导航窗口部件。
4. 定义 Window 类，继承自 FramelessWindow，设置窗口大小、标题栏和侧边导航栏。
5. 初始化用户界面布局、导航栏选项以及窗口设置。
6. 使用 addSubInterface 方法将子界面添加到导航栏。
7. 使用 QStackedWidget 切换不同的子界面。
8. 连接信号和槽（如当当前界面改变时，调用 onCurrentInterfaceChanged 方法）。
9. 在点击 AvatarWidget 时调用 showMessageBox 方法，显示一个消息框。
 应用程序的界面包括主页、下载列表、XM解密和设置等页面，可以通过点击侧边栏的选项在这些页面之间进行切换。
'''
import sys
from typing import Optional
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont
from PySide6.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, qrouter)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar

from view.DecryptPage import Ui_decryptPageFrame
from view.DownloadPage import Ui_downloadPageFrame
from view.FrontPage import Ui_frontPageFrame
from view.SettingPage import Ui_settingPageFrame


class FrontPageFrame(QFrame, Ui_frontPageFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class DownloadPageFrame(QFrame, Ui_downloadPageFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class DecryptPageFrame(QFrame, Ui_decryptPageFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class SettingPageFrame(QFrame, Ui_settingPageFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class AvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage('resource/shoko.png').scaled(
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
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # draw avatar
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            font = QFont('Segoe UI')
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, 'BrandNewMe')


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        # use dark theme mode
        # setTheme(Theme.DARK)

        # change the theme color
        # setThemeColor('#0078d4')

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
        self.addSubInterface(self.decryptPageInterface, FIF.UNPIN, 'XM解密')

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
        self.setWindowIcon(QIcon('resource/favicon.png'))
        self.setWindowTitle('Ximalaya-Downloader')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.setQss()

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

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

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
