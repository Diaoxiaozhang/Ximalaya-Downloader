# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DownloadPage.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QWidget)

class Ui_downloadPageFrame(object):
    def setupUi(self, downloadPageFrame):
        if not downloadPageFrame.objectName():
            downloadPageFrame.setObjectName(u"downloadPageFrame")
        downloadPageFrame.resize(850, 650)
        downloadPageFrame.setStyleSheet(u"background-color: rgb(249, 249, 249);")
        self.horizontalLayout = QHBoxLayout(downloadPageFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(downloadPageFrame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)


        self.retranslateUi(downloadPageFrame)

        QMetaObject.connectSlotsByName(downloadPageFrame)
    # setupUi

    def retranslateUi(self, downloadPageFrame):
        downloadPageFrame.setWindowTitle(QCoreApplication.translate("downloadPageFrame", u"Frame", None))
        self.label.setText(QCoreApplication.translate("downloadPageFrame", u"\u4e0b\u8f7d\u5217\u8868", None))
    # retranslateUi

