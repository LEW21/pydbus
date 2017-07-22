========
Overview
========

Pydbus with translation enabled:  

>`       dbuspath_object.method_name(myClassObject)`  
`       print(myClassObject.y)`  
`       >>> 'Updated_y'`   

Pydbus without translation:

>`        myclass.x, myclass.y = dbuspath_object.method_name(helper(myClassObject.x),lookup_number[myClassObject.y].byteswap())`  
        `print(str(myClassObject.y))`  
`        >>> 14`



When using PyDbus, if you enable a translation dictionary for a dbus path that describes anything special about it, all the dbus-specific issues
are invisibly managed so well it's very hard to tell the difference between a
python method, property or signal written from the ground up in python vs. one
handled by a partner over the dbus. Given a well written translation spec, hopefully distributed freely in the pydbus translations directory for widely used packages, 
the user need know nothing further about how the dbus delivers capability.

PyDBus without translation enabled does expose DBus properties, methods and signals as python class attributes and methods, but requires comprehension of DBus 'machinery' and cumbersome one-of glue functions to mutate arguments from native python usages to and from DBus needs, except for the most basic DBus services. 

First time users, start with [Goal, Rationale and Use Cases](https://github.com/hcoin/pydbus/wiki/Goal,-Rationale-&-Use-Cases-(First-visit%3F-Start-here.))

To use a ready-to-go translation to access a pydbus partner, read [Basic PyDBus Usage](https://github.com/hcoin/pydbus/wiki/Basic-PyDbus-Usage)

To write a translation specification for a dbus path, start with [Introduction To Translation Specifications](https://github.com/hcoin/pydbus/wiki/Introduction-to-Translation-Specifications)

See [status.txt](https://github.com/hcoin/pydbus/blob/master/status.txt) for development plans and status information.

