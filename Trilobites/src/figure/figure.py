#!/usr/bin/env python
# -*- coding : utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    x = np.linspace(-2, 2, 1000)
    for i in range(1, 7):
        plt.plot(x, x ** i)
    plt.show()
