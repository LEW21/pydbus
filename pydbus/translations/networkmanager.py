'''
Created on Feb 23, 2017

@author: Harry G. Coin
@copyright: 2016, Quiet Fountain LLC


  *- Mode: C; tab-width: 4; indent-tabs-mode: t; c-basic-offset: 4 -*-
  * This program is free software; you can redistribute it and/or modify
  * it under the terms of the GNU General Public License as published by
  * the Free Software Foundation; either version 2 of the License, or
  * (at your option) any later version.
  *
  * This program is distributed in the hope that it will be useful,
  * but WITHOUT ANY WARRANTY; without even the implied warranty of
  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  * GNU General Public License for more details.
  *
  * You should have received a copy of the GNU General Public License along
  * with this program; if not, write to the Free Software Foundation, Inc.,
  * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
  *
  * Copyright 2017 Quiet Fountain LLC,
  * Produced to meet specifications set forth by The Gnome Project
  * at https://developer.gnome.org/libnm-util/stable/libnm-util-NetworkManager.html
  * and https://developer.gnome.org/NetworkManager/stable/spec.html
 
  * Definitions related to NetworkManager's D-Bus interfaces.
  *
  * See https://developer.gnome.org/NetworkManager/stable/spec.html
  * for details
'''

# General Interface and Path Definitions

NM_DBUS_SERVICE = "org.freedesktop.NetworkManager"

NM_DBUS_PATH = "/org/freedesktop/NetworkManager"

NM_DBUS_INTERFACE = "org.freedesktop.NetworkManager"
NM_DBUS_INTERFACE_DEVICE = NM_DBUS_INTERFACE + ".Device"
NM_DBUS_INTERFACE_DEVICE_WIRED = NM_DBUS_INTERFACE_DEVICE + ".Wired"
NM_DBUS_INTERFACE_DEVICE_ADSL = NM_DBUS_INTERFACE_DEVICE + ".Adsl"
NM_DBUS_INTERFACE_DEVICE_WIRELESS = NM_DBUS_INTERFACE_DEVICE + ".Wireless"
NM_DBUS_INTERFACE_DEVICE_BLUETOOTH = NM_DBUS_INTERFACE_DEVICE + ".Bluetooth"
NM_DBUS_INTERFACE_DEVICE_OLPC_MESH = NM_DBUS_INTERFACE_DEVICE + ".OlpcMesh"

NM_DBUS_INTERFACE_ACCESS_POINT = NM_DBUS_INTERFACE + ".AccessPoint"
NM_DBUS_PATH_ACCESS_POINT = NM_DBUS_PATH + "/AccessPoint"

NM_DBUS_INTERFACE_DEVICE_MODEM = NM_DBUS_INTERFACE_DEVICE + ".Modem"
NM_DBUS_INTERFACE_DEVICE_WIMAX = NM_DBUS_INTERFACE_DEVICE + ".WiMax"

NM_DBUS_INTERFACE_WIMAX_NSP = NM_DBUS_INTERFACE + ".WiMax.Nsp"
NM_DBUS_PATH_WIMAX_NSP = NM_DBUS_PATH + "/Nsp"

