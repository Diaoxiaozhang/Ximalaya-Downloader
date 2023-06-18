# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DownloadPage.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QSizePolicy, QTableWidgetItem, QWidget)

from qfluentwidgets import TableWidget

class Ui_downloadPageFrame(object):
    def setupUi(self, downloadPageFrame):
        if not downloadPageFrame.objectName():
            downloadPageFrame.setObjectName(u"downloadPageFrame")
        downloadPageFrame.resize(850, 650)
        downloadPageFrame.setStyleSheet(u"background-color: rgb(249, 249, 249);")
        self.horizontalLayout = QHBoxLayout(downloadPageFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TableWidget = TableWidget(downloadPageFrame)
        if (self.TableWidget.columnCount() < 5):
            self.TableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.TableWidget.setObjectName(u"TableWidget")
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TableWidget.setSelectionMode(QAbstractItemView.NoSelection)

        self.horizontalLayout.addWidget(self.TableWidget)


        self.retranslateUi(downloadPageFrame)

        QMetaObject.connectSlotsByName(downloadPageFrame)
    # setupUi

    def retranslateUi(self, downloadPageFrame):
        downloadPageFrame.setWindowTitle(QCoreApplication.translate("downloadPageFrame", u"Frame", None))
        ___qtablewidgetitem = self.TableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("downloadPageFrame", u"\u58f0\u97f3\u540d", None));
        ___qtablewidgetitem1 = self.TableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("downloadPageFrame", u"\u4e13\u8f91\u540d", None));
        ___qtablewidgetitem2 = self.TableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("downloadPageFrame", u"\u65f6\u957f", None));
        ___qtablewidgetitem3 = self.TableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("downloadPageFrame", u"\u5927\u5c0f", None));
        ___qtablewidgetitem4 = self.TableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("downloadPageFrame", u"\u4e0b\u8f7d\u8fdb\u5ea6", None));
    # retranslateUi

