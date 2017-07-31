_This document assumes you are familiar with ['Basic Python D-Bus Usage'](https://github.com/hcoin/pydbus/wiki/Basic-PyDbus-Usage), and that you've looked over some translation specifications just in an overview way before proceeding here._

======================================
The Translation Guidance Specification
======================================


Each dbus path in need of translation guidance to appear as though the service was written in python to begin with associates the dbus path name to a translation structure.  Whether that structure is passed as a parameter when access to the dbus path is first requested, or fetched from the translations pydbus subfolder, the structure specification is the same. 

### Advantages of file-based translation guidance specs.
If the dbus service in question has components that require the use of the "_match_function" facility (usually calling user or library functions to contain several arguments in one python class instance), using a file based system encourages a good practice: including the functions the particular specification needs with the spec itself.  It's a good idea whenever possible if only for maintainability.  **Beyond the python code in the spec, that file is understood by all pydbus users to be the one place everything there is to know about understanding that service in the python context may be found.** 

Whether that includes exhaustive details about the 'pythonic way' to access every key the service supports, or just how to understand the related general-use service publication document in the python context documenting only the python enhancements: A python user of the dbus spec knows to start there.  Don't let them down.

Argument based translation specifications have value during development, and for dbus services that are entirely 'in house', with no intent to publish for other developers to access.

### Overview
Before reading further here, get a feeling for how all this goes by giving a little attention to a few existing specifications in the translations subfolder of pydbus.  Not for detail, but a general idea about the structure and organization.

Note: All of the pydbus code related to these features is called internally,
only by pydbus routines, not the users. All access is via the dbus proxy's published properties, methods and signals.
As such, the documentation in
the code itself is meant for the maintainers.

With that, what follows is the specification for the translation structure
understood by this package, described 'organicly' from general to detail:

Describing whether and how to translate by levels:
1. File organization / dbus paths
1. The signal, method or property keys and dataflow direction in use per path
1. For each key, call type and dataflow direction: the number of arguments and whether or not to translate some, none or all of them.
1. For each specific argument to be translated: whether to name it, what part of the introspection string (data format definition) dbus thinks it should match, whether to translate some or only part of it, whether to call user defined translation functions or built-in translation capabilities.
1. Guidance sections describing different built-in often used specific translation choices.
1. Special Cases


Fully implemented translation specs for well known dbus interfaces
renders the dbus 'fully pythonic'-- meaning anything that's a class
is aggregated into an instance of the class, all variables have names
and are numbers only if used as an offset from 0, and it's possible
to just pass an instance of a class that has the necessary variables
as members to any method, property or signal and the system will
figure out how to pack it up and send it off.
