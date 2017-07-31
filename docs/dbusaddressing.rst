A 'Pythonic' way to understand Dbus object paths, interface names, etc.
=======================================================================

*"I found the DBus method or property or signal I want.  What's*
*with the dots, slashes, connections, object paths, interfaces, and other*
*overlapping addressing machinery? Internet connections are easier than these local ones."*

By Harry Coin

Documents explaining DBus programming take a 'top down' approach most of the time.
That works when the reader already has an understanding of the issues involved when
creating a dbus service. They proceed from a general
to specific perspective. `For that type of DBus specification read here <https://dbus.freedesktop.org/doc/dbus-specification.html>`_, 


As software of any complexity is more 'grown first' then 'specified later', I found it's much easier to understand both the how and the
why of the DBus's seeming mishmash
of addressing elements from the point of view of a team of people
setting about creating a DBus service from the beginning.  It's much
more 'obvious' why the DBus addressing seems 'natural' when presented
from this, more or less, 'bottom up' view.

*This document explains terms like 'bus_name', 'object_path', 'interface member' and 'proxy'.* 

Waycool.org's Airtaxi Service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
Suppose you and three other Python engineers at waycool.org decide to provide a DBus
service so your product can be used by pretty much any program written in any language.

You decide to call the service 'airtaxi'.

It is a big project, so you divide it into four different
conceptual areas,  natural to the purpose of the project. You decide
to call them, 'setup', 'status', 'operations' and 'reports'.

Method, Property and Signal Names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each engineer is assigned one area, when done they each return with a directory
full of many methods, properties and signals.

  A method is a routine that is capable of both accepting and returning information. Pretty much the
  same as a function combined with the process running it.  Lots of processes may be using the same function 
  with different 'global' variables.  The DBus 'object path' is, more or less, like the process id.
  DBus here borrows from the language of 'Object oriented programming'. 

  It's better if the writers are careful to use the same names for the named arguments methods if they convey the same meaning.

  A read-only property is a routine that takes no parameters/arguments that can only appear on the right side of =.
  A write-only property can appear only on the left side of an =.  Readwrite properties (most of them)
  can appear on either side of the =, though they can take no parameters.

  A signal calls a user routine with details about an event of interest. 

 
So, back to the example, very creatively,
the first engineer calls her routines 'a1,b1,c1,version'.  They add 'version' because
of their long range thinking.  The second engineer writes code, calling theirs
'a2,b2,c2, and version'.  Similarly for engineer 3 and 4.

They notice some of their routines have the same name, but do different things.

What to do?

Interface Members
^^^^^^^^^^^^^^^^^

Engineer 1 preprends 'setup.' to their routines, 2 prepends 'status.' to
theirs, 3 prepends 'operations.' and 4 prepends 'reports.'.  Why? Because 
those names best describe what each person's work is for, what that basket of
routines does, what they have in common.   

If it happened any two of them used the same name for some routine, because they
stuck the purpose name in front of it, and no two purpose names are the same, there
would be no mistake about which was desired.

So, now we have 'setup.a1' and 'setup.version' and 'reports.a4' and 'reports.version'
and so on.  So it can be clear which area of the project the version function describes.

The name DBus gives such as 'setup' and 'reports' and 'status' and 'operations' as used above 
is 'interface members'.  More or less, the names for baskets of like-purpose routines. 

 Because most of the time
 the routines have names that differ across the whole project, and the name of the routine makes it 
 pretty clear what role it has in the overall project, it seems an avoidable bother
 to have to always use the interface member name when there is no conflict.
 
 So, if there
 is no conflict, it is optional whether to use the interface member name. The system
 will puzzle out which to use.  If there 
 is a conflict, and there is no interface member name specified, the routine
 specified by the service publisher is the 'default' and as such the
 interface member name is used.  So in this case, a call for 'version' gets
 the same as if, say, operations.version was used. 


Project names
^^^^^^^^^^^^^

Our waycool.org company has got quite a few projects going, airtaxi is only one, and
nobody wants to keep track whether any two of them will pick the same names for interface members.

So, for pretty much the same reason 'setup.' and 'operations.' was stuck on before
the routine name, they stick 'airtaxi.' in front of all of them.

