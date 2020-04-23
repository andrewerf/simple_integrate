import sys, math
import numpy as np
from PyQt5 import QtWidgets, uic

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from integrate import convert_function, integrate, inf_integrate


class MplCanvas(FigureCanvasQTAgg):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		uic.loadUi('Form.ui', self)

		self.integrate_btn = self.findChild(QtWidgets.QPushButton, 'integrate_btn')
		self.func_lne = self.findChild(QtWidgets.QLineEdit, 'func_lne')
		self.var_lne = self.findChild(QtWidgets.QLineEdit, 'var_lne')
		self.err_lne = self.findChild(QtWidgets.QLineEdit, 'err_lne')
		self.low_lne = self.findChild(QtWidgets.QLineEdit, 'low_lne')
		self.up_lne = self.findChild(QtWidgets.QLineEdit, 'up_lne')
		self.ans_lne = self.findChild(QtWidgets.QLineEdit, 'ans_lne')
		self.plot_wdg = self.findChild(QtWidgets.QWidget, 'plot_wdg')
		self.plot_layout = self.plot_wdg.findChild(QtWidgets.QGridLayout, 'plot_layout')
		# self.main_layout = self.findChild(QtWidgets.QGridLayout, 'main_layout')
		self.plot_cvs = MplCanvas(self)
		self.plot_layout.addWidget(self.plot_cvs)

		self.integrate_btn.clicked.connect(self.integrate)

	def integrate(self):
		f = convert_function(self.func_lne.text(), self.var_lne.text())
		err = float(self.err_lne.text())
		a = float(self.low_lne.text())
		b = self.up_lne.text()

		digits = round(math.log(1/err, 10))

		if b == 'inf' or b == '+inf':
			res, b = inf_integrate(f, a, err)
		else:
			b = float(b)
			res = integrate(f, a, b, err)

		self.ans_lne.setText(str(round(res, digits)))
		self.plot(f, a, b)

	def plot(self, f, a, b):
		# if self.plot_layout.count() > 0:
		# 	self.plot_layout.itemAt(0).widget().setParent(None)

		step = 0.00001
		x = np.arange(a, b, step)
		y = list(map(f, x))

		# mx = max(max(x), max(y), 1)
		# mn = min(min(x), min(y), -1)

		self.plot_cvs.axes.cla()
		# self.plot_cvs.axes.set_ylim(mn, mx)
		# self.plot_cvs.axes.set_xlim(mn, mx)

		self.plot_cvs.axes.plot(x, y)
		self.plot_cvs.draw()



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()