NM_DBUS_INTERFACE_ACTIVE_CONNECTION = NM_DBUS_INTERFACE + ".Connection.Active"
NM_DBUS_INTERFACE_IP4_CONFIG = NM_DBUS_INTERFACE + ".IP4Config"
NM_DBUS_INTERFACE_DHCP4_CONFIG = NM_DBUS_INTERFACE + ".DHCP4Config"
NM_DBUS_INTERFACE_IP6_CONFIG = NM_DBUS_INTERFACE + ".IP6Config"
NM_DBUS_INTERFACE_DHCP6_CONFIG = NM_DBUS_INTERFACE + ".DHCP6Config"
NM_DBUS_INTERFACE_DEVICE_INFINIBAND = NM_DBUS_INTERFACE_DEVICE + ".Infiniband"
NM_DBUS_INTERFACE_DEVICE_BOND = NM_DBUS_INTERFACE_DEVICE + ".Bond"
NM_DBUS_INTERFACE_DEVICE_TEAM = NM_DBUS_INTERFACE_DEVICE + ".Team"
NM_DBUS_INTERFACE_DEVICE_VLAN = NM_DBUS_INTERFACE_DEVICE + ".Vlan"
NM_DBUS_INTERFACE_DEVICE_BRIDGE = NM_DBUS_INTERFACE_DEVICE + ".Bridge"
NM_DBUS_INTERFACE_DEVICE_GENERIC = NM_DBUS_INTERFACE_DEVICE + ".Generic"
NM_DBUS_INTERFACE_DEVICE_VETH = NM_DBUS_INTERFACE_DEVICE + ".Veth"
NM_DBUS_INTERFACE_DEVICE_TUN = NM_DBUS_INTERFACE_DEVICE + ".Tun"
NM_DBUS_INTERFACE_DEVICE_MACSEC = NM_DBUS_INTERFACE_DEVICE + ".Macsec"
NM_DBUS_INTERFACE_DEVICE_MACVLAN = NM_DBUS_INTERFACE_DEVICE + ".Macvlan"
NM_DBUS_INTERFACE_DEVICE_VXLAN = NM_DBUS_INTERFACE_DEVICE + ".Vxlan"
NM_DBUS_INTERFACE_DEVICE_GRE = NM_DBUS_INTERFACE_DEVICE + ".Gre"
NM_DBUS_INTERFACE_DEVICE_IP_TUNNEL = NM_DBUS_INTERFACE_DEVICE + ".IPTunnel"
NM_DBUS_INTERFACE_DEVICE_STATISTICS = NM_DBUS_INTERFACE_DEVICE + ".Statistics"

NM_DBUS_INTERFACE_SETTINGS = NM_DBUS_INTERFACE +".Settings"
NM_DBUS_PATH_SETTINGS = NM_DBUS_PATH + "/Settings"

NM_DBUS_INTERFACE_SETTINGS_CONNECTION = NM_DBUS_INTERFACE_SETTINGS+".Connection"
NM_DBUS_PATH_SETTINGS_CONNECTION = NM_DBUS_PATH_SETTINGS + "/Connection"

NM_DBUS_INTERFACE_SETTINGS_CONNECTION_SECRETS = NM_DBUS_INTERFACE_SETTINGS_CONNECTION + ".Secrets"

NM_DBUS_INTERFACE_AGENT_MANAGER = NM_DBUS_INTERFACE + ".AgentManager"
NM_DBUS_PATH_AGENT_MANAGER = NM_DBUS_PATH + "/AgentManager"

NM_DBUS_INTERFACE_SECRET_AGENT = NM_DBUS_INTERFACE + ".SecretAgent"
NM_DBUS_PATH_SECRET_AGENT = NM_DBUS_PATH+"/SecretAgent"

NM_DBUS_INTERFACE_DNS_MANAGER = NM_DBUS_INTERFACE + ".DnsManager"
NM_DBUS_PATH_DNS_MANAGER = NM_DBUS_PATH + "/DnsManager"

NM_LLDP_ATTR_DESTINATION = "destination"
NM_LLDP_ATTR_CHASSIS_ID_TYPE = "chassis-id-type"
NM_LLDP_ATTR_CHASSIS_ID = "chassis-id"
NM_LLDP_ATTR_PORT_ID_TYPE = "port-id-type"
NM_LLDP_ATTR_PORT_ID = "port-id"
NM_LLDP_ATTR_PORT_DESCRIPTION = "port-description"
NM_LLDP_ATTR_SYSTEM_NAME = "system-name"
NM_LLDP_ATTR_SYSTEM_DESCRIPTION = "system-description"
NM_LLDP_ATTR_SYSTEM_CAPABILITIES = "system-capabilities"
NM_LLDP_ATTR_IEEE_802_1_PVID = "ieee-802-1-pvid"
NM_LLDP_ATTR_IEEE_802_1_PPVID = "ieee-802-1-ppvid"
NM_LLDP_ATTR_IEEE_802_1_PPVID_FLAGS = "ieee-802-1-ppvid-flags"
NM_LLDP_ATTR_IEEE_802_1_VID = "ieee-802-1-vid"
NM_LLDP_ATTR_IEEE_802_1_VLAN_NAME = "ieee-802-1-vlan-name"

