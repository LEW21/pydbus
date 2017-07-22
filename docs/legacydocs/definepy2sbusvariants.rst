=======================
Python to DBus Variants
=======================

**Guidance Item: { '_variant_expansion' : \<vinfo\> [,\<vinfo\>]\* }**  
*Where*   
**\<vinfo\> ::  \<guidance\>[/\<guidance\>]\*[.<repeated tail>]  and**  
**\<guidance\>:: 'an introspection string with no variants'**  
**\<repeated tail>:: 'a convenience, appends 'repeated tail' to each guidance'**

## Typical Use: Specify all possible argument formats to accept for a 'v' in an introspection string when going from Python to DBus 
    
### Discussion: There exists a bothersome meaning asymmetry in the dbus architecture.
        
It arises when going from python to dbus when the dbus introspection
string contains a 'v' (meaning GLib Variant). Variant is pretty close to
the python idea of object, the actual content could be anything the DBus
service can parse for that key.
        
This is not a problem when going from dbus to python, as each variant sent over the
D-Bus has within code that describes what it is about in precise format detail, and so has the
information necessary to convert it to a native python type.  This is
done automatically by GLib unpack routines before the translation
functions are called.  In fact this list is what pydbus returns when no translation is
asked for, and the one supplied as input to the translation routines.
        
So, from the Dbus, it is baked in to the message how to set it all ready
for the next level to deal with.
        
Not so going from python to dbus if the published dbus
specification has a 'v' / variant.  While technically the DBus will 
accept nearly anything it can express within a 'v' and ship it over
to the DBus service:  Each service can parse only specific patterns, 
which patterns are known only to the service.

Without using this feature at all, pydbus will parse the arguments and
take reasonable guesses to build then send a correct DBus message.
Should you be very confident the other side can handle
any legal dbus message matching the overall spec, you don't need to
read any further.

However:

1. What if the remote service accepts only 32 bit unsigned integers?  This
is not the default format for a python int.  The service will throw
an error message when it gets 'ii' instead of 'uu'.

1. The introspection string is a 'v', the argument is an int.
Is the recipient expecting a signed or unsigned value? 
An 8, 16, 32, 64 or other sized integer?  Big endian or
little endian?
        
1. The introspection string is a 'v', the argument is a floating
point number.  Is the recipient expecting a double or a float?

1. The introspection string a{sv} or a{sa{sv}} is often seen in dbus
server specs even when there is but one legal way for the types the v's
can contain that the recipient is capable to understand in the message.


This feature provides pydbus the guidance necessary to transform the 
python arguments into the specific variant forms expected by the remote DBus
partner.  As there can be many possible legal argument formats, 
the first specification that matches the provided python argument
structure is chosen.  If none match, an error is thrown.


### Implementation Details:
        
1. To dbus 'v' values MUST be translated by the full dictionary formatted
per argument guidance entities.  The shorthand guidance forms mentioned before that
in this document will throw an exception.
        
1. The very first top level dictionary translating an argument that includes
an introspection string
with a 'v' SHOULD have something like a { "_variant_expansion" : 'this/that/theother','what to do with next v', etc }.
Before argument processing begins, the overall expansion is built by extending the list.  
So, It's
up to you whether to include everything in the _variant_expansion
key/value pair in arg[0], or spread it out over arguments.  For code re-use it's probably best
to include a string in the associated argument with a v.


However it gets built,
the whole "_variant_expansion" directive to understand any v in the passed in 
introspection string is applied against the entire string
before any argument processing occurs.

Detail: By 'applied against the passed introspection string', 
is meant the translation guidance for an argument is no longer
passed just a 'v', but (say for two legal ways to parse a v):

'v:\<guidance\>/\<guidance\>:' 

         
If there is no _variant_expansion key, or not enough to match 
all the v's demanded in the introspection string for the call, the
v will be replaced in the translation specification v:: and pydbus
will take it's best reasonable guess how to fill the variant from
the arguments provided.

Note that v:...: is treated as a single introspection string unit, like u or s.
The unmodified introspection string is retained
for all uses outside these routines.)
        
Note: If the arguments are to be managed by function calls using {
'_match_to_function' : True } then it is up to that function to manage
all the parsing possibilities and details. Nothing further in this section applies,
however the introspection string passed to the external function will
be the modified v:: one for its use.

### Further examples:
        
The explanation below uses phrases like 'a{sv}' is parsed as as a{su}'.
While that is so, the actual data passed to dbus does not pass a 'u', it
passes a variant that contains a 'u'
        
All this is so because without guidance, a python list with 
two integers would be by default packed as ai, when it is
completely possible the recipient is expected au and rejects
the ai (e.g. the network manager parsing a network address/prefix
combo).
        
So the string {'_variant_expansion' : "u/s,s/(i)"}
applied against the introspection provided string "ava{sv}' would be
broken into two argument calls: av and then a{sv}.
This would attempt to parse the first argument with information
av:u/s: first as an au, and if that failed, an as. In either
case the result would be an array of variants with only the content
differing.
        
The second would be parsed first as a{ss} and if that failed a{s(i)},
again with the ..s or ..(i) would actually be packed as a variant
containing an s or a variant containing a tuple holding ints.
        
        
If there is the '_variant_expansion' key, and the value is anything other than 
a string, or is v:: the system will attempt a default parsing. Lists become
arrays, tuples are tuples, dictionaries are arrays of dictionary entries,
strings of any length, including single characters, are strings, floating
points are doubles and ints are unsigned 32 bit values, boolean is bool,
and None argument elements are parsed as 0, false, '' etc.
        
If this parsing is acceptable, just include
{'_variant_expansion' : None }
        
If a \<vinfo\> is empty, e.g. ',i' the first variant would
get the default parsing above (functions would see v::),
the second would parse a signed integer and convert it
to variants containing an int.

Last, just as a convenience,  instead of writing axyz/bxyx  the same can be written a/b.xyz

