## Argument Specification Guidance Dictionaries
      
The previous sections documented argument specification capabilities available
when the argument specification is a string or list or tuple, just convenience readability shorthand for the full specification here.  Provided by the shorthand when the specification is:

1. A string: names the variable position, so that  
   `myclass.x = 234`  
   `myclass.y = 567`  
   `myclass.z = 890`  
   `myclass.x, myclass.y, myclass.z = path_object.method(myclass.x,myclass.y,myclass.z)`  

   becomes:

   `myclass.data['x']=234`  
   `myclass.data['y']=456`  
   `myclass.data['z']=890`  
   `path_object.method(myclass.data)`  

    Or, almost equivalently:

    `path_object.method(x=234,y=456,z=890)`

    The presence of any keyword argument changes the argument style
    from a single dictionary to the python keyword style argument list.

    **However: Whereas in the single dictionary argument case, if a translation spec gives an**
    **argument position the same name on the call and return side, the entry**
    **in the dictionary passed will be updated.  That is not available when**
    **using the keyword style.**

    The point of these two possibilities (and the attribute based possibility below)
    is:

    1. To offer the typical 'python' suite of argument passing styles, but also:
    1. Give the translation writer the ability to provide a python class that tightly integrates one or more related dbus services.  By carefully choosing matching names for method call and return arguments, a 'call by reference' capability is simulated. 

1. A list or tuple:  for integers that 'stand for' something else so that  
   `myclass.property = lookup_number_for['all good']  `  
   `print(myclass.property2)  `  
   `14`  

   becomes:

   `myclass.property = 'all good'`  
   `print(myclass.property2)`  
   `'what 14 means to me'`  

    
The full capability of the per
argument translation specification is delivered when using a dictionary as the
translation guidance argspec follows.  

