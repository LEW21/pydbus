**Guidance:**  

Packing many meanings into a single integer evolved from concerns of memory use, communications efficiency and electrical engineering.  This relieves the python user from having to keep track of 'what a bit position means', instead dealing only with importance: the meaning. 

When mapping whole dbus integers to strings, at most one pair in an argument's guidance dictionary matches.  However, when the pair: 

`{ '_is_bitfield' : True }` 

is included, each bit in the dbus value is, potentially, an independent flag with its own name, or part of a smaller integer used as an amount, or part of a smaller integer where each value 'stands for' or 'means' a named condition,  or some combination.  So, all the pairs in the guidance dictionary are evaluated, they are meant to be taken in combination. There are many allowed ways to format the argument(s) to be translated on the way to the dbus, and several options for formatting the results for python of the dbus translations.  When building a dbus argument, the value starts at zero, then the matches are applied.

This documentation has four sections: Argument formats going from Python to Dbus, guidance dictionary key/value entries defining bits/labels/mini-integers of interest, special commands to do with dbus-to-python data formats and other matching controls, finally discussion and examples.

### Python to DBus Argument Format:
No matter the format requested when processing from dbus to python, all of these formats from python to dbus are always valid. Any string matching in the python to dbus direction is not case sensitive.  If a dbus client, this direction applies to arguments in method calls (not returns), and setting properties.

* None:  A zero will be sent over the dbus.
* True/False:  Looks for the labels 'True' and 'False' (case insensitive) in the guidance. If there are none, it is sent as is.  If there's a match, the related value is set.
* A single int where the guidance defines only one thing: a single int bit-shifting definition.  The result bits will be computed per the definition and those sent.  If no such guidance is in the definition, the int itself will be sent as-is.  If more than one match is found in the guidance, an exception is thrown.
* A simple string that is mapped to a true/match value in the guidance. The associated value will be sent over the dbus.  All other bits will be zero. An exception is thrown if the string matches nothing.  Not case sensitive.
* A dictionary: The keys are the labels defined in the guidance, the values processed through the matching guidance to build the dbus result using the values.  Labels specified in the guidance but not included in the dictionary have no affect on the result.  Not case sensitive.
* A list or tuple:  Any string list member is processed as if the tuple ('string', True). The only other allowed members are tuples or lists with at least one element, usually two.  It is processed as if a dictionary where (key , value) is { key , value }.  If there is only one value, True/1 is used for the second.  Not case sensitive.

The DBus value sent is the result of 'oring' together the results of matching the arguments above to the guidance defined below.

### Labeling bit(s) and smaller int(s) within an int argument


Below are the various ways to associate the state of one or more bits with python strings or as if independent, smaller, integers.  They can be used in any combination unless stated otherwise.

Convenience Note: These guidance pairs defined below obeys the 

`{  _from_python_to_dbus : \<True/False\> } `

