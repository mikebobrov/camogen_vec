#! /usr/bin/env python
# coding=utf-8
#
# Copyright © 2017 Gael Lederrey <gael.lederrey@epfl.ch>
#
# Distributed under terms of the MIT license.
#
# Based on the code of Ulf Alstrom (http://www.happyponyland.net/camogen.php)

import camogen

# Generate the examples given

# for i in range(0,100):
  # Green Blots
  # parameters = {'width': 735, 'height': 812, 'polygon_size': 900, 'color_bleed': 3,
                # 'colors': ['#F1F1F1', '#FF3333', '#333333'],
               # }

  # camogen.generate(parameters, './images/result_{}.svg'.format(i))
# parameters = {'width': 735, 'height': 812, 'polygon_size': 900, 'color_bleed': 3,
parameters = {'width': 735, 'height': 812, 'polygon_size': 400, 'color_bleed': 1,
                'colors': ['#F1F1F1', '#FF3333', '#333333'],
               }

# camogen.generate(parameters, './images/result.svg')
# for i in range(0,100):
camogen.generate3(parameters, './images/result_{}.svg'.format(1))
for i in range(0, 10):
  camogen.generate4(parameters, './images/result_b_{}.svg'.format(i))
