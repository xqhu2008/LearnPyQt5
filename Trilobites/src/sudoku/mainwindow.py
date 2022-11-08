#!/usr/bin/env python
# -*- coding : utf-8 -*-

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QEvent, QTimer

from sudokuui import Ui_sudokuMainWindow
from sudoku import Sudoku


class SudokuWindow(QWidget, Ui_sudokuMainWindow):

    def __init__(self, parent=None):
        super(SudokuWindow, self).__init__(parent)
        self.setupUi(self)

        self._labels = [
            [self.label1_1, self.label1_2, self.label1_3, self.label1_4, self.label1_5,
             self.label1_6, self.label1_7, self.label1_8, self.label1_9],
            [self.label2_1, self.label2_2, self.label2_3, self.label2_4, self.label2_5,
             self.label2_6, self.label2_7, self.label2_8, self.label2_9],
            [self.label3_1, self.label3_2, self.label3_3, self.label3_4, self.label3_5,
             self.label3_6, self.label3_7, self.label3_8, self.label3_9],
            [self.label4_1, self.label4_2, self.label4_3, self.label4_4, self.label4_5,
             self.label4_6, self.label4_7, self.label4_8, self.label4_9],
            [self.label5_1, self.label5_2, self.label5_3, self.label5_4, self.label5_5,
             self.label5_6, self.label5_7, self.label5_8, self.label5_9],
            [self.label6_1, self.label6_2, self.label6_3, self.label6_4, self.label6_5,
             self.label6_6, self.label6_7, self.label6_8, self.label6_9],
            [self.label7_1, self.label7_2, self.label7_3, self.label7_4, self.label7_5,
             self.label7_6, self.label7_7, self.label7_8, self.label7_9],
            [self.label8_1, self.label8_2, self.label8_3, self.label8_4, self.label8_5,
             self.label8_6, self.label8_7, self.label8_8, self.label8_9],
            [self.label9_1, self.label9_2, self.label9_3, self.label9_4, self.label9_5,
             self.label9_6, self.label9_7, self.label9_8, self.label9_9],
        ]

        self._buttons = [None, self.numberButton1, self.numberButton2, self.numberButton3,
                               self.numberButton4, self.numberButton5, self.numberButton6,
                               self.numberButton7, self.numberButton8, self.numberButton9]

        self._currentNumber = 0
        self._comsumTime = -1
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.timeoutProcess)

        for i in range(Sudoku.rows):
            for j in range(Sudoku.cols):
                self._labels[i][j].installEventFilter(self)

        for i in range(1, 10):
            self._buttons[i].clicked.connect(self.selectCurrentNumber)
            self._buttons[i].setStyleSheet("QPushButton{background-color:rgb(224,224,224)}")

        self.newGameButton.clicked.connect(self.startNewGame)

        self.comsumeTime.setStyleSheet("QLabel{background-color:rgb(0,0,0)}")

    def selectCurrentNumber(self):
        sender = self.sender()
        number = int(sender.text())
        if self._currentNumber != 0:
            self._buttons[self._currentNumber].setChecked(False)
            self._buttons[self._currentNumber].setStyleSheet("QPushButton{background-color:rgb(224,224,224)}")

        if number != self._currentNumber:
            self._currentNumber = number
            self._buttons[self._currentNumber].setChecked(True)
            self._buttons[self._currentNumber].setStyleSheet("QPushButton{background-color:rgb(170,200,50)}")
        else:
            self._currentNumber = 0

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if self._currentNumber != 0:
                obj.setText(str(self._currentNumber))
            return True

        return False

    def startNewGame(self):
        sudo = Sudoku.produceSudoku()
        self.updateSudokuWindow(sudo)
        self._timer.stop()
        self._timer.start(1000)
        self._comsumTime = -1
        self.updateComsumeTime()

    def updateComsumeTime(self):
        self._comsumTime += 1

        minute, second = divmod(self._comsumTime, 60)
        self.comsumeTime.setText(f"{minute}:{second:02d}")

    def timeoutProcess(self):
        self.updateComsumeTime()
        self._timer.start(1000)

    def updateSudokuWindow(self, sudo):
        for i in range(Sudoku.rows):
            for j in range(Sudoku.cols):
                if sudo[i, j] != 0:
                    self._labels[i][j].setText(str(sudo[i, j]))
                else:
                    self._labels[i][j].setText(' ')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    sudo = SudokuWindow()
    sudo.show()
    sys.exit(app.exec_())


