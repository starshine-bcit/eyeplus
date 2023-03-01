
from PyQt6 import QtGui, QtWidgets

from qt.parameterui import Ui_parameterDialog


class ParameterWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QMainWindow) -> None:
        super().__init__(parent)
        self.ui = Ui_parameterDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/icons/rotate-3d.svg')))
        self.setWindowTitle('Parameter Tuner | eyeplus')
        self._connect_internal_events()

    def _connect_internal_events(self) -> None:
        self.ui.horizontalSliderHorizonFuzzy.sliderMoved.connect(
            self._update_horizon_text)
        self.ui.horizontalSliderPitchMulti.sliderMoved.connect(
            self._update_pitch_text)
        self.ui.horizontalSliderRollOffset.sliderMoved.connect(
            self._update_roll_text)
        self.ui.lineEditRollOffset.editingFinished.connect(
            self._update_roll_slider)
        self.ui.lineEditHorizonFuzzy.editingFinished.connect(
            self._update_horizon_slider)
        self.ui.lineEditPitchMulti.editingFinished.connect(
            self._update_pitch_slider)
        self.ui.pushButtonReset.clicked.connect(self.reset)

    def reset(self) -> None:
        self.ui.lineEditHorizonFuzzy.setText('0')
        self.ui.lineEditPitchMulti.setText('1000')
        self.ui.lineEditRollOffset.setText('90')
        self.ui.horizontalSliderHorizonFuzzy.setValue(0)
        self.ui.horizontalSliderPitchMulti.setValue(1000)
        self.ui.horizontalSliderRollOffset.setValue(90)
        self.resize(524, 212)
        self.ui.pushButtonApply.setFocus()

    def _update_horizon_text(self) -> None:
        self.ui.lineEditHorizonFuzzy.setText(
            str(self.ui.horizontalSliderHorizonFuzzy.value()))

    def _update_pitch_text(self) -> None:
        self.ui.lineEditPitchMulti.setText(
            str(self.ui.horizontalSliderPitchMulti.value()))

    def _update_roll_text(self) -> None:
        self.ui.lineEditRollOffset.setText(
            str(self.ui.horizontalSliderRollOffset.value()))

    def _update_horizon_slider(self) -> None:
        self.ui.horizontalSliderHorizonFuzzy.setValue(
            int(self.ui.lineEditHorizonFuzzy.text()))

    def _update_pitch_slider(self) -> None:
        self.ui.horizontalSliderPitchMulti.setValue(
            int(self.ui.lineEditPitchMulti.text()))

    def _update_roll_slider(self) -> None:
        self.ui.horizontalSliderRollOffset.setValue(
            int(self.ui.lineEditRollOffset.text()))

    def set_values(self, roll_offset: int, pitch_multi: float, horizon_offset: float) -> None:
        self.ui.lineEditRollOffset.setText(str(roll_offset))
        self.ui.horizontalSliderRollOffset.setValue(roll_offset)
        self.ui.lineEditPitchMulti.setText(str(int(pitch_multi * 1000)))
        self.ui.horizontalSliderPitchMulti.setValue(int(pitch_multi * 1000))
        self.ui.lineEditHorizonFuzzy.setText(str(int(horizon_offset * 1000)))
        self.ui.horizontalSliderHorizonFuzzy.setValue(
            int(horizon_offset * 1000))
