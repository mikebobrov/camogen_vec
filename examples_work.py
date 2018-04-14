#! /usr/bin/env python
# coding=utf-8
#
# Copyright © 2017 Gael Lederrey <gael.lederrey@epfl.ch>
#
# Distributed under terms of the MIT license.
#
# Based on the code of Ulf Alstrom (http://www.happyponyland.net/camogen.php)

from camogen.generate import generate

parameters = {'width': 735, 'height': 812, 'polygon_size': 300, 'color_bleed': 3, 'max_depth': 50,
              'colors': ['#F1F1F1', '#FF3333', '#333333'],
              }

generate(parameters, './images/result.svg')
