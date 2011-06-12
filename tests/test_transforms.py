# -*- coding=utf-8 -*-


from baseline import transforms
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
                assert transforms.classify_token(datum)[0] == typ

    def test_classify_token_value(self):
        assert transforms.classify_token(u'¹⁰⁰')[2] == 100
        # TODO: more here?

    def test_basic_tokenize(self):
        from baseline.transforms import richtoken
        line = u'¹⁰⁰ ⁼ ⁷⁸ ⁷⁸₄₅⁷⁸66₄₅ ₄ ₅'
        tokens = transforms.tokenize_line(line)
        pprint(tokens[0])
        assert tokens[0] == richtoken('number', 'up', 100, u'¹⁰⁰', (0,))
        assert tokens[7] == richtoken('number', 'down', 45, u'₄₅', (11,))
        # TODO: more here?

class TestParsing():
    def test_well_formedness(self):
        parse = transforms.parse_fundef

        assert parse("foo bar baz 22") == None      # line with no non-comment tokens

        with raises(ValueError):
            parse(u' ⁼ ⁷⁸ ⁷⁸₄₅⁷⁸')                  # line does not start with number
        with raises(ValueError):
            parse(u'¹⁰⁰ ⁼ dude')                    # line with not enough tokens
        with raises(ValueError):
            parse(u'⁷⁸ ⁷⁸₄₅⁷⁸')                     # line does not have = as second token

        #line = u'¹⁰⁰ ⁼ ⁷⁸ ⁷⁸₄₅⁷⁸66₄₅ ₄ ₅'
        #assert False, "show me the output"
        



