# -*- coding=utf-8 -*-

from pytest import raises
from pprint import pprint

#₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎˱˲˰˯˳
#⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾˂˃˄˅˚

import sys, StringIO
from baseline import runtime, transforms

class TestStdlib():
    def _runprogram(self, definitions):
        fns = dict(filter(None, (transforms.parse_fundef(unicode(f, 'utf-8')) for f in definitions)))
        env = runtime.BaselineRuntime(fundefs = fns)
        capture = StringIO.StringIO()
        env.pipes[1] = capture
        env.run()
        return capture.getvalue()

    def test_helloworld(self):
        prog = '''
¹⁰⁰ ⁼ ⁽⁽⁷² ¹⁰¹ ¹⁰⁸ ¹⁰⁸ ¹¹¹ ⁴⁴ ³² ¹¹⁹ ¹¹¹ ¹¹⁴ ¹⁰⁸ ¹⁰⁰ ³³ ¹⁰⁾⁾    define string literal
¹⁰¹ ⁼ ₁₀₀ ₃ ⁽¹⁾ ²¹                                              bottom-push literal, move len to top, push fd=1 (stdout), produce
⁰   ⁼ ⁽¹⁰¹⁾ ³⁰ ¹                                                push name of HW function, eval that name, pop the returnval
'''
        assert self._runprogram(prog.strip().split('\n')) == "Hello, world!\n"

    def test_stackcmds(self):
        # TODO
        pass

    def test_stackcmds_extra(self):
        # TODO
        pass

    def test_pipes(self):
        # TODO
        pass

    def test_flowcontrol(self):
        '''Test stdlib functions 30-35 (flow control)'''        # TODO: 33-35, 39
        prog = ["¹⁰⁰ ⁼ ⁽⁽¹¹⁵ ¹⁰¹ ¹²¹⁾⁾ ⁽¹⁾ ²¹ ¹",                       # print "yes" to stdout
                "¹⁰¹ ⁼ ⁽⁽¹¹¹ ¹¹⁰⁾⁾ ⁽¹⁾ ²¹ ¹",                           # print "no" to stdout
                "⁰ ⁼ ⁽¹⁰⁰⁾ ³⁰",                                         # test dynamic function call
                "",
                ]
        assert self._runprogram(prog) == "yes"

        prog[3] = "⁰ ⁼ ⁽¹ ¹⁰⁰⁾ ³¹"                                      # test if(True)
        assert self._runprogram(prog) == "yes"
        prog[3] = "⁰ ⁼ ⁽⁰ ¹⁰⁰⁾ ³¹"                                      # test if(False)
        assert self._runprogram(prog) == ""

        prog[3] = "⁰ ⁼ ⁽¹ ¹⁰⁰ ¹⁰¹⁾ ³²"                                      # test if(True)
        assert self._runprogram(prog) == "yes"
        prog[3] = "⁰ ⁼ ⁽⁰ ¹⁰⁰ ¹⁰¹⁾ ³²"                                      # test if(False)
        assert self._runprogram(prog) == "no"



    def test_arith(self): 
        '''Test stdlib functions 50-57 (the basic math operators)'''
        prog = ["¹⁰⁰ ⁼ ⁽⁵ ⁷ ⁵⁾ ⁵⁰ ⁵² ⁽³⁾ ⁵³ ⁽⁹⁾ ⁵¹ ⁽²⁾ ⁵⁵",             # square(((5+7) * 5 / 3 ) - 9)   should equal 121
                "⁰ ⁼ ₁₀₀ ⁽⁹⁹⁹ ¹⁾ ²¹",                                   # do #100, dump entire stack to stdout
                ]                                                       # tests 50-53, 55
        assert self._runprogram(prog) == 'y'
        prog = ["¹⁰⁰ ⁼ ⁽⁶²³³ ¹⁹¹⁾ ⁵⁴ ⁽¹⁵¹⁵⁹ ¹¹ ¹⁰⁾ ⁵⁷ ⁵⁶",              # 6233 % 101 ; log₁˳₁15159
                "⁰ ⁼ ₁₀₀ ¹⁹ ⁽⁹⁹⁹ ¹⁾ ²¹",                                # do #100, dump entire stack to stdout
                ]                                                       # tests 54, 56, 57
        assert self._runprogram(prog) == 'ye'

    def test_logic(self):
        '''Test stdlib functions 60-63 (the wordwise logic functions)'''
        prog = ["¹⁰⁰ ⁼ ⁽⁰⁾ ⁶⁰ ⁽⁶⁾ ⁶⁰ ⁽⁶⁶⁰⁾ ⁶⁰",
                "⁰ ⁼ ₁₀₀ ¹⁹ ⁽⁹⁹⁹ ¹⁾ ²¹",                                # do #100, dump entire stack to stdout
                ]
        truefalsefalse = self._runprogram(prog)
        assert truefalsefalse[0] != '\x00'
        assert truefalsefalse[1:] == '\x00\x00'
        prog = ["¹⁰⁰ ⁼ ⁽⁰ ⁰⁾ ⁶¹ ⁽⁰ ¹⁾ ⁶¹ ⁽¹ ⁰⁾ ⁶¹ ⁽¹ ¹⁾ ⁶¹ ⁶⁰",         # test wordwise and (61)
                "¹⁰¹ ⁼ ⁽⁰ ⁰⁾ ⁶² ⁽⁰ ¹⁾ ⁶² ⁶⁰ ⁽¹ ⁰⁾ ⁶² ⁶⁰ ⁽¹ ¹⁾ ⁶² ⁶⁰",   # test wordwise or  (62)
                "¹⁰² ⁼ ⁽⁰ ⁰⁾ ⁶³ ⁽⁰ ¹⁾ ⁶³ ⁶⁰ ⁽¹ ⁰⁾ ⁶³ ⁶⁰ ⁽¹ ¹⁾ ⁶³",      # test wordwise xor (63)
                "⁰ ⁼ ₁₀₀ ₁₀₁ ₁₀₂ ¹⁹ ⁽⁹⁹⁹ ¹⁾ ²¹",                        # do #100 #101 #102, dump entire stack to stdout
                ]
        assert self._runprogram(prog) == '\x00' * 4 * 3

    def test_bitwise(self):
        '''Test stdlib functions 71-75 (the bitwise logic functions)'''
        # 0b010101 == 21, 0b101010 == 42, 0b000111 == 7, 0b111000 == 56
        prog = ["¹⁰⁰ ⁼ ⁽²¹ ⁷⁾ ⁷¹ ² ⁽⁴²⁾ ⁷²",                            # 010101 & 000111, clone, | 101010  : test 71 and 72
                "¹⁰¹ ⁼ ⁽²¹ ⁷⁾ ⁷³",                                      # 010101 ^ 000111
                "¹⁰² ⁼ ² ⁽³⁾ ⁷⁴ ⁽⁴² ⁴⁾ ⁷⁵",                             # clone the 18, << 3, 42 >> 4
                "⁰ ⁼ ₁₀₀ ₁₀₁ ₁₀₂ ¹⁹ ⁽⁹⁹⁹ ¹⁾ ²¹",                        # do #100 #101 #102, dump entire stack to stdout
                ]
        assert self._runprogram(prog) == '\x05\x2f\x12\x90\x02'


    def test_comparisons(self):
        # TODO
        pass



#₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎˱˲˰˯˳
#⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾˂˃˄˅˚


