'''
Created on Mar 25, 2017

@author: Harry G. Coin
@copyright: 2017 Quiet Fountain LLC
'''

#import pydbus
from gi.repository.GLib import (Variant)  # ,VariantBuilder,VariantType)

#from pydbus.translator import (PydbusCPythonTranslator)

import unittest



class BlankObject(object):
    pass

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_isolate_format(self):
        # Test everything other than variants
        #print(str(dir( translator)))
        from pydbus.translator import _isolate_format
        next_arg, remainder = _isolate_format("should do nothing")
        self.assertTrue(next_arg == "s")
        self.assertTrue(remainder == 'hould do nothing')

        next_arg, remainder = _isolate_format("a{sa{si}}ua{si}")
        self.assertTrue(next_arg == 'a{sa{si}}')
        self.assertTrue(remainder == 'ua{si}')

        next_arg, remainder = _isolate_format(remainder)
        self.assertTrue(next_arg == 'u')
        self.assertTrue(remainder == 'a{si}')
        
        next_arg, remainder = _isolate_format(remainder)
        self.assertTrue(next_arg == 'a{si}')
        self.assertTrue(remainder == None)

        next_arg, remainder = _isolate_format(remainder)
        self.assertTrue(next_arg == None)
        self.assertTrue(remainder == None)
        
        next_arg, remainder = _isolate_format('u(s)')
        self.assertTrue(next_arg == 'u')
        self.assertTrue(remainder == '(s)')

        next_arg, remainder = _isolate_format(remainder)
        self.assertTrue(next_arg == '(s)')
        self.assertTrue(remainder == None)

        next_arg, remainder = _isolate_format('s{su}')
        self.assertTrue(next_arg == 's')
        self.assertTrue(remainder == '{su}')

        next_arg, remainder = _isolate_format(remainder)
        self.assertTrue(next_arg == '{su}')
        self.assertTrue(remainder == None)

        next_arg, remainder = _isolate_format(remainder)
        self.assertTrue(next_arg == None)
        self.assertTrue(remainder == None)
        
        # Test variants
        next_arg, remainder = _isolate_format('sv::u')
        self.assertTrue(next_arg == 's')
        self.assertTrue(remainder == 'v::u')

        next_arg, remainder = _isolate_format(remainder)
        self.assertTrue(next_arg == 'v::')
        self.assertTrue(remainder == 'u')
        
        next_arg, remainder = _isolate_format('sv:a{s}:u')
        self.assertTrue(next_arg == 's')
        self.assertTrue(remainder == 'v:a{s}:u')

        next_arg, remainder = _isolate_format(remainder)
        self.assertTrue(next_arg == 'v:a{s}:')
        self.assertTrue(remainder == 'u')
        
    def test_module_loading_variations(self):
        from pydbus.translator import PydbusCPythonTranslator
        self.assertRaises(ImportError, PydbusCPythonTranslator, 'bad module', 'pydbus.unittest')
