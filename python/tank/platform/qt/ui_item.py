# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'item.ui'
#
# Created: Mon Mar  4 14:32:23 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from . import QtCore, QtGui

class Ui_Item(object):
    def setupUi(self, Item):
        Item.setObjectName("Item")
        Item.resize(415, 141)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Item.sizePolicy().hasHeightForWidth())
        Item.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Item)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name = QtGui.QLabel(Item)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        self.name.setStyleSheet("font-size: 14px;\n"
"border: none;\n"
"border-bottom-color: rgba(150,150,150,100);\n"
"border-bottom-width: 1px;\n"
"border-bottom-style: solid;\n"
"margin-top: 20px;")
        self.name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name.setWordWrap(True)
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.value = QtGui.QLabel(Item)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value.sizePolicy().hasHeightForWidth())
        self.value.setSizePolicy(sizePolicy)
        self.value.setStyleSheet("font-size: 12px;\n"
"margin-top: 2px;")
        self.value.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.value.setWordWrap(True)
        self.value.setObjectName("value")
        self.verticalLayout.addWidget(self.value)
        self.type = QtGui.QLabel(Item)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type.sizePolicy().hasHeightForWidth())
        self.type.setSizePolicy(sizePolicy)
        self.type.setStyleSheet("font-size: 12px;\n"
"margin-top: 2px;")
        self.type.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.type.setWordWrap(True)
        self.type.setObjectName("type")
        self.verticalLayout.addWidget(self.type)
        self.description = QtGui.QLabel(Item)
        self.description.setStyleSheet("font-size: 11px; margin-top: 2px")
        self.description.setTextFormat(QtCore.Qt.RichText)
        self.description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.description.setWordWrap(True)
        self.description.setObjectName("description")
        self.verticalLayout.addWidget(self.description)

        self.retranslateUi(Item)
        QtCore.QMetaObject.connectSlotsByName(Item)

    def retranslateUi(self, Item):
        Item.setWindowTitle(QtGui.QApplication.translate("Item", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.name.setText(QtGui.QApplication.translate("Item", "Settings Name", None, QtGui.QApplication.UnicodeUTF8))
        self.value.setText(QtGui.QApplication.translate("Item", "Value: foo bar", None, QtGui.QApplication.UnicodeUTF8))
        self.type.setText(QtGui.QApplication.translate("Item", "Type: bool", None, QtGui.QApplication.UnicodeUTF8))
        self.description.setText(QtGui.QApplication.translate("Item", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">description</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
