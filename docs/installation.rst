Installation
------------


1: Download PyDBus along with support files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyDBus comes with source, testing and support files.  The easiest way to load them is
to install the 'git' package, then run::

		cd ~
		git clone https://github.com/hcoin/pydbus

To browse the code, perhaps choose an earlier release or learn other ways to get a copy,
`visit this link to the github website <https://github.com/hcoin/pydbus/tree/master>`_

  Note the python pip package manager may have a version of pydbus3.  While the pip system does load
  necessary python support packages, it doesn't check necessary Linux libraries.  Follow the 
  instructions below to load the support packages your system may require before you attempt a pip based install.


2: Install required Linux support packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All Linux distributions share some setup details, but each has its own special cases and available Python versions.  
While PyDbus is 'fully Pythonic', many popular Linux releases do not provide or by default install system libraries PyDBus needs.
Some releases provide faulty versions of necessary libraries, PyDbus supports them using extra code.  PyDbus does not change
any standard system library. 

So, installation details vary
among Linux distributions.  Names of the necessary packages often differ, and other nuances.  The 
biggest difference is seen between Debian/Ubuntu based and Fedora/RedHat/Centos.

Some distributions are of such an age their dbus libraries do not natively support things like DBus publishing, or
are simply missing altogether, or aren't compatible with the python version you may desire.

However, these distributions are very stable and widely used nevertheless.  As such, Pydbus re-distributes many
packages it requires to support your distribution needed for proper operation.  The very latest versions of
some distributions often have everything needed by default.

The .dockerfile for your setup will have details.   

To find PyDbus installation instructions specific to your particular Linux distribution, distro version, and also python version:

* Read the file `in this directory /tree/master/tests>`_ whose name most closely matches your installation and
  that ends with .dockerfile. 

The .dockerfile contains all the instructions necessary to get your system ready for PyDBus.  

* The .dockerfile instructions presume you have copied all
  the files into the /root directory on your system.  Change those references to point to the PyDbus library
  on your system.  If you followed the instructions above, that will be ~/pydbus.


Notice the source
home for PyDbus on github includes a 'badge' linking to 'TravisCI', following that link shows the result of our testing the installation instructions
against each supported Linux system type.  If that does not show 'green' for your distribution (which it should always be), something
has gone far wrong and should be investigated before putting more time into installing PyDbus.

The instructions for a few distributions use links to distribution specific files to find necessary packages.  While the distribution
support people rarely change or 'break' these, it has happened.  If when installing a package the system reports it can't be found on
your distribution, it may be because the directory the package was in when PyDbus was tested has since moved.  We try to catch these
things, but you may need to find the needed package elsewhere. 

Note: If you want to use the version of pydbus loaded on pip, be sure to use the pip version that matches the python version you intend to use,
(i.e. pip3 or pip3.4 etc).  The pip system also requires all the packages
named in the .dockerfile for your system to have been installed before it will succeed. 


3: Setup and test PyDbus
^^^^^^^^^^^^^^^^^^^^^^^^^

The last step in every set of .dockerfile instructions uses setup.py to install pydbus.  That step should complete without error.

As a check, all instruction files show how to run a 'unit testing' suite to confirm proper PyDbus operations on your system.
If that unit test suite completes without errors, PyDbus is properly installed on your system and it is ready to go.  If that
test reports errors: verify the setup instructions used match your setup very closely, that the version of python you intend
to use works, and that the pydbus release downloaded did not come from an experimental branch.






