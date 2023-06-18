# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingPage.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from enum import Enum
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,QMetaObject,
                            QObject, QPoint, QRect,QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,QFont, 
                           QFontDatabase, QGradient, QIcon,QImage, QKeySequence, 
                           QLinearGradient, QPainter,QPalette, QPixmap, QRadialGradient, 
                           QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,QVBoxLayout, 
                               QWidget, QFileDialog, QSpacerItem)
from qfluentwidgets import (SettingCardGroup, PushSettingCard, QConfig, ConfigItem,
                            FolderValidator, OptionsSettingCard, PrimaryPushSettingCard, 
                            FluentIconBase, Theme, HyperlinkCard, ExpandLayout)
from qfluentwidgets import FluentIcon as FIF
from main import VERSION
import resource.resource_rc

GITHUB_URL = 'https://github.com/Diaoxiaozhang/Ximalaya-Downloader'

class Ui_settingPageFrame(object):
    def setupUi(self, settingPageFrame):
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self.settingLabel = QLabel('设置', settingPageFrame)
        self.settingLabel.setFont(QFont('Microsoft YaHei UI', 20))

        self.downloadGroup = SettingCardGroup('下载设置', self.scrollWidget)
        self.downloadFolderCard = PushSettingCard('选择文件夹', FIF.DOWNLOAD, '下载目录', Config().get(Config().downloadFolder), self.downloadGroup)
        self.downloadFolderCard.clicked.connect(self.onDownloaderFolderCardClicked)
        self.downloadGroup.addSettingCard(self.downloadFolderCard)
        self.soundQualityCard = OptionsSettingCard(Config().themeMode, FIF.MUSIC, '音质', '选择下载声音的音质', texts=['高音质', '标准音质', '低音质'], parent=self.downloadGroup)
        self.downloadGroup.addSettingCard(self.soundQualityCard)
        
        self.aboutGroup = SettingCardGroup('关于', self.scrollWidget)
        self.helpCard = HyperlinkCard(GITHUB_URL, '打开Github页面', FIF.HELP, '帮助', '如果您遇到问题，请在Github上寻找解决方法，如果没有可以提出issue', self.aboutGroup)
        self.aboutGroup.addSettingCard(self.helpCard)
        self.donateCard = PrimaryPushSettingCard('显示捐赠二维码', Icon.GIFT, '捐赠', '如果你觉得这个软件不错，可以考虑捐赠作者以支持软件的发展', self.aboutGroup)
        self.aboutGroup.addSettingCard(self.donateCard)
        self.versionCard = PrimaryPushSettingCard('检查更新', FIF.INFO, '版本', f'当前版本：{VERSION}', self.aboutGroup)
        self.aboutGroup.addSettingCard(self.versionCard)

        # QMetaObject.connectSlotsByName(settingPageFrame)
    # setupUi

    def onDownloaderFolderCardClicked(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if not folder or Config().get(Config().downloadFolder) == folder:
            return


class Config(QConfig):
    downloadFolder = ConfigItem("Folders", "Download", "app/download", FolderValidator())


class Icon(FluentIconBase, Enum):
    GIFT = "gift"

    def path(self, theme=Theme.AUTO):
        return f":/{self.value}.svg"