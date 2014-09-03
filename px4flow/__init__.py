'''
PX4Flow - a Python class for collecting data from the PX4Flow sensor

Copyright (C) 2014 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''

# Message ID fom https://pixhawk.ethz.ch/mavlink/
MSG_OPTICAL_FLOW = 100

# Arbitrary
_BUFSIZE = 2048

import serial
import platform

from px4flow.mavlink_parser import MavLinkParser

class PX4Flow(MavLinkParser):
    '''
    An abstract class for reading from the PX4Flow optical flow sensor. Your subclass should provide an update method that
    calls one or more of the accessor methods below.
    '''
    
    def __init__(self, port):
        '''
        Creates a new PX4Flow object on the specified port.
        '''
        
        # Baud rate is unspecified
        self.dev = serial.Serial(port)

        # Create MAVLink object for parsing
        MavLinkParser.__init__(self, self, MSG_OPTICAL_FLOW)

    def close(self):
        '''
        Closes the port on which the sensor was opened.
        '''
        self.dev.close()

    def refresh(self):
        '''
        Refreshes the optical flow reading.
        '''
            
        # Grab bytes from the device        
        bytes = self.dev.read(_BUFSIZE)
                
        # Check for MAVLINK messages in bytes
        MavLinkParser.process(self, bytes)

    def getFlow(self):
        '''
        Returns raw sensor X,Y.
        '''
        return MavLinkParser.unpack(self, 'hh', 20, 24, 2)
        
    def getFlowComp(self):
        '''
        Returns computed X,Y in meters.
        '''
        return MavLinkParser.unpack(self, 'ff', 8, 16, 2)
        
    def getGroundDistance(self):
        '''
        Returns ground distance (height) in meters.
        '''
        return MavLinkParser.unpack1(self, 'f', 16, 20)
        
    def getQuality(self):
        '''
        Returns quality in percent.
        '''
        return MavLinkParser.unpack_uint8(self, 25)

    def getTime(self):
        '''
        Returns current time in microseconds.
        '''
        return MavLinkParser.unpack1(self, 'Q', 0,  8)
