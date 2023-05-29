# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DecryptPage.ui'
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

class Ui_decryptPageFrame(object):
    def setupUi(self, decryptPageFrame):
        if not decryptPageFrame.objectName():
            decryptPageFrame.setObjectName(u"decryptPageFrame")
        decryptPageFrame.resize(850, 650)
        decryptPageFrame.setStyleSheet(u"background-color: rgb(249, 249, 249);")
        self.horizontalLayout = QHBoxLayout(decryptPageFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(decryptPageFrame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)


        self.retranslateUi(decryptPageFrame)

        QMetaObject.connectSlotsByName(decryptPageFrame)
    # setupUi

    def retranslateUi(self, decryptPageFrame):
        decryptPageFrame.setWindowTitle(QCoreApplication.translate("decryptPageFrame", u"Frame", None))
        self.label.setText(QCoreApplication.translate("decryptPageFrame", u"XM\u89e3\u5bc6", None))
    # retranslateUi

