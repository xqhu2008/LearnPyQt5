#!/usr/bin/env python
# -*- coding : utf-8 -*-

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import QEvent, QTimer

from sudokuui import Ui_sudokuMainWindow
from sudoku import Sudoku, SudokuLevel


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
        self._originSudoku = Sudoku()
        self._currentSudoku = Sudoku()

        self._operationList = []

        for i in range(Sudoku.rows):
            for j in range(Sudoku.cols):
                self._labels[i][j].installEventFilter(self)

        for i in range(1, 10):
            self._buttons[i].clicked.connect(self.selectCurrentNumber)
            self._buttons[i].setStyleSheet("QPushButton{background-color:rgb(224,224,224)}")

        self.newGameButton.clicked.connect(self.startNewGame)
        self.restartButton.clicked.connect(self.restartGame)
        self.rollbackButton.clicked.connect(self.rollbackGame)

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
                x, y = self.findMouseClickPos(obj)
                if x != -1 and y != -1:
                    self._currentSudoku[x, y] = self._currentNumber
                    self._operationList.append((x, y, self._currentNumber))

                obj.setText(str(self._currentNumber))
                obj.setStyleSheet("QLabel{background-color:rgb(170,200,50)}")
            return True

        return False

    def findMouseClickPos(self, obj):
        for i in range(Sudoku.rows):
            for j in range(Sudoku.cols):
                if self._labels[i][j] == obj:
                    return i, j
        return -1, -1

    def initGame(self):
        self._currentSudoku = self._originSudoku.copy()
        self._operationList = []

    def getGameLevel(self):
        levels = {
            "初级" : SudokuLevel.P,
            "中级" : SudokuLevel.M,
            "高级" : SudokuLevel.H,
            "特级" : SudokuLevel.S,
            "超级" : SudokuLevel.T
        }

        return levels.setdefault(self.gameLevelComboBox.currentText(), SudokuLevel.P)

    def startNewGame(self):
        # self._originSudoku = Sudoku.buildSudoku()
        self._originSudoku = Sudoku.generateSudoku(self.getGameLevel())
        self.initGame()

        self.updateSudokuWindow(self._originSudoku)
        self._timer.stop()
        self._timer.start(1000)
        self._comsumTime = -1
        self.updateComsumeTime()

        if self._currentNumber != 0:
            self._buttons[self._currentNumber].setChecked(False)
            self._buttons[self._currentNumber].setChecked(False)
            self._buttons[self._currentNumber].setStyleSheet("QPushButton{background-color:rgb(224,224,224)}")
            self._currentNumber = 0

    def restartGame(self):
        self.initGame()
        self.updateSudokuWindow(self._originSudoku)
        self._timer.stop()
        self._timer.start(1000)
        self._comsumTime = -1
        self.updateComsumeTime()

        if self._currentNumber != 0:
            self._buttons[self._currentNumber].setChecked(False)
            self._buttons[self._currentNumber].setChecked(False)
            self._buttons[self._currentNumber].setStyleSheet("QPushButton{background-color:rgb(224,224,224)}")
            self._currentNumber = 0

    def rollbackGame(self):
        if len(self._operationList) == 0:
            return

        x, y, num = self._operationList.pop()
        self._currentSudoku[x, y] = 0
        self._labels[x][y].setText(' ')

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
                    self._labels[i][j].setStyleSheet("QLabel{background-color:rgb(232,232,232)}")
                else:
                    self._labels[i][j].setText(' ')
                    self._labels[i][j].setStyleSheet("QLabel{background-color:rgb(232,232,232)}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    sudo = SudokuWindow()
    sudo.show()
    sys.exit(app.exec_())


