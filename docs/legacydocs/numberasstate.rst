
=========
Guidance
=========  

* **Implemented by pair { \<dbus int-like item\> : \<what that item means in python\> }**  
 **Unless optional pair:        { '_from_python_to_dbus' : True }**  
 **Then:               { \<what that item means in python\> : \<dbus int-like item\> }**  

* **Optional:           { '_replace_unknowns' : (\<string if int missing\>,\<number if string missing \>) }**  

**Conveniences:**
*   Can use the same guidance dict whether data flow is from or to DBus.  
*   Python to dbus only: If a python arg is an int, pass it as is, no lookup.  
*   If no _replace_unknowns key: missed dbus lookup yields 'UNKNOWN_0x\<hex number\>'  
*   String "UNKNOWN_0x\<hex number\>" always sends \<hex number\> to dbus.  

### Typical Use: Integers when not used as amounts, but to 'stand for a state' or 'express a condition'.

Also when an int is used as a collection of related booleans packed into an integer when at most one can be set, each a different power of 2 to avoid conflict.

Translation Dictionary Example:

`SimplePath = { 'KeyNameForLocation' : { 'property' :  `  
    `    { 0 : "at a store" },`  
    `    { 17 : "in my office" },`  
    `    { 102 : "at the airport" },`  
    `    { 23 : "at home" } }}`  

`from pydbus.bus import SystemBus`  
`bus = SystemBus() `  

`#New Way`  
`mydbuspathobject = bus.get('my.dbus.path', translation_spec = SimplePath ) `  
`mydbuspathobject.KeyNameForLocation = 'in my office'`  
`assertEqual( mydbuspathobject.KeyNameForLocation, 'in my office' )`  
`mydbuspathobject.KeyNameForLocation = 102`  
`assertEqual( mydbuspathobject.KeyNameForLocation, 'at the airport' )`  

`#Old Way`  
`mydbuspathobject = bus.get( 'my.dbus.path' )`  
`assertEqual( mydbuspathobject.KeyNameForLocation, 102 )`  
`mydbuspathobject.KeyNameForLocation = \<any illegal int\>`


### Discussion: 
      
This feature is most often used, and most often used this way:

In the case each expected value of integer 'stands for' a meaning described
in a string, create the dictionary this way if specifying what should
happen when going FROM dbus and TO python:  
         
        { <dbus returned value key> : <pythonic interpretation of returned value> , ...}
        
so 
                
        { 1234 : 'whatever1234means' }

        
With that, if one does pydbusitem.property='whatever1234means', it will
result in a dbus call replacing that argument with the integer 1234.

pydbusitem.property == 'whatever1234means'
        
### Migrating away from usage imposed by C 

Style suggestion:  Many 'C include files' have entries like
    
        typedef { PROPERTYNAME_MEANING1 = VALUE1, PROPERTYNAME_MEANING2 = VALUE2 } ITEMNAME;
        
Consider a translation entry like  PROPERTYNAME = { "MEANING1" : VALUE1, "MEANING2" : VALUE2 }
stripping off the repeated parts of the definition.  Python is much better
about namespaces. This avoids repetitive string content and eases 'pretty printing'.
        
Likewise typical 'include' file content like  
`#define THE_BLUE_FAN_OFF 1`  
`#define THE_BLUE_FAN_LOW 2`  
`#define THE_BLUE_FAN_HIGH 3`  
`#define THE RED_FAN_OFF 4`  
`#define THE_RED_FAN_LOW 5`  
`#define THE_RED_FAN_HIGH 6`  

assigned to such as:  
`int RedFanStatus;`  
`int BlueFanStatus;`  
        
consider renaming to the least redundant possible form:
        
RedFanStatus = { 4 : "Off" , 5 : "Low", 6 : "High" }  
BlueFanStatus = { 1 : "Off" , 2 : "Low", 3 : "High" } 

### Convenience, writing  { string : number } instead of { number : string }

If the dictionary includes the key value pair

        { '_from_python_to_dbus' : True }
        
then the entries are understood as being not {1234, 'whatever1234means'} but
rather {'whatever1234means' : 1234 }
        
For what little it is worth, If {'_from_python_to_dbus' : False } is included, the default first understanding
is used.
        
NOTE: When used as a key, 'whatever1234means' is case insensitive. This is to make
pretty printing not interfere with whatever capitalization the dbus partner
is using. So write key names that will appear in the preferred display capitalization
format.
        
### Handling End Conditions:

If when coming from dbus a value has no matching key entry relating it to a python string,
"UNKNOWN_0x" where X is the hex rep of the dbusvalue is returned. 
        
When going to dbus from python, the value "UNKNOWN_0x..." is parsed always and the
hexidecimal number after the x used as the value.
        
HOWEVER: if the dictionary has the key, value pair 
        
        { '_replace_unknowns' : (<string>,<number>) } 
        
though UNKNOWN_0x.. will be parsed when going
TO the dbus as described above, strings with no matching guidance values will not 
throw an exception but instead send the number above. FROM dbus will return the
string argument above (Which can be anything, including 'None') and not "UNKNOWN_0x..." when a number comes from dbus that is out of range of the name tuple as the field.

        
Without a { 'replace_unknowns'...} as above, if a pythonic string value has no
mapping as a dbus integer, an exception is thrown. 
        
Feature: TO DBUS: If there is reason not to define every possible value
as a string, just pass the integer itself and that will be transmitted
as is to the dbus partner.
        
WARNING: If providing the same dictionary to both the to and from dbus
routines and letting this module compute the inverse for the one
not in the format required:  If  two different keys result in the same
value, it is NOT DEFINED which of the keys the value will return when
(if ever) that dictionary is used in the 'other' direction.