NM_LLDP_DEST_NEAREST_BRIDGE = "nearest-bridge"
NM_LLDP_DEST_NEAREST_NON_TPMR_BRIDGE = "nearest-non-tpmr-bridge"
NM_LLDP_DEST_NEAREST_CUSTOMER_BRIDGE = "nearest-customer-bridge"

NM_DBUS_PATH_VPN = NM_DBUS_PATH + "/VPN/Manager"
NM_DBUS_INTERFACE_VPN = NM_DBUS_INTERFACE + "VPN.Manager"

NM_DBUS_PATH_VPN_CONNECTION = NM_DBUS_PATH+"/VPN/Connection"
NM_DBUS_INTERFACE_VPN_CONNECTION = NM_DBUS_INTERFACE + ".VPN.Connection"

NM_VPN_DBUS_PLUGIN_PATH = NM_DBUS_PATH+"/VPN/Plugin"
NM_VPN_DBUS_PLUGIN_INTERFACE = NM_DBUS_INTERFACE + ".VPN.Plugin"

# VPN Errors
NM_DBUS_NO_ACTIVE_VPN_CONNECTION = NM_DBUS_INTERFACE + ".VPNConnections.NoActiveVPNConnection"
NM_DBUS_NO_VPN_CONNECTIONS = NM_DBUS_INTERFACE + ".VPNConnections.NoVPNConnections"
NM_DBUS_INVALID_VPN_CONNECTION = NM_DBUS_INTERFACE + ".VPNConnections.InvalidVPNConnection"


#End of General Definitions

#Dictionaries follow translating from the C version like " typedef enum { myvar_alpha=0, myvar_bravo=1, myvar_charlie=2 } myvar "
#to the python version myvar = { 'alpha' : 0, 'bravo' : 1, 'charlie' : 2 }
#Note the string as capitalizated here will be what is returned to the python caller when the associated 
#value is returned by the dbus partner.  However, when passing arguments to the dbus caller, the strings
#are NOT case sensitive.  In the above example, 1 will return 'bravo', but if used to pass arguments
#to a dbus partner, 'BRAVO' 'Bravo' or 'bravo' will be translated to 1.
#Because of namespace collisions in C and related, it was necessary to prepend 'myvar_' to each element.
#As python has no such restriction, and since it's better for printing, I advise stripping the
#redunant prefix.  'myvar_alpha' in C becomes 'alpha' in the example above.  

#The example above is appropriate when each value returned by a dbus partner has but one meaning.
#It is common in C and related programming for reasons of efficiency to package a collection of
#boolean variables associated by a common theme into a single integer with each boolean value
#assigned a unique bit position (power of 2) in the integer. In such cases, it's also common
#to associate a 0 overall value, meaning 'all variables/flags 0', with its own name. This is done
#instead of creating several 'freestanding' boolean variables to preserve the common meaning
#associated among the variables.  In these cases, include in the dictionary _is_bitfield : True.
#For example: " typedef enum { myvar_all_quiet=0, myvar_is_running=1, myvar_has_audience=2, myvar_doors_open=4 } myvar #flags "
#as
#myvar = { 'all_quiet':0, 'is_running':1, 'has_audience':2, 'doors_open':4, '_is_bitfield':True }"
#Note the definitions below MUST completely describe the universe of legal values and associated meanings.
#for the managed variables.  Variables that are not amenable to this should not be included in the 
#translation specification.
#Values passed either in or out that do not have entries will generate an exception.
#It may be later versions will ease the above restriction.

