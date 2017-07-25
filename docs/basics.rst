================
Basic Operations
================

While there are many ways to 'fine tune' PyDBus operations (all documented elsewhere), the defaults
are usually all that's needed.

These documents presume you understand the basics of what a DBus is and what it can do. The DBus system
was created so that programs written in various languages all operating at any time could make use
of capabilities provided by a 'service' no matter the language in which that service is written.

The means by which various Linux distributions launch services, whether the service is provided on the
same host as the client/user (usually via systemd) , whether the user's authorizations include access to this or that part of
this or that service (usually via polkit), and so on are distribution specific though largely similar.

As PyDBus
aims to handle most of the details about DBus operations internally, it is likely all you will
need to make use of a DBus service is:

#. The ability to import PyDbus services (see the installation section if this doesn't work for you).
   And, whether the service is provided via the system dbus (most of them), or the session dbus (services to do with the GUI usually).
   For example::
  
     from pydbus import SystemBus # or SessionBus

#. The dbus name of the service.  For example, to access one of the Network Manager's services::

     sb = SystemBus() 
     NetworkManager = sb.get("org.freedesktop.NetworkManager",translation_spec=True)
  
   If you leave out 'translation_spec...' then there is no access of arguments by name, just position.

#. The name(s) of the methods, properties or signals of interest.  For example::

      result = NetworkManager.ActivateConnection(....)

#. The name(s) and expected contents of the arguments to be set or fetched (or the position of that argument
   in the method call).  For example, suppose ActivateConnection was implemented on the service side, maybe something like::

     class NetworkManager(...):
  	      def ActivateConnection(device,connection=somedefault, specific_object=anotherdefault):
  	         ....
 
   Then way that would be accessed via a PyDbus client could be::

	  my_connection_info = ....
	  my_device_info = ....
	  my_netobject = ...
	
      result = NetworkManager.ActivateConnection(my_device_info,my_connection_info,my_netobject)
    
   or, if there are defaults for some arguments (or you don't want to have your code break when
   the service publisher changes the order or number of arguments)::

     result = NetworkManager.ActivateConnection(device=my_new_device_info)
   
#. Return values. Suppose the result above was a list.  For discussion, suppose the names of the
   list entries are::

    [condition, load, cost]

#. Let's say an argument, whether named in the call or the return, is a number, but, the number
   isn't used to represent a count of something.  Instead each possible number 'stands for' some
   named state or condition.  
   
   For example the dbus service documentation explains for argument 'load' above, '0 means off, 1 means low,
   2 means middle and 3 means high.'  Then if translation is active, the PyDbus value for load will not be an integer, but one of the
   strings 'off', 'low', 'middle' and 'high'.  Both when reading and when setting.  
   
   This is only the case
   when there is a 'translation specification' provided for that dbus service.  See the folder 'translations' within
   the pydbus source folder to see what services have translation capabilities.  Use of these is optional.  So, if translation
   is active this works::
     result[1] in ('off', 'low', 'middle', 'high) ==True
     
     result[1] = 'middle'
   
   otherwise if translation is inactive, result[1] would be a number.  The PyDbus service is presented only
   with the related number.
    
#. Let's say argument result.condition above is defined as so many are as flags, one per bit.  So for instance if:: 

     all defined bits 0 -> off.
     bit 1 on -> 'wide' , off 'narrow'.
     bit 2 on -> 'tall' , off 'short'.
     bits 4 and 5 -> both off 'slow', ==1 'normal', ==2 'fast', ==3 'too fast'
     bit 6 -> don't care, ignore it whether it's on or off.
     
   then, for example::
   
     result.condition == result[0] == ('narrow','tall','slow')
   there are options to not include 0 values in the list, to have defaults for unset values and 
   the like.

Notice the DBus service specifications give names to not only the arguments required by methods, but
also the names of the results.  Then, if translation is not active or you are using the older
Pydbus, this is the way you can access that result::
  result[1]
  
But, if translation services are active, these are the ways you can access the result variable::

  result[1] == result.load \
            == result['load'] \
            == result._arg_load \
            == NetworkManager._state.load

The _arg_ above provides a means to access properties whose names conflict with all the names and properties defined
by the list class.

Notice the yyy._state.xxx above. As it is the custom among DBus service writers that an argument name has the
same meaning and format every time it appears in an argument list for all the functions, properties and signals
that use it: PyDbus updates the ._state.argname every time it is changed whether set during a function call or
set in a return.  

The PDbus setting override_defaults_with_state, for example::
  
  NetworkManager = sb.get("org.freedesktop.NetworkManager",translation_spec=True,override_defaults_with_state=True)
  
provides the last value set for a given argument name (whether by call or named in a return value) as a default for any use of that argument within the
particular bus.get / interface.  Anytime an argument is omitted whether by name or position, instead of the
default fixed once at setup time, the latest known value for that argument name is used.

This saves a great deal of keeping track of which argument
goes in what position, and repeatedly entering arguments that are used often but not changed by client code.

It's also a great boon to code maintainability because: It's entirely up to pydbus to manage which arguments
go in what position in method calls, and it gets that information directly from the service publisher using
whatever version of it is provided by the version of the service that happens then to be running.

Should the service change the number or order of arguments, so long
as all the argument names specified by the client still exist, the client side code need not change.

For example::

  r = NetworkManager.somemethod('wide','middle',4)
  ...
  r = NetworkManager.somemethod(cost=5) == NetworkManager.somemethod('wide','middle',5)
  ...
  #suppose
  NetworkManager.GetCost ==10  #reads pydbus property with argument name 'cost'
  ...
  r = NetworkManager.somemethod() == NetworkManager.somemethod('wide','middle',10)

While some would call this capability 'dangerous', remember that many DBus services have just a few methods and properties,
and have a namespace that is consistent within it, including argument names.  While the ._state attribute is always updated,
it is optional to use it in place of defaults for argument names or positions omitted in any particular method call.

Last, the scope of all settings, names, timeouts, etc  is not global across all uses of pydbus, but
limited to the object returned, in the case above::
  instance1 = sb.get(<a set of items>)
  instance2 = sb.get(<the same thing as instance1>)
  instance3 = sb.get(<something else>)
  
Even if an argument position should have the same name, its contents are in no way connected among
instances above. Changes to any one do not affect any of the others (unless the same dbus service is used by both and the service 
chooses to use one value for all callers).


*To get more familiar with the concepts in general terms, see the examples section.*
*To see runnable examples, look in the tests and examples folder within the pydbus source.*



