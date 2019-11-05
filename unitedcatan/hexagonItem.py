#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:25:05 2019

@author: jamie
"""
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QGraphicsView
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsPolygonItem
from PyQt5.QtCore import QSize, QPointF, QObject, Signal, Slot
from PyQt5.QtGui import QPolygonF, QColor, QBrush, QPen
from PyQt5.QtCore import Qt
from math import sqrt


class HexagonItem(QGraphicsPolygonItem):

    def __init__(self, center, radius, parent=None):
        QGraphicsPolygonItem.__init__(self, makeHexagon(center, radius), parent)
        self._center = center
        self._radius = radius
        self.setZValue(0)
        self.setBoundingRegionGranularity(1.0)
        self.setBrush(QBrush(QColor(0, center.y() % 256, center.x() % 256)))
        self.setPen(QPen(Qt.NoPen))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setPolygon(makeHexagon(self._center, self._radius * 1.2))
        self.setZValue(1)

    def hoverLeaveEvent(self, event):
        self.setPolygon(makeHexagon(self._center, self._radius))
        self.setZValue(0)

    def x(self):
        return self._center.x()

    def y(self):
        return self._center.y()

    def radius(self):
        return self._radius


def makeHexagon(center, radius):
    x1 = center.x() - radius
    x2 = center.x() - (radius / 2.0)
    x3 = center.x() + (radius / 2.0)
    x4 = center.x() + radius
    y1 = center.y() - (radius * sqrt(3) / 2.0)
    y2 = center.y()
    y3 = center.y() + (radius * sqrt(3) / 2.0)
    points = [QPointF(x1, y2), QPointF(x2, y3), QPointF(x3, y3),
              QPointF(x4, y2), QPointF(x3, y1), QPointF(x2, y1)]
    return QPolygonF(points)
