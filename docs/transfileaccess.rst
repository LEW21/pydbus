=============
Translation File Specfication
=============

Restating some of the 'getting started' document, but more formally, a typical pydbus startup pattern is:

`  from pydbus.bus import SystemBus`  
  `bus=SystemBus()  # or SessionBus() `  
  `xx=bus.get(...usual arguments...,translation_spec=<TranslationDictOptions>,method_return_format=<byname or argpos>,method_inarg_format=<byname or argpos>)`  
  
  Where \<TranslationDictOptions\> is one of:
  
* True: Look in pydbus' built in translations subdirectory for a module
whose name matches the dbus path with _ replacing . and from that
module, use the dictionary in it with the same name as the module.
e.g. org_freedesktop_NetworkManager

* 'module_name':  import the module 'module_name', use the
dictionary with name matching the dbus path with
_ replacing . So 'my_module' containing dictionary
org_freedesktop_NetworkManager = { ... }
              
* translation_dictionary: A dictionary object in the format described in the next section.

* 'method_return_format' and 'method_inarg_format' is one of:
   per_pydbus_spec_only
   dict_if_service_provides_argnames
   dict_if_service_provides_2_or_more_argnames  (default)
   
   These are essentially about whether and how to use the argument names provided directly by the service. 

   method_return_format controls whether method calls are returned as a dictionary of name:value pairs, or a single value, or a tuple.  method_inarg_format controls whether method calls are to expect a single value, a tuple, or dictionary of name:value pairs.
 
   per_pydbus_spec_only will ignore argument position names provided by the server using only what's in the translation spec. 

   dict_if_service_provides_argnames will expect/return a dictionary of name:value pairs if the service gives names for argument positions. Otherwise it will use what's in the translation dictionary.
  
   dict_if_service_provides_argnames will expect/return a dictionary of name:value pairs if the service gives names for argument positions. Otherwise it will use what's in the translation dictionary.

   dict_if_service_provides_2_or_more_argnames is as above, but will expect as the translation spec provides if there is but one argument.  It makes little sense to use argument names when there is only one either in or out. An argument name:value pair dictionary (of length 1) will still be used if there is a translation spec that provides for it.

