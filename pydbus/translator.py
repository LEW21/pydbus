'''
Created on Feb 24, 2017

@author: Harry G. Coin
@copyright: 2017 Quiet Fountain LLC
'''

import re

class PydbusCPythonTranslator(object):
    '''See tests/nmdefines.py for documentation on the creation of the translation specification.
       
       The operation of this class is built in to method, property and signal routines.
       
       To activate translation, instead of bus.get(...) do bus.get(...,translation_spec=your_translation) 
       
       There should be little need to read further for usual operations.
        
       The details of this class internally:  Upon initialization do an optimization so that 
       conversions from numeric results to pythonic format is as fast as the passed in
       tables associating pythonic results to numeric format.  
       
        These routines are used internally:
        
        instance.ctop(pydbus_item,"property_or_method_name",value_or_tuple_to_be_translated_from_c_to_pythonic)
        
        instance.ptoc(pydbus_item,"property_or_method_name",value_or_tuple_to_be_translated_from_pythonic_to_c)
        
        These will return a tuple if passed a tuple, or a value if passed a value, in the expected format.
        So, for example, networkmanager_transinstance.ctop(pydev_network_manager_instance,"Metered",0) would return "UNKNOWN"
        and networkmanager_transinstance.ctop(pydev_network_manager_instance,"Metered","UNKNOWN") would return 0.
        
        These functions are meant for use in subclassing getitem, setitem type entries in pydbus, and similar.
        To make capitalization as the situations change easier:
        The strings returned are the strings given, while the strings matched are not case sensitive.
        
        Style suggestion:  Many 'C include files' have entries like
        typedef { PROPERTYNAME_MEANING1 = VALUE1, PROPERTYNAME_MEANING2 = VALUE2 } ITEMNAME;
        Consider a translation entry like  PROPERTYNAME = { "MEANING1" : VALUE1, "MEANING2" : VALUE2 }
        stripping off the repeated parts of the definition.  Avoids unhelpful string content and eases 'pretty printing'.
    '''
    
    def _swapdictspecial(self,dictitem):
        ret={}
        for k, v in dictitem.items():
            if k=='_is_bitfield':
                ret["_is_bitfield"]=True
            else:
                ret[v] =  k 
        return ret
    
    def _updictkeyspecial(self,dictitem):
        ret={}
        for k, v in dictitem.items():
            if k=='_is_bitfield':
                ret["_is_bitfield"]=True
            else:
                ret[k.upper()] =  v 
        return ret
    
    def _upcase_one(self,roster):
        if isinstance(roster,tuple):
            ctoproster=()
            for item in roster:
                if item==None:
                    ctoproster+=(None,)
                else:
                    ctoproster+= (self._updictkeyspecial(item),)
        elif roster==None:
            return None
        else:
            ctoproster = self._updictkeyspecial(roster)
        return ctoproster
       
    def _swapone(self,roster):
        if isinstance(roster,tuple):
            ctoproster=()
            for item in roster:
                if item==None:
                    ctoproster+=(None,)
                else:
                    ctoproster+= (self._swapdictspecial(item),)
        elif roster==None:
            return None
        else:
            ctoproster = self._swapdictspecial(roster)
        return ctoproster

    def __init__(self,translation_spec):
        #Process spec so that it is as quick to look up value -> string as string -> value
        self.p2cspec = translation_spec  #This one holds the string to value info
        self.c2pspec = {}  #This one will hold the value to string info
        for transpath, transdict in self.p2cspec.items():
            c2pitem={}
            self.c2pspec[transpath]=c2pitem
            for objectstring,(methodinroster,methodoutroster,signalroster,propertyroster) in transdict.items():
                #consider transpath:transspect <-> org.freedesktop.foo: {name:(what,to,dowithit)}
                c2pmethodinroster = self._swapone(methodinroster)
                c2pmethodoutroster = self._swapone(methodoutroster)
                c2psignalroster = self._swapone(signalroster)
                c2propertyroster = self._swapone(propertyroster)
                c2pitem[objectstring]=(c2pmethodinroster,c2pmethodoutroster,c2psignalroster,c2propertyroster)
        #Upcase the p to c keys.
        for transpath, transdict in self.p2cspec.items():
            for objectstring,(methodinroster,methodoutroster,signalroster,propertyroster) in transdict.items():
                transdict[objectstring]=(self._upcase_one(methodinroster),self._upcase_one(methodoutroster),self._upcase_one(signalroster),self._upcase_one(propertyroster))
                
    

    def _one_ctop(self,transdict,cvalue):
        if transdict.get("_is_bitfield",None)==None:
            return transdict.get(cvalue,None)
        retlist=()
        for k,v in transdict.items():
            if k=='_is_bitfield': continue
            if (k & cvalue): retlist += (v,)
        if retlist == ():
            zerotext = transdict.get(0,None)
            if zerotext==None: return None
            return (zerotext,)
        return retlist
    
    def _one_ptoc(self,transdict,plist):
        if transdict.get("_is_bitfield",None)==None:
            return transdict.get(plist.upper(),None)
        cval=0
        if transdict==None: return 0
        if len(transdict)==0: return 0
        if plist==None: return 0
        if len(plist)==0: return 0
        for k,v in transdict.items():
            if k=='_is_bitfield': continue
            if k in plist: cval |= v
        return cval

    
    
    def translate(self,pydevobject,itemname,itemvalue,offset,ctop=True): #0- method, 1-signal, 2-property, False for p to c.
        '''pydevobject is returned by pydbus.[SessionBus|SystemBus]().get(...) with optional ...[particular.device.path]
        itemname is a string that's the name of either a dbus method, signal or property.
        itemvalue is a tuple containing the argument(s) to be evaluated for translation.
        offset is 0 for a method, 1 for a signal, 2 for a property.
        ctop = True when processing arguments being returned by a method, signal or property.
        ctop = False when processing arguments being passed to a method, signal or property.
        '''
        if isinstance(pydevobject,str):
            pathlist = (pydevobject,)
        else:
            class_str = str(pydevobject.__class__)
            if class_str.find('CompositeObject')>=0:
                pathlist = re.split("\\(|\\)",class_str)[1].split('+')
            else:
                pathlist_m = re.search("'DBUS\.(.*)\'",class_str)
                if not pathlist_m: return itemvalue
                pathlist = (pathlist_m[1],)
        ret_tuple = []
        for t in itemvalue: 
            #make the return list the same as the passed list.
            ret_tuple += [t]
        #If we find any matches, we'll replace the item as we go along.
        #Now, hunt for reasons to translate return items.
        for onepath in pathlist: #pydev classes are often composite, search all the classes used to make it.
            itemdict = self.c2pspec.get(onepath,None) if ctop else self.p2cspec.get(onepath,None) 
            if itemdict==None: continue
            #One of the paths in the class exists in our translation spec.
            itemtuple = itemdict.get(itemname,None)
            if itemtuple==None: continue
            #One of the translation tuples has a name that matches the requested one.
            itemaction = itemtuple[offset]
            if itemaction==None: continue
            #The matched item has translation work for the type of call this is (method, signal, property)
            #Is the work to do a one-of or are we translating one or more in a tuple?
            if isinstance(itemaction,tuple):
                #One or more jobs to do on the same argument list.
                minlen = min(len(itemaction),len(itemvalue))
                for i in range(0,minlen):
                    if itemaction[i]==None: continue  #not that one.
                    ret_tuple[i] = self._one_ctop(itemaction[i],itemvalue[i]) if ctop else self._one_ptoc(itemaction[i],itemvalue[i])
            else:
                ret_tuple[0] = self._one_ctop(itemaction,itemvalue[0]) if ctop else self._one_ptoc(itemaction,itemvalue[0])
            break
        return tuple(ret_tuple) if len(ret_tuple)>1 else ret_tuple[0]




     