#        self.assertRaises(ModuleNotFoundError,PydbusCPythonTranslator,'bad module','pydbus.unittest')
        self.assertRaises(ValueError, PydbusCPythonTranslator, 'pydbus.translations.pydbus_unittest', 'pydbus.unittest.badbus')
        self.assertRaises(ValueError, PydbusCPythonTranslator, 'pydbus.translations.pydbus_unittest', 'pydbus.unittest.noentries')
        self.assertRaises(ValueError, PydbusCPythonTranslator, True, 'pydbus.unittest.nothere')
        self.assertRaises(ValueError, PydbusCPythonTranslator, {}, 'pydbus.unittest.noentries')
        # Pass a valid but basic dictionary directly.  Should have no error.
        PydbusCPythonTranslator({ 'some_key' : {'method_py_to_dbus' : 'argname'}}, 'pydbus.unittest.noentries')
        # pass a valid but basic dictionary with dict name dervied from a module name. Should have no error
        PydbusCPythonTranslator(True, 'pydbus.unittest', unit_test_dictname='pydbus_unittest_basic')
        
        # self.trans = PydbusCPythonTranslator(True,'pydbus.unittest.noentries')
        # self.trans = PydbusCPythonTranslator('pydbus.unittest','pydbus.unittest.wontfindit')
        
    def test_bitfield_entry(self):
        # c = PydbusCPythonTranslator(True,'pydbus.unittest',unit_test_dictname='pydbus_unittest_basic')
        from pydbus.translator import SingleArgumentOptimizedGuidance
        c = SingleArgumentOptimizedGuidance({ '_is_bitfield' : True,
                                                     0 : 'all bits zero',  # should be forced to (-1,0)
                                                    '#everything_else' : True
                                                    },
                                                    0, True)
        b = c._bitfield_entry(0xf00, 0x0f0, 'fieldname', True)
        self.assertEqual(b.int_value(0), 0)
        self.assertEqual(b.int_value(1), 0)
        self.assertEqual(b.int_value(0xff01), 0)  # if offbits are on, it's zero no matter what else
        self.assertEqual(b.int_value(0x1), 0)  # properly ignore bits not in onbits.
        self.assertEqual(b.int_value(0x10), 1)  # validate first possible onbit results in 1
        self.assertEqual(b.int_value(0xf0), 15)  # validate highest onbit result in onbits with first 1 shifted to 0
        self.assertEqual(b.int_value(0xf0f0), 15)  # if offbits are on, it's zero no matter what else
        
        b = c._bitfield_entry(0xf00, 0x0f4, 'fieldname', True)
        # now we test non-consecutive onbits.
        self.assertEqual(b.int_value(0x4), 1)  # validate first possible onbit results in 1
        self.assertEqual(b.int_value(0xf0), 30)  # validate highest onbit result in onbits with first 1 shifted to 0
        self.assertEqual(b.int_value(0xf4), 31)  # if offbits are on, it's zero no matter what else
        
        b = c._bitfield_entry(0xf00, 0x0f4, 'fieldname', True, 0)
        self.assertEqual(b.onbits, 0)
        self.assertEqual(b.offbits, 0xff4)
        self.assertTrue(b.mask_test(0))
        self.assertFalse(b.mask_test(0x100))
        
        b = c._bitfield_entry(0xf00, 0x0f4, 'fieldname', True, 1)
        self.assertEqual(b.onbits, 4)
        self.assertEqual(b.offbits, 0xff0)
        self.assertTrue(b.mask_test(4))
        
        b = c._bitfield_entry(0xf00, 0x0f4, 'fieldname', True, 2)
        self.assertEqual(b.onbits, 0x10)
        self.assertEqual(b.offbits, 0xfe4)
        self.assertTrue(b.mask_test(0x10))
        
        
        b = c._bitfield_entry(0xf00, 0x0f4, 'fieldname', True, 3)
        self.assertEqual(b.onbits, 0x14)
        self.assertEqual(b.offbits, 0xfe0)
        self.assertTrue(b.mask_test(0x14))
        
        b = c._bitfield_entry(0xf00, 0x0f4, 'fieldname', True, 31)
        self.assertEqual(b.onbits, 0xf4)
        self.assertEqual(b.offbits, 0xf00)
        self.assertTrue(b.mask_test(0xf4))
        self.assertFalse(b.mask_test(2))
        self.assertFalse(b.mask_test(0x1f4))
        self.assertTrue(b.bits_tested(), 0xff4)

        self.assertRaises(ValueError, c._bitfield_entry, 0xf00, 0x0f4, 'fieldname', True, 32)
        
    def test_init_helper_guidance_validate_bitfield(self):
        # c = PydbusCPythonTranslator(True,'pydbus.unittest',unit_test_dictname='pydbus_unittest_basic')
        # check out bitfield specs from python, to dbus
        # First, simplest case: onbits -> label
        from pydbus.translator import SingleArgumentOptimizedGuidance
        guidance = SingleArgumentOptimizedGuidance({ '_is_bitfield' : True,
                                                     (-1, 0) : "All bits zero",
# NOTICE: 'All bits zero' is NOT the same thing as
# (1,0) which requires the 1 bit to be off no matter the other on bits.                                                      
                                                     0x6 : 'what 6 means',
                                                     (0x60, 1) : '60 off- 1 on',
                                                    '#everything_else' : True
                                                    },
                                                    0, True)
        self.assertFalse(guidance.all_arguments)
        self.assertEqual(guidance.arg_format, 'dict')
        self.assertEqual(guidance.arg_position_index, 0)
        self.assertFalse(guidance.attributename)
        self.assertFalse(guidance.container)
        self.assertFalse(guidance.container_keys)
        self.assertFalse(guidance.dictkey)
        # Note: the _specification direction_ is dbus to python,
        self.assertFalse(guidance.from_python_to_dbus)
        # the simulated guidance position is the other way.
        self.assertTrue(guidance.direction_is_from_python_to_dbus)
        self.assertFalse(guidance.forced_replacement)
        self.assertFalse(guidance.force_replacement_specified)
        self.assertTrue(guidance.is_bitfield)
        self.assertFalse(guidance.is_one_to_one_map)
        self.assertTrue(guidance.wants_everything_else)
        self.assertFalse(guidance.match_to_function)
        self.assertFalse(guidance.return_as_list)
        self.assertFalse(guidance.show_all_names)
        self.assertFalse(guidance.variant_expansion)
        self.assertTrue(guidance.wants_everything_else)
        o = guidance.original_spec
        self.assertTrue(((-1, 0), 'All bits zero') in o)
        self.assertTrue((6, 'what 6 means') in o)
        self.assertTrue(((0x60, 1), '60 off- 1 on') in o)
        self.assertTrue(('#everything_else', True) in o)
        
        self.assertTrue('ALL BITS ZERO' in guidance.map)
        g = guidance.map['ALL BITS ZERO']
        self.assertTrue(g.is_zero_test)
        self.assertEqual(g.label, 'ALL BITS ZERO')
        self.assertEqual(g.offbits, -1)
        self.assertEqual(g.onbits, 0)
        self.assertFalse(g.treat_as_int)
        
        self.assertTrue('WHAT 6 MEANS' in guidance.map)
        g = guidance.map['WHAT 6 MEANS']
        self.assertFalse(g.is_zero_test)
        self.assertEqual(g.label, 'WHAT 6 MEANS')
        self.assertEqual(g.offbits, None)
        self.assertEqual(g.onbits, 6)
        self.assertFalse(g.treat_as_int)
        
        self.assertTrue('60 OFF- 1 ON' in guidance.map)
        g = guidance.map['60 OFF- 1 ON']
        self.assertFalse(g.is_zero_test)
        self.assertEqual(g.label, '60 OFF- 1 ON')
        self.assertEqual(g.offbits, 0x60)
        self.assertEqual(g.onbits, 1)
        self.assertFalse(g.treat_as_int)

        # Next, check for the correct 'mini int' both as a value and
        # converted to bitmasks associated with labels.
        guidance = SingleArgumentOptimizedGuidance({ '_is_bitfield' : True,
                                                     (0xf00, 0x22) : ('zero', '1->2', '2->20', '3->22'),
                                                     (0xf000, 0x200) : '#MiniIntZeroOrOne',
                                                    },
                                                    1, True)
        self.assertFalse(guidance.wants_everything_else)
        self.assertEqual(guidance.arg_position_index, 1)

        self.assertTrue('MiniIntZeroOrOne'.upper() in guidance.map)
        g = guidance.map['MiniIntZeroOrOne'.upper()]
        self.assertTrue(g.treat_as_int)

        self.assertTrue('ZERO' in guidance.map)
        g = guidance.map['ZERO']
        self.assertFalse(g.treat_as_int)
        self.assertEqual(g.onbits, 0)
        self.assertEqual(g.offbits, 0xf22)

        g = guidance.map['1->2']
        self.assertFalse(g.treat_as_int)
        self.assertEqual(g.onbits, 2)
        self.assertEqual(g.offbits, 0xf20)

        g = guidance.map['2->20']
        self.assertFalse(g.treat_as_int)
        self.assertEqual(g.onbits, 0x20)
        self.assertEqual(g.offbits, 0xf02)
        
        g = guidance.map['3->22']
        self.assertFalse(g.treat_as_int)
        self.assertEqual(g.onbits, 0x22)
        self.assertEqual(g.offbits, 0xf00)
        
        
    def test_init_helper_guidance_validate_name_value_map(self):
        # c = PydbusCPythonTranslator(True,'pydbus.unittest',unit_test_dictname='pydbus_unittest_basic')
        from pydbus.translator import SingleArgumentOptimizedGuidance 
        guidance = SingleArgumentOptimizedGuidance({ 0 : "what0means",
                                                    10 : "what10means",
                                                    '_replace_unknowns' : ("string value", 10)
                                                    },
                                                    0, True)
        self.assertFalse(guidance.is_bitfield)
        self.assertTrue(guidance.is_one_to_one_map)
        self.assertTrue(guidance.replace_unknowns)
        self.assertTrue("WHAT0MEANS" in guidance.map)
        g = guidance.map["WHAT0MEANS"]
        self.assertEqual(g, 0)
        self.assertTrue("WHAT10MEANS" in guidance.map)
        g = guidance.map["WHAT10MEANS"]
        self.assertEqual(g, 10)
        self.assertEqual(guidance.replace_unknowns, ("string value", 10))
        
        
    def test_dbus_to_python_translations(self):
        from pydbus.translator import PydbusCPythonTranslator
        c = PydbusCPythonTranslator(True, 'pydbus.unittest', unit_test_dictname='pydbus_dbus_to_python')

        argspec = c.translate('who.knows.what', 'testkey', (1, 4, 100, 'never see it', 'no changes'), 0, True, 'uui', None, None)
        self.assertEqual(argspec[0], 1)
        self.assertEqual(argspec[1], 4)
        argspec = c.translate('pydbus.unittest', 'leave_me_alone', (1, 4, 100, 100000), 0, True, 'uui', None, None)
        self.assertEqual(argspec[0], 1)
        self.assertEqual(argspec[1], 4)
        self.assertRaises(ValueError, c.translate, 'pydbus.unittest', 'testkey', (1, 4, 100, (1, 2, 3, "won't see me"), 'no changes', 4, 4), 0, True, 'uiussi', None, None)
        argspec = c.translate('pydbus.unittest', 'testkey', (1, 4, 100, (1, 2, 3, "won't see me"), 'no changes', 4, 4), 0, True, 'uiussii', None, None)
        self.assertEqual(argspec[0], 'value_should_be_one')
        self.assertEqual(argspec[1], 'Test Case Matching on 4')
        self.assertEqual(argspec[2], 'whatta number')
        self.assertEqual(argspec[3], 'forced replacement item')
        self.assertEqual(argspec[4], 'no changes')
        self.assertTrue('bit 1 off' in argspec[5])
        self.assertTrue('bit 2 on' in argspec[5])
        self.assertTrue('bit 0 on' not in argspec[5])
        self.assertTrue(argspec[6]['bit 1 off'])
        self.assertTrue(argspec[6]['bit 2 on'])
        self.assertFalse(argspec[6]['bit 0 on'])
        
        argspec = c.translate('pydbus.unittest', 'fromDbusNamedBitFormats', (1, 0x14, 100, 'never see it', 'no changes'), 1, True, 'uuiss', None, None)
        self.assertTrue(isinstance(argspec[0], list))
        self.assertTrue(['bit 0 on', True] in argspec[0])
        self.assertTrue(['bit 2 off', True] in argspec[0])
        self.assertTrue(len(argspec[0]) == 2)

        self.assertTrue(isinstance(argspec[1], list))
        self.assertTrue('bit 2 off' in argspec[1])
        self.assertTrue(['zero_to_sixteen', 1] in argspec[1])
        self.assertTrue('left two of nibble2 is one' in argspec[1])
        self.assertTrue(len(argspec[1]) == 3)
        
        self.assertRaises(ValueError, c.translate, 'pydbus.unittest', 'singletest', (1,), 1, True, 'uui', None, None)
        argspec = c.translate('pydbus.unittest', 'singletest', (0,), 1, True, 'b', None, None)
        self.assertTrue(argspec, 'bit 2 off')
        
        argspec = c.translate('pydbus.unittest', 'prettydicttest', (5,), 1, True, 'i', None, None)
        # print(str(argspec))
        self.assertTrue(isinstance(argspec, dict))
        self.assertEqual(argspec['the first three bits if not the fourth'], 5)
        self.assertTrue(argspec['seek the number, Luke'])
        self.assertTrue(len(argspec) == 2)
        
        argspec = c.translate('pydbus.unittest', 'prettydicttest', (0x10,), 1, True, 'u', None, None)
        # print(str(argspec))
        self.assertTrue(argspec == True)
        
        argspec = c.translate('pydbus.unittest', 'prettylisttest', (3,), 1, True, 'u', None, None)
        # print(str(argspec))
        self.assertTrue(isinstance(argspec, list))
        self.assertTrue(['the first three bits if not the fourth', 3] in argspec)
        self.assertTrue('seek the number, Luke' in argspec)
        self.assertTrue(len(argspec) == 2)
        
        argspec = c.translate('pydbus.unittest', 'prettylisttest', (0x10,), 1, True, 'i', None, None)
        # print(str(argspec))
        self.assertTrue(argspec == True)

        argspec = c.translate('pydbus.unittest', 'simplematchfunction', (0x10,), 0, True, 'i', None, None)
        # print(str(argspec))
        self.assertTrue(argspec[0] == (0x11, 0, 'i', True))

        self.assertRaises(ValueError, c.translate, 'pydbus.unittest', 'simplematchfunction', (0x10,), 0, True, 'goodluckwiththat', None, None)
        argspec = c.translate('pydbus.unittest', 'simplematchfunction', (0x10,), 0, True, 'i', None, None)
        # print(str(argspec))
        self.assertEqual(argspec[0], (0x11, 0, 'i', True))

        argspec = c.translate('pydbus.unittest', 'allargsin1matchfunction', (0x10, 0x20), 0, True, 'i', None, None)
        # print(str(argspec))
        self.assertTrue(argspec == 0x30)
        

    def test_variant_guidance_possibilities(self):
        from pydbus.translator import variant_guidance_possibilities
        self.assertEqual(('u',), tuple(variant_guidance_possibilities('u')))
        self.assertEqual(('ss',), tuple(variant_guidance_possibilities('ss')))
        self.assertEqual(('v:u:',), tuple(variant_guidance_possibilities('v:u:')))
        self.assertEqual(('sv:i:',), tuple(variant_guidance_possibilities('sv:i:')))
        self.assertEqual(('sv:i:', 'sv:s:'), tuple(variant_guidance_possibilities('sv:i/s:')))
        self.assertEqual(('sv:i:au', 'sv:s:au'), tuple(variant_guidance_possibilities('sv:i/s:au')))
        self.assertEqual(('sv:i:auv::', 'sv:s:auv::'), tuple(variant_guidance_possibilities('sv:i/s:auv::')))
        self.assertEqual(('sv:i:auv:i:', 'sv:s:auv:i:'), tuple(variant_guidance_possibilities('sv:i/s:auv:i:')))
        self.assertEqual(('sv:i:auv:i:', 'sv:i:auv:u:', 'sv:s:auv:i:', 'sv:s:auv:u:'), tuple(variant_guidance_possibilities('sv:i/s:auv:i/u:')))
        self.assertEqual(('sv:iss:au', 'sv:sss:au'), tuple(variant_guidance_possibilities('sv:i/s.ss:au')))

    def test_variant_introspection_rewrite(self):
        from pydbus.translator import variant_introspection_rewrite
        self.assertEqual('u', variant_introspection_rewrite('u', []))
        self.assertEqual('au', variant_introspection_rewrite('au', []))
        self.assertEqual('auv:i:', variant_introspection_rewrite('auv', ['i']))
        self.assertEqual('auv:i:s', variant_introspection_rewrite('auvs', ['i']))
        # So the arglist in the above case is [unsigned int,unsigned int..],int,string
        self.assertEqual('auv:i/b:s', variant_introspection_rewrite('auvs', ['i/b']))
        self.assertEqual('auv:i/b:sv::', variant_introspection_rewrite('auvsv', ['i/b']))
        self.assertEqual('auv:i/b:sv:as:', variant_introspection_rewrite('auvsv', ['i/b', 'as']))
        self.assertEqual('auv:i/b.ss:sv::', variant_introspection_rewrite('auvsv', ['i/b.ss']))

    def test_python_to_dbus_translations(self):
        from pydbus.translator import PydbusCPythonTranslator
        c = PydbusCPythonTranslator(True, 'pydbus.unittest', unit_test_dictname='pydbus_python_to_dbus')

        argspec = c.translate('who.knows.what', 'testkey', (1, 4, 100, 'never see it', 'no changes'), 0, False, 'uui', None, None)
        self.assertEqual(argspec[0], 1)
        self.assertEqual(argspec[1], 4)        
        self.assertEqual(argspec[3], 'never see it')
        
        argspec = c.translate('pydbus.unittest', 'leave_me_alone', (1, 4, 100, 100000), 0, False, 'uui', None, None)
        self.assertEqual(argspec[0], 1)
        self.assertEqual(argspec[1], 4)
        
        argspec = c.translate('pydbus.unittest', 'testkey', (
            'value_should_be_one',
            'Test Case Matching on 4',
            'value should be thirty',
            (1, 2, 3, "won't see me"),
            'no changes',
            ('bit 1 off', 'bit 2 on', 'bit 0 on'),
            {'bit 1 off' : True, 'bit 2 on':True, 'bit 0 on' :True}), 0, False, 'uiussii', None, None)
        self.assertEqual(argspec[0], 1)
        self.assertEqual(argspec[1], 4)
        self.assertEqual(argspec[2], 30)
        self.assertEqual(argspec[3], 'forced replacement item')
        self.assertEqual(argspec[4], 'no changes')
        self.assertEqual(argspec[5], 5)
        self.assertEqual(argspec[6], 5)
        
        argspec = c.translate('pydbus.unittest', 'fromDbusNamedBitFormats',
            (('bit 0 on', 'bit 2 off'),
             ('bit 2 off', ['zero_to_sixteen', 9], 'left two of nibble2 is one'),
             100,  # oass ints along as they come
             'never see it',
             'no changes'
             ), 0, False, 'uuiss', None, None)
        self.assertEqual(argspec[0], 1)
        self.assertEqual(argspec[1], 0x910)
        self.assertEqual(argspec[2], 100)
        
        self.assertRaises(ValueError, c.translate, 'pydbus.unittest', 'singletest', ('should fail', 6), 0, False, 'uui', None, None)
        argspec = c.translate('pydbus.unittest', 'singletest', 'bit 0 ON', 0, False, 'u', None, None)
        self.assertTrue(argspec, 1)
        
        argspec = c.translate('pydbus.unittest', 'prettydicttest', { 'the first three bits if not the fourth':5, 'solo True, seldom seen' : True}, 0, False, 'i', None, None)
        # print(str(argspec))
        self.assertEqual(argspec[0], 5 + 16)
        self.assertTrue(len(argspec) == 1)
        
        argspec = c.translate('pydbus.unittest', 'prettylisttest', (('solo True, seldom seen', ('the first three bits if not the fifth', 3),),), 0, False, 'i', None, None)
     
        # print(str(argspec))
        self.assertEqual(argspec[0], 0x13)      
        
        argspec = c.translate('pydbus.unittest', 'simplematchfunction', ("The answer should be five",), 0, False, 'i', None, None)
        # print(str(argspec))
        self.assertTrue(argspec[0] == 5)        

        argspec = c.translate('pydbus.unittest', 'allargsin1matchfunction', ("The answer should be seven", "Hi Mom"), 0, False, 'i', None, None)
        # print(str(argspec))
        self.assertTrue(argspec[0] == 7)
        
        argspec = c.translate('pydbus.unittest', 'pytodbusvariants', (('label for 0', 1, 2, 'two', 'strings'), ['some', 'more', 'strings']), 0, False, 'vv', None, None)
        self.assertEqual(argspec[0], Variant('(iiiss)', (0, 1, 2, 'two', 'strings')))
        self.assertEqual(argspec[1], Variant('as', ['some', 'more', 'strings']))

        argspec = c.translate('pydbus.unittest', 'pytodbusvariants2', (('label for 0', 1, 2, 'two', 'strings'),
                                                                     ['label for 10', 'who', 'knows'],
                                                                     ('label for 10', 'who', 'knows'),
                                                                     ), 0, False, 'vvv', None, None)
        self.assertEqual(argspec[0],
            Variant('(iiiss)', (0, 1, 2, 'two', 'strings')))
        self.assertEqual(argspec[1],
            Variant('ai', [10, -101, -101])) 
        self.assertEqual(argspec[2],
            Variant('(iss)', (10, 'who', 'knows'),))
        self.assertTrue(len(argspec) == 3)
        
        argspec = c.translate('pydbus.unittest', 'dictionary_test',
                              ({ 0 : 'label for 1', 1 : 10},
                               { 0 : 'label for 1', 20 : 'label for 20', 99:99, 42: "who knows", 100 : "label for 1"}),
                              0, False, 'a{ii}a{ii}', None, None)

        self.assertEqual(argspec, ({ 0 : 1 , 1: 10},
                                  {0:1, 20:20, 99:99, 42:-101, 100:-101}))

        argspec = c.translate('pydbus.unittest', 'dictionary_keys', ({ 'label for 1' : 'is 1', 2 : 'is 2'},
                                                                   { 'label for 1' : 'is 1', 2 : 'is 2'},
                                                                   ), 0, False, 'a{is}a{ii}', None, None)
        # print(str(argspec))
        self.assertEqual(argspec[0], { 1 : 'is 1' , 2: 'is 2'})
        self.assertEqual(argspec[1], { 1 : 1 , 2: 2})

        t = BlankObject()
        t.arg0 = 'zero'
        t.arg1 = 'one'
        t.arg2 = 2
        argspec = c.translate('pydbus.unittest', 'named_arguments', t, 0, False, 'ssi', None, None)
        self.assertEqual(argspec, ('zero', 'one', 2))
        
        d = { 'arg0' : 'zero', 'arg1':'one', 'arg2' : 2}
        argspec = c.translate('pydbus.unittest', 'named_arguments2', d, 0, False, 'ssi', None, None)
        self.assertEqual(argspec, ('zero', 'one', 2))
        # Now test both of those dbus to python.
        # print(str(argspec))
        
    def test_dbus_to_python_variable_naming(self):
        from pydbus.translator import PydbusCPythonTranslator
        c = PydbusCPythonTranslator(True, 'pydbus.unittest', unit_test_dictname='pydbus_dbus_to_python')
        argspec = c.translate('pydbus.unittest', 'd_to_p_named_args', (1, 4, 'one hundred'), 0, True, 'uus', None, None)
        self.assertEqual(argspec.arg0, 1)
        self.assertEqual(argspec.arg1, 4)
        self.assertEqual(argspec.arg2, 'one hundred')

        argspec = c.translate('pydbus.unittest', 'd_to_p_dict_args', (1, 4, 'one hundred'), 0, True, 'uus', None, None)
        self.assertEqual(argspec['arg0'], 1)
        self.assertEqual(argspec['arg1'], 4)
        self.assertEqual(argspec['arg2'], 'one hundred')

        d = { 'still' : 'here'}
        argspec = c.translate('pydbus.unittest', 'd_to_p_dict_args', (1, 4, 'one hundred'), 0, True, 'uus', d, None)
        self.assertEqual(argspec['arg0'], 1)
        self.assertEqual(argspec['arg1'], 4)
        self.assertEqual(argspec['arg2'], 'one hundred')
        self.assertEqual(len(argspec), 3)

        d = { 'still' : 'here'}
        argspec = c.translate('pydbus.unittest', 'd_to_p_dict_args2', (1, 4, 'one hundred'), 0, True, 'uus', d, None)
        self.assertEqual(argspec['arg0'], 1)
        self.assertEqual(argspec['arg1'], 4)
        self.assertEqual(argspec['arg2'], 'one hundred')
        self.assertEqual(argspec['still'], 'here')
        self.assertEqual(len(argspec), 4)
        
        b = BlankObject()
        b.arg0 = '441'
        b.newguy = '2'
        argspec = c.translate('pydbus.unittest', 'd_to_p_named_args3', (1, 4, 'one hundred'), 0, True, 'uus', b, None)
        self.assertEqual(argspec.arg0, 1)
        self.assertEqual(argspec.arg1, 4)
        self.assertEqual(argspec.arg2, 'one hundred')
        self.assertEqual(argspec.newguy, '2')



    def test_user_facing_interface(self):
        from pydbus import SessionBus
        import multiprocessing as mp
        import time

        #mp.set_start_method('spawn')
        ready = mp.Value('i',0)
        server_process = mp.Process(target=pydbus_server,args=(ready,),daemon=True)
        server_process.start()
        sb = SessionBus()
        while ready.value==0: time.sleep(1)
        test_server = sb.get('pydbus.unittest',timeout=10)
        r = test_server.NoArgsStringReply()
        self.assertEqual(r,0,"Translation Inactive") 
        r = test_server.AddTwo(2)
        self.assertEqual(r, 4,"Translation Inactive")

        test_server = sb.get('pydbus.unittest',translation_spec=True,timeout=10)
        r = test_server.NoArgsStringReply()
        self.assertEqual(r,"first string","Translation Active") 
        r = test_server.AddTwo(2)
        self.assertEqual(r, 4,"Translation Active")
        test_server.Quit()
        server_process.join()



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

    def NoArgsStringReply(self):
        """returns the string 'Hello, World!'"""
        return 0  # Should show up as 'first string' via translation

    def AddTwo(self, i):
        """Returns two more than it gets."""
        return i + 2

    def Quit(self):
        """removes this object from the DBUS connection and exits"""
        self.loop.quit()

def pydbus_server(ready):
    from pydbus import SessionBus
    from gi.repository.GLib import MainLoop
    from pydbus.extensions.PatchPreGlib246 import compat_dbus_connection_register_object # @UnresolvedImport @Reimport @UnusedImport
    from pydbus.extensions.PatchPreGlib246 import compat_dbus_invocation_return_value  # @UnresolvedImport @Reimport @UnusedImport
    from pydbus.extensions.PatchPreGlib246 import compat_dbus_invocation_return_dbus_error  # @UnresolvedImport @Reimport @UnusedImport
    loop = MainLoop()
    bus = SessionBus()
    try:
        bus.get('pydbus.unittest')
    except:
        with bus.publish("pydbus.unittest", PyDbusUnitTestService(loop)):
            ready.value=True
            loop.run()
        

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test)
    unittest.TextTestRunner().run(suite)

