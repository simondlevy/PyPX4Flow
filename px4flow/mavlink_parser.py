'''
mavlink_parser.py - Simon's homebrew code for parsing MAVLink messages.
                    DOES NOT VERIFY CHECKSUM!!!

Based on http://en.wikipedia.org/wiki/MAVLink, but hoping to replace it
with pymavlink, so we can get checksum and other features.

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

import struct

# States for message parsing
# From http://qgroundcontrol.org/mavlink/start#packet_anatomy
STATE_DFLT = 0
STATE_STX  = 1
STATE_LEN  = 2
STATE_SEQ  = 3
STATE_SYS  = 4
STATE_COMP = 5
STATE_MSG  = 6
STATE_CKA  = 7
STATE_CKB  = 8

# STX delimiter byte for Mavlink 1.0
STX_BYTE = 0XFE

class MAVLinkParser(object):

    def process(self, buf):

        for b in bytearray(buf):
            
            if b == STX_BYTE:         
                self.state = STATE_STX
                
            elif self.state == STATE_STX:
                self.msglen = b
                self.state = STATE_LEN
                
            elif self.state == STATE_LEN:
                self.state = STATE_SEQ
                
            elif self.state == STATE_SEQ:
                self.state = STATE_SYS
                
            elif self.state == STATE_SYS:
                self.state = STATE_COMP
                
            elif self.state == STATE_COMP:
                self.msgid = b
                self.msg = bytearray('', 'utf8')
                self.state = STATE_MSG
                
            elif self.state == STATE_MSG:
                self.msg.append(b)
                if len(self.msg) == self.msglen:
                    self.state = STATE_CKA
                    
            elif self.state == STATE_CKA:
                self.state = STATE_CKB
                
            elif self.state == STATE_CKB:
                if self.msgid == self.tgtid:
                    self.handler.update() 
                    self.msg = bytearray('', 'utf8')
                    self.state = STATE_DFLT

    def __init__(self, handler, targetid):
        
        self.state = STATE_DFLT
        self.msglen = 0
        self.msgid  = 0
        self.msg    = bytearray('', 'utf8')
        
        self.handler = handler
        self.tgtid = targetid

    def unpack_uint8(self, lo):
        return self.unpack1('B', lo, lo+1)

    def unpack1(self, fmt, lo, hi):
        return self.unpack(fmt, lo, hi, 1)[0]

    def unpack(self, fmt, lo, hi, n):
        return struct.unpack(fmt, self.msg[lo:hi])[0:n]
