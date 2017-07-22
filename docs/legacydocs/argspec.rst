==============
Argspec Format
==============
Previous sections covered: loading translation specs per dbus path, identifying which keys in that path need translating, then isolating per key the whether the data flow is to or from the dbus and whether for a method, property or signal. For each of those last elements, this section describes how to manage the argument list for that purpose.

### Managing the argument list, the argspec format:

_Note: when an argument to/from dbus is described as 'unchanged' below, take that_
_to mean 'what pydbus would have done had no translation been requested', not_
_'nothing'_

_Specifically: When flowing from dbus to python, what the GLib function_
_variant.unpack\(\) creates is either passed unchanged through the translation process, or passed to these routines_
_for translation then passing that on.  When flowing from python to dbus, 'unchanged' means whatever the Glib's_
_Variant parser does with the to-dbus direction introspection string and the caller's arguments (all ints are introspection 'i', not 'u' or byteswapped, or..).  If translation is active, it accepts those values as input.  What the glib_
_library does in these functions is often correct, and on other occasions needs the attention of these_
_routines)._

The format for managing the argument list is same for all argument directions and for methods, properties and signals.

### The Argspec Dictionary

The argument specification dictionary has key / value pairs as follows:

{ \<argument position number (leftmost is 0)\> :  \<single argument translation guidance\> , ... }

Like:

{ 0 : translation_guidance_for_arg0 , 2 : translation_guidance_for_arg2, ...}
 
The translation guidance value may be None, or as described in the next section.

So, 

{ 1 : single_argument_translation_guidance } 

would leave arguments 0, 2 and up unchanged, and would use 'single_argument_translation_guidance' defined in the next section, to manage the translation for argument 1.
           
### Alternatives for readability and convenience:

* If the argument processing specification is not a dictionary, but instead a list or tuple, it is processed as if each member is a dictionary pair above:

{ list_index : list_content_at_index }

So if the argument specification is 

(argspec_0, argspec_1, None, argspec_3)               

The leftmost argument and the one next to it would be translated further.  The one after that skipped, and the next translated, and any more skipped.  An equivalent dictionary as described above is:

{ 0 : argspec_0 , 1 : argspec_1, 3 : argspec_3 }

*  Anything other than a dictionary, None, list or tuple:

So many argument lists have just one argument, for example, all properties. For readability, it is possible to pass a single argument argspec itself: not in a list or dictionary or tuple.  It is the same as if passed

{ 0 : argspec }

A dataflow dictionary entry for this sort of argspec (previous document) might look like this:

{ "property", argspec }

Avoids syntax clutter, improving spec readability.

### Adding arguments on the Python side:

The above specification calls for an integer corresponding to the position of the argument in the list to be the key, with the value being the argspec translation guidance for what to do with it.  If the value for the key is -1, then the argument is added to the python side (only when using non-default named arguments, see the next section).  But the value of these added arguments never traverses the dbus.  The next section describes a way to specify default values for arguments.  The combination of those two features makes it possible to send to upper level code details such as the version number of the translation specification, dummy values for dbus services specified but unimplemented, and more.

