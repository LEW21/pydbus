#!/usr/bin/env python

# Based on http://stackoverflow.com/questions/22390064/use-dbus-to-just-send-a-message-in-python

# Python script to call the methods of the DBUS Test Server

from pydbus import SessionBus

#get the session bus
bus = SessionBus()
#get the object
the_object = bus.get("net.lew21.pydbus.ClientServerExample")

#call the methods and print the results
reply = the_object.Hello()
print(reply)

reply = the_object.EchoString("test 123")
print(reply)

the_object.Quit()