#The most common case is for each single dictionary below to completely describe how to translate
#a property, as there is but one argument in and out and it has the same meaning each way.
#But in the case of methods, it may be the number of arguments input to a method has some that are translated
#and some that are not, for example as the second of four arguments when only one is translated
#create a definition like  myvar_method_in = (None,myvar,None,None). And in like fashion if a method
#returns a tuple, and say, the middle two of them are to be translated while, say the outer 2 are not,
#create myvar_method_out = (None,myvar,myothervar,None,None)
#These will be used in the next section. 
 
NMCapability = {
     "TEAM" : 1
} 
 
 
NMState = {
     "UNKNOWN" :   0,
     "ASLEEP" :   10,
     "DISCONNECTED" :   20,
     "DISCONNECTING" :   30,
     "CONNECTING" :   40,
     "CONNECTED_LOCAL" :   50,
     "CONNECTED_SITE" :   60,
     "CONNECTED_GLOBAL" :   70
}
 

NMConnectivityState = {
     "UNKNOWN" :   0,
     "NONE" :   1,
     "PORTAL" :   2,
     "LIMITED" :   3,
     "FULL" :   4,
}

 
NMDeviceType = {
     "UNKNOWN" :   0,
     "ETHERNET" :   1,
     "WIFI" :   2,
     "UNUSED1" :   3,
     "UNUSED2" :   4,
     "BT" :   5,  # Bluetooth
     "OLPC_MESH" :   6,
     "WIMAX" :   7,
     "MODEM" :   8,
     "INFINIBAND" :   9,
     "BOND" :   10,
     "VLAN" :   11,
     "ADSL" :   12,
     "BRIDGE" :   13,
     "GENERIC" :   14,
     "TEAM" :   15,
     "TUN" :   16,
     "IP_TUNNEL" :   17,
     "MACVLAN" :   18,
     "VXLAN" :   19,
     "VETH" :   20,
     "MACSEC" :   21,
} 
 
 
NMDeviceCapabilities = {  # Flags
     "NONE" :   0x00000000,
     "NM_SUPPORTED" :   0x00000001,
     "CARRIER_DETECT" :   0x00000002,
     "IS_SOFTWARE" :   0x00000004,
     "_is_bitfield" : True
} 
 
 
NMDeviceWifiCapabilities = {  # Flags
     "NONE" :   0x00000000,
     "CIPHER_WEP40" :   0x00000001,
     "CIPHER_WEP104" :   0x00000002,
     "CIPHER_TKIP" :   0x00000004,
     "CIPHER_CCMP" :   0x00000008,
     "WPA" :   0x00000010,
     "RSN" :   0x00000020,
     "AP" :   0x00000040,
     "ADHOC" :   0x00000080,
     "FREQ_VALID" :   0x00000100,
     "FREQ_2GHZ" :   0x00000200,
     "FREQ_5GHZ" :   0x00000400,
     "_is_bitfield" : True
}
 
 
NM80211ApFlags = {  # underscore_name=nm_802_11_ap_flags, flags
     "NONE" :   0x00000000,
     "PRIVACY" :   0x00000001,
     "_is_bitfield" : True
}
 
NM80211ApSecurityFlags = {  # underscore_name=nm_802_11_ap_security_flags, flags
     "NONE" :   0x00000000,
     "PAIR_WEP40" :   0x00000001,
     "PAIR_WEP104" :   0x00000002,
     "PAIR_TKIP" :   0x00000004,
     "PAIR_CCMP" :   0x00000008,
     "GROUP_WEP40" :   0x00000010,
     "GROUP_WEP104" :   0x00000020,
     "GROUP_TKIP" :   0x00000040,
     "GROUP_CCMP" :   0x00000080,
     "KEY_MGMT_PSK" :   0x00000100,
     "KEY_MGMT_802_1X" :   0x00000200,
     "_is_bitfield" : True
}
 
NM80211Mode = {  # underscore_name=nm_802_11_mode
     "UNKNOWN" :   0,
     "ADHOC" :   1,
     "INFRA" :   2,
     "AP" :   3,
} 
 
