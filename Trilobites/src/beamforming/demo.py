import matplotlib.pyplot as plt

from beamforming.BeamDemo import Ui_Dialog
from beamforming.beam import Beamforming, BeamformingWeightType

from PyQt5.QtWidgets import QApplication, QDialog

import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
plt.style.use('seaborn-whitegrid')
# plt.style.use('ggplot')
# plt.rcParams['font.family'] = 'microsoft YaHei'


class BeamformingCanvas(FigureCanvas):

    def __init__(self, parent=None):
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

    def drawFigure(self, x, y, polar=False, grid=False, legends=None, title=None, ticks=None):
        self.figure.clear()
        axes = self.figure.add_subplot(111, polar=polar)
        if legends is None:
            for i, val in enumerate(y):
                axes.plot(x, val)
        else:
            for i, val in enumerate(y):
                axes.plot(x, val, label=legends[i])

        axes.grid(grid)

        if legends:
            axes.legend()

        if title:
            axes.set_title(title)
        axes.set_xlabel([f'{(x1 * 180 / np.pi) : .01f}' for x1 in x])

        self.draw()


class BeamformingDialog(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.figure = BeamformingCanvas(self)
        self.figureGridLayout.addWidget(self.figure)
        self.updateButton.clicked.connect(self.updateFigure)
        self.antennaNumberSlider.valueChanged.connect(self.updateAntennaNumber)
        self.antennaSpaceSlider.valueChanged.connect(self.updateAntennaSpace)
        self.beamNumberSlider.valueChanged.connect(self.updateBeamNumber)
        self.displayLegendCheckBox.stateChanged.connect(self.updateDisplayConfiguraton)
        self.displayNormalCheckBox.stateChanged.connect(self.updateDisplayConfiguraton)
        self.polarButton.clicked.connect(self.updateDisplayConfiguraton)
        self.plotButton.clicked.connect(self.updateDisplayConfiguraton)

        self.updateFigure()

    def updateDisplayConfiguraton(self, value):
        self.updateFigure()

    def updateBeamNumber(self, value):
        self.beamNumberEdit.setText(str(value))
        self.updateFigure()

    def updateAntennaNumber(self, value):
        self.antennaNumberEdit.setText(str(value))
        self.updateFigure()

    def updateAntennaSpace(self, value):
        self.antennaSpaceEdit.setText(str(value/10))
        self.updateFigure()

    def updateFigure(self):
        ant = int(self.antennaNumberEdit.text())
        space = float(self.antennaSpaceEdit.text())
        grid = self.displayGridCheckBox.isChecked()
        polar = self.polarButton.isChecked()
        beam = int(self.beamNumberEdit.text())
        angle = int(self.antennaAngleEdit.text())
        normal = self.displayNormalCheckBox.isChecked()
        title = self.displayTitleCheckBox.isChecked()
        axes = self.displayAxesCheckBox.isChecked()
        legend = self.displayLegendCheckBox.isChecked()

        bf = Beamforming(ant, space, normalize=normal, weightType=BeamformingWeightType.DFT)
        beams = []
        x = None
        legends = []
        for i in range(beam):
            x, y = bf.calculateBeamforming(i, phi=60)
            beams.append(y)
            legends.append(f"beam {i}")

        if legend:
            self.figure.drawFigure(x, beams, polar, grid, legends, title, axes)
        else:
            self.figure.drawFigure(x, beams, polar, grid, None, title, axes)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = BeamformingDialog()
    Dialog.show()
    sys.exit(app.exec_())