'''
Created on Mar 26, 2017

@author: Harry G. Coin
@copyright: 2017 Quiet Fountain LLC

File holding a pydbus translation dictionary
for use in pydus translation module unit testing
routines.

This is non standard in that this file holds several translation
dictionaries.  That is only enabled for unit testing to avoid
file clutter.

'''

pydbus_unittest_noentries =  {
    }


pydbus_unittest_basic = { 'testkey' : {'method_py_to_dbus' : 'argname'} }


def add_one(the_arg,the_arg_index,the_introspection_format,is_python_to_dbus):
    return (the_arg+1,the_arg_index,the_introspection_format,is_python_to_dbus)

def add_two(the_arg,the_arg_index,the_introspection_format,is_python_to_dbus):
    return the_arg+2

def add_them(the_arg,the_arg_index,the_introspection_format,is_python_to_dbus):
    #print(str(the_arg))
    return the_arg[0] + the_arg[1]

def count_words(the_arg,the_arg_index,the_introspection_format,is_python_to_dbus):
    #print(str(the_arg))
    return len(the_arg.split())

def count_words_from_both_args(the_arg,the_arg_index,the_introspection_format,is_python_to_dbus):
    #print(str(the_arg))
    return [len(the_arg[0].split()) + len(the_arg[1].split())]

# Here we test the one to one mapping of integers to strings
# For return arguments from methods, reading properties, and 
# getting signals.
pydbus_dbus_to_python = { 'testkey' :
                            { 'method_dbus_to_py' : 
                                { 0 : 
                                    {
                                    1 : 'value_should_be_one',
                                    2 : 'value should be two',
                                    100: 'value should be one hundred'
                                    },
                                  1  :
                                    {
                                    '_from_python_to_dbus' : True ,
                                    'value should be three' : 3 ,
                                    'Test Case Matching on 4' : 4 
                                    },
                                  2  :
                                    {
                                    '_from_python_to_dbus' : True ,
                                    '_replace_unknowns' : ('whatta number',-101),
                                    'value should be thirty' : 30 ,
                                    'Test Case Matching on 40' : 40 
                                    },
                                  3  :
                                    {
                                     "_forced_replacement":'forced replacement item'
                                    },
                                  5  : 
                                    {
                                      "_is_bitfield" : True,
                                      1 : 'bit 0 on',
                                      4 : 'bit 2 on',
                                      (1,0) : 'bit 1 off',
                                    },
                                  6  : 
                                    {
                                    '_from_python_to_dbus' : True ,
                                      "_is_bitfield" : True,
                                      '_show_all_names': True,
                                      'bit 0 on' : 1,
                                      'bit 2 on' : 4,
                                      'bit 1 off' : (1,0),
                                     }, #end of arg spec
                                } #end of arg list spec
                            }, #end of direction spec
                           # next key
                        'fromDbusNamedBitFormats' :
                            { 'signal_dbus_to_py' :
                                { 0 :
                                    {
                                    "_is_bitfield" : True,
                                    1 : 'bit 0 on',
                                    (2,0) : 'bit 2 off',
                                    2  : 'bit 2 on',
                                    "_arg_format" : 'list'
                                    },
                                  1 :
                                    {
                                    "_is_bitfield" : True,
                                    1 : 'bit 0 on',
                                    (2,0) : 'bit 2 off',
                                    2  : 'bit 2 on',
                                    0xf0 : '#zero_to_sixteen',
                                    0x30 : ( 'left two of nibble2 are zero','left two of nibble2 is one','left two of  nibble2 is 2'), #leaving 3 out on purpose.
                                    "_arg_format" : 'shortlist'
                                    },  #end of arg 1 spec
                                } # end of arg specs
                            }, # end of direction specs
                        'singletest':
                            { 'signal_dbus_to_py' :
                                {  0 :
                                    {
                                    "_is_bitfield" : True,
                                    1 : 'bit 0 on',
                                    (2,0) : 'bit 2 off',
                                    2  : 'bit 2 on',
                                    "_arg_format" : 'single'
                                    },  #end of arg 1 spec
                                } #end of arg specs
                             }, # end of direction specs
                        'prettydicttest':
                            { 'signal_dbus_to_py' :
                                {  0 :
                                    {
                                    "_is_bitfield" : True,
                                    (0x10,7) : '#the first three bits if not the fourth',
                                    0x10 : 'solo True, never seen',
                                    (0x10,0) : 'seek the number, Luke',
                                    "_arg_format" : 'prettydict'
                                    },  #end of arg 1 spec
                                } #end of arg specs
                             }, # end of direction specs
                        'prettylisttest':
                            { 'signal_dbus_to_py' :
                                {  0 :
                                    {
                                    "_is_bitfield" : True,
                                    (0x10,7) : '#the first three bits if not the fourth',
                                    0x10 : 'solo True, never seen',
                                    (0x10,0) : 'seek the number, Luke',
                                    "_arg_format" : 'prettylist'
                                    },  #end of arg 1 spec
                                } #end of arg specs
                             }, # end of direction specs
                         'simplematchfunction' :
                            { 'method_dbus_to_py' :
                                {  0 :
                                    {
                                    "_match_to_function" : True,
                                    "0:i" : add_one,
                                    ".*" : ('pydbus.translations.pydbus_unittest','add_two')
                                    },
                                }
                            },
                         'allargsin1matchfunction' :
                            { 'method_dbus_to_py' :
                                {  0 :
                                    {
                                    "_match_to_function" : True,
                                    "_all_arguments" : True,
                                    "0:i" : add_them, #In functions, the introspection has to match the function result.
                                    },
                                }
                            },
                         'd_to_p_named_args' :
                            { 'method_dbus_to_py': 
                                { 0: 
                                    { '_attributename': "arg0"},
                                 1: 
                                    { '_attributename': "arg1"},
                                 2: 
                                    { '_attributename': "arg2"},
                                }
                            },
                         'd_to_p_dict_args' :
                            { 'method_dbus_to_py': 
                                { 0: 
                                    { '_dictkey': "arg0"},
                                 1: 
                                    { '_dictkey': "arg1"},
                                 2: 
                                    { '_dictkey': "arg2"},
                                }
                            },
                         'd_to_p_dict_args2' :
                            { 'method_dbus_to_py': 
                                { 0: 
                                    { '_dictkey': "arg0"},
                                 1: 
                                    { '_dictkey': "arg1"},
                                 2: 
                                    { '_dictkey': "arg2",
                                      '_new_return_instance' : True},
                                }
                            },
                         'd_to_p_named_args3' :
                            { 'method_dbus_to_py': 
                                { 0: 
                                    { '_attributename': "arg0"},
                                 1: 
                                    { '_attributename': "arg1",'_new_return_instance' : True},
                                 2: 
                                    { '_attributename': "arg2"},
                                }
                            },
                         
                        } #end of key specs




