================================================
Forced replacement of a variable with a constant
================================================

**Guidance Item: { '_forced_replacement' : \<whatever\> }**
        
## Typical Use: Ignore the argument supplied, return \<whatever\>.

This is a convenience.  Instead of having to write match_to_function methods that
do nothing but 'zero out' values such as for which upper level code are not 
capable to understand, use this.  Just a space saver.

### Detail:

From python to dbus, \<whatever\> replaces the value supplied at call
time. If more sophistication is required, use the _match_to_function
facility.
        
From dbus to python, ignore the dbus value returned and replace it with
\<whatever\> to the python caller.
     
### Discussion:

Handy for occasions argument positions hold per-run constants. Version
numbers, hostname strings, system property or capability, etc. With this,
the user only need bother with actually possibly varying arguments.
        
The system will correctly handle None or False as an argument.
If present the variable will be replaced with None or False.

