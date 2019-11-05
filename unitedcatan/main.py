import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPolygonItem
from PyQt5.QtCore import QSize, QPointF
from PyQt5.QtGui import QPolygonF
from math import sqrt
from hexagonItem import HexagonItem
from board import Board


class CatanWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 300))
        self.setWindowTitle("Hello world")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        view = QGraphicsView(self)
        view.setMouseTracking(True)
        scene = QGraphicsScene(view)
        radius = 30.0
        length = radius / 2 * sqrt(3)
        t = HexagonItem(QPointF(50, 50), radius)
        t2 = HexagonItem(QPointF(t.x(), t.y() + 2 * length), radius)
        scene.addItem(t)
        scene.addItem(t2)
        view.setScene(scene)
        gridLayout.addWidget(view, 1, 1)

        title = QLabel("Hello World from PyQt", self)
        title.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title, 0, 0)

        menu = self.menuBar().addMenu('Action for quit')
        action = menu.addAction('Quit')
        action.triggered.connect(QtWidgets.QApplication.quit)


if __name__ == "__main__":
    def run_app():
        app = QtWidgets.QApplication(sys.argv)
        mainWin = CatanWindow()
        mainWin.show()
        app.exec_()
    run_app()