NMBluetoothCapabilities = {  # Flags
     "NONE" :   0x00000000,
     "DUN" :   0x00000001,
     "NAP" :   0x00000002,
     "_is_bitfield" : True
}


 
NMDeviceModemCapabilities = {  # Flags
     "NONE" :   0x00000000,
     "POTS" :   0x00000001,
     "CDMA_EVDO" :   0x00000002,
     "GSM_UMTS" :   0x00000004,
     "LTE" :   0x00000008,
     "_is_bitfield" : True
} 

 
NMWimaxNspNetworkType = {
     "UNKNOWN" :   0,
     "HOME" :   1,
     "PARTNER" :   2,
     "ROAMING_PARTNER" :   3,
} 
 
NMDeviceState = {
     "UNKNOWN" :   0,
     "UNMANAGED" :   10,
     "UNAVAILABLE" :   20,
     "DISCONNECTED" :   30,
     "PREPARE" :   40,
     "CONFIG" :   50,
     "NEED_AUTH" :   60,
     "IP_CONFIG" :   70,
     "IP_CHECK" :   80,
     "SECONDARIES" :   90,
     "ACTIVATED" :   100,
     "DEACTIVATING" :   110,
     "FAILED" :   120,
}
 
NMDeviceStateReason = {
     "NONE" :   0,
     "UNKNOWN" :   1,
     "NOW_MANAGED" :   2,
     "NOW_UNMANAGED" :   3,
     "CONFIG_FAILED" :   4,
     "IP_CONFIG_UNAVAILABLE" :   5,
     "IP_CONFIG_EXPIRED" :   6,
     "NO_SECRETS" :   7,
     "SUPPLICANT_DISCONNECT" :   8,
     "SUPPLICANT_CONFIG_FAILED" :   9,
     "SUPPLICANT_FAILED" :   10,
     "SUPPLICANT_TIMEOUT" :   11,
     "PPP_START_FAILED" :   12,
     "PPP_DISCONNECT" :   13,
     "PPP_FAILED" :   14,
     "DHCP_START_FAILED" :   15,
     "DHCP_ERROR" :   16,
     "DHCP_FAILED" :   17,
     "SHARED_START_FAILED" :   18,
     "SHARED_FAILED" :   19,
     "AUTOIP_START_FAILED" :   20,
     "AUTOIP_ERROR" :   21,
     "AUTOIP_FAILED" :   22,
     "MODEM_BUSY" :   23,
     "MODEM_NO_DIAL_TONE" :   24,
     "MODEM_NO_CARRIER" :   25,
     "MODEM_DIAL_TIMEOUT" :   26,
     "MODEM_DIAL_FAILED" :   27,
     "MODEM_INIT_FAILED" :   28,
     "GSM_APN_FAILED" :   29,
     "GSM_REGISTRATION_NOT_SEARCHING" :   30,
     "GSM_REGISTRATION_DENIED" :   31,
     "GSM_REGISTRATION_TIMEOUT" :   32,
     "GSM_REGISTRATION_FAILED" :   33,
     "GSM_PIN_CHECK_FAILED" :   34,
     "FIRMWARE_MISSING" :   35,
     "REMOVED" :   36,
     "SLEEPING" :   37,
     "CONNECTION_REMOVED" :   38,
     "USER_REQUESTED" :   39,
     "CARRIER" :   40,
     "CONNECTION_ASSUMED" :   41,
     "SUPPLICANT_AVAILABLE" :   42,
     "MODEM_NOT_FOUND" :   43,
     "BT_FAILED" :   44,
     "GSM_SIM_NOT_INSERTED" :   45,
     "GSM_SIM_PIN_REQUIRED" :   46,
     "GSM_SIM_PUK_REQUIRED" :   47,
     "GSM_SIM_WRONG" :   48,
     "INFINIBAND_MODE" :   49,
     "DEPENDENCY_FAILED" :   50,
     "BR2684_FAILED" :   51,
     "MODEM_MANAGER_UNAVAILABLE" :   52,
     "SSID_NOT_FOUND" :   53,
     "SECONDARY_CONNECTION_FAILED" :   54,
     "DCB_FCOE_FAILED" :   55,
     "TEAMD_CONTROL_FAILED" :   56,
     "MODEM_FAILED" :   57,
     "MODEM_AVAILABLE" :   58,
     "SIM_PIN_INCORRECT" :   59,
     "NEW_ACTIVATION" :   60,
     "PARENT_CHANGED" :   61,
     "PARENT_MANAGED_CHANGED" :   62,
}
NMDeviceStateChangedSignal = (NMDeviceState, NMDeviceState, NMDeviceStateReason)

 
# NM_AVAILABLE_IN_1_2
NMMetered = {
     "UNKNOWN" :   0,
     "YES" :   1,
     "NO" :   2,
     "GUESS_YES" :   3,
     "GUESS_NO" :   4,
}

 
NMActiveConnectionState = {
     "UNKNOWN" :   0,
     "ACTIVATING" :   1,
     "ACTIVATED" :   2,
     "DEACTIVATING" :   3,
     "DEACTIVATED" :   4,
}


 
NMSecretAgentGetSecretsFlags = {  # Flags
     "NONE" :   0x0,
     "ALLOW_INTERACTION" :   0x1,
     "REQUEST_NEW" :   0x2,
     "USER_REQUESTED" :   0x4,
 
     # Internal to NM; not part of the D-Bus API 
     "ONLY_SYSTEM" :   0x80000000,
     "NO_ERRORS" :   0x40000000,
     "_is_bitfield" : True
}
NMSecretAgentGetSecretsMethod = (None, None, None, None, NMSecretAgentGetSecretsFlags, None, None)

 
NMSecretAgentCapabilities = {  # < flags >
     "NONE" :   0x0,
     "VPN_HINTS" :   0x1,
 
     # boundary value 
     "LAST" :  0x1,  # NM_SECRET_AGENT_CAPABILITY_VPN_HINTS,
     "_is_bitfield" : True
}

