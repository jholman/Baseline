# -*- coding=utf-8 -*-


from baseline import transforms

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
        line = u'¹⁰⁰ ⁼ ⁷⁸ ⁷⁸₄₅⁷⁸66₄₅ ₄ ₅'
        tokens = transforms.tokenize_line(line)
        assert tokens[0] == (('number', 'up', 100), u'¹⁰⁰', (0,))
        assert tokens[7] == (('number', 'down', 45), u'₄₅', (11,))



