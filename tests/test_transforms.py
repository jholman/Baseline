# -*- coding=utf-8 -*-

from baseline.transforms import parse_fundef as parse
from baseline.transforms import classify_token, richtoken, tokenize_line
from pytest import raises
from pprint import pprint


#₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎˱˲˰˯˳
#⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾˂˃˄˅˚

class TestLexing():
    def test_classify_token_type(self):
        data = {"number" : [u'¹⁰⁰', u'₄₅'],
                "paren" : [u'₍', u'₎', u'⁽', u'⁾'],
                "operator" : u"₊₋₌˱˲˰˯⁺⁻⁼˂˃˄˅",
                }
        for typ in data:
            for datum in data[typ]:
                print "testing %s is a %s" % (datum, typ)
                assert classify_token(datum)[0] == typ

    def test_classify_token_value(self):
        assert classify_token(u'¹⁰⁰')[2] == 100
        # TODO: more here?

    def test_basic_tokenize(self):
        line = u'¹⁰⁰ ⁼ ⁷⁸ ⁷⁸₍₍₄₅₎₎⁷⁸66₄₅ ₄₍₅₎'
        tokens = tokenize_line(line)
        pprint(tokens)
        assert tokens[0] == richtoken('number', 1, 100, u'¹⁰⁰', (0,))
        assert tokens[8] == richtoken('number', 0, 45, u'₄₅', (13,))
        registers = [t.reg for t in tokens if t.typ != 'comment']
        assert registers == [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        types = [t.typ for t in tokens if t.typ != 'comment']
        assert types == ['number', 'operator', 'number', 'number', 'paren', 
                        'number', 'paren', 'number', 'number', 'number', 
                        'paren', 'number', 'paren']

class TestParsing():
    def test_well_formedness(self):

        assert parse("foo bar baz 22") == None      # line with no non-comment tokens

        with raises(ValueError):
            parse(u' ⁼ ⁷⁸ ⁷⁸₄₅⁷⁸')                  # line does not start with number
        with raises(ValueError):
            parse(u'¹⁰⁰ ⁼ dude')                    # line with not enough tokens
        with raises(ValueError):
            parse(u'⁷⁸ ⁷⁸₄₅⁷⁸')                     # line does not have = as second token
        with raises(Exception):
            parse(u'¹⁰⁰ ⁼ ⁷⁸⁺⁷⁸')                   # wtf is that "+" doing there?

    def test_parse_fncalls(self):
        line = u'¹⁰⁰ ⁼ ⁷⁸ ⁷⁸66₄₅ ₄'
        fnid, fnbody = parse(line)
        assert len(fnbody) == 4
        assert [t.reg for t in fnbody] == [1, 1, 0, 0]

    def test_parse_literals(self):
        line = u'¹⁰⁰ ⁼ ⁷⁸₍₍₄₅ ₅₄₎₎₄₍₅₎⁷⁸⁽⁽¹⁰ ¹¹⁾⁾'
        fnid, fnbody = parse(line)
        assert len(fnbody) == 10
        assert [t.reg for t in fnbody] == [1, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        assert [t.val for t in fnbody if t.typ == 'literal'] == [45, 54, 2, 5, 10, 11, 2]