pydbus_python_to_dbus = { 'testkey' :
                            { 'method_py_to_dbus' : 
                                { 0 : 
                                    {
                                    1 : 'value_should_be_one',
                                    2 : 'value should be two',
                                    100: 'value should be one hundred'
                                    },
                                  1  :
                                    {
                                    '_from_python_to_dbus' : True ,
                                    'value should be three' : 3 ,
                                    'Test Case Matching on 4' : 4 
                                    },
                                  2  :
                                    {
                                    '_from_python_to_dbus' : True ,
                                    '_replace_unknowns' : ('whatta number',-101),
                                    'value should be thirty' : 30 ,
                                    'Test Case Matching on 40' : 40 
                                    },
                                  3  :
                                    {
                                     "_forced_replacement":'forced replacement item'
                                    },
                                  5  : 
                                    {
                                      "_is_bitfield" : True,
                                      1 : 'bit 0 on',
                                      4 : 'bit 2 on',
                                      (1,0) : 'bit 1 off',
                                    },
                                  6  : 
                                    {
                                    '_from_python_to_dbus' : True ,
                                      "_is_bitfield" : True,
                                      '_show_all_names': True,
                                      'bit 0 on' : 1,
                                      'bit 2 on' : 4,
                                      'bit 1 off' : (1,0),
                                     }, #end of arg spec
                                } #end of arg list spec
                            }, #end of direction spec
                           # next key
                        'fromDbusNamedBitFormats' :
                            { 'method_py_to_dbus' :
                                { 0 :
                                    {
                                    "_is_bitfield" : True,
                                    1 : 'bit 0 on',
                                    (2,0) : 'bit 2 off',
                                    2  : 'bit 2 on',
                                    "_arg_format" : 'list'
                                    },
                                  1 :
                                    {
                                    "_is_bitfield" : True,
                                    1 : 'bit 0 on',
                                    (2,0) : 'bit 2 off',
                                    2  : 'bit 2 on',
                                    0xf00 : '#zero_to_sixteen',
                                    0x30 : ( 'left two of nibble2 are zero','left two of nibble2 is one','left two of  nibble2 is 2'), #leaving 3 out on purpose.
                                    "_arg_format" : 'shortlist'
                                    },  #end of arg 1 spec
                                } # end of arg specs
                            }, # end of direction specs
                        'singletest':
                            { 'method_py_to_dbus' :
                                {  0 :
                                    {
                                    "_is_bitfield" : True,
                                    1 : 'bit 0 on',
                                    (2,0) : 'bit 2 off',
                                    2  : 'bit 2 on',
                                    "_arg_format" : 'single'
                                    },  #end of arg 1 spec
                                } #end of arg specs
                             }, # end of direction specs
                        'prettydicttest':
                            { 'method_py_to_dbus' :
                                {  0 :
                                    {
                                    "_is_bitfield" : True,
                                    (0x10,7) : '#the first three bits if not the fourth',
                                    0x10 : 'solo True, seldom seen',
                                    (0x10,0) : 'seek the number, Luke',
                                    "_arg_format" : 'prettydict'
                                    },  #end of arg 1 spec
                                } #end of arg specs
                             }, # end of direction specs
                        'prettylisttest':
                            { 'method_py_to_dbus' :
                                {  0 :
                                    {
                                    "_is_bitfield" : True,
                                    (0x20,7) : '#the first three bits if not the fifth',
                                    0x10 : 'solo True, seldom seen',
                                    (0x10,0) : 'seek the number, Luke',
                                    "_arg_format" : 'prettylist'
                                    },  #end of arg 1 spec
                                } #end of arg specs
                             }, # end of direction specs
                         'simplematchfunction' :
                            { 'method_py_to_dbus' :
                                {  0 :
                                    {
                                    "_match_to_function" : True,
                                    "0:i" : count_words,
                                    ".*" : ('pydbus.translations.pydbus_unittest','add_two')
                                    },
                                }
                            },
                         'allargsin1matchfunction' :
                            { 'method_py_to_dbus' :
                                {  0 :
                                    {
                                    "_match_to_function" : True,
                                    "_all_arguments" : True,
                                    "0:i" : count_words_from_both_args,
                                    },
                                }
                            },
                         'pytodbusvariants' :  #test introspection will be ivvsv
                            { 'method_py_to_dbus' :
                                {  0 :
                                    {
                                    "_variant_expansion" : '(uu/(iii.ss)',
                                    "_container" : {
                                            0 : {
                                                    0 : 'label for 0',
                                                    1 : 'label for 1',
                                                }
                                        },
                                    },
                                   1 : 
                                   { "_variant_expansion" : 'as',
                                    #No translation for this field (which will be either a u or i
                                     #   "_default_guidance"
                                    },
                                }
                            },
                         'pytodbusvariants2' : 
                            { 'method_py_to_dbus' :
                                {  0 :
                                    {
                                    "_variant_expansion" : '(uu/(iii.ss)',
                                    "_container" : {
                                            0 : {
                                                    0 : 'label for 0',
                                                    1 : 'label for 1',
                                                }
                                        },
                                    },
                                   1 : 
                                   { "_variant_expansion" : 'ai',
                                        10 : 'label for 10',
                                        '_replace_unknowns' : ('whatta number',-101)
                                    },
                                   2 : 
                                   { "_variant_expansion" : '(iss)',
                                     "_container" : {
                                            0 : { 
                                                    10 : 'label for 10',
                                                    '_replace_unknowns' : ('whatta number',-101)
                                             }
                                        }
                                    },
                                }
                            },
                        'dictionary_test' : {
                            'method_py_to_dbus' : {  
                                0 : {
                                    "_container" : {
                                        0 :  {
                                            0 : 'label for 0',
                                            1 : 'label for 1',
                                        },
                                    },
                                },
                                1 : {
                                    "_container" : {
                                        0 :  {
                                            0 : 'label for 0',
                                            1 : 'label for 1', 
                                        },
                                        "_default_guidance" : {
                                            30 : 'label for 30',
                                            20 : 'label for 20',
                                            '_replace_unknowns' : ('whatta number',-101)
                                        },
                                    }
                                 },
                            },
                        },
                        'dictionary_keys' : {
                            'method_py_to_dbus' : {  
                                0 : {
                                    "_container_keys" : {
                                        "_default_guidance" :  {
                                            0 : 'label for 0',
                                            1 : 'label for 1',
                                        },
                                    }
                                },
                                1 : {
                                    "_container_keys" : {
                                        "_default_guidance" :  {
                                            0 : 'label for 0',
                                            1 : 'label for 1',
                                        },
                                    },
                                    "_container" : {
                                        "_default_guidance" :  {
                                            2 : 'is 2',
                                            1 : 'is 1', 
                                        },
                                    },
                                },
                            },
                        },
                        'named_arguments' : {
                            'method_py_to_dbus' : {  
                                0: { "_attributename" : 'arg0'},
                                1: { "_attributename" : 'arg1'},
                                2: { "_attributename" : 'arg2'},
                            }
                        },
                        'named_arguments2' : {
                            'method_py_to_dbus' : {  
                                0: { "_dictkey" : 'arg0'},
                                1: { "_dictkey" : 'arg1'},
                                2: { "_dictkey" : 'arg2'},
                            }
                        }
                         
                    }
                


