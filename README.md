PyPX4Flow
=========

A simple Python package for reading from the PX4Flow optical-flow sensor

<p>

I needed an easy way to access data from the <a href="http://pixhawk.org/modules/px4flow">PX4Flow</a> sensor using 
Python, so I wrote this little package, which
you can 
<a href="https://github.com/simondlevy/PyPX4Flow">download from github</a>.  
It runs on Windows, Linux, and
OS X in Python 2 and 3.  As with the <a href="http://home.wlu.edu/~levys/software">other Python packages</a> I've 
written, the API is very simple.  For example, this program prints the computed X and Y flow velocities from the sensor:

<b>
<pre>
from px4flow import PX4Flow

class ShowFlow(PX4Flow):

    def update(self):

            print(self.getFlowComp())


if __name__ == '__main__':

    sensor = ShowFlow('/dev/ttyACM0')

    while True:

        sensor.refresh()

</pre>
</b>

As this example shows, <tt><b>PX4Flow</b></tt> is an abstract class that you subclass with a class implementing the
<tt><b>update</b></tt> method.  To see the other methods avaiable, look at the 
<a href="px4flow.html">documentation</a>.

<p>

I've also included a <a href="https://github.com/simondlevy/PyPX4Flow/blob/master/display/px4flow_display.py">program</a> that will display the sensor data in a useful way (depicted above) and log the data to
a .CSV file for Excel.

<p>

<h3>Instructions</h3>

You will need:

<ol>
<li> A <a href="https://store.3drobotics.com/products/px4flow">PX4Flow kit</a>.  I recommend 
following the <a href="http://pixhawk.org/modules/px4flow#image_quality_and_output">Image Quality and Output</a>
instructions to make sure the sensor is working properly.
<li> <p> The ability to program in Python
<p><li> The <a href="http://pyserial.sourceforge.net/">PySerial</a> package installed on your computer.  
Like many people, I found it easiest to <a href="http://pyserial.sourceforge.net/pyserial.html#from-source-tar-gz-or-checkout">install from source</a>.
<p><li>Administrator (root) privileges on your computer
<p><li>The PyPX4Flow <a href="https://github.com/simondlevy/PyPX4Flow">repository</a>.  
</ol>

Once you've downloaded the repositry, use a terminal (Linux or OS X) or command shell
(Windows) to change to the directory where you put it, and issue the command

<b>
<pre>
  python setup.py install
</pre>
</b>

On Linux or OS X, you may need to issue this command as root:

<b>
<pre>
  sudo python setup.py install
</pre>
</b>

Then you should be able to run the <b>px4flow_display.py</b> program in the <b>display</b> folder.

<p>

<h3>Known issues</h3>

<ol>

<li> Some users have reported a bug in which the display program crashes immediately with a stack trace ending in the following output:

<pre>
 File "/usr/local/lib/python2.7/dist-packages/px4flow/mavlink_parser.py", line 99, in unpack
    return struct.unpack(fmt, self.msg[lo:hi])[0:n]
error: unpack requires a string argument of length 4
</pre>

So far this bug seem to occur only with versions of Python below 2.7.5, so I've added a 
<a href="https://github.com/simondlevy/PyPX4Flow/tree/PrePython2-7-5">branch</a> to the repository that
should work with such earlier versions. If you are running 2.7.5 or above and still experience this problem,
please  <a href="mailto:simon.d.levy@gmail.com">let me know</a>.

<p><li>At startup, the display program occasionally computes and displays bogus large values for the distance traveled.
This may have to do with the fact that I am not using the checksum to validate each message.

</ol>

<h3>Copyright and licensing</h3>

Copyright and licensing information (Gnu 
<a href="https://www.gnu.org/licenses/lgpl.html">LGPL</a>) 
can be found in the header of each source file.

<h3>Acknowledgments</h3>

This work was supported in part by a  Commonwealth Research Commercialization Fund
grant from the Center for Innovative Technology (CRCF #MF14F-011-MS) and a
Lenfest summer research grant from Washington and Lee University.


