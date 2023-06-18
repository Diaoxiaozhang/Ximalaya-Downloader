# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrontPage.ui'
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
    QHeaderView, QLabel, QSizePolicy, QSpacerItem,
    QTableWidgetItem, QVBoxLayout, QWidget)

from qfluentwidgets import (CheckBox, LineEdit, PushButton, TableWidget)

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
        self.TableWidget.setObjectName(u"TableWidget")
        font = QFont()
        font.setPointSize(9)
        self.TableWidget.setFont(font)
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TableWidget.setSelectionMode(QAbstractItemView.NoSelection)

        self.verticalLayout.addWidget(self.TableWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, -1)
        self.CheckBox = CheckBox(frontPageFrame)
        self.CheckBox.setObjectName(u"CheckBox")

        self.horizontalLayout_2.addWidget(self.CheckBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_2 = QLabel(frontPageFrame)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setFamilies([u"Microsoft YaHei UI"])
        font1.setPointSize(10)
        font1.setBold(False)
        self.label_2.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.LineEdit_3 = LineEdit(frontPageFrame)
        self.LineEdit_3.setObjectName(u"LineEdit_3")
        self.LineEdit_3.setMinimumSize(QSize(60, 30))
        self.LineEdit_3.setMaximumSize(QSize(60, 30))

        self.horizontalLayout_2.addWidget(self.LineEdit_3)

        self.label = QLabel(frontPageFrame)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setFamilies([u"Microsoft YaHei UI"])
        font2.setPointSize(10)
        self.label.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label)

        self.LineEdit_2 = LineEdit(frontPageFrame)
        self.LineEdit_2.setObjectName(u"LineEdit_2")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_2.sizePolicy().hasHeightForWidth())
        self.LineEdit_2.setSizePolicy(sizePolicy)
        self.LineEdit_2.setMinimumSize(QSize(60, 30))
        self.LineEdit_2.setMaximumSize(QSize(60, 30))

        self.horizontalLayout_2.addWidget(self.LineEdit_2)

        self.label_3 = QLabel(frontPageFrame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.PushButton_2 = PushButton(frontPageFrame)
        self.PushButton_2.setObjectName(u"PushButton_2")
        self.PushButton_2.setMinimumSize(QSize(60, 30))
        self.PushButton_2.setMaximumSize(QSize(60, 30))

        self.horizontalLayout_2.addWidget(self.PushButton_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.PushButton_3 = PushButton(frontPageFrame)
        self.PushButton_3.setObjectName(u"PushButton_3")
        self.PushButton_3.setMinimumSize(QSize(80, 30))
        self.PushButton_3.setMaximumSize(QSize(80, 30))

        self.horizontalLayout_2.addWidget(self.PushButton_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


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
        ___qtablewidgetitem.setText(QCoreApplication.translate("frontPageFrame", u"\u5e8f\u53f7", None));
        ___qtablewidgetitem1 = self.TableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("frontPageFrame", u"\u58f0\u97f3\u540d", None));
        ___qtablewidgetitem2 = self.TableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("frontPageFrame", u"\u4e13\u8f91\u540d", None));
        ___qtablewidgetitem3 = self.TableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("frontPageFrame", u"\u65f6\u957f", None));
        self.CheckBox.setText(QCoreApplication.translate("frontPageFrame", u"\u6587\u4ef6\u540d\u6dfb\u52a0\u5e8f\u53f7", None))
        self.label_2.setText(QCoreApplication.translate("frontPageFrame", u"\u4ece\u7b2c", None))
        self.label.setText(QCoreApplication.translate("frontPageFrame", u"\u96c6\u5230\u7b2c", None))
        self.label_3.setText(QCoreApplication.translate("frontPageFrame", u"\u96c6", None))
        self.PushButton_2.setText(QCoreApplication.translate("frontPageFrame", u"\u4e0b\u8f7d", None))
        self.PushButton_3.setText(QCoreApplication.translate("frontPageFrame", u"\u5168\u90e8\u4e0b\u8f7d", None))
    # retranslateUi

