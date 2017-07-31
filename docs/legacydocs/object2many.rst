==============
Guidance Items
==============

**Guidance Item:      { "_all_arguments" : True }**

## Typical Use: express one python object as multiple D-Bus arguments.

With this omitted or False (the default): if a 'from  D-Bus' message came in providing introspection string
'uu', translation guidance spec [0] would be given the first u integer to work on,
translation guidance spec [1], the second u, and each translation result returned
in the same position to the python routine.  

If { "_all_arguments" : True } appears,
translation guidance spec [0] would be passed [arg0, arg1] and introspection string (uu).
The result returned is always a list, whatever the length, it is unpacked and
sent on to Python.  Similarly to D-Bus. See below.
  

## Discussion:

Here we provide a means to manage occasions when the information necessary
to transform D-Bus traffic into a class object isn't specified by the D-Bus
publisher as a single container class with all the necessary in one argument,
but requires information spread across more than one D-Bus argument. 
 
For example, consider a python standard library network address and prefix class instance.  These often
traverse the D-Bus as an unsigned integer for the address packed often in the
reverse byte order than most machines out there, followed by another integer
expressing the number of bits that are part of the network part of the address.

If the D-Bus service publisher chose to express that using format 'au',
(array of unsigned), then a single translation specifying a function to
manage converting both numbers into a class instance would be simplest.  One
argument to the function, one result from the function. Typical.

However, what if the D-Bus service publisher chose to express that using 
format 'uu'.  One argument position for the ip address, and the next argument
position for the network prefix?

Ordinarily, with the default, or guidance { "_all_arguments" : False } there would
be two translation specifications, one for each 'u'
argument position, and then some manner of quite hack-ish glue to associate the
processing of one function to the other in order to create the one class instance that
represents both correctly.

Instead of that shortcoming, in these occasions use the guidance pair  

        { "_all_arguments" : True }

which changes argument processing as follows:

### Case - Information flowing from D-Bus, to Python ( arguments returned by methods, sent by signals for D-Bus service clients and reading properties):
 
The very first translation
routine will not deal with the first argument position, the second the next and
so on as usual.  Instead, the very first translation routine will be passed all
the arguments from the D-Bus packaged in a single in-order list, and with the entire introspection string.

Translation processing commences, which always results in a list (though the length may differ)
passed on to the python code.  The length will only differ in the case the user specified
a match function as well in this guidance (the usual case, combining D-Bus arguments into
fewer python object instances).  

If no match function is specified, all this will accomplish
is allowing ordinary translation guidance to cause the python result to fill what would have been
the first return argument instead with a list of all of them.  Useful if one desires to express
many D-Bus values as a single property being read by a python caller.

        
### Case - Information flowing from Python, to D-Bus ( arguments to methods, sent to properties for D-Bus service client):

All the arguments coming from Python are combined into one list passed as one argument
to the first translation specification.  If there is no match function there to separate
class instances into (usually) more arguments, the list coming from the translation will
be unpacked in order then sent as the requested D-Bus arguments.  If a match function is used
to accept the list, however long the list is that it returns are unpacked in order as the
dbus arguments.

        
Note that even if this is used for single valued methods/etc, the input
will be a one member tuple and the output is expected to be a tuple.
        
        