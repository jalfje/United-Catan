#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:52:02 2019

@author: jamie
"""

from enum import Enum, auto


class HexType(Enum):
    DESERT = auto()
    WATER = auto()
    GOLD = auto()
    MOUNTAIN = auto()  # rock
    FIELD = auto()  # wheat
    GRASS = auto()  # sheep
    FOREST = auto()  # log
    CLAY = auto()  # brick

    # Indicates whether this hex type needs a number, i.e. whether or not
    # it generates resources.
    def needsNumber(self):
        return self not in (HexType.WATER, HexType.DESERT)