Specification setting.  ( If False, the default, the format is as below: 

`{ \<dbus value\> , \<python value\> }.` 

If True, the order is reversed in the spec, 

`{ \,<python value\> , \<dbus value\> },` 

either one can be used whether going to or from dbus. This the same as the system described elsewhere that matches a whole integer to a label.   Sometimes it makes for easier reading to put the python value on the left, and the dbus equivalent on the right.

### Specifics:

`{ \<number\> , 'label' }  `  
* From dbus: if (number & dbusvalue) == number, add 'label' to the list of matches.
* From python: if label (case insensitive) is among list to match, set to_dbus_value |= number.
* Typical use: 0x1 means "this is on", 0x2 means "that is so", 0x4 means "something else is on".

`{ (\<number off\>, \<number on\> or None), 'label' }`  or  
`{ (\<any_on_bits\>, \<number off\>, \<number on\> or None), 'label' }` 
* From dbus: if ((any_on_bits | dbusvalue)!=0) or ((number_off & dbusvalue)==0) and ((number_on==None) or ((number_on & dbusvalue)==number_on)), then add 'label' to the list of matches.
* From python: if label (case insensitive) is among list to match, set to_dbus_value |= number_on. If number_on ==None, use 0.
* Typical use: When 'this is off' needs its own name, beyond just the absence of 'this is on' in the match list, i.e. `{ (0,1), 'this is on' }, { (1,0), 'this is off' }`
* Also used when the presence of a zero bit voids the meaning of another, i.e.: { (0x0,0x3) , "fan high" }, { (0x1, 0x2 ) , "fan low" }, { (0x2, None ) , "fan off" } , { (0x3, 0, 0, "fan on" ) } so when 0x2 is off, 0x1 is a 'don't care', it can be 0 or 1 from dbus.  
* Note: If when going to dbus the 'don't care' bit needs to be a 1, then the 'todbus' and 'fromdbus' versions of the argument guidance need to be different: same labels, but with { (0x2,1), 'power off' } for the todbus side.
* Common Mistakes: A bit test line appears among the true results when the result of the test is true, which may or may not be the same as the bits named being on.  So:
     (0,0) is always true, it means 'don't care what's off, and don't care what's on'.  
     (1,0) means 'Report True/match only when bit position zero is off, don't care about the others'  
     (-1,0) means 'Report True/match when all bits are zero'  
     1 appears in the 'True' results when bit 1 is on, don't care about the others.  
     If the list is { (1,0) : 'bit zero off", 1 : 'bit zero on' } then one or the other will always
     be among the results, and if showing all the true/false values of results, the will both be among them.

`{ \<number\>, ('labelfor0','labelfor1', ..) }`
* From dbus: In short: make a 'mini integer'. Use the 1 bits in number to define the desired bit positions in the mini-int. Collect those bits in order from the dbus value, use the smaller int result as an index to the label list, add the matching value to the list of matches.  Also, the non-zero bits in number need not be consecutive.
* To dbus: Look up the index that matches the label (case insensitive), reverse the to-dbus math to determine the on and off status of the correct bits in number, set just those bits in the dbus value to match. 
* Typical use, unpacking smaller integers from a larger one: 

`{  0x30, ( 'heat off', 'heat low', 'heat medium', 'heat high' ) } , `  
`{   0x3, ('fan off','fan low','fan medium','fan high') } , `  
`{ (0x33,0) , 'power off' } , `  
`{ (0x33,0,0) , 'unit active' }`  

`{ (\<number off\>, \<number\>) , ('labelfor0','labelfor1', .. ) } `  

* If dbusval&\<number off\> != 0, continue. Otherwise as above.

`{ \<number\> , '#label_for_mini_int' } `  

* As above, but instead of using the 'mini-int' as an index into a list of labels, use the value itself.
* The leading # is stripped from the label name before any use.
* If to Dbus: if the tuple or list ('label_for_mini_int',value_of_mini_int) appears, use the mini-int to reverse the math above, set those bits on the to-bus larger int.
* If from Dbus: the tuple ('label_for_mini_int',value_of_mini_int) will appear in the match list in any case, with the value ranging from 0 to the maximum allowed by the number of non-zero bits in the number.
* Typical use: when some subset of the bits in an integer represent an amount, not names for states or conditions.  This is the easiest way to have a label appear no matter its state , i.e. 1 bit, on or off.

`{ (\<number off\>, \<number\>) , '#label_for_mini_int' } `   
* From Dbus: Same as above, but only include the match tuple at all if  dbus&\<number off\>==0.
* To Dbus: \<number off\> is ignored.
* Note: There is an option below which, if set, ignores the \<number off\> value.

`{ '#everything_else', '#the name of your catch-all variable' }`  

* Dbus to python: Treat all bit(s) not referenced in any way elsewhere as an 'and' mask for the dbus value, call the value x, assign it as the value of the tuple: ('the name of your catch-all variable', x)
* Python to Dbus: If the tuple ('the name of your catch-all variable', x) appears, dbusvalue |= x.
* NOTE: From Dbus to python: ONLY IF an #everything_else pair appears THEN: if the computed mini-int 'index' is out of range, has no label in the list, do not throw an exception but include those bits here.

Note: Everything above this line *does* obey the 

`{  '_from_python_to_dbus' : \<True/False\> } `

setting, if False, 

`{ \<dbus value\> , \<python value\> }, `  
if True,  
`{ \<python value\> , \<dbus value\> }, `  

just as does the system that matches a whole integer to a label.  However, the directives below are always as written.


### DBus to Python result formats and Special Options:

Below are several options below like { 'special name', value } which if non False, changes the behavior described above.

`{ (-1,0) , 'your name for all_bits_off' }`  

* This special pair does what it seems to do, with one extra fact, as follows:
* To dbus: no changes to the dbus outbound value.
* From Dbus: Adds the label 'name for all_bits_off' to the match set when the dbus value is 0. 
* Typical Use: There is a habit that gives its own name and meaning to a zero dbus value when many of the bits are used as on/off condition flags for a collection of related parts. This is a meaning beyond each of the bits individually used as flags to mean 'this is on'.  Consider a frequently found case where, each of the bits, if on, stands for some sub-component being active.  When all of them are off, the recognition of the group of things sharing the off state is important. There is is a need to give that its own name, to not return an empty match list.
* SPECIAL PROCESSING:  Use of this pair does not affect anything to do with '_everything_else' pair.
                    
**Dbus to Python Format and Detail Control**:

These have meaning for dbus to python traffic only, usually return values from methods, signal arguments and reading properties:
        
`{ '_show_all_names': True } `  
* Dbus to python: consider the truth value of every pair defined, return a value for all of them, using False for those not matched, not just the true/ matched ones, according to the format specified below. By default, any pair that does not match does not have a label/value result included. So, if there are 15 single bit 'report this if that bit is on' tests, and only one bit is on, the result will have one entry. With this pair included, that example will have 15 return entries, 14 false and 1 true.  If True, the return value format must be either a dictionary or a list.


`{ "_arg_format" : 'dict' }`  
* The default. Dbus results are returned as a single dictionary to python. Keys are labels, True or mini-int result is the value.  True/match labels and mini-ints are always included.  See '_show_all_names' above for more control over what is and isn't included.

`{ "_arg_format" : 'list' }`  
* Same as above in all respects, except a list of two value lists for what would have been a { key : value } pair.  The first element the key, the second the value.The python results from dbus are, by default, returned as a dictionary[label]=dbusvalue pairs.

`{ "_arg_format" : 'shortlist' }`  
* As above for a list, but every return value that would have looked like (\<entry\>,\<entry\>, (label:True), \<entry\>) becomes becomes (\<entry\>,\<entry\>, label, \<entry\>) 

`{ "_arg_format" : 'single' }`  
* Require the result to be just one label/value pair or throw an exception.  Return the value.

`{ "_arg_format" : 'prettydict' } `  
* For pretty-printing.  Try 'single' above.  If that throws an exception, behave as 'dict'
                                        
`{ "_arg_format" : 'prettylist' } `  
* For pretty-printing.  Try 'single' above.  If that throws an exception, behave as 'shortlist'
    

## Further Discussion, Rationale and Examples:
**_With more detail than above, the description below is a restatement,_**
**_with examples and discussion._**

_There is no new capability described below, if there is any conflict detected in what follows, what is above should be preferred._
    
The usual use of this facility is to avoid forcing the python user from having to keep track of details having nothing whatever to do with the important decisions but all about writing yet
another bit-fiddling routine.  So we have the usual case of
'1's bit means this', '2s bit means that', '4s bit means something else'.
        
However, the waters can get a lot deeper than that.
    
Reading this, those that are new might wonder what software engineer in
their right mind would pack booleans and smaller integers interspersed
in the bits of a single integer? The answer is a requirement for
projects 'close to the hardware' as seldom do hardware engineers use
different addresses for each flag for reasons that are really obvious
given some electrical engineering or data transmission background.
These artifacts, totally unrelated to the meanings of the inforation involved, tend to carry over
into 'C' code / device drivers, which habit bleeds onto the dbus.

Probably as far from 'pythonic' sensibility as might be. 
        
However, there have been 'real world' setups where the state of a bit in
a position several away from the first of a few materially changes the
understanding of the first few. Consider a aircraft related setup where
a bit near the most significant end is
'true-> display full range, false-> display idle range', and the
bottom two bits 'speed, 0..3'. A reasonable map would be

'off','ground idle','flight idle', 'approach idle',
'max climb thrust', 'max continuous thrust','military thrust'

skipping over lots of bits in between to do with related topics or often
just marked 'reserved'.  This facility aims to let the translation
structure writer take what amounts to distraction from the point of it
all away from the python user's to-do list.
    


**General Concepts:**
   
Whereas in the last section we had:

`{ \<a number\> : 'what the number means string' }`  

and, if 

`{ '_from_python_to_dbus' : True }`  

is there, then the same thing looks like:

`{ 'what the number means string' : \<a number\> }`  
        
But if

`{ '_isbitfield' : True } `  

is present,  each number is treated as an 'and mask' so that
only the bits that are a 1 in the number must also be set
in the dbus value to match if from dbus, and will be set if
going from python to dbus-- either way, they are associated
with the 'what the number means string'. 

All the entries
in the dictionary for this argument are considered as being
part of just one composite int.
            
Simple 'this 1 bit on <--> this variable name':

`{ 0x4 , 'what the 3rd bit position on means' }`  
        
So, including two strings in a tuple for this argument
would result in the 'or' of the integer masks associated 
with it.  Likewise on the way 'back' to python from dbus,
every 'what the number means string' is included in a tuple
when the variable from dbus has a non-zero value when it
is 'anded' with each <a number> value.
                       
So far, so good. But what if the number has more than one
bit on?  For example if the 5th and 6th bit of an integer
was meant to be understood as its own number between 0 and 3?
Or, the 6th bit when the 10th bit is 'on' means this or that,
and when the 10th bit is off means some other two things.
            
Slightly more complex: '2 or more bits on \<--\> this variable name'

`{ 0x5 , 'what to call the 0 and 2 bit when both are on' }`  

The 'what the number means' string now has a changed meaning.
if it is a simple string, as before, then using it in an argument
to dbus will turn 'on' all the associated bits. On the 
way back from the dbus to python, if all those bits are 'on',
the string will be included in the 'answer tuple'.
            
It is not an error to include two entries with bitmasks that share a
bit position in common.  There's little point if only one bit is
selected in the mask, but there are occasions when a certain
'pattern' of two or more on bits with one in common 'means'
something different depending on the 'common' bit being
on and the other this or that.
            
What if we also need certain bits to be off, and other on?

`{ (0x2,0x5) , 'what to call the 0 and 2 bit on, only when the 1 bit is off'} `  

So far, we've discussed bitmasks that act when certain bits are on,
without regard to whether other bits are off or on.

If the bitmask position is a two member tuple, an argument is
recognized as matching when going from dbus to python if the [0]
element, when 'anded' with the argument, must be 0 and the [1]
element when anded with the argument must equal the element.

When going from python to dbus the [0] offset is ignored
because the base value upon which the final dbus value is
built is all 0 to begin with.

            
What about if all 0 means something altogether different?

`{ (-1,0)    , 'what all bits off means' }`  
            
Note: To include a string that appears only when all the values are
0, that is, to capture a special meaning that 'all off' has, use the
pair for the bits (-1,0) which will require no bits to be on but
also all bits to be 0.

What if some bits taken together is a number where each has it's own name?

`{ 5    , ('what 0 means', 'what 1 means', 'what 4 means', 'what 5 means') }`  

How about a way create two names, one for off and another for on, do I
need two lines  like  { (4,0) , "4 is off" } and { 4, "4 is on" }?
  No. 

`{ 4 , ('what 4 off means', 'what 4 on means')}`  
        
If the 'what the bits mean' string is a not a string, but a tuple or
list of strings? Then the first string will be equivalent to 'all
1 bits off', the second 'the least significant bit on', the third 'the
bit next left of the last one in the mask on', and so forth. So if
the two bits in the mask are consecutive, it would seem like an
entry for a typical integer with a name, number pair for 0, 1, and
2. But it would be the same if the mask was for the 3 and 9 bit position
as well-- a four value tuple for both off, 3 on, 9 on, 3 and 9 on.
            
Now, most of the time, there's just going to be one bit on in the
mask, so the first entry in the tuple is 'off' or 'false', and the
next 'on' or 'true'.  When used in arguments, these string entries
will appear as any other members of the tuple which together makes
up all the bits of the integer.
            
This 'string tuple' option is the only way to cause a tuple to 
be in the argument list when an 'off' condition exists.
        
Q: Can I have two entries that refer one way or another to the same bit(s)?

A:Yes, but be really sure there's no other way.  And test the code
with all possibilities because the results are often not obvious.
                      
Q: What if when going from python to dbus, one guidance entry
 requires a certain bit to be both on, and another off?

A: On wins. 
            
Q: Suppose one entry uses a bit in a number, but another 
uses the same bit in an and match test?  It works, but
take care if providing names for each number there
are enough names to cover all the cases.  
            
Q: I want one variable name to hold more than 'this matches' like
a small number, or 0/False, 1/True. A 'mini-integer'
out of certain bits?  I don't want a name for off and another
for on. Or four different names to express two bits. One only.

A:

`{ \<some bit or bits\> : "#Result as 0 based integer" }`  
            
We see often in hardware device i/o control registers, some of the
bits 'stand for' this or that condition, but a couple here or there
are actually to be understood as simple unsigned integers but with a
much smaller maximum?  Even just one bit to be understood not as
on/off but used as the integer range(0,2)
            
In these cases, instead of 'what the number stands for' as a string
which will only deal with bits as such described above, or a tuple
of strings wherein the first one 'means' 0, the second entry 'means'
1, etc. begin the string with a #. so 

`{ 0x6 , '#number between 0 and 3' }`  
            
The name of the variable when used does not include the leading #.
            

Q: Is there a 'catch all' way to collect in one place any bits not
otherwise defined?

A:

`{ '_everything_else', '#the name of your catch-all variable' }`  

If instead of a bit mask or tuple for (off bits, on bits),
the string '_everything_else' is used, then it expects a single
#nameforthatvariable as the name. 
            
When going from python to dbus, if in a list or simple string the
value will be 0 (it will be ignored). In a dictionary or tuple, the value
will be 'ored', as is, with the final integer computed above.
            
When going from dbus to python, any bit that is not mentioned
anywhere else in the dictionary will mask the to python variable and
the result returned as the value for this key.  

Note: a `{ ( \<these must be 0\>, \<these must be 1\>) , "Here's the name for that" } ` entry
removes all both the 0 and 1 bits mentioned above from the
'everything else' bin: EXCEPT { (-1,0), "all off name" } which does
not affect the 'everything else' variable content. 
            
Why? This feature exists because sometimes dbus values are mapped to hardware
registers meant to be read, changed, then written, set up with bits that
are to be 'unchanged' upon writing but not defined by the manufacturer.

Just including this key in the bitfield guidance and then using the same
argument dictionary on the way in and out takes care of this situation.
            
Q: Is there a way to alert if there are bits set that aren't described in the
list?

A:  Yes.  Test for the _everything_else variable to be non-zero when going
from dbus to python. So this can be used as a check to alert there
are non-zero bits that weren't otherwise defined in the guidance.

When going to the dbus, any bit not explicitly set to non-zero will be zero.
When going to the dbus, variable names are not case sensitive.

            
Bitfield Argument Formats:
        
There are several ways to structure the argument when traversing from python to dbus. 
            
Python to Dbus:
        
All these formats are always recognized.
        
* One string: If passed a string, only the 'on'
bits for that string are set. If a #variety variable representing
an integer appears, 0 will be the value used for it.

* A list or tuple containing only strings: If passed a list or tuple, all the on bits associated with each member
are 'ored' together.  If a string that represents a mini integer appears, 0 is used as the value.  
            
* A list containing any mix of strings or (name,value) tuples: If in a string list or tuple, a list a sub-list or sub-tuple appears as a member, the [0] entry is taken to be the name of the variable, and the [1] entry the
value to use.
            
* A dictionary: If passed a dictionary from python, the names for the variables are the keys
and the values are the state of that key. 0/False/None, 1/True, 2, 3, 4...
            
What if I leave a key out that has a definition?  0/False will be used.
            
What if I put in two values that affect the same bits?  
We assume you meant it.  Be sure if such is coming
from dbus to python there is at least one entry
in the guidance that will match the combined ored result.

            
When going from python, unrecognized strings throw exceptions.
            
When going from dbus to python for 'mini integers' wherein
each value 'stands for' a string, and there is no entry in the
list for the dbus value returned, none of the string names will appear,
and the #variablename associated with '_everything_else' if such
exists, will include those bits.  If there is no _everything_else
variable, and when there is no entry in a list for a dbus variable
included in a bit mash:  an exception is thrown. 
            
     
There are a few special cases left to define.
             
               
Dbus to Python:
     
When passing arguments to dbus from python, almost all formats are accepted. But,
with so many possibilities, what can I expect the dbus to return in these situations?
        
The default to-python argument format is a dictionary that: 

`{ "_arg_format" : 'dict' }`  
        
'Just the True things':
    
 will always have a { 'variable_name' : True } entry for on or
 (off, on) variables that match.
         
 will always have a { 'variable_name' : <integer value> } entries for
 variables that have a #variable_name specification in the dictionary,
 even if the value is 0.
        
 will always have a {'variable_name' : True } entry for exactly one
 of the names in a list given to coorrespond 1 \<--\> 1 to a mini-integer.
        
 That's the default.  It is possible to change that.
    
 'Everything, either way':
        
 It in the guidance the pair { '_show_all_names': True } appears,
 then the dictionary returned will list every variable named in the 
 guidance, with value False or True, or if a mini-integer that value.
        
 'I want a list with possible tuple pairs for mini-integers':
        
`{ "_arg_format" : 'list' }`  

If the above appears, a
tuple or list, even if there is only one thing in it, or possibly
nothing in it will be returned. Mini-integers appear as tuples
within the list ( variablename , mini-int value )

        
'I know there's only ever going to be exactly one match, either 
exactly one mini int, or zero or one variable matches. I
don't want a container.  I just want to be able to set
and read a property of this sort using the variable name
and let this thing figure out what bit to fiddle it in.
        
`{ "_arg_format" : 'single' }`  

If the above appears, the list above is computed,
and if it has length 1 the [0] value is returned, if length 0 -> None,
otherwise an exception is thrown. Very useful for those situations where
it is certain that at most one bit in the field is to be on. In this
case, if no bits are on, 'None' is returned to python from dbus.  In this
case the name associated with a mini-ints used as a number 
will be included iff the number is !0.
        

If `{'_arg_format' : 'shortest' }`  
    
Then if _return_as_list : 'single' throws an exception, 
return_as_list = True is used.


`{ "_arg_format" : 'shortlist' }`

Then as above for a list, but every return value that would have looked like (\<entry\>,\<entry\>, (label:True), \<entry\>) becomes becomes (\<entry\>,\<entry\>, label, \<entry\>) 


'I want the shortest possible non-dictionary result, it's all for
pretty printing and I don't want to show containers of one thing':

`{ "_arg_format" : 'prettydict' } `  
For pretty-printing.  Try 'single' above.  If that throws an exception, behave as 'dict'

`{ "_arg_format" : 'prettylist' } `
For pretty-printing.  Try 'single' above.  If that throws an exception, behave as 'shortlist'
    
