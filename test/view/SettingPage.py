# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingPage.ui'
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

class Ui_settingPageFrame(object):
    def setupUi(self, settingPageFrame):
        if not settingPageFrame.objectName():
            settingPageFrame.setObjectName(u"settingPageFrame")
        settingPageFrame.resize(850, 650)
        settingPageFrame.setStyleSheet(u"background-color: rgb(249, 249, 249);")
        self.horizontalLayout = QHBoxLayout(settingPageFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(settingPageFrame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)


        self.retranslateUi(settingPageFrame)

        QMetaObject.connectSlotsByName(settingPageFrame)
    # setupUi

    def retranslateUi(self, settingPageFrame):
        settingPageFrame.setWindowTitle(QCoreApplication.translate("settingPageFrame", u"Frame", None))
        self.label.setText(QCoreApplication.translate("settingPageFrame", u"\u8bbe\u7f6e", None))
    # retranslateUi