NMAgentCapabilitiesMethod = (None, NMSecretAgentCapabilities)

 
 
 
NMIPTunnelMode = {
     "UNKNOWN" :   0,
     "IPIP" :   1,
     "GRE" :   2,
     "SIT" :   3,
     "ISATAP" :   4,
     "VTI" :   5,
     "IP6IP6" :   6,
     "IPIP6" :   7,
     "IP6GRE" :   8,
     "VTI6" :   9,
 } 
 
 
NMCheckpointCreateFlags = {  # skip
     "NONE" :   0,
     "DESTROY_ALL" :   0x01,
     "DELETE_NEW_CONNECTIONS" :   0x02,
     "DISCONNECT_NEW_DEVICES" :   0x04,
     "_is_bitfield" : True
}
NMCheckpointCreateMethod = (None, None, NMCheckpointCreateFlags, None)


 
NMRollbackResult = {  # skip
     "OK" :   0,
     "ERR_NO_DEVICE" :   1,
     "ERR_DEVICE_UNMANAGED" :   2,
     "ERR_FAILED" :   3,
} 
NMRollbackResultMethod = (None, NMRollbackResult)

 
 
 
 
NMVpnServiceState = {  # VPN daemon states
# Values
"UNKNOWN" : 0,  # The state of the VPN plugin is unknown.
"INIT" : 1,  # The VPN plugin is initialized.
"SHUTDOWN": 2,  # Not used.
"STARTING": 3,  # The plugin is attempting to connect to a VPN server.
"STARTED" : 4,  # The plugin has connected to a VPN server.
"STOPPING" : 5,  # The plugin is disconnecting from the VPN server.
"STOPPED" : 6  # The plugin has disconnected from the VPN server.
}
     

NMVpnConnectionState = {  # VPN connection states
# Values
"UNKNOWN" : 0,  # The state of the VPN connection is unknown.
"PREPARE" : 1,  # The VPN connection is preparing to connect.
"NEED_AUTH" : 2,  # The VPN connection needs authorization credentials.
"CONNECT" : 3,  # The VPN connection is being established.
"IP_CONFIG_GET" : 4,  # The VPN connection is getting an IP address.
"ACTIVATED" : 5,  # The VPN connection is active.
"FAILED" : 6,  # The VPN connection failed.
"DISCONNECTED" : 7,  # The VPN connection is disconnected.
}
     
