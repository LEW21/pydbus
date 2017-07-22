`translation_spec = {  'keyname' : \<dataflow spec\> ,...}`

==========================
The DataFlow Specification
==========================

This level resolves two general conflict areas.  The first is the possible
use of one key name for any combination of signal, property or method.

The second is the possibly different translation needs of arguments flowing
from python code to the dbus such as when a service client calls a method or 
sets a property, or

from the translation needs of arguments flowing back from
the dbus to the caller.  In this case return arguments to the function call,
the value of a property being read, or the arguments to a user provided
signal function.  

When publishing a service, the dbus to python are arguments TO the method.
python to dbus are the return values FROM the method. So, the data flow is reversed.


The allowed key : value pairs in the dataflow level dictionary are:

`{ 'method_py_to_dbus': to_dbus_method_argspec_described_below,`  
  `#used when calling a method or publishing a reply`  

  `'method_dbus_to_py': from_dbus_method_argspec_described_below,`  
  `#used to process method return values or accept published method arguments`  

  `'signal_dbus_to_py': from_dbus_signal_argspec_described_below,`  
  `#used to accept information when receiving a signal`  

  `'signal_py_to_dbus': to_dbus_signal_argspec_described_below,  `  
  `#used when sending a published signal`  
  
  `'property': property_dbus_argspec_described_below`  
  `#used both for setting and reading a property`  

  `'property_dbus_to_py': from_dbus_property_argspec_described_below`  
  `'property_py_to_dbus': to_dbus_property_argspec_described_below`  
   `#used in rare cases when a property needs a different set and get translation`  
  `}`  

Note: In the rare case there is a need for a different spec for when
getting and another for setting a property, the keys: property_dbus_to_py
and property_py_to_dbus can be specified, and if so, they override any
value set in property.

All the ...argspec... objects mentioned above as values follow the same specification, described in the next section.

It is often the case that a dbus service does not offer properties or signals or methods.
There need only be entries for offered services.

It is often the case there is data flow from dbus to python for a signal, property or method, but not
from python to dbus for the same method. There need only be entries for cases where there is
data flow.  However, if there is nothing in a particular data flow that needs translation services,
(For example, a property key that accepts and sets only a string), that key-value pair may be omitted.  

When there is no translation service needed for
an entire direction for a signal, key or method, while it is usual to leave out the related name, it
may be included with a value of None.

Any other key/value pairs are ignored, but may be used in the future.

A sample program fragment to access the Connectivity method of the NetworkManager, jumping ahead a bit:

`    from pydbus.bus import SystemBus`  
    `bus=SystemBus() `  
    `nm=bus.get('org.freedesktop.NetworkManager',translation_spec={`  
    `'Connectivity' : { 'method_py_to_dbus' : \<argspec for the call arguments, defined next section\> })`  
`                       'method_dbus_to_py' : \<argspec for the return arguments, defined next section\> })`  
    `print(str(nm.Connectivity))`

would print a string describing the connectivity (only if the \<argspec...\> is fully defined).  But

`from pydbus.bus import SystemBus`  
`nm=bus.get('org.freedesktop.NetworkManager')`  
`print(str(nm.Connectivity))`  

would print an integer.

The next section describes whether to translate none, some or all of the arguments flowing across the dbus in a particular direction for a particular key : the argspec section.
