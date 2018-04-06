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

for i in range(0,700, 10):
  # Green Blots
  parameters = {'width': 700, 'height': 700, 'polygon_size': i, 'color_bleed': 1,
                'colors': ['#F1F1F1', '#FF3333', '#333333'],
               }

  camogen.generate(parameters, './images/result_{}.svg'.format(i))