So, 'airtaxi.reports.a4' 'airtaxi.operations.b3' and so on.

Organization names
^^^^^^^^^^^^^^^^^^

Our waycool.org folks know their airtaxi service could be one of a great
many services written by who knows who running on a machine.  And, there
could be who knows how many different divisions of waycool might be cooking
up their own version of airtaxi.  So, for pretty much the same reason the
interface member name got stuck on before the routine name, and the project name got
stuck on before the interface name, DBus sticks on whatever else is needed
to make all that clear.  It is prepended in the order of most general to
most specific.  In our case 'org.waycool.'  Could be as.long.as.it.needs.to.be.  

If the company is a one trick pony, having but the one project,
then it may leave the 'project name' noted above off.  It's not a good idea
to do that.

So, now, all the routines together have no possibility of name conflict::  

 <organization.thru.project> .<interface member like 'operations'> .<a routine of that member>


DBus terms <organization.thru.project> above the 'interface',  So Dbus naming is::

  <interface.usually.with.dots>.<interface member no dots>.<method, signal or property of that member no dots>

  
Usage of the above in other online documentation tends to use just the word
'interface' or 'interface spec' rather loosely, leaving to the reader to
puzzle through from the context whether it's just the <interface> above they
mean when using the word 'interface'. Or, the interface with the member name.  Or, the whole
thing.   But Pydbus makes a clear distinction. 

  Jumping ahead, pydbus infers the <interface> part from elements discussed
  later below. All of the interface members of an <interface> are loaded as 
  keys to a dictionary.  The method, signal and so forth above are either
  attributes or method names of the object returned as the value for that
  key.  If the method, signal or property name is unique, then it can
  be accessed without the [interface mamber] bit.

*From here, the work of the service designers is done, all their routines have* 
*names that are different enough to let out into the world without fear of*
*conflict.*

Keeping with the implementation story, now comes the time for the DBus engineering team to do all the connection
plumbing needed to make it available. 

First up, is it to be one service per system, or one service for each user's session?

System or Session Bus?
^^^^^^^^^^^^^^^^^^^^^^

The engineers notice the airtaxi service is to be provided
to any process launched by any user.  Linux calls that
the namespce the SystemBus.  Had the service been to provide something
to each user's GUI session, pretty much independently of
other users that may or may not do the same thing, the
SessionBus would be the namespace to use.  DBus provides
a rich set of other options, which 99% of Linux services
will never use. i.e. dbus connections over TCP.

The PyDBus code returning the root object connecting a client
program to either the systemwide or user-session-wide overall communications
environment is::

  import pydbus
  mysysbus = SystemBus()
  #mysessionbus = SessionBus()
  

Next up:  The client knows where their end of the communications pipe
is.  But how and where to connect the other end to the service?  

Bus Name: Connection Destination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Much as a website address connects a browser client to whatever it may be the
server offers:  A PyDbus destination address is the name on the DBus for connecting
the client to whatever number of interfaces a dbus service publisher offers.

It may be the dbus service publisher has combined a several entirely different
whole services, including airtaxi named above, from any number of organizations, 
into one service.   Just as one website may offer connections to many things that
perhaps have little to do with one another.

PyDbus calls this more-or-less dns style address the 'bus name'.  The parameter
name used for this later on is bus_name.

Nearly all the time, it is exactly the same as the <interface> element described 
above.  In our example 'org.waycool.airtaxi' .  As it is almost always the same
as that, it uses the this.that.other string format.

Confusingly, the bus_name connecting the client to the published service software
need have no terms in common whatsoever with the interface names offered there.
com.quietfountain.permanet could offer the waycool.org.airtaxi interface.  Most of
the time, to use some elements of an interface, the bus name is the same as the
<interface> term above.


Next up:  Finally,  how to choose from among the interfaces one to access?

Object Path: Name the routine needed.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The designers have created a suite of interfaces described above, and connected the bunch of those
to the appropriate session or system bus and given it a bus name (usually the <interface> above).