NMVpnConnectionStateReason = {  # VPN connection state reasons
# Values
"UNKNOWN" : 0,  # The reason for the VPN connection state change is unknown.
"NONE" : 1,  # No reason was given for the VPN connection state change.
"USER_DISCONNECTED" : 2,  # The VPN connection changed state because the user disconnected it.
"DEVICE_DISCONNECTED" : 3,  # The VPN connection changed state because the device it was using was disconnected.
"SERVICE_STOPPED" : 4,  # The service providing the VPN connection was stopped.
"IP_CONFIG_INVALID" : 5,  # The IP config of the VPN connection was invalid.
"CONNECT_TIMEOUT" : 6,  # The connection attempt to the VPN service timed out.
"SERVICE_START_TIMEOUT" : 7,  # A timeout occurred while starting the service providing the VPN connection.
"SERVICE_START_FAILED" : 8,  # Starting the service starting the service providing the VPN connection failed.
"NO_SECRETS" : 9,  # Necessary secrets for the VPN connection were not provided.
"LOGIN_FAILED" : 10,  # Authentication to the VPN server failed.
"REMOVED" : 11,  # The connection was deleted from settings.
}
NMVpnStateChangedSignal = (NMVpnConnectionState, NMVpnConnectionStateReason)
    

NMVpnPluginFailure = {  # VPN plugin failure reasons
# Values
"LOGIN_FAILED" : 0,  # Login failed.
"CONNECT_FAILED" : 1,  # Connect failed.
"BAD_IP_CONFIG" : 2,  # Invalid IP configuration returned from the VPN plugin.
}

NMReload = {  # Network Manager Reload methods
            "Everything":0,
            "NetworkManager.conf":1,
            "UpdateDNS":2,
            "RestartDNS":4,
            "_is_bitfield":True
            }


#End of the individual translation element definitions.

#In this last section, we create the overall translation variable which
#will be passed in to the tranlastion routines when translation services
#are desired. The general format is:
#TranslationSpecificationName = {
#  "for.example.org.freedesktop.path.to.your.interface" :
#     {
#       "Method or Signal or Property Name" :  #If the same name is given for 2+ uses, only put in one entry.
#          (AboveDictOrTupleToInterpretArgumentsToMethods,ReturnedByMethods,IssuedBySignals,UsedForAProperty),
#          ...
#     },
#   ...
# }
# If a name is not used for the purpose named in each tuple position, use None and the
# values will be passed through unchanged should that name be used for the associated purpose.

# Last, to use a translation specification, for example, do:
# from pydbus import SystemBus
# bus = SystemBus()
# my_composite_interface = bus.get( ... usual arguments ..., translation_spec=TranslationSpecificationName)
 
# Note the above will result in a composite interface, each individual interface in the composite
# will be matched against the translation table when processing, processing will match against
# all the specifications in order, and will stop at the first match of a method/signal/property.
# if you have the situation of method/signal/property name collisions among classes and wish a later
# class spec translation in the composite to apply for a given name, generate an interface as follows:
# my_single_interface = 
# bus.get( ... usual arguments ..., translation_spec=TranslationSpecificationName)['the single interface I want']


# Full Translation Specification for the Network Manager:

