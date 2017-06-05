'''
Created on Feb 1, 2017

@author: administrator
'''

import ipaddress

#import pydbus
from pydbus.translations.org_freedesktop_NetworkManager import PydbusNetworkManagerSpec, NM_DBUS_INTERFACE, NM_DBUS_PATH_SETTINGS
from pydbus import SystemBus


SysDbus=SystemBus()

def nm_get(path):
    return SysDbus.get(NM_DBUS_INTERFACE,path,translation_spec=PydbusNetworkManagerSpec)

def nm_get_indirect(path):
    '''When the path returns a string which is a path'''
    if isinstance(path,str): return nm_get(path)
    return [nm_get(x) for x in path]

if __name__ == '__main__':
    """
    Display information about everything network-related that network-manager can
    say something about.
    To get the necessary pre-reqs:  yum install python3X(4,6..)-dbus; yum install dbus-python;pip install python-networkmanager
    ln -s /var/run <your anacondadirectory>/var/run
    """
    NetworkManager=nm_get(None)
    
    print("%-30s %s" % ("Version:", NetworkManager.Version))
    print("%-30s %s" % ("Networking enabled:", NetworkManager.NetworkingEnabled))
    print("%-30s %s" % ("Wireless enabled:", NetworkManager.WirelessEnabled))
    print("%-30s %s" % ("Wireless hw enabled:", NetworkManager.WirelessHardwareEnabled))
    print("%-30s %s" % ("Wwan enabled:", NetworkManager.WwanEnabled))
    print("%-30s %s" % ("Wwan hw enabled:", NetworkManager.WwanHardwareEnabled))
    print("%-30s %s" % ("Wimax enabled:", NetworkManager.WimaxEnabled))
    print("%-30s %s" % ("Wimax hw enabled:", NetworkManager.WimaxHardwareEnabled))
    print("%-30s %s" % ("Overall state:", NetworkManager.State))

    Settings = nm_get(NM_DBUS_PATH_SETTINGS)
    print("%-30s %s" % ("Can modify:", Settings.CanModify))
    print("%-30s %s" % ("Hostname:", Settings.Hostname))
    
    print("")
    
    print("Permissions")
    for perm, val in sorted(NetworkManager.GetPermissions().items()):
        print("%-30s %s" % (perm[31:] + ':', val))
    
    print("")
    
    print("Available network devices")
    print("%-10s %-19s %-20s %s" % ("Name", "State", "Driver", "Managed?"))
    for dev in nm_get_indirect(NetworkManager.GetDevices()):
        print("%-10s %-19s %-20s %s" % (dev.Interface, dev.State, dev.Driver, dev.Managed))
    
    print("")
    
    print("Available connections")
    print("%-30s %s" % ("Name", "Type"))
    for conn in nm_get_indirect(Settings.ListConnections()):
        settings = conn.GetSettings()['connection']
        print("%-30s %s" % (settings['id'], settings['type']))
    
    print("")
    
    print("Active connections")
    print("%-30s %-20s %-10s %s" % ("Name", "Type", "Default", "Devices"))
    for active_conn in nm_get_indirect(NetworkManager.ActiveConnections):
        s= [nm_get(dev_str).Interface for dev_str in active_conn.Devices]
        print("%-30s %-20s %-10s %s" % (active_conn.Id, active_conn.Type, active_conn.Default, ", ".join(s)))
    
    for active_conn in nm_get_indirect(NetworkManager.ActiveConnections):
        conn = nm_get(active_conn.Connection)
        settings=conn.GetSettings()
        s=repr(settings)
        print(s.replace(',',',\n'))
    
        for s in list(settings.keys()):
            if 'data' in settings[s]:
                settings[s + '-data'] = settings[s].pop('data')
                
                
        has_secrets = ['802-1x', '802-11-wireless-security', 'cdma', 'gsm', 'pppoe', 'vpn']
        secrets={}
        for key in has_secrets:
            if key in settings:
                secrets=conn.GetSecrets(key)
                break
            
        for key in secrets:
            settings[key].Update(secrets[key])
    
        devices = ""
        if active_conn.Devices:
            devices = " (on %s)" % ", ".join([nm_get(x).Interface for x in active_conn.Devices])
        print("Active connection: %s%s" % (settings['connection']['id'], devices))
        size = max(
                [
                    max(
                            [   
                                len(y) for y in x.keys()
                            ] + [0]
                        ) for x in settings.values()
                ]
            )
        sformat = "      %%-%ds %%s" % (size + 5) 
        for key, val in sorted(settings.items()):
            print("   %s" % key)
            for name, value in val.items():
                print(sformat % (name, value))
        for dev in nm_get_indirect(active_conn.Devices):
            print("Device: %s" % dev.Interface)
            print("   Type             %s" % dev.DeviceType)
            if not callable(dev.HwAddress):
                print("   MAC address      %s" % dev.HwAddress)

            ip4c=nm_get(dev.Ip4Config)
            print("   IPv4 config")
            print("      Addresses")
            for addr in ip4c.AddressData:
                print("         %s/%d -> %s" % (addr['address'],addr['prefix'],ip4c.Gateway))
            print("      Routes")
            for route in ip4c.RouteData:
                print("         %s/%d -> %s (%d)" % tuple(route['dest'],route['prefix'],route['next-hop'],route['metric']))
            print("      Nameservers")
            for ns in ip4c.Nameservers:
                print("         %s" % ipaddress.IPv4Address(ns.to_bytes(4,byteorder='little')))

            ip6c=nm_get(dev.Ip6Config)
            print("   IPv6 config")
            print("      Addresses")
            for addr in ip6c.AddressData:
                print("         %s/%d -> %s" % (addr['address'],addr['prefix'],ip6c.Gateway))
            print("      Routes")
            for route in ip6c.RouteData:
                print("         %s/%d -> %s (%d)" % tuple(route['dest'],route['prefix'],route['next-hop'],route['metric']))
            print("      Nameservers")
            for ns in ip6c.Nameservers:
                print("         %s" % ipaddress.IPv6Address(ns.to_bytes(16,byteorder='little')))

                

