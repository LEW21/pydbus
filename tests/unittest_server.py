'''
Created on Jun 16, 2017

@author: administrator
'''
from gi.repository.GLib import MainLoop
from gi.repository import GObject
import pydbus
from pydbus.extensions.PatchPreGlib246 import compat_dbus_connection_register_object # @UnresolvedImport @Reimport @UnusedImport
from pydbus.extensions.PatchPreGlib246 import compat_dbus_invocation_return_value  # @UnresolvedImport @Reimport @UnusedImport
from pydbus.extensions.PatchPreGlib246 import compat_dbus_invocation_return_dbus_error  # @UnresolvedImport @Reimport @UnusedImport


class PyDbusUnitTestService(object): 
    """
    <node>
        <interface name='pydbus.unittest'>
            <method name='NoArgsStringReply'>
                <arg type='i' name='response' direction='out'/>
            </method>
            <method name='AddTwo'>
                <arg type='i' name='addinput' direction='in'/>
                <arg type='i' name='addedoutput' direction='out'/>
            </method>
            <method name='Quit'/>
        </interface>
    </node>
    """
    def __init__(self,loop):
        self.loop = loop
        self.timeout_id = GObject.timeout_add(60*1000,self.on_timeout,None)
        
    def on_timeout(self,user_data):
        self.Quit()

    def NoArgsStringReply(self):
        """returns the string 'Hello, World!'"""
        return 0 #"first string"  # Should get translated as 0 over the bus, then show up as 'first string' via translation

    def AddTwo(self, i):
        """Returns two more than it gets."""
        return i + 2

    def Quit(self):
        """removes this object from the DBUS connection and exits"""
        self.loop.quit()

def pydbus_server():
    loop = MainLoop()
    bus = pydbus.SessionBus()
    try:
        bus.get('pydbus.unittest',timeout=1)
    except:
        with bus.publish("pydbus.unittest", PyDbusUnitTestService(loop)):
            loop.run()

pydbus_server()
