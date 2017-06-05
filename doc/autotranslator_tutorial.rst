Pydbus Int Autotranslation
==========================
by Harry G. Coin, Quiet Fountain LLC, 2/2017

dbus/'C' ints as states or flags <--> python strings or tuples
--------------------------------------------------------------

tl;dr:
======
::
 Many flags packed in an integer:
         >>> print(dbus.interface.property_boolean_packed_int)
     was >>> 0x1001
 becomes >>> ('what1000means','what1means')
     was >>> dbus.interface.property_flag = 0x1002
 becomes >>> dbus.interface.property_flag = ('what1000means','what2means')

 Int value not used as a number but representing a state or condition:
         >>> print(dbus.interface.property)
    was  >>> 1234
 becomes >>> 'whatcondition1234means'
    was  >>> dbus.interface.property=1234
 becomes >>> dbus.interface.property='whatcondition1234means'
::

Same for arguments to/from methods and from signals. 

No changes to anything else in the pydbus tutorial except:
bus.get(... ,translation_spec=your_spec_here)

See_tests/nmdefines.py for details.

Aim:
====

The autotranslator extension to pydbus takes the package further in 
its aim to make dbus entirely and natively 'pythonic'. It makes integer
variables passed in dbus that 'mean something other than a number' into
python variables that 'mean as they appear': strings or tuples. 

Secondary Benefits:
-------------------

1. Collect into exactly one readable place all obscure relationships
   layered on integers that 'mean other things'.
2. Avoid requiring all source files that use dbus to include all
   the definition myvar_isblue = 1, myvar_isred = 2, etc. files.
3. Avoid repetitive kludgey code that 'looks up' printable strings
   from variables and interprets strings into 'the int the dbus
   partner needs'
4. Create a standard for translating 'c include headers' into python.
5. Avoids implementing partial variable interpretations in
   multiple files.



Use Case Details:
=================

dbus integers better represented as one member of a tuple
---------------------------------------------------------

Many dbus interfaces represent variables as integers such that
each integer value has a specific meaning.  There are thousands of
'include file'.h or similar files written in C and its variants that
have section after section that read something like:

::
	int myvariable;
	#define myvariable_isred 1
	#define myvariable_isgreen 2
	#define myvariable_isblue 3
::

or

::
	typedef enum 
  		{ myvariabletype_isred=1, myvariabletype_isgreen=2, myvariabletype_isblue=3 } myvariabletype;
	myvariabletype instance1, instance2
::

A quick look at gnome's various dbus interface specifications has many such examples.

When used as dbus properties, or arguments to or results from dbus methods, or
passed as information to signal callbacks, there is always extra work to render
the information in printing or to translate the information often in xml text
or similar to the right number.  What this extension does is to burn a dictionary
of sorts right into pydbus so that all the conversions from integers-as-state-info
to/from 'the shortest string that defines the state' happens before the user has
to deal with it.

so:
::
    from what_was_a_c_dot_h_file import mycondition_isX, mycondition_isY, mycondition_isZ
	...
	bus=SessionBus()
	interface=bus.get("what.not")
	mycondition = interface.someproperty
	if mycondition==mycondition_isX: do_this()
	elif mycondition==mycondition_isY: do_that()
	...
	choice = get_from_user("desired condition?")
	if choice == 'string that means X': num_condition = mycondition_isX
	elif choice == 'string that means Y': num_conditon = mycondition_isY
	else: print("Not found...")
	interface.someproperty=num_condition
	>>> print(lookup_what_mycondition_means(mycondition))
	>>> 'myconditon_isZ'
::
with this extension becomes
::
	bus=SessionBus()
	interface=bus.get("what.not",translation_spec=your_spec_here)
	work = { 'X': do_this, 'Y': do_that }
	work[interface.someproperty](args)
	...
	choice = get_from_user("desired condition?")
	try:
	   interface.property=choice #not case sensitive
	except:
	   print("Not found...")
	>>>  print(interface.someproperty)
	>>> 'Z'
::
Once the interface is defined using the translation spec, 
it can be referenced elsewhere without importing all
the int-to-meaning files.

v2.0 will allow the values to be arbitrary objects that support ==, not just strings.

Dbus integer as (different power of 2 for each item)*(item true/false value) --> tuple
--------------------------------------------------------------------------------------

Dbus's C legacy has many instances where the individual bits in one integer
stand for a collection of boolean variables that are related to the state of 
some activity.  Often termed 'flags'. We see many examples like:
::
	#define myvariable_isdead 0x0
	#define myvariable_iswarm 0x1
	#define myvariable_isrunning 0x2
	#define myvariable_isready_for_whatnot 0x4
	int myvariable /* see above */
	myvariable = myvariable_iswarm | myvariable_isrunning
::

While that's more 'readable' than myvariable = 3, it can't be rendered as 
a string without code that's been written and rewritten in almost
every program and that has to maintained separately from the 
definitions.  And, even when 'automated' still has a preprocessor
that 'has to be run' that 'looks for changes in the code' and 'writes them
to an output module' etc. etc. 

This extension to pydbus allows for a natively python, and logically
cleaner, way to relate to dbus with these variables.  The examples
above become
::
	pydbus_interface.myproperty = ('ready_for_whatnot','Warm') #not case sensitive 
::
which this extension would translate invisibly as 5 when being passed
into dbus, and ('ready_for_whatnot','warm') when being received from dbus.

The Translation Specficication
------------------------------

Check the nmdefines.py file in the tests directory for full details.

In summary, the translation spec is a python dictonary with a key that is
the dbus.interface.spec and whose value is a dictionary.  That dictionary
has keys which are the names of properties, methods or signals that have
integers used as flag bitfields, or integers that represent one condition
for each value, and have as values a tuple that describes what to do
when that key is used as a method's arguments, a method's return value,
a signal or a property.

The 'what to do' item is usually just a dictionary that looks up the
number of the key as the name of a condition. If the item is used
for a signal or method that takes many arguments, then it is a tuple
with 'none' if the argument is to be passed through unchanged, or
the name of a simple 'name':'number that goes with it' dictionary.
There's a special entry in the dictionary if the integer is to
be used as a collection of on/off,true/false flags.


That's it!
==========
See the __main__ entry at the end of pydbus.translator.py for tests and examples.
See the file test/nmdefines.py for a completely finished definition for Gnome's
NetworkManager, with extensive stage-by-stage instructional comments.

License
=======

This file, test/nmdefines.py and pydbus/translator.py are
Copyright 2017, Quiet Fountain LLC.