Here we make the big perspective shift from the people designing and publishing a service, to
the programmer making use of it.  The means whereby the client programmer tells the dbus system
which one from among all the routines it wants to use is called the 'object path'.  Not the same
as the interface name above.  The interface system is as the contents of filesystem or directory,
the object path is about picking one of them.

  
Each routine the client wants to use is  termed a dbus object and its name is the 'object path'.  It nearly always leads with the name of 
the related <interface> and, technically (the pydbus syntax is different),  ends with the specific routine name.

An example of a whole object path could be /org/waycool/airtaxi/reports/version  though it won't look like that in the client code.

The object path format has three differences from interface names (which use a .) and bus names (which use a .):

1:  It leads with a /

2:  It replaces all the . in the (possibly) related interface name or bus name with a /

3:  When used, it is broken into three parts. 

The first part is nearly always the / version of the bus name (which is usually but not always the <interface> above, such as org.waycool.airtaxi becomes object path /org/waycool/taxi).

So often is the object path the / version of the bus_name, that the routines that set up the connection to the bus use
the / version of the bus name and the object path argument can be omitted.

The second part is one from among the entire collection of <interface members> that lie 'under' the first part. In practice,
The interface desired is given as the key in a dictionary having as values objects that stand for each of the interfaces the organization publishes.


The third part is the name of the specific routine the client wants the publisher to run.  These are attributes of the interface value named above.

So, the object /org/waycool/airtaxi/setup/initialize  

in python / pydbus it looks like::

 result =  pydbus.SystemBus.get('org.waycool.airtaxi')['.setup'].initialize(parameter, parameter)
           |               |                          |         \__________v 
           comm structure  .get('the bus_name')       ['interface member'] . method name

The first term above chooses the bus that has one instance of the service for the whole system.

Then it chooses the bus_name org.waycool.airtaxi as the general dns-like name for the particular server on the bus.
It sets the start of the default <interface> above to be also org.waycool.airtaxi,
As the object path is omitted, it automatically sets the object path to start with /org/waycool/airtaxi

Then it chooses from among all the interfaces 'setup'.  As it starts with a '.', it implies to not overwrite
the initial object path and interface name, but to append .setup as the name of the <interface member>
desired, and append /setup to the object path desired.

Then it chooses from among all the methods, properties and objects in org.waycool.airtaxi.setup the method initialize.
It appends .initialize to the interface specification, finalizing that, and it appends /interface to the object path,
finalizing that.

*Which explains a lot, but is a bit clunky to read and use.  Read on.*
 

Proxies: One Name to Rule them All
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Great, we have bus types and bus connection names and object paths and interface names leading to the routines wanted, how to actually call them
without repeating all the detail above each time?  DBus / Pydbus calls the objects that retain all that detail in themselves 'proxies' or 'proxy objects'.

So, the code to access the airtaxi routines written by waycool's engineers, selected from whatever
else may be in the entire collection marketing added to the object path /org/waycool/airtaxi provides that would be::

   waycoolAirtaxi = mysysbus.get(bus_name='org.waycool.airtaxi',object_path='/org/waycool/airtaxi', .. other parameters)
   or 
   waycoolAirtaxi = mysysbus.get(bus_name='org.waycool.airtaxi', .. other parameters) 
   or
   waycoolAirtaxi = mysysbus.get('org.waycool.airtaxi', .. other parameters) 
   

Because so very many interface names begin with org.freedesktop, any bus name that begins with a . is presumed to 
include org.freedesktop before the particular name.   So '.bus_name' is understood to mean 'org.freedesktop.bus_name'.

Finally:  Using the service's capabilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

so, above, we have the proxy named waycoolAirtaxi all set, ready to go.  We call call engineer 1's status routine a1 like this::

  mystatus_a1 = waycoolsAirTaxi['.status'].a1(<arguments ...>)

and, engineer 2's reporting property b2 like this::

  myreport_b2 = waycoolsAirTaxi['.reporting'].b2
  
We could have used the whole interface spec::  

  myreport_b2 = waycoolsAirTaxi['org.waycool.airtaxi.reporting'].b2

Being able to name the specific <interface member> is great because both the .status and .reporting collection (a.k.a interfaces) have routines called 'Version' and they are not the same.