(Recap: An 'argspec' describes what to do with a particular argument position when used specifically as an argument or as a return value for a particular named method, signal or property of a particular key for a specific dbus path e.g. y in bdus_path_object.key_that_object_publishes(x,y,z).

The following dictionary specification outlines all available translation options.  There are many further convenience and readability features, not least using the same argspec for setting and reading properties, and for method arguments which return values of the same sort. The details follow.

**The general form of the dictionary argspec is:**

`dictionary_argspec = { \<directive name\> : \<directive setting\> , ...`  
                       `#Then one of the following two styles:`  
                       `\<dbus value match info\> : \<how python should convert it\>, ...`  
                       `#or`  
                       `\<python value match info\> : \<how dbus wants to see it\>, ...`  
                     `}`  
        
### 1. Argument format: default positional, named via dictionary, and class attributes.
        
To offer full python capability, Dbus translations must
be able to offer users more than the default positional arguments.  Pydbus offers
two other ways to define method and signal arguments (and add optional context to properties as well):  dictionary style and attribute style.

1. Default: 'traditional' argument meaning by position in argument list.

    By default, the methods and signals expect the arguments on the 'python side' of any dbus operation to
    to be the usual list with the position of the argument in the list defining its purpose.  The DBus
    side always uses positional arguments as defined by the dbus service spec. If this
    is desired, nothing further need be added to the argspec translation guidance.

1. Dictionary Style:

    If the pair:
        
    `{ '_dictkey' : 'name for what the argument in this position is for' }`  

    is included, it is expected a single dictionary argument will be passed and returned
    on the python side no matter the number of arguments defined by the dbus service.  That all the 
    arguments for this key have no conflicting settings.
        
    In that single dictionary argument, the keys are the names given in the
    above _dictkey pairs for each argspec position, the values are what would have been in the
    respective argument position had the default list style been used.

    There are three benefits:  Giving the same name in a function call and function return
    argspec will cause a data item to be passed to the method then updated automatically
    upon return.  The other benefit is changes can be made to the dbus service or the
    user's code regarding the number and purpose of the arguments to the method without
    forcing refactoring of the user's code. Last, by using a dictionary instead of object
    attributes to name arguments, related groups of arguments can be kept in one place
    at arm's length from the method, akin to a 'structure' in other programming languages.
    This can ease some database and other disk read/write issues.

   _Note: If even one argument specification sets the dictionary style, the entire argument_
   _list changes from the default list to the dictionary style._

        
1. Attribute Style:

    If the argspec dictionary has the pair:

   `{ '_attributename' : "attribute for this argument"}`  

    Only a single class instance is passed on the python side.  The arguments
    to the dbus partner will be read from the object using the attribute
    name above to identify the appropriate dbus argument position.

    So:

   `myclassinstance.x = dbus_path_object.method(myclassinstance.a,myclassinstance.b,myclassinstance.c)`  

    becomes:

   `dbus_path_object.method(myclassinstance)`  

    Note: If even one argument specification sets the '_attributename' style, the
    entire argument list changes from the default list to the attribute style.

    It is an error for _attributename and _dictkey both to appear anywhere in the
    specifications for one argument list, or within the specification of one argument.

    While, technically, this could be done for a property, the occasions to do so
    seem few as there ever is only one argument.
                
The argument naming feature, combined with passing class instances to methods and signals (or
dictionaries instead of argument lists), makes it possible for the python
programmer to not have to remember argument order.  It's also a boost to
maintainability, since service spec changes can be expressed in the translation guidance
and translation spec without disturbing established code, or code able to run on
different versions of the service.   

Remember, all attributes of objects used in these calls that are not mentioned
        in the guidance are ignored. In that way, complex objects upon which
        many different dbus methods might offer services can use the same
        instance so long as the attributes names don't conflict.

   
### **Special Note for translating Methods**
        
Only when using the "_attributename" style 
calling procedure in the guidance on BOTH the call side and the
        return side of a method call, will the same object will be populated by the
        return call as was passed to the method.  This is the default.

The idea being if the same attribute name
appears in both guidance structures associating (probably different)
argument positions to the same name, the return call value will replace
the value used on the way in. If the names differ, the return side of a method
call will add/update other attributes to that object.

Only when using the "_dictkey" style calling procedure the default is
that a NEW dictionary will be returned to hold the responses to a method call.

HOWEVER: If the pair 

`        {"_new_return_instance" : False }`  

appears in the guidance for a method call on both the call side
specification AND the return side, the dictionary or object passed
as an argument on the call side will be populated by the return values.

If the pair 

`        {"_new_return_instance" : True }`  

appears in the guidance on either the calling or returning
argument spec, the response to a method call will be a new dictionary or a 
new class with only the return values as keys / attributes respectively.
        
Of course, if using the traditional list of arguments on either side
of a method call, or not matching attribute / dict style arguments
then the _new_return_instance will be treated as False, even if
it is otherwise specified.
        
This feature has no meaning for signals or properties, since
these are ever only sending information one way per call.
        
      
### Default Values for Named Arguments

In order to duplicate the python capability of defaults in the case named
variables do not appear in a dictionary or as an attribute in the information
passed in on the python side, the argument dictionary pair 
        
`        { "_default" : <whatever> }`  
        
Will cause the missing argument to be added by pydbus with the default named in the pair as the value.
Otherwise, arguments specified in the translation but missing when used are defaulted to None (which is usually an error on the dbus). 

This is useful for maintaining the functioning of legacy code when new
arguments are added to dbus keys that older code does not supply.

## Specific Translation Capabilities

So far, almost everything has been described except the actual business of
changing the python side argument to be compatible with the dbus side,
and back.  Calling conventions, default values, and a few convenience features
one of which translates an integer that 'stands for' something into the
thing it "stands for" and back.

Described now is the actual business of deciding whether to change
a specific argument, and if so, to what and how.

### The Default Translations:

Each argument presents to the translator with an initial value, and the portion of an 'introspection string' the dbus service indicates should direct the format and nature of the argument.  [Click here for introspection string usage information](https://dbus.freedesktop.org/doc/dbus-specification.html#type-system)

_**Unless specifically stated otherwise below, the translation routines pass the data as presented along without change.**_

When the argument is a string, or a boolean, or otherwise have but one representation on both the dbus side and the python side, there is no need to provide any further detail (unless condensing several arguments into or from a new object instance, see below).  However, there are the following capabilities for the other situations:

* When the argument is a list or tuple

Absent any further direction, when a list ('array' in dbus parlance) appears as an argument, or a tuple appears, the default is to pass the list or tuple with all its contents unexamined along unchanged. However, if the pair

`        { "_container" : < another entire per_arg_translation_spec > }`  

appears, this will cause the given whole new argspec translation specification to be applied to every element
of the container.  The introspection string passed along will reflect only the container contents.  The secondary argument specification is formatted exactly as is this, but any directives to do with argument format are ignored. This can be nested to any necessary depth.

The resulting argument will be a container of the same
sort the argument was, in the same order.

* When the argument is a dictionary

Absent any further direction, when a dictionary appears as an argument ('array of key value pairs' in dbus parlance), the dictionary is passed along unchanged.  However, if the pair

`        { "_container" : < another entire per_arg_translation_spec > }`  

appears, the new translation specification will be applied **ONLY TO THE VALUES** of the keys in the dictionary.

If there is a translation activity to be applied to the keys of a dictionary argument, the entry

`        { "_container_keys" : < another entire per_arg_translation_spec > }`  

Will apply the named guidance to the keys of the dictionary, while applying
the argspec named in "_container" to the values.  If it is not desired to translate the values
but only the keys, omit the "_container" entry.    

The introspection string passed along to the key translation argspec will be just that of the key value in the dictionary, likewise the value/container argspec will be passed the string covering just the values.

Some may notice there is no facility to operate on the keys and values as a pair.  There is, in the form of user supplied functions, see below.  Any other approach seemed, 'unpythonic' as it were.

**Convenience and Readability Feature:**

At a level the translation writer expects a container argument (tuple, list, dict) to appear for translation, and the argument specification at that point expects an integer to 'stand for' some other meaning (usually a string),  the translator will act as though:

     `{ "_container" : <whatever was there that wasn't a dictionary> }`

was written.  That is, the shorthand will be applied to each member of a list or tuple, and the values if a dictionary.  So, if the plan is to translate all the contents of a tuple or list, or all the values
        in a dictionary, just include the spec for the values.  Note: the integer to label mapping applies
only one level, to the members of the immediate container which the dbus expects to be an integer and the python side an equivalent label (usually string), not further containers.  If the same mapping is used in more than one place in a specification, then define it outside the translation structure then use that variable name as the value of the related container arguments.

### Wrapping it up

There is, of course, much more.  Everything left has to do with particular translation situations and the capabilities available for acting on them.  Those are documented online.  Check the links in the documentation for such as  "TS Guidance ..." and "TS Special Case". 

Documented there are new specific purpose translation capabilities, including the specific argspec guidance necessary to engage them.  For example, how to give names to flags as individual bit positions in an integer, how to connect integers with values that 'stand for' something else, and more. 

Remember: any argument given to the translator is passed through unchanged if no translation specification has been written for it **EXCEPT**: When going from python to DBus and the introspection string has even one 'v' in it.  

If that's the case, read [TS Special Case: Define Python To DBus Variants](https://github.com/hcoin/pydbus/wiki/TS-Special-Case:-Define-Python-To-DBus-Variants).  Whether by inattention to detail by dbus service publishers or a gap in the dbus specification: translation routines must be engaged in these situations, there is no other way to create the necessary dbus message.  That is, without forcing upon the pydbus user the need to comprehend GLib packing details and other code to do purely with below the water line machinery to the meanings involved).

In these cases it is almost always best if the translation writer supplies information as to what formats the dbus service can handle without error when the argument is marked as 'variant' (determined at run time). The above document describes that process.

