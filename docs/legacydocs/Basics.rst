================
Getting Started:
================

Those new to this package should start with [Goal, Rationale and Use Cases](https://github.com/hcoin/pydbus/wiki/Goal,-Rationale-&-Use-Cases-(First-visit%3F-Start-here.))

_Experienced pydbus users: this version of pydbus is backward compatible if translation services are not enabled. [Jump to differences](#Differences)_

The project of 'native python' access to a dbus service begins with reading through the pydbus translation specification in the file whose name is the D-Bus service path of interest in the PyDBus translations sub folder.  How to reference that file and begin using that file in programs is described here.

Pydbus allows for a translation structure for each dbus service
string, e.g. 'org.freedesktop.NetworkManager.Device'.  Each translation
structure is a dictionary describing everything necessary to express the dbus service as if it was written from the ground up in python.  It may contain custom functions in complex cases or when a collection of arguments for a dbus method or signal, or even property, is best represented as an instance of a python class.

If no such file is found, then either the native pydbus untranslated system was enough to make the service appear as if it was written in python in the first place, or there is no translation spec as yet for that service.  Writing a translation specification often can be a short effort, look a few of them over then read [Introduction To Translation Specifications](https://github.com/hcoin/pydbus/wiki/Introduction-to-Translation-Specifications). If you write one, and it is for a published dbus service, consider submitting it here for publication so everyone can use it.

The translation guidance specification file will either be documented and readable enough to be complete for that service.  A minimally documented file will still contain everything necessary to understand the published d-bus specification from the python perspective.  From there, read through this "Basic PyDBus Usage" and that should be enough to succeed.

If your need is met by the roster below, you might be able to skip everything to do with pythonic translation files. It's worth a check.  


* D-Bus services that all accept/return a format fixed not at call time but when programming.
* Signals and methods would not benefit from named arguments, they use only positional arguments.
* Only make calls to D-Bus methods or publish signals that do not permit variant arguments (arguments whose format is specified at call time --whether or not it's known at programming time how it will be used.)
* Do not use integers for anything other than amounts.  Not describing a state or condition forcing the user to maintain information about what each number 'means'.
* Do not use an integer to mean more than one thing.  So, no 'bit position X means Y is active'.  No 'these bits are a number from x to y, those bits are flags, these two are another number' etc.
* Do not use classes that represent within one instance more than one argument to or from a D-Bus server.
* Uses only arguments that can be expressed as basic python tuples, dicts, lists, string, ints, booleans and doubles.
* Accept writing 'one of' code necessary to convert D-Bus-formatted arguments to/from 'the right endian-ness', 'the right signed/unsigned', 'the right byte count', or merge them to/from python classes.

**To activate translation services and begin programming, read on:**

Summary: If the translation specification for the bus name is in the translation folder:

 ` from pydbus.bus import SystemBus # or SessionBus  `  
  `bus=SystemBus()  # or SessionBus()  `  
  `proxy_for_dbus_object=bus.get(<bus name>,<object path>,translation_spec=True)`  
  `#any use of proxy_for_dbus_object will need only python standard classes and variables.`  

If the translation specification will be passed at setup time:

 ` from pydbus.bus import SystemBus # or SessionBus`  
  `bus=SystemBus()  # or SessionBus() `  
  `proxy_for_dbus_object=bus.get(<bus name>,<object path>,translation_spec=<translation guidance dict>)`  
  `#any use of proxy_for_dbus_object will need only python standard classes and variables.`  

After that, dbus service properties, methods and signals are native python properties and methods.  All the details necessary to succeed with pydbus and each service should be in the translation file spec for that service.

Generally speaking:

* If a dbus service publishes MyProperty, continuing the example above

`>>>proxy_for_dbus_object.MyProperty = 'Red'  #set the property.  `  
`>>>print(proxy_for_dbus_object.MyProperty)  #read the property.  `  
`Red  `  

* If a dbus service publishes a method (function) called MyFunction continuing the example above and the translation spec supports named arguments, there are three options: passing one object instance and both extracting arguments and setting return values from object attributes whose names are in the translation specification, or using typical python named arguments

`>>>object_instance = ClassICareAbout()  `  
`#...  `  
`>>>proxy_for_dbus_object.MyFunction(object_instance)  `  

`#If it does not support named arguments (boo!):`  

`>>> returnarg1, returnarg2 = proxy_for_dbus_object.MyFunction(object_instance.var1,object_instance.var2)`  

* If a dbus service offers to send a signal, and the translation spec supports named arguments:

`def MySignalHandler(signal_object_instance):  `  
    `pass`  

`def ILikeToKeepTrackOfArgumentPositions(a,b,c):  `  
   `useful_object= MyClass(a,b,c)`  
   `pass  `  

`from gi.repository import GLib  `  
`proxy_for_dbus_object.onStateChanged = MySignalHandler   `  
`#replaces  `  
`#proxy_for_dbus_object.onStateChanged = ILikeToKeepTrackOfArgumentPositions  `  
`loop = GLib.MainLoop()  `  


* Publishing A New Service:

`from gi.repository import GLib  `  
`proxy_for_dbus_object.onStateChanged = MySignalHandler   `  
`bus.publish("path.to.my.service",`  
  `MyFunction(),`  
  `("Subfunction1", MyFunction()),`  
  `("Subfunction2", MyFunction()),`  
  `("Subfunction2/NextLevel", MyFunction())`  
`)`  
`loop = GLib.MainLoop()  `  

* Accessing Path SubFolders:

`    from pydbus import SystemBus  `  
`    from tests.nmdefines import PydbusNetworkManagerSpec,NM_DBUS_INTERFACE,NM_DBUS_INTERFACE_DEVICE  `  

`bus=SystemBus()  `

`\old C way`   
`nm=bus.get("org.freedesktop.NetworkManager",'Devices/0')["org.freedesktop.NetworkManager.Device"]  `  
`print(str(nm.Capabilities) + ", "+str(nm.DeviceType))  `  
`\7, 14`  

`#pythonic way  `  
`nm_trans=bus.get(NM_DBUS_INTERFACE,'Devices/0',translation_spec=PydbusNetworkManagerSpec)[NM_DBUS_INTERFACE_DEVICE]`    
`print(str(nm_trans.Capabilities) + ", "+str(nm_trans.DeviceType))  `  
`#('NM_SUPPORTED', 'CARRIER_DETECT', 'IS_SOFTWARE'), GENERIC  `  


##  Other Pydbus differences when translation services are active
<a name="Differences"></a>
###  The 'timeout' named argument in pydbus's method and signal functions is deprecated, replaced by "_pydbus_timeout"
The translation services enabled named arguments in dbus operations.  The named argument 'timeout' is a popular name for a named argument for dbus services, and as such should not be claimed by pydbus.  The facility to wait for dbus services to reply only for a fixed amount of time is now "_pydbus_timeout".   The new phrase is recognized whether or not translation operations are chosen.  For backward compatibility, 'timeout' retains its old meaning only when translation service are not engaged.


 

* As ever:

Help(object)

is useful.
