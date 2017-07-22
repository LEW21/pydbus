Installation
------------

.. _Tests: 
.. _root: 

1: Install Distribution Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All Linux distributions share some setup details, but each has its own special cases and available python versions.  
While PyDbus is 'fully Pythonic', it uses Linux system libraries which are not.  Often installation details vary
among Linux systems because the names of the necessary packages often differ, and other nuances.


To find PyDbus installation instructions specific to a particular Linux distribution, distro version, and also python version:

Read the file `in this directory <https://github.com/hcoin/pydbus/tree/master/tests>`_ whose name most closely matches your installation and
that ends with .dockerfile. 


The .dockerfile will contain all the instructions necessary to get PyDBus installed and ready for first use on your system.

Read and follow the instructions in those files.  The instructions presume you have copied all
the files `from the pydbus root directory <https://github.com/hcoin/pydbus/tree/master>`_ into the /root
directory on your system.  Feel free to install these files in any empty directory, then use its name instead
of /root in the instructions.  So, for example to use the pydbus folder in your home directory as a setup base, do::

		cd ~
		git clone https://github.com/hcoin/pydbus

* DO NOT run setup.py until after you have sucessfully installed all the necessary packages named in your distro's .dockerfile.

2: Follow the instructions in the .dockerfile that applies to your setup.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All the files named above and more will now be on your system.  Proceed as indicated in the .dockerfile.

  As a check, each file also shows how to run a test suite to confirm proper PyDbus operations on your system.
  If that unit test suite completes without errors, PyDbus is properly installed on your system and it is ready to go.

Note the python pip package manager may have a version of pydbus3.  The pip system also requires all the packages
named in the .dockerfile to have been installed before it will succeed. 

Some distributions are of such an age their dbus libraries do not natively support things like publishing, or
are simply missing altogether, or aren't compatible with the python version you may desire.

However, these distributions are very stable and widely used nevertheless.  As such, Pydbus re-distributes many
packages that may or may not apply to your situation needed for proper operation.  The .dockerfile for your setup will have details.   

Last, PyDBus3 is based on the PyDBus package written by Linus Lewandowski, with some parts by Collabra Ltd.

PyDBus3 is backward compatible with PyDBus. 





