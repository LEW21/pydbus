==================
User Supplied Translation Functions
==================

So far, there's a way to pass an argument through without change, or optionally, do
translation work on it if it is an integer that means something else, or optionally,
work on the contents of a list or tuple dictionary values and/or dictionary keys.
    
What if the translation requirement is more complex for an argument?  For example, an integer that needs to be
packed or unpacked as an internet address? Or some other translation function
that can do all it needs to do using one argument?

For those cases, the translation specification for each dbus path can 
include its own translation functions. 

**Note: If a user supplied translation function requires access to more than one argument**
**to work, such as making a class instance out of several arguments, or vice versa, read**
**[TS Special case: Convert one object instance to \ from many DBus arguments](https://github.com/hcoin/pydbus/wiki/TS-Special-case:-Convert-one-object-instance-to-%5C-from-many-DBus-arguments)**
**then return to this document**
### Calling User or Standard Translation Functions
    
If key,value pair: 
        
`        { '_match_to_function' : True } ` 

exists in the translation dictionary for an argument, any other routines that could have changed the argument are ignored, and the following processing replaces it:

This is the facility whereby dbus arguments are converted into 
python class instances more complex than the above, and vice versa.
also any special argument filtering or custom translations can occur.
        
If this pair is in the dictionary, processing proceeds as follows:
            
First: The argspec keys are searched for an exact match to the dbus/Glib
format substring that is meant to describe the argument the 
translation is to deal with. So if the format string that is an exact
match for the argument (Such as 'au' as 'array of unsigned'),             
treat the value string as either a directly callable function, or: if not callable, then 
a tuple of strings like ('the module to import','the callable function in it')

`     So:  { "au", ('import_module_argument','function to deal with au')}`

and if directly callable: 

`     (name)(argument,argument_index,dbus_format,to_dbus)`  

using the function's return value as the argument value returned to the caller. 

So if the user supplied a function 

`def foo(arg,idx,fmt,direction): `
    `return str(arg)+" is special"`
            
an an argspec dictionary key value pair (along with the _match_function : True pair above):
            
`{ 's' , foo } `
`# or`
`{ 's', ('module_with_foo','foo'}`
            
function foo would be called as 
            
`foo('string argument',1,'s',True)`  

This, assuming we are dealing with the argument next right from the first.
and the dbus variable replaced with whatever foo returns.

So in this case, every simple string would have ' is special' added to it
both on the way to and on the way from dbus.
            
Note: The dbus format for a particular argument is just that portion of the
whole dbus introspection string that is to match that argument. So 'us'
would apply 'u' to the first argument, and 's' to the second argument.
            
If the function can deal with a container, then it can be passed containers
and match such things as 'au'.  Howvever, it's perfectly legal to use the
description above to manage containers and if this function call feature
is specified within a container, each element will be a separate call
and the format string would be just for that element. 

So in the 'au' case, if called to process the elements of the a (list) container, the
function would be called for each element in the list and with the format
guidance 'u'.
            
            
Exactly likewise if going from python to dbus. The argument to foo
will be the python supplied one, the return value passed to dbus, except
the to_dbus variable will be false.  However,
it is good maintainability to be able to write one function that deals with going
to or from a python class to keep like semantics together.
            
Second:

If there is no key in the dictionary matching the dbus introspection 
string, all the argspec keys are treated as regular expressions, and the
introspection string is modified to have the argument index as a prefix:
            
`str(argument_index)+':'+dbus_introspection_arg_format_substring`  
            
The system will match the keys against the string as formatted above, stop at the first match and call
respective function as above. 

So:  
`translation_spec = { 'dbus_path_key_name' : { method_py_to_dbus :            `  
                         `'simplematchfunction' :`  
                            `{ 'method_dbus_to_py' :`  
                                `{  0 :`  
                                    `{`  
                                    `"_match_to_function" : True,`  
                                    `".*" : ('my.module.to.import.with.foo','foo')`  
                                    `}}}}}`  

would convert every return value to the string version in the example above.

If no regular expression matches, an exception is thrown. 

For performance, if there is a choice, it's always preferable to use specific introspection strings the related functions are able to handle.
            
Some functions are included and available by default.  Only the value
below is relevant, the match keys used are possible suggestions only:

`{ '2:u', pydbus.to_ipv4_address } `  

converts unsigned 32 bit byte-swapped integers to
the python ipaddress.IPv4Address class, only if this is argument index
2 (third from left).

`{ 'au', pydbus.to_ipv4_network } `  

converts the first unsigned value in the array as
the network address of an IPv4Network class with prefix length = the second value
without regard to which argument index this is. 

Other functions are:
* pydbus.to_ipv6_address  -- converts a byte-swapped byte array to the ipv6 address class.
* pydbus.to_ipv6_network  -- converts the tuple (byte-swapped byte array address,prefixlength)
* pydbus.to_ipv6_address_list -- converts [{'prefix':num},{'address':byteswappeduint32},..    to [ IPv6Address, IPV6Address, ... ]

etc.  To see the full list, look in the translations directory in the pybus folder. 