To improve speed and readability, to get a particular interface basket of routines and guarantee no name collisions, 
there is a shorthand convenience for readability.  Append the [.<inteface name>] above to the get call and omit it from
the uses.  Be careful to name the object instance appropriately as only the routines published under that particular
interface will be available if the [.<interface name>] is appended in the .get call.  So::

   waycoolAirtaxi = mysysbus.get(bus_name='org.waycool.airtaxi', .. other parameters)
   mystatus_a1 = waycoolsAirTaxi['.status'].a1(<arguments ...>)
  
   #is delivers the same value as 

   waycoolAirtaxi_status = mysysbus.get(object_path='/org/waycool/airtaxi', .. other parameters)['.status']
   mystatus_a1 = waycoolsAirTaxi_status.a1(<arguments ...>)

As a further convenience, noticing that nearly all the routines in all the interfaces written by the waycool.org engineers have 
names that differ, if there is no method, signal or property name conflict it is allowed to omit the <interface member> part above::

   waycoolAirtaxi = mysysbus.get(bus_name='org.waycool.airtaxi', .. other parameters)
   mystatus_a1 = waycoolsAirTaxi['.status'].a1(<arguments ...>)

   #is the same as

   waycoolAirtaxi = mysysbus.get('org.waycool.airtaxi', .. other parameters)
   mystatus_a1 = waycoolsAirTaxi.a1(<arguments ...>)
   
Wait? Where did the part of the interface name that comes before the specific routine but after 'airtaxi' go?

Nowhere, it can still be accessed explicitly as shown above.  However this shorthand takes advantage of the
fact routine names rarely conflict and so specifying the last bit of the interface name (.status,.reports,.setup,.operations)
above doesn't really add anything other than length to the code.

Also, it's a bit of a convenience since the service publisher can specify which <interface member> has 'the latest' version of
routine with a given name, and so provide that without forcing the client to specify one if it wants the latest, while still
being able to specify a particular one if desired. 

*Gotcha -- Routines with the same name, different interfaces*

Notice if the 'Version' name is used, like waycoolsAirTaxi.Version, there are four Version routines, each provided by 
a different interface. The one that gets called is controlled by the service publisher.  This scheme can help replace old versions
of routines with new ones without changing any names for the client.  Clients that want a specific routine provided by a particular
interface even if there are others should specify in the interface name in the .get call or as a ['.<interface name>'] later on.

Moving deeper:
^^^^^^^^^^^^^^

Often, a method in an interface will return a string or more of other interfaces of interest, all of which are related to the
one called but not specified in advance except as a general template. For example, a service doc may specifically identify
how to get a list of, say, usb devices. But the whole interface spec for each device may not begin with anything like the
spec used to collect the names.  So, the object path may not be the same as the interface spec.  


In those cases, while the bus_name will still be 'org.waycool', the object name (which picks from among the specifications), could
be /com/warranty/usb and the spec also com.warranty.usb...  If the call to get the proxy fails, check whether the object_name  ( ='/com/warranty') parameter must be stated
explicitly in the .get call above.



Argument Names as object-wide variables and defaults
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  

So many DBus services use the same argument position name in more than one method.  What's more,
usually with the same meaning across functions. So in some ways, each such name is an attribute that
has a meaning within the bus.get(...) object. 

In the example above, waycoolAirTaxi._state.<argument position name> is always updated whenever
data is supplied for that parameter, whether by default or passed in to a method or named as 
a member of the result returned by the method.

PyDbus has an option *override_defaults_with_state*, which when true causes the latest value
for an argument name in ._state.argname (also ._state._arg_argname) to be supplied to the method
as a default value for an omitted parameter. With that, code like::

    status = waycoolAirTaxi.GetStatus(condition='warm')
    waycoolAirTaxi.report(status,condition)

becomes::

	waycoolAirTaxi.GetStatus(condition='warm')
	waycoolAirTaxi.report()
	


So, what's 'Introspection' about?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Routine Names
^^^^^^^^^^^^^

DBus provides a way to fetch the names of the routines in the basket of functions each interface provides.  

