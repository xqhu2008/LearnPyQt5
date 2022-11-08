#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
from enum import Enum


def calculteBeamforming(ant, d=0.5, theta0=0):
    step = 0.001 * np.pi
    theta = np.arange(-0.5 * np.pi, 0.5 * np.pi + step, step)
    beam = sum([np.exp(2.0j * np.pi * d * i * (np.sin(theta) - np.sin(theta0))) for i in range(ant)])

    return theta, np.abs(beam)


def calculteWeightedBeamforming(ant, d=0.5, weights=None):
    step = 0.001 * np.pi
    theta = np.arange(-0.5 * np.pi, 0.5 * np.pi + step, step)
    beam = sum([np.exp(2.0j * np.pi * d * i * (np.sin(theta) - np.sin(theta0))) for i in range(ant)])

    return theta, np.abs(beam)


class BeamformingWeightType(Enum):
    Normal = 0
    DFT = 1
    EDFT = 2
    Chebyshev = 3


class Beamforming:
    MIN_DB = -25

    def __init__(self, ant, d=0.5, *,
                 weightType=BeamformingWeightType.DFT,
                 oversamples=1,
                 offset=0,
                 logtrans=False,
                 normalize=False):
        self._ant = ant
        self._d = d
        self._oversamples = oversamples
        self._weightType = weightType
        self._offset = offset
        self._logtrans = logtrans
        self._normalize = normalize

    def calculateBeamforming(self, beamid=0, *, phi=0):
        thetas = np.linspace((0 - self._offset) * np.pi / 180, (180 - self._offset) * np.pi / 180, 1000)
        beams = []
        for theta in thetas:
            beam = np.array([np.exp(2.0j * np.pi * self._d * i * (np.sin(theta) - phi * np.pi / 180))
                             for i in range(self._ant)])
            beam = np.abs(np.sum(beam * self._calculateWeights(beamid)))
            if self._logtrans:
                beam = value if (value := 10 * np.log10(beam)) >= Beamforming.MIN_DB else Beamforming.MIN_DB

            beams.append(beam)

        beams = np.array(beams)
        if self._normalize:
            beams = beams / max(beams)

        return thetas, beams

    def _calculateWeights(self, beamid):
        if self._weightType == BeamformingWeightType.Normal:
            return np.array([1 for _ in range(self._ant)])
        elif self._weightType == BeamformingWeightType.DFT:
            return np.array([np.exp(-2.0j * np.pi * beamid * n / (self._ant * self._oversamples))
                             for n in range(self._ant)])
        elif self._weightType == BeamformingWeightType.EDFT:
            return np.array([np.exp(-2.0j * np.pi * (beamid + 0.5) * n / (self._ant * self._oversamples))
                             for n in range(self._ant)])
        elif self._weightType == BeamformingWeightType.Chebyshev:
            # TODO: for chebyshev algorithm
            return np.array([1 for _ in range(self._ant)])


class ChebyshevWeight:

    def __init__(self, ant):
        self._ant = ant

    def calculateWeights(self, beamid):
        pass


if __name__ == "__main__":
    # samples = np.linspace(-1.0 * (2.0 * np.pi) / 6.0, (2.0 * np.pi) / 6.0, 8)
    #
    # # x, y = beamforming(4, 0.5, samples[3])
    # # plt.polar(x, np.abs(y), label=str(2))
    #
    # for i, theta in enumerate(samples):
    #     x, y = calculteBeamforming(4, 0.5, theta)
    #     plt.plot(x, np.abs(y), label=str(i))

    bf = Beamforming(8, 0.5, weightType=BeamformingWeightType.EDFT)
    for i in range(8):
        theta, beam = bf.calculateBeamforming(i, phi=30)
        # plt.plot(theta, beam, label=f"beam id = {i}")
        #
        plt.polar(theta, beam, label=f"beam id = {i}")

    plt.legend()
    plt.show()