PydbusNetworkManagerSpec = {
    NM_DBUS_SERVICE: 
        {
        "Reload" : (NMReload, None, None, None),
        "CheckConnectivity" : (None, NMConnectivityState, None, None),
        "State" : (None, NMState, None, NMState),
        "CheckpointCreate" : (NMCheckpointCreateMethod, None, None, None),
        "CheckpointRollback " : (None, NMRollbackResultMethod, None, None),
        "StateChanged" : (None, None, NMState, None),
        "Metered" : (None, None, None, NMMetered),
        "Capabilities" : (None, None, None, NMCapability),
        "Connectivity" : (None, None, None, NMConnectivityState)
        },
   NM_DBUS_INTERFACE_DEVICE:
        {
        "StateChanged" : (None, None, NMDeviceStateChangedSignal, None),
        "Capabilities" : (None, None, None, NMDeviceCapabilities),
        "State" : (None, None, None, NMDeviceState),
        "StateReason" : (None, None, None, (NMDeviceState, NMDeviceStateReason)),
        "DeviceType" : (None, None, None, NMDeviceType),
        "Metered": (None, None, None, NMMetered),
        },
   NM_DBUS_INTERFACE_ACCESS_POINT:
        {
        "Flags" : (None, None, None, NM80211ApFlags),
        "WpaFlags" : (None, None, None, NM80211ApSecurityFlags),
        "RsnFlags" : (None, None, None, NM80211ApSecurityFlags),
        "Mode" : (None, None, None, NM80211Mode)
        },
   NM_DBUS_INTERFACE_VPN_CONNECTION:
        {
        "VpnStateChanged" : (None, None, NMVpnStateChangedSignal, None),
        "VpnState" : (None, None, None, NMVpnConnectionState),
        },
   NM_VPN_DBUS_PLUGIN_INTERFACE:
        {
        "StateChanged":(None, None, NMVpnServiceState, None),
        "Failure":(None, None, NMVpnPluginFailure, None),
        "State":(None, None, None, NMVpnServiceState)
        },
   NM_DBUS_INTERFACE_ACTIVE_CONNECTION:
        {
        "State" : (None, None, None, NMActiveConnectionState)    
        },
   NM_DBUS_INTERFACE_DEVICE_BLUETOOTH:
        {
        "BtCapabilities" : (None, None, None, NMBluetoothCapabilities)
        },
   NM_DBUS_INTERFACE_DEVICE_MODEM:
        {
        "ModemCapabilities" : (None, None, None, NMDeviceModemCapabilities),
        "CurrentCapabilities" : (None, None, None, NMDeviceModemCapabilities)
        },
   NM_DBUS_INTERFACE_DEVICE_WIRELESS:
        {
        "Mode" : (None, None, None, NM80211Mode),
        "WirelessCapabilities" : (None, None, None, NMDeviceWifiCapabilities)
        },
   NM_VPN_DBUS_PLUGIN_INTERFACE:
        {
        "State" : (None, None, None, NMVpnServiceState),
        "SetFailure" : (None, None, None, NMVpnConnectionStateReason),
        "Failure" : (None, None, None, NMVpnConnectionStateReason)
        },
   NM_DBUS_INTERFACE_WIMAX_NSP:
        {
        "network-type": (None, None, None, NMWimaxNspNetworkType)
        },
   NM_DBUS_INTERFACE_SECRET_AGENT:
        {
        "GetSecrets" : (NMSecretAgentGetSecretsMethod, None, None, None)
        },
   NM_DBUS_INTERFACE_AGENT_MANAGER:
        {
        "RegisterWithCapabilities" : (NMAgentCapabilitiesMethod, None, None, None)
        },
   NM_DBUS_INTERFACE_DEVICE_IP_TUNNEL:
        {
        "Mode":(None, None, None, NMIPTunnelMode)
        }
    }

#Then, using the above example, for instance:
#    from tests.nmdefines import PydbusNetworkManagerSpec,NM_DBUS_INTERFACE,NM_DBUS_INTERFACE_DEVICE
#    from pydbus.bus import SystemBus
#    bus=SystemBus()    nm=bus.get(NM_DBUS_INTERFACE,'Devices/0',translation_spec=PydbusNetworkManagerSpec)
#
#    print(str(nm.Capabilities) + ", "+str(nm.DeviceType))
#    
#    nm=bus.get(NM_DBUS_INTERFACE,translation_spec=PydbusNetworkManagerSpec)
#    print(str(nm.Connectivity) + " , "+str(nm.CheckConnectivity()))
#    print(nm.CheckpointCreate(None,10,'NONE'))
# when run returns, on one particular system:
#
#('NM_SUPPORTED', 'CARRIER_DETECT', 'IS_SOFTWARE'), GENERIC
#FULL , FULL
#/org/freedesktop/NetworkManager/Checkpoint/6