if __name__ == '__main__':
    from tests.nmdefines import PydbusNetworkManagerSpec,NM_DBUS_INTERFACE,NM_DBUS_INTERFACE_DEVICE
    from pydbus.bus import SystemBus
    from gi.repository import GLib
    
    def time_is_up(mainloop):
        mainloop.quit()
        return False
    
    def show_state_change(state):
        print("New Network Manager State:" + str(state))
    
    bus=SystemBus()
    nm=bus.get(NM_DBUS_INTERFACE)
    trans = PydbusCPythonTranslator(PydbusNetworkManagerSpec)
    #Test searching through a composite dbus class and a 1 to 1 map of strings to values 
    print(str(trans.translate(nm, "State", (10,), 3, True)))           
    print(str(trans.translate(nm, "State", ('ASleep',), 3, False)))
    #Test translating a single dbus class/path and a bitfield of flags 
    nm=bus.get(NM_DBUS_INTERFACE,'Devices/0')[NM_DBUS_INTERFACE_DEVICE]
    rv = trans.translate(nm,"Capabilities",(3,),3,True)
    print(str(rv))
    print(str(trans.translate(nm,"Capabilities",(rv,),3,False)))

    nm_oldway=bus.get( "org.freedesktop.NetworkManager",'Devices/0')["org.freedesktop.NetworkManager.Device"]
    print(str(nm_oldway.Capabilities) + ", "+str(nm_oldway.DeviceType))
    
    nm=bus.get(NM_DBUS_INTERFACE,'Devices/0',translation_spec=PydbusNetworkManagerSpec)

    print(str(nm.Capabilities) + ", "+str(nm.DeviceType))
    
    nm=bus.get(NM_DBUS_INTERFACE,translation_spec=PydbusNetworkManagerSpec)
    print(str(nm.Connectivity) + " , "+str(nm.CheckConnectivity()))
    print(nm.CheckpointCreate(None,10,'NONE'))
            
    loop = GLib.MainLoop()  
    GLib.timeout_add_seconds(15, time_is_up,loop)
    nm.StateChanged.connect(show_state_change)       
    loop.run()
    print("Done")

#Run results:
#ASLEEP
#10
#('NM_SUPPORTED', 'CARRIER_DETECT')
#3
#7, 14
#('NM_SUPPORTED', 'CARRIER_DETECT', 'IS_SOFTWARE'), GENERIC
#FULL , FULL
#/org/freedesktop/NetworkManager/Checkpoint/1
#New Network Manager State:CONNECTED_LOCAL
#New Network Manager State:CONNECTING
#New Network Manager State:CONNECTED_LOCAL
#New Network Manager State:CONNECTED_GLOBAL
#Done

