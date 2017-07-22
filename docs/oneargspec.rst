This document begins the seemingly 'main work' of the translation module: What to do with
a particular argument in a call with possibly other arguments, to a method,
signal, or a property, knowing whether the direction of the data is to or
from python re: dbus traffic.  These are the values of the dictionary keys
<argspec> in the previous section, they provide translation guidance, just called 'guidance' below.

Everything in this document is a convenience readability shorthand that accomplishes a subset
of what a full translation dictionary argument specification (described in the next document) can do.

**_NOTE: If the direction of data is from python to dbus, and the introspection_**
**_string contains a 'v', be sure to read "Special Cases 2" below after_**
**_reading the main definition._**

Each of the following sections is a convenience and readability shorthand for a more capable but harder to read dictionary format described in the next section.  At the top of each section is summary statement, how the capability would be expressed if using the full dictionary spec (presented later).    
    
* Argspec entry:  None

    None - Do nothing, as if the request to process this argument was omitted.
        
* Argspec entry: string or equivalent.  Names the argument position. Changes the argument format to dictionary.

    Summary: any non container argument, almost always a string, is equivalent to   
    { '_dictkey' : str(non_container_arg) } 

    If guidance is a non-container type (int,string..), 
    name the argument position.  Also causes the arguments
    flowing to python to be in the form of a dictionary with
    keys using these names, values translated from the dbus,
    this in place of a positional argument list.

    Rationale: Here we define an optional facility to free the python programmer
    from retaining the distracting knowledge of which argument goes in what
    dbus argument position, and also allows naming each of the dbus
    arguments used in a method or signal (or property, but as there is
    only ever one, it's redundant to the property name).

    **When calling methods, the dictionary used to create the argument**
    **list on the way to the dbus server is the same as used on the way out.**
    **If the purpose of the method is to update some argument, give that**
    **argument the same name in both the translation specifications.**
           
    Restated: If the return value of a method is the updated version of
    a value passed as an argument, give it the same name.  Then the user
    will not have to write busy-work code assigning output variables.

    One might imagine a class with many well named variables then passing
    vars(instance) as the argument to any number of dbus methods without
    further ado, trusting the translation to ignore whatever it doesn't
    need and arranging what it does need in the order the dbus routine
    wants and in the format it's looking for.
           
    Not so useful for single valued signals, methods and properties,
    but very useful for more complex calls.
           
    Detail: Let's call the passed in non-container (almost always string) 
    guidance value 'argument_name'.
           
    When going from python to dbus, instead of the usual arguments expected
    by the dbus recipient, expect exactly one dictionary with members:

    {argument_name : <the variable that would have been in that argument position> ,...}

    The translation routine will call the dbus proxy with an argument list built
    with the values in the dictionary ordered in the variable position associated
    with 'argument_name' in the translation spec.
           
    Note: If even ONE translation argument_name position is specified,
    any missing specifications for other arguments will be replaced by an
    integer equal to the 0 based index of that argument position as the
    dictionary key and the translated dbus value as the argument when
    going to python, and

    Any omitted argument position/name when going from python to dbus is
    called as if { <argument position> : None } was included.
                  
    Example:

    So, a dbus method that takes/returns two arguments, with a translation spec:

`    { 'MyDbusKeyNameLikeAddConnection', {'method_py_to_dbus': { 1 : 'foo' }}}, `    
    `#'foo' is not a container, so it is the name used for argument position 1`  
    `{'method_dbus_to_py': { 0 : 'bar' } } }  `  
    `#'bar' is the name used when argument position 0 is meant.`

     would expect as an argument from python to dbus not the arguments themselves in a 
     fixed order, but instead one dictionary with

`      { 0 : \<whatever arg 0 is expected\> ,  `  
`      'foo' : \<what would have been next after the first argument\> }`

       n.b. if the 0: ..  key value pair was omitted, the original pydbus function would be called with arguments

       ( None , \<what would have been next after the first argument\> )

       and return from dbus to python a dictionary (not a tuple or list): 

`       { 1 : <whatever the response in arg position 1 was> ,  `  
            `'bar': <whatever the response in arg position 0 was}`

        n.b. the spec did not include a name for argument position one, 
        so the translator uses the argument position number as the default
        name.
           
        Note: when defined in this way, the variable content itself is as
        pydbus would have done with no translation.
        
        Moving on:

1. Argspec entry:  List or Tuple -- When number 'means' a string value

        Here is a 'convenience feature' that does in a shorter form 
        what the full dictionary structure could do with more typing:
        
        Summary: Guidance (a,b,c) or [a,b,c] is shorthand for

        { 0 : a, 1:b, 2:c, "_from_python_to_dbus" : False }
                   
        If the guidance is a tuple or a list for a argument position, and
        not a full dictionary spec, when going from dbus to python,
        replace the dbus argument with guidance[dbusargument]. If evaluating
        guidance[argument] results in an exception, None is passed to
        python.
            
        When going from python to dbus, replace the python argument with
        dbarg such that argument = guidance[dbarg].  In cases where more
        than one argument results in the same guidance[argument] the result
        will be the highest argument. If the string from python has no
        member in the tuple, an exception is thrown.
    
        n.b. The 'inverse' map (in which python arguments result in dbus
        integers used when going from python to dbus is
        computed once when the translation structure is first passed. It is this way:

        inverse_map = { guidance[arg] : arg for arg in argument}
            
        Feature: If an element in the list or tuple is a string, when
        going from python to dbus the string is not case sensitive. 
        When going from dbus to python, the result is capitalized as in the list or
        tuple.
            
        Remember: This specification is ALWAYS given as a tuple or list
        with members being the python representation, and offset being
        the dbus equivalent --- even if the only time it's used is when
        going from dbus to python. 
            
        The list/tuple facility above is the easiest way to specify short
        more or less one to one maps between a reasonable python object and
        what dbus is looking for that 'stands for' or 'means' that object.
        Most often it's just ('what 0 means','what 1 means', ...) when the
        list is short with no gaps, (or None is used to fill a gap and you know
        what you are in for)
            
        Note however, there is no way give the argument position described in
        this shorthand a name, so doing this shorthand blocks the use of passing
        arguments as dictionaries.
  


      Recap:
      
        So far, we have a way to give a name to an argument and otherwise leave it unchanged.
        This changes the python side of all routines from passing a list of arguments to
        passing a single dictionary. It has as keys the names given and lets these routines keep track of which
        one goes in what dbus argument position.
        
        We have a way to swap integer arguments that aren't used for arithmetic with strings that
        describe the situation (instead of a number that means a string the user has to keep
        track of that describes a situation.) 

###         Coming up: 

        A way to spare the python user
        having to figure out how to pack and unpack which bit in an integer 'means what'.
        We can also give these argument positions names to enable passing methods and
        signals a single dictionary instead of keeping track of which argument goes in 
        what spot.
                 
        What if the argument is something we want to do translation
        work on, but it is a container type? List, Tuple or dict?  What if it
        is a container that has other containers inside it?
        