Much of the time this is of no use as that detail is in the documentation for the service.  But, this can be
a useful when some of the routines list the names of further interfaces.  The number of those may vary from time to time or machine to
machine.  For example the number of network adapters a machine has may control the number of sub interfaces each providing
the same basket of routines but with the assumption all related activity refers to the particular interface.

This can also be a good way to check whether the particular version of a dbus service has the routines necessary by the caller's code.

Parameter Names
^^^^^^^^^^^^^^^

Also, Introspection provides, usually, the names of each of the parameters in a method call.  This version of PyDbus
allow you to use either positional or named parameters. 

In something of a twist, introspection names the results of method calls and property calls as if parameters.  Even the
name for not only a property, but also for what the one argument would have been named had it been a one argument
method call.

Types and order of data per parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Last, introspection defines almost everything to do with the order and data type of each parameter.  Whether it should
be a list, or an array of integers, or a tuple of some list of other data types.  



The Python to Dbus Variant Conundrum
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The only thing introspection does not provide is to do with a data type called 'Variant' when it is being used
as a python parameter element to a dbus method.  Variant data types are a shorthand for 'don't presume to know
anything about what this has within it until the moment you get it'.  All the details as to what's in it come
along with it so it can be unpacked and used.  

Which in some ways is just fine when information is coming from the dbus toward a python use.  Pydbus can puzzle
it all out and use the most relevant python type needed each time a Variant comes in.

But, it is often the case that a DBus service which specifies that a Variant data type should be supplied, in fact
cannot cope with whatever combination of data types the python client may choose to send.  Introspection is of no use,
as there is no guidance from it as to what Variant content a method can cope with.  The service doc just asks for 'variant'.

Pydbus Translation Specifications allow PyDbus to check for the various allowed data type patterns the service can actually
manage.

Pydbus Pythonic "Full Introspection"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*When integers are not amounts, but each 'stands for' some condition or state*

The documentation for nearly all services provides not only all the paths and interfaces and routines and parameter names and 
(mostly) what data types to use.  Those documents also define how to interpret what integer results 'mean' when used as flags
or descriptions and not as amounts.  Right in those same documents you'll read something like::
 
   #define MYSERVICE_RUNNING_HOT 1 
   #define MYSERVICE_RUNNING_WARM 2
   #define MYSERVICE_RUNNING_COLD 3
   
Then there will be property like 'running_status' that returns a number leaving the programmer to puzzle out what the publisher
meant by it.  That help is not provided in the introspection.   So PyDbus offers it.  Properties like 'running_status' mentioned earlier
returns 'HOT' or 'WARM' or 'COLD'.  And can be set the same way if the publisher allows it::

  myservice.running_status='HOT'
  #instead of 
  myservice.running_status=dict_of_meaning_to_value_for_running['HOT']
  #or, worse,
  myservice.running_status=1
  
Similarly for integers used as a collection of bit flags.  flag&1 means on or off, flag&2 means high or low, etc. etc.



Someday:
^^^^^^^^

You might suppose if::

   waycoolsAirtaxi = mysysbus.get('org.waycool.airtaxi', .. other parameters)

and the routines available in the .status so called <interface member>  term is ::

   waycoolsAirtaxi_status_proxy = waycoolsAirtaxi['.status']

and then the .status interface has some further level of routines in 'sub' interface .status.substatus then you
should be able to access those routines by::

   waycoolsAirtaxi_substatus_proxy = waycoolsAirtaxi['.status']['.substatus']
   
I'd like to see something like::

   myobject = bus.get('bus.name' , ...)
   #then
   myobject['some.interface.or.other'].foo(arg)
   #and
   mysubobject_method_yadda_result = myobject['some.interface.or.other']['.deeper.object'].whatnot(yadda)
   #and have interface .<whatnot> by default refer to the object with / changed from .
   #so
   mysubobject == myobject['.deeper.object'] == myobject[some.interface.or.other]['.deeper.object'] 
   
The point is to avoid mostly redundant 'pydbus.SystemBus.get(...)' calls for one-of use of sub-interfaces.
   
*Not so much yet.*



By Harry Coin,
Copyright Quiet Fountain LLC, July 2017
Document License: GPL

