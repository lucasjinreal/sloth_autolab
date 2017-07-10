from PyQt4.QtCore import *
from PyQt4.QtGui import *

class AttributeDialog(QDialog):
    def __init__(self, parent=None):
        super(AttributeDialog, self).__init__(parent)

        layout = QVBoxLayout(self)

        label = QLabel('ID: ')
        layout.addWidget(label)

        self.edit = QtGui.QLineEdit()
        layout.addWidget(self.edit)

        self.cb1 = QCheckBox('Occlusion')
        layout.addWidget(self.cb1)

        self.cb2 = QCheckBox('Illumination Variation')
        layout.addWidget(self.cb2)

        self.cb3 = QCheckBox('Motion Blur')
        layout.addWidget(self.cb3)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    
    @staticmethod
    def getAttributes(parent = None):
        dialog = AttributeDialog(parent)
        result = dialog.exec_()
        return (int(dialog.edit.text()), result == QDialog.Accepted)

    # def dateTime(self):
    #     return self.datetime.dateTime()

    # @staticmethod
    # def getDateTime(parent = None):
    #     dialog = AttributeDialog(parent)
    #     result = dialog.exec_()
    #     date = dialog.dateTime()
    #     return (date.date(), date.time(), result == QDialog.Accepted)


import sys
from PyQt4 import QtGui
from PyQt4 import QtCore


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.button = QtGui.QPushButton('Dialog', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)

        self.button.move(20, 20)
        self.connect(self.button, QtCore.SIGNAL('clicked()'),
            self.showDialog)
        self.setFocus()

        self.label = QtGui.QLineEdit(self)
        self.label.move(130, 22)

        self.setWindowTitle('InputDialog')
        self.setGeometry(300, 300, 350, 80)


    def showDialog(self):
        text, ok = AttributeDialog.getAttributes()
        if ok:
            self.label.setText(str(text))


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()