'''
gauge.py - Gauge-display classes for Tkinter projects

Copyright (C) 2014 Simon D. Levy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''

from sys import version

if version[0] == '3':
    import tkinter as tk
else:
    import Tkinter as tk

class VerticalGauge(object):
    '''
    A class for vertical gauges.
    '''

    def __init__(self, canvas, left, bottom, width, height, color, label, minval, maxval, fmt):
        '''
        Creates a labeled vertical gauge of specified dimensions on a specified canvas.
        FMT for min and max values is as for print(); for example '+%3.3f', '%d', etc.
        '''

        right = left + width

        self.height = height
        self.canvas = canvas
        self.minval = minval
        self.maxval = maxval

        top    = bottom - self.height
        bbox = (left, bottom, right, top)
        self.bbox = bbox
        self.rect = canvas.create_rectangle(bbox, fill=color)
        canvas.create_rectangle((bbox[0]-1, bbox[1]-1, bbox[2]+1, bbox[3]+1), outline='white')
        self._create_label(left, bottom+20, text=label)
        self._create_label(left-30, bottom, text= fmt % minval)
        self._create_label(left-30, top ,   text= fmt % maxval)

    def update(self, newval):
        '''
        Updates the VerticalGauge with a new value.
        '''

        new_height = self.height * (newval-self.minval) / (self.maxval - self.minval)
        bbox = self.bbox
        self.canvas.coords(self.rect, (bbox[0], bbox[1], bbox[2], bbox[1]-new_height))

    def _create_label(self, x, y, text):

        return self.canvas.create_text(x, y, anchor=tk.W, font=('Helvetica', 12), fill='white', text=text)
