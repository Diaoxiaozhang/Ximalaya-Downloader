# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrontPage.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QSizePolicy, QTableWidgetItem, QVBoxLayout, QWidget)

from qfluentwidgets import (LineEdit, PushButton, TableWidget)

class Ui_frontPageFrame(object):
    def setupUi(self, frontPageFrame):
        if not frontPageFrame.objectName():
            frontPageFrame.setObjectName(u"frontPageFrame")
        frontPageFrame.resize(850, 650)
        frontPageFrame.setStyleSheet(u"background-color: rgb(249, 249, 249);")
        self.verticalLayout = QVBoxLayout(frontPageFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.LineEdit = LineEdit(frontPageFrame)
        self.LineEdit.setObjectName(u"LineEdit")

        self.horizontalLayout.addWidget(self.LineEdit)

        self.PushButton = PushButton(frontPageFrame)
        self.PushButton.setObjectName(u"PushButton")

        self.horizontalLayout.addWidget(self.PushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.TableWidget = TableWidget(frontPageFrame)
        if (self.TableWidget.columnCount() < 4):
            self.TableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.TableWidget.rowCount() < 1):
            self.TableWidget.setRowCount(1)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.TableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.TableWidget.setItem(0, 0, __qtablewidgetitem5)
        self.TableWidget.setObjectName(u"TableWidget")

        self.verticalLayout.addWidget(self.TableWidget)


        self.retranslateUi(frontPageFrame)

        QMetaObject.connectSlotsByName(frontPageFrame)
    # setupUi

    def retranslateUi(self, frontPageFrame):
        frontPageFrame.setWindowTitle(QCoreApplication.translate("frontPageFrame", u"Frame", None))
#if QT_CONFIG(whatsthis)
        self.LineEdit.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.LineEdit.setPlaceholderText(QCoreApplication.translate("frontPageFrame", u"\u8bf7\u8f93\u5165\u58f0\u97f3\u6216\u4e13\u8f91\u7684\u94fe\u63a5", None))
        self.PushButton.setText(QCoreApplication.translate("frontPageFrame", u"\u89e3\u6790", None))
        ___qtablewidgetitem = self.TableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("frontPageFrame", u"\u58f0\u97f3\u540d", None));
        ___qtablewidgetitem1 = self.TableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("frontPageFrame", u"\u4e13\u8f91\u540d", None));
        ___qtablewidgetitem2 = self.TableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("frontPageFrame", u"\u65f6\u957f", None));
        ___qtablewidgetitem3 = self.TableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("frontPageFrame", u"test", None));

        __sortingEnabled = self.TableWidget.isSortingEnabled()
        self.TableWidget.setSortingEnabled(False)
        self.TableWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

