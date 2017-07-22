The top level translation specification is a dictionary.  It can be passed directly within
the bus.get(...,translation_spec=myspec), or in a translation file for dbus path
my.dbus.path:

pydbus/translations/my_dbus_path.py

Which contains:

`'''Everything the user needs to be successful with this translation.'''`  

`my_dbus_path = { #translation spec for my.dbus.path`    
  `'key name of signal, property or method 1': { \<a dataflow spec\> },`  
  `'key name of signal, property or method 2': { \<another dataflow spec\> },`   
  `'key name of signal, property or method 3': { \<yet another dataflow spec\> },`   
`#...`  
`}`  



The argument to translation_spec MUST be a dictionary or 'None' or omitted
(same as 'None').  The keys of the dictionary are the names of the methods,
properties or signals for which translations are provided, one entry no matter
the same name be used for any combination of signal, method or property.

If you are creating a dbus service, think twice about using the same name for these things.

The next level of spec is the dataflow dictionary.


