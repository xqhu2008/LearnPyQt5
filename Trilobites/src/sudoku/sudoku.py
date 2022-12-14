#!/usr/bin/env python
# -*- coding : utf-8 -*-

import numpy as np
from enum import Enum
from functools import reduce
from typing import *


class SudokuLevel(Enum):
    P = 'P'
    M = 'M'
    H = 'H'
    S = 'S'
    T = 'T'


class Sudoku:
    rows = 9
    cols = 9
    boxes = 3

    def __init__(self, sudo : str = None) -> None:
        self._level = SudokuLevel.P
        self._boards = np.zeros((Sudoku.rows, Sudoku.cols), dtype=np.int8)

        if sudo is not None:
            self.loadFomString(sudo)

    def __getitem__(self, index):
        return self._boards[index]

    def __setitem__(self, key, value):
        self._boards[key] = value

    def findEmpty(self):
        for i in range(Sudoku.rows):
            for j in range(Sudoku.cols):
                if self[i, j] == 0:
                    return i, j
        return Sudoku.rows, Sudoku.cols

    def isSolved(self):
        row, col = self.findEmpty()
        return True if row >= Sudoku.rows or col >= Sudoku.cols else False

    def isValid(self, row, col, num):
        if num in self[row, :]:
            return False

        if num in self[:, col]:
            return False

        rowBlockStart = row // Sudoku.boxes * Sudoku.boxes
        rowBlockEnd = rowBlockStart + Sudoku.boxes
        colBlockStart = col // Sudoku.boxes * Sudoku.boxes
        colBlockEnd = colBlockStart + Sudoku.boxes

        if num in self[rowBlockStart : rowBlockEnd, colBlockStart : colBlockEnd]:
            return False

        return True

    def solve(self):
        row, col = self.findEmpty()
        if row >= Sudoku.rows or col >= Sudoku.cols:
            return True

        for num in range(1, Sudoku.rows + 1):
            if self.isValid(row, col, num):
                self[row, col] = num

                if self.solve():
                    return True

                self[row, col] = 0

        return False

    # def solveWithCached(self):
    #     row, col = self.findEmpty()
    #     if row >= Sudoku.rows or col >= Sudoku.cols:
    #         return True
    #
    #     for num in self.findAllowedNumber(row, col):
    #         if self.isValid(row, col, num):
    #             self[row, col] = num
    #
    #             if self.solveWithCached():
    #                 return True
    #
    #             self[row, col] = 0
    #
    #     return False

    @staticmethod
    def generateSudoku(level=SudokuLevel.M):
        maskRateTable = {
            SudokuLevel.P : 0.4,
            SudokuLevel.M : 0.5,
            SudokuLevel.H : 0.6,
            SudokuLevel.S : 0.7,
            SudokuLevel.T : 0.8
        }

        rate = maskRateTable[level]

        while True:
            m = np.zeros((Sudoku.rows, Sudoku.cols), dtype=np.int8)
            n = Sudoku.rows
            rg = np.arange(1, n + 1)
            m[0, :] = np.random.choice(rg, n, replace=False)
            try :
                for r in range(1, n):
                    for c in range(n):
                        colRest = np.setdiff1d(rg, m[:r, c])
                        rowRest = np.setdiff1d(rg, m[r, :c])
                        avb1 = np.intersect1d(colRest, rowRest)
                        boxR, boxC = r//3 * 3, c//3 * 3
                        avb2 = np.setdiff1d(np.arange(0, n+1), m[boxR : boxR + 3, boxC : boxC + 3].ravel())
                        avb = np.intersect1d(avb1, avb2)
                        m[r, c] = np.random.choice(avb, size=1)
                break
            except ValueError:
                pass

        mm = m.copy()
        mm[np.random.choice([True, False], size=m.shape, p=[rate, 1 - rate])] = 0

        return Sudoku(level.value + ', ' + ", ".join(map(str, mm.ravel())))

    def findAllowedNumber(self, row, col):
        colRest = self[row, :].tolist()
        rowRest = self[:, col].tolist()
        boxRest = self[row//3 * 3:row//3 * 3 + 3, col//3 * 3:col//3 * 3 + 3].ravel().tolist()
        return np.array(set(range(self.rows + 1)) - set(colRest + rowRest + boxRest))

    def findConflictedNumber(self, row, col, num):
        pos = set()
        colRest = np.argwhere(self[row, :] == num)
        for y in colRest:
            pos.add((row, y[0]))

        rowRest = np.argwhere(self[:, col] == num)
        for x in rowRest:
            pos.add((x[0], col))
        boxRest = np.argwhere(self[row//3 * 3 : row//3 * 3 + 3, col//3 * 3 : col//3 * 3 + 3] == num)
        for p in boxRest:
            pos.add((p[0] + row//3 * 3, p[1]+col//3 * 3))

        return np.array(pos)

    def findConflictedPos(self, row, col):
        back = self[row, col]
        self[row, col] = 0
        result = self._findConflictedNumber(row, col, back)
        self[row, col] = back
        if len(result) != 0:
            result.add((row, col))

        return result

    def loadFomString(self, sudo):
        s = sudo.split(', ')
        self._level = self.parseSudokuLevel(s[0])
        for i in range(self.rows):
            for j in range(self.cols):
                self[i, j] = int(s[i * self.cols + j + 1])

    def parseSudokuLevel(self, s):
        for level in SudokuLevel:
            if level.value == s:
                return level
        return SudokuLevel.P

    def copy(self):
        return Sudoku(repr(self))

    def __repr__(self):
        sudo = [self._level.value]
        for i in range(self.rows):
            for j in range(self.cols):
                sudo.append(f'{self[i, j]}')

        return ", ".join(sudo)

    def __str__(self):
        result = []
        for i in range(Sudoku.rows):
            result.append(",".join([f"{num}" for num in self[i, :]]))

        return "\n".join(result)

    @staticmethod
    def buildSudoku(level=SudokuLevel.P):
        sudo = Sudoku()
        sudo.loadFomString("P, "
                           "0, 4, 0, 0, 0, 2, 0, 1, 9, "
                           "0, 0, 0, 3, 5, 1, 0, 8, 6, "
                           "3, 1, 0, 0, 9, 4, 7, 0, 0, "
                           "0, 9, 4, 0, 0, 0, 0, 0, 7, "
                           "0, 0, 0, 0, 0, 0, 0, 0, 0, "
                           "2, 0, 0, 0, 0, 0, 8, 9, 0, "
                           "0, 0, 9, 5, 2, 0, 0, 4, 1, "
                           "4, 2, 0, 1, 6, 9, 0, 0, 0, "
                           "1, 6, 0, 8, 0, 0, 0, 7, 0")

        return sudo


if __name__ == "__main__":
    sudo = Sudoku()

    sudo.loadFomString("P, "
                       "0, 4, 0, 0, 0, 2, 0, 1, 9, "
                       "0, 0, 0, 3, 5, 1, 0, 8, 6, "
                       "3, 1, 0, 0, 9, 4, 7, 0, 0, "
                       "0, 9, 4, 0, 0, 0, 0, 0, 7, "
                       "0, 0, 0, 0, 0, 0, 0, 0, 0, "
                       "2, 0, 0, 0, 0, 0, 8, 9, 0, "
                       "0, 0, 9, 5, 2, 0, 0, 4, 1, "
                       "4, 2, 0, 1, 6, 9, 0, 0, 0, "
                       "1, 6, 0, 8, 0, 0, 0, 7, 0")
    print(sudo)
    sudo.solveWithCached()
    print("\n")
    print(sudo)
    # # print(Sudoku.generateSudoku())
    # print(sudo.findConflictedNumber(2, 2, 4))
    # print(sudo.findAllowedNumber(0, 0))