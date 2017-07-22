===========
Rationale
===========


The original PyDBus author, Linus Lewandowski, wrote this package's aim as a sentiment:  _PyDBus aims to make [D-Bus](https://www.freedesktop.org/wiki/Software/D-Bus/) ['fully pythonic'](https://www.python.org/dev/peps/pep-0020)_.  

Such a package for the D-Bus system, (which passes structured messages including the message's format between  entirely independent processes to provide well described services), would include the ability to: 

* name arguments in methods and signals as well as 'C style' position sensitive argument lists.  The first pydbus allowed:  
    `a,b = dbuspath.method(b,c,False)`

    to that, we add:  
    `a,b = dbuspath.method(this=c,that=b) #third arg has a default.`

    and    
    `myarg = { 'this' : c , 'that' : b }`  
    `dbuspath.method(myarg)`  
    `print(myarg['new_key_was_a'] + ' updated: ' + myarg['that'] + ' ' + myarg['this'])`  

    and  
    `myarg.this = c`  
    `myarg.that = b`  
    `dbuspath.method(myarg)`  
    `print(myarg.new_attrib_was_a + ' updated: ' + myarg.that + ' ' + myarg.this)`  
    
* exchange typical standard library and other class instances as such, that is: not forcing each user to write custom code to pick out and reformat attributes into the data format, argument position order the messaging system understands. i.e for an object 'myobject' that has attributes this, that and whatnot:


      YourDBusPath.dbus_key_update_this_that_using_whatnot(myobject)

      not

      return_args = YourDBusPath.dbus_key_update_this_that_using_whatnot(helper(myobject.this),
                                       myobject.that.byteswap(),str(myobject.whatnot))   
      myobject.this = str(return_args[0])  
      myobject.that = return_args[1].byteswap()  
`
* create a means for D-Bus service publishers / python porters to specify once then distribute to everyone everything necessary to bring D-Bus published services to 'pythonic' standards,
* offer default values for missing named arguments,
* build in 'future proofing' to existing code: so only changes to the translation spec are necessary to allow code for future or older versions of either the python or D-Bus side to work with available python/D-Bus code,
* provide a means to add version information to methods/signals so python users can write more maintainable code,
* remove the need for python users to manage distracting, non-pythonic, D-Bus-specific machinery like:
    1. whether an integer is packed big or little end first, signed or not, number of bits,
    1. whether a floating point number is double or single precision, 
    1. whether a D-Bus server is expecting a single character string to be sent as a char or a byte or a string,
    1. managing the formatting of arguments to those D-Bus methods that allow argument variability from call to call (D-Bus 'variants' in python-to-D-Bus introspection strings),
    1. D-Bus services using integers not to keep track of amounts but to represent a state or condition instead of the name for it (e.g. 1 instead of 'red', 2 instead of 'blue'.)
    1. D-Bus services using individual bits in one integer as a collection of related boolean 'flags' (e.g. & 1 fan on, & 2 heat on, & 4 light on, &7==0 all off)
    1. D-Bus services that use a few bits here and there in a larger integer as little integers representing list indexes, while using other bits as boolean flags, and others as mini-integers. ( e.g.: 0x1 fan up, 0x2 fan middle, 0x3 fan down, 0x4 light on, bits 0x8,0x10,0x20 as vent angle 0 to 7)  These formats are common in hardware device registers.


While this version of PyDBus does do those things, earlier versions did not.  The original package gave a hint it was possible: to do all the 'plumbing' necessary to make remote service provided processing seem no different than using a typical python package. The original package did connect python attributes and methods to D-Bus properties and methods/signals, and hid the details of control and data flow on to, and off of the D-Bus.  The original package pretty much stopped at the boundaries of D-Bus capabilities common to all server specifications, including D-Bus design gaps which forced 'low level' very 'un-pythonic' D-Bus byte-fiddling into higher level code (e.g. calling methods that expect variant formatted arguments).

By now it should be plain the key to this capability for each D-Bus server is the python translation guidance used by PyDBus. Summarizing this: The translation spec aims to provide enough expressive power so that no add-on functions are needed in most cases to describe how to deliver a fully pythonic D-Bus interface. When the D-Bus information is too complex, the spec provides a concise means to pass to user functions included directly in the per-service spec everything required to turn D-Bus traffic into native python results.

I offer these extensions are the natural 'next steps' needed.

***

## The three levels of PyDBus users

1. Most users: Those who want to make use of already finished, fully pythonic, D-Bus capabilities.  There are two basic steps: Reading through the translation guidance file for the desired D-Bus service to see examples, then get started.  From here, go to [Basic PyDbus Usage](https://github.com/hcoin/pydbus/wiki/Basic-PyDbus-Usage) 

1. Translation spec writers: If there is no translation specification available for the D-Bus path/service of interest, in most cases it is straightforward to write one.   First read through a few translation specifications and use examples to get familiar with the look and feel.  Then kindly read through the documentation in this wiki, starting with [Introduction to Translation Specifications](https://github.com/hcoin/pydbus/wiki/Introduction-to-Translation-Specifications).  Your spec can be tested by passing it directly at bus access setup time.  When finished, put a copy of it in the translations folder under the D-Bus path name (with _ instead of .).  If the D-Bus service your spec completes (from a python perspective) is widely offered, consider sending your spec for general distribution in the project's translations folder.

1. Maintainers:  Translation spec writers would find little benefit from reading the source code. The PyDBus source code operates so 'down in the engine room' there is little in it of interest to anyone but maintainers.  Although I think most readers would find taking the time to understand it would generate deep insight into the capabilities that make python so popular.


***


Personal Note: This software and documentation amounts to my 'thank you' to the open source community after years of use and a few other contributions. 


By [Harry G. Coin](https://www.linkedin.com/in/harrygcoin),
Initial version complete: March 29, 2017.
