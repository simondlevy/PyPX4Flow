#! /usr/bin/python

'''
px4flow_display.py - Display / logging program for PyPX4Flow package

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

# Pick your port
PORT  = '/dev/ttyACM0'          # Linux
#PORT  = 'COM5'                  # Windows
#PORT = '/dev/tty.usbmodem1431'  # Mac OS X

# Sensor params (units are meters, seconds)

GRND_DIST_MIN = 0.3
GRND_DIST_MAX = 5.0

VELOCITY_MAX = 5.0

DISTANCE_MAX = 10

# Display params (Width, Height, X, Y, Radius, Distance)

DISPLAY_W = 1000
DISPLAY_H = 300

GAUGE_Y   = DISPLAY_H - 60
GAUGE_W   = 90
GAUGE_H   = 200

VELOCITY_X  = 450
VELOCITY_Y  = DISPLAY_H / 2
VELOCITY_R  = 5
VELOCITY_D  = 100

DISTANCE_X  = 800
DISTANCE_Y  = VELOCITY_Y
DISTANCE_D  = VELOCITY_D
DISTANCE_R  = 5

from px4flow import PX4Flow
from gauge import VerticalGauge

from sys import exit, version
from time import time, strftime

if version[0] == '3':
    import tkinter as tk
else:
    import Tkinter as tk

class PX4FlowPlotter:

    def __init__(self, reader):   

        # Store the PX4Flow reader
        self.reader = reader

        # Set up the frame
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root, borderwidth=4, width=DISPLAY_W, height=DISPLAY_H, relief='sunken')
        self.frame.master.title('PX4Flow: Hit ESC to quit')

        # Add a canvas for drawing
        self.canvas =  tk.Canvas(self.frame, width = DISPLAY_W, height = DISPLAY_H, background = 'black')

        # Add a text item for reporting acquisition rate
        self.rate_label = self.create_label(DISPLAY_W-140, DISPLAY_H-20, color='red')

        # Add a gauge for grnd_dist
        self.grnd_dist_gauge = VerticalGauge(self.canvas, 40, GAUGE_Y, GAUGE_W, GAUGE_H, 'blue', 'Grnd dist (m)', GRND_DIST_MIN, GRND_DIST_MAX, '%2.1f')

        # Add a gauge for quality
        self.quality_gauge = VerticalGauge(self.canvas, 200, GAUGE_Y, GAUGE_W, GAUGE_H, 'yellow', '    Quality', 0, 255, '%d')

        # Add axes for velocity
        self.create_axis_line(-1, 0) 
        self.create_axis_line(+1, 0) 
        self.create_axis_line(0, -1) 
        self.create_axis_line(0, +1) 

        # Add labels for velocity
        self.create_label(VELOCITY_X+120,   VELOCITY_Y,    'X m/sec')
        self.create_label(VELOCITY_X-30,    DISPLAY_H-275, 'Y m/sec')

        # Add lines for displaying velocities
        self.x_line = self.create_null_line()
        self.y_line = self.create_null_line()

        # Add widgets for displaying distance traveled
        box_lx = DISTANCE_X - DISTANCE_D
        box_rx = DISTANCE_X + DISTANCE_D
        box_uy = DISTANCE_Y - DISTANCE_D
        box_ly = DISTANCE_Y + DISTANCE_D
        self.canvas.create_rectangle((box_lx, box_uy, box_rx, box_ly), outline='white')
        self.create_label(box_lx+DISTANCE_D/2+30, box_ly+20, 'X (m)')
        self.create_label(box_rx+10, DISTANCE_Y, 'Y (m)')
        self.create_label(box_rx+10, box_uy-10, '+%d' % DISTANCE_MAX)
        self.create_label(box_lx-30, box_ly+10, '-%d' % DISTANCE_MAX)
        self.location_circle = self.canvas.create_oval(self.location_to_oval(0, 0), width=1, outline='red')
        self.location_pix_prev = None

         # Pack the widgets into the canvas
        self.canvas.pack(fill=tk.BOTH, expand=1)

        # Set up a key event for exit on ESC
        self.frame.bind("<Key>", self.key)
        self.frame.pack()

        # This call gives the frame focus so that it receives input
        self.frame.focus_set()

        self.failcount = 0

    def location_to_oval(self, xpix, ypix):

        return xpix-DISTANCE_R, ypix-DISTANCE_R, xpix+DISTANCE_R, ypix+DISTANCE_R, 

    def location_to_pixels(self):

        xpix = DISTANCE_X + (self.reader.X_accum/ DISTANCE_MAX) * DISTANCE_D
        ypix = DISTANCE_Y + (self.reader.Y_accum/ DISTANCE_MAX) * DISTANCE_D

        return xpix, ypix
    
    def create_null_line(self):

        return self.canvas.create_line(VELOCITY_X, VELOCITY_Y, VELOCITY_X, VELOCITY_Y, width=4)

    def create_axis_line(self, dx, dy):

        self.canvas.create_line(VELOCITY_X, VELOCITY_Y, VELOCITY_X+dx*VELOCITY_D, VELOCITY_Y+dy*VELOCITY_D, fill='white')

    def create_label(self, x, y, text=None, color='white'):

        return self.canvas.create_text(x, y, anchor=tk.W, font=('Helvetica', 12), fill=color, text=text)

    def run(self):

        # Start timing
        self.start_sec = time()
 
        # Start the recursive timer-task
        self.task() 

        # Set Tkinter's main loop
        self.root.mainloop()

    def task(self):

        reader = self.reader

        # Refresh PX4Flow data
        reader.refresh()

        # Ground distance will be None on sensor fail
        grnd_dist = reader.H

        # Update sensor display
        if grnd_dist:

            xpix, ypix = self.location_to_pixels()
            self.canvas.coords(self.location_circle, self.location_to_oval(xpix, ypix))
            if self.location_pix_prev:
                self.canvas.create_line(self.location_pix_prev[0], self.location_pix_prev[1], xpix, ypix, fill='red')
            self.location_pix_prev = xpix, ypix

            self.grnd_dist_gauge.update(grnd_dist)
            self.quality_gauge.update(reader.Quality)

            x = VELOCITY_X + 2
            y = VELOCITY_Y + 2

            self.canvas.coords(self.x_line, (x, y, int(VELOCITY_X+reader.X/VELOCITY_MAX*VELOCITY_D), y))
            self.canvas.itemconfigure(self.x_line, fill = 'red' if reader.X < 0 else 'green')

            self.canvas.coords(self.y_line, (x, y, x, int(VELOCITY_Y+reader.Y/VELOCITY_MAX*VELOCITY_D)))
            self.canvas.itemconfigure(self.y_line, fill = 'red' if reader.Y < 0 else 'green')

        else:
            self.failcount += 1
            print('Fail %d' % self.failcount)

        # Report speed after several seconds
        elapsed_sec = time() - self.start_sec
        if elapsed_sec > 5:
            self.canvas.itemconfigure(self.rate_label, text='%d updates / sec' % \
                                     int(reader.count/elapsed_sec))

        # Reschedule this task immediately
        self.frame.after(1, self.task)

    def click(self, event):
        print("Clicked at: ", event.x, event.y)

    def key(self, event):

        # Make sure the frame is receiving input!
        self.frame.focus_force()
        if event.keysym == 'Escape':
            exit(0)

class PX4FlowReader(PX4Flow):
    
    def __init__(self, port):
        
        PX4Flow.__init__(self, port)
        
        # No readings yet
        self.SensorX,self.SensorY = None, None
        self.X,self.Y = None, None
        self.H = None
        self.Quality = None
        
        # Create logfile named by current date / time
        filename = 'px4flow_' + strftime('%d_%b_%Y_%H_%M_%S') + '.csv'
        self.logfile = open(filename, 'w')
        self.write_and_flush('Time (sec), Ground Dist (m), Flow X, Flow Y, Flow Comp X (m), Flow Comp Y (m), Quality (/255),,')
        self.write_and_flush('X accum (m), Y accum (m)\n')

        # These will get the accumulated X,Y distances in meters
        self.timeSecPrev = None
        self.X_accum = 0
        self.Y_accum = 0

        self.count = 0

    # Implements missing method in parent class    
    def update(self):
                    
        # Grab raw sensor X,Y
        self.SensorX,self.SensorY = self.getFlow()
        
        # Grab computed X,Y in meters
        self.X,self.Y = self.getFlowComp()     
        
        # Grab ground distance (height) in meters
        self.H = self.getGroundDistance()
        
        # Grab quality in percent
        self.Quality = self.getQuality()

        # Time in seconds
        timeSec = self.getTime() / 1e6

        # Computed flow in meters per second
        flowCompX, flowCompY = self.getFlowComp()

        self.write_and_flush('%6.3f, %+3.3f, %d, %d, %+3.3f, %+3.3f, %d' % \
                     (timeSec, self.H, self.SensorX, self.SensorY, self.X, self.Y, self.Quality))

        # After first iteration, compute accumualted distances
        if self.count:

            # Compute distance if elapsed time available
            if self.timeSecPrev:

                elapsedSec = timeSec - self.timeSecPrev

                # Elapsed time should never be more than a small fraction of a second
                if elapsedSec < 0.1:
                    self.X_accum += flowCompX * elapsedSec
                    self.Y_accum += flowCompY * elapsedSec

                self.timeSecPrev = timeSec
 
                self.write_and_flush(',,%+3.3f, %+3.3f' % (self.X_accum, self.Y_accum))

        self.write_and_flush('\n')

        # Update count for speed reporting
        self.count += 1
        self.timeSecPrev = timeSec

    def write_and_flush(self, s):

        self.logfile.write(s)
        self.logfile.flush()

if __name__ == "__main__":

    reader = PX4FlowReader(PORT)

    plotter = PX4FlowPlotter(reader)

    plotter.run()
