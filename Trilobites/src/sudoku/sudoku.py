#!/usr/bin/env python
# -*- coding : utf-8 -*-

import numpy as np
from enum import Enum


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

    def __init__(self, sudo=None):
        if sudo is None:
            self._level = SudokuLevel.P
            self._boards = np.zeros((Sudoku.rows, Sudoku.cols), dtype=np.int8)
        else:
            self.loadFomString(sudo)

    def __getitem__(self, index):
        return self._boards[index]

    def __setitem__(self, key, value):
        self._boards[key] = value

    def loadFomString(self, sudo):
        s = sudo.split(', ')
        self._level = self._parseSudokuLevel(s[0])
        for i in range(self.rows):
            for j in range(self.cols):
                self[i, j] = int(s[i * self.cols + j + 1])

    def _parseSudokuLevel(self, s):
        for level in SudokuLevel:
            if level.value == 's':
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

    @staticmethod
    def produceSudoku(level=SudokuLevel.P):
        sudo = Sudoku()
        sudo.loadFomString("P, 0, 4, 0, 0, 0, 2, 0, 1, 9, "
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
    print(sudo)

    sudo.loadFomString("P, 0, 4, 0, 0, 0, 2, 0, 1, 9, 0, 0, 0, 3, 5, 1, 0, 8, 6, 3, 1, 0, 0, 9, 4, 7, 0, 0, 0, 9, 4, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 8, 9, 0, 0, 0, 9, 5, 2, 0, 0, 4, 1, 4, 2, 0, 1, 6, 9, 0, 0, 0, 1, 6, 0, 8, 0, 0, 0, 7, 0")
    print(sudo)