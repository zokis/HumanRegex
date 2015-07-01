# encoding: utf-8
import unittest

from itertools import combinations

from hre import *


class TestHRE(unittest.TestCase):

    def test_human_match(self):
        hm = HumanMatch(a=1, b=2, c=3)
        self.assertEqual(hm['a'], 1)
        self.assertEqual(hm['b'], 2)
        self.assertEqual(hm['c'], 3)
        self.assertIsNone(hm['d'])
        self.assertEqual(hm.get('a'), 1)
        self.assertEqual(hm.get('b'), 2)
        self.assertEqual(hm.get('c'), 3)
        self.assertIsNone(hm.get('d'))

        self.assertEqual(hm.get('a', 1), 1)
        self.assertEqual(hm.get('b', 2), 2)
        self.assertEqual(hm.get('c', 3), 3)
        self.assertIsNone(hm.get('d', None))
        self.assertIsNotNone(hm.get('d', 6))

    def test_simple_api(self):
        my_re = RE('[0-9]+')

        self.assertTrue(bool(my_re('number: 25')))
        self.assertFalse(bool(my_re('zZz')))
        self.assertEqual(my_re('number: 25')[0], '25')
        self.assertIsNone(my_re('zZz')[0])

        my_re = RE('(?P<number>[0-9]+)')
        self.assertEqual(my_re('number: 25')['number'], '25')
        self.assertIsNone(my_re('zZz')['number'])

    def test_flags(self):
        my_re = HR().find('cat')
        self.assertFalse(bool(my_re('CAT or dog')))

        my_re = my_re.ignorecase()
        self.assertTrue(bool(my_re('CAT or dog')))

        my_re = SOL() & F('DOG')
        self.assertFalse(bool(my_re('CAT or \ndog')))

        my_re = my_re & FI() | FM()
        self.assertTrue(bool(my_re('CAT or \ndog')))

        my_re = my_re & (FI() | FM())
        self.assertTrue(bool(my_re('CAT or \ndog')))

        with self.assertRaises(TypeError):
            ((FI() | FM()) | 1)
        with self.assertRaises(TypeError):
            ((FI() | FM()) & 1)
        with self.assertRaises(TypeError):
            (FI() & 1)

        self.assertEqual(((FI() | FM()) & RE('x')).get_flags(), 10)

        self.assertEqual((FI() & RE('z')).get_flags(), 2)
        self.assertEqual((FI() | RE('z')).get_flags(), 2)

        self.assertEqual(repr(FI()), 'ignorecase')
        self.assertEqual(repr(FL()), 'locale')
        self.assertEqual(repr(FM()), 'multiline')
        self.assertEqual(repr(FS()), 'dotall')
        self.assertEqual(repr(FU()), 'unicode')
        self.assertEqual(repr(FX()), 'verbose')

        ops = ['', 'I', 'L', 'M', 'S', 'U', 'X']
        ops_s = ['', FI, FL, FM, FS, FU, FX]
        for i in xrange(1, 8):
            for cop in combinations(ops, i):
                my_re = RE('x')
                flags = 0
                co_flags = Flags()
                for op in cop:
                    if op:
                        j = ops.index(op)
                        co_flags = co_flags | ops_s[j]()
                        getattr(my_re, op)()
                        flags = flags | (2 ** j)
                self.assertEqual(my_re.get_flags(), flags)
                self.assertEqual(int(co_flags), flags)

    def test_methods(self):
        text = "violets are red"
        my_re = RE('(?:red)')

        self.assertEqual(my_re.match('red').group(), 'red')

        self.assertEqual(my_re.replace(text, 'blue'), "violets are blue")

        self.assertEqual(my_re.get_flags(), 0)

        text = """Ross McFluff: 834.345.1254 155 Elm Street
        Ronald Heathmore: 892.345.3428 436 Finley Avenue
        Frank Burger: 925.541.7625 662 South Dogwood Way
        Heather Albrecht: 548.326.4584 919 Park Place"""
        expected = [
            'Ross McFluff: 834.345.1254 155 Elm Street',
            '        Ronald Heathmore: 892.345.3428 436 Finley Avenue',
            '        Frank Burger: 925.541.7625 662 South Dogwood Way',
            '        Heather Albrecht: 548.326.4584 919 Park Place'
        ]
        self.assertEqual(RE(r'\n+').split(text), expected)

        text = "He was carefully disguised but captured quickly by police."
        self.assertEqual(RE(r"\w+ly").test(text), True)
        self.assertEqual(RE(r"\w+zz").test(text), False)

        self.assertEqual(RE(r"\w+ly").findall(text), ['carefully', 'quickly'])
        self.assertEqual(RE(r"\w+zz").findall(text), [])

        my_re = RE(r"(?P<first_name>\w+) (?P<last_name>\w+)")
        self.assertEqual(my_re.groups('Malcolm Reynolds'), ('Malcolm', 'Reynolds'))
        self.assertEqual(
            my_re.groupdict('Malcolm Reynolds'),
            {
                0: 'Malcolm Reynolds',
                1: 'Malcolm',
                2: 'Reynolds',
                'last_name': 'Reynolds',
                'first_name': 'Malcolm'
            }
        )

    def test_then(self):
        then_re = HR().then('@')
        then_match = then_re('a@b')
        self.assertTrue(bool(then_match))
        self.assertEqual(then_match[0], '@')
        then_re = HR().then('@', name='x')
        then_match = then_re('a@b')
        self.assertTrue(bool(then_match))
        self.assertEqual(then_match[0], '@')
        self.assertEqual(then_match['x'], '@')
        then_re = HR().then('@', quantifier=2)
        then_match = then_re('a@b')
        self.assertFalse(bool(then_match))
        self.assertIsNone(then_match[0])
        self.assertIsNone(then_match['x'])
        then_match = then_re('a@@b')
        self.assertTrue(bool(then_match))
        self.assertEqual(then_match[0], '@@')
        then_re = HR().then('@', name='x', quantifier=2)
        then_match = then_re('a@@b')
        self.assertEqual(then_match['x'], '@@')

        then_re = HR() & T('@')
        then_match = then_re('a@b')
        self.assertTrue(bool(then_match))
        self.assertEqual(then_match[0], '@')
        then_re = HR() & T('@', name='x')
        then_match = then_re('a@b')
        self.assertTrue(bool(then_match))
        self.assertEqual(then_match[0], '@')
        self.assertEqual(then_match['x'], '@')
        then_re = HR() & T('@', quantifier=2)
        then_match = then_re('a@b')
        self.assertFalse(bool(then_match))
        self.assertIsNone(then_match[0])
        self.assertIsNone(then_match['x'])
        then_match = then_re('a@@b')
        self.assertTrue(bool(then_match))
        self.assertEqual(then_match[0], '@@')
        then_re = HR() & T('@', name='x', quantifier=2)
        then_match = then_re('a@@b')
        self.assertEqual(then_match['x'], '@@')

    def test_with(self):
        with RE(r'\w+') as r:
            self.assertTrue(bool(r('testes')))

    def test_repr(self):
        self.assertEqual(repr(RE(r'x')), "'x'")

    def test_mul(self):
        r = RE('a|b') * 2
        self.assertTrue(bool(r('a')))
        self.assertTrue(bool(r('ab')))
        self.assertTrue(bool(r('b')))
        self.assertFalse(bool(r('x')))
        with self.assertRaises(TypeError):
            RE('a|b') * 'a'

    def test_find(self):
        find_re = HR().find('@')
        find_match = find_re('a@b')
        self.assertTrue(bool(find_match))
        self.assertEqual(find_match[0], '@')
        find_re = HR().find('@', name='x')
        find_match = find_re('a@b')
        self.assertTrue(bool(find_match))
        self.assertEqual(find_match[0], '@')
        self.assertEqual(find_match['x'], '@')
        find_re = HR().find('@', quantifier=2)
        find_match = find_re('a@b')
        self.assertFalse(bool(find_match))
        self.assertIsNone(find_match[0])
        self.assertIsNone(find_match['x'])
        find_match = find_re('a@@b')
        self.assertTrue(bool(find_match))
        self.assertEqual(find_match[0], '@@')
        find_re = HR().find('@', name='x', quantifier=2)
        find_match = find_re('a@@b')
        self.assertEqual(find_match['x'], '@@')

        find_re = HR() & F('@')
        find_match = find_re('a@b')
        self.assertTrue(bool(find_match))
        self.assertEqual(find_match[0], '@')
        find_re = HR() & F('@', name='x')
        find_match = find_re('a@b')
        self.assertTrue(bool(find_match))
        self.assertEqual(find_match[0], '@')
        self.assertEqual(find_match['x'], '@')
        find_re = HR() & F('@', quantifier=2)
        find_match = find_re('a@b')
        self.assertFalse(bool(find_match))
        self.assertIsNone(find_match[0])
        self.assertIsNone(find_match['x'])
        find_match = find_re('a@@b')
        self.assertTrue(bool(find_match))
        self.assertEqual(find_match[0], '@@')
        find_re = HR() & F('@', name='x', quantifier=2)
        find_match = find_re('a@@b')
        self.assertEqual(find_match['x'], '@@')

    def test_any(self):
        any_re = HR().any('xyz')
        any_match = any_re('abacate')
        self.assertFalse(bool(any_match))
        any_match = any_re('abacaxi')
        self.assertTrue(bool(any_match))
        self.assertEqual(any_match[0], 'x')
        any_re = HR().any('xyz', name='x')
        any_match = any_re('abacaxi')
        self.assertEqual(any_match['x'], 'x')
        any_re = HR().any('srt', quantifier=2).U()
        any_match = any_re(u'Pêssego')

        any_re = HR() & A('xyz')
        any_match = any_re('abacate')
        self.assertFalse(bool(any_match))
        any_match = any_re('abacaxi')
        self.assertTrue(bool(any_match))
        self.assertEqual(any_match[0], 'x')
        any_re = HR() & A('xyz', name='x')
        any_match = any_re('abacaxi')
        self.assertEqual(any_match['x'], 'x')
        any_re = HR() & A('srt', quantifier=2).U()
        any_match = any_re(u'Pêssego')

    def test_anything(self):
        anything_re = HR().then('@').anything(name='x').then('@')
        anything_match = anything_re('dsafh4353')
        self.assertFalse(bool(anything_match))
        anything_re = HR().then('@').anything(name='x').then('@')
        anything_match = anything_re('@dsafh4353@')
        self.assertTrue(bool(anything_match))
        self.assertEqual(anything_match[0], '@dsafh4353@')
        self.assertEqual(anything_match[1], 'dsafh4353')
        self.assertEqual(anything_match['x'], 'dsafh4353')

        anything_re = HR() & T('@') & AT(name='x') & T('@')
        anything_match = anything_re('dsafh4353')
        self.assertFalse(bool(anything_match))
        anything_re = HR() & T('@') & AT(name='x') & T('@')
        anything_match = anything_re('@dsafh4353@')
        self.assertTrue(bool(anything_match))
        self.assertEqual(anything_match[0], '@dsafh4353@')
        self.assertEqual(anything_match[1], 'dsafh4353')
        self.assertEqual(anything_match['x'], 'dsafh4353')

    def test_anything_but(self):
        anything_but_re = HR().then('@').anything_but('@#', name='x').then('@')
        anything_but_match = anything_but_re('@12@123213213213@')
        self.assertTrue(bool(anything_but_match))
        self.assertEqual(anything_but_match[0], '@12@')
        self.assertEqual(anything_but_match[1], '12')
        self.assertEqual(anything_but_match['x'], '12')

        anything_but_re = HR().then('@') & ATB('@#', name='x') & T('@')
        anything_but_match = anything_but_re('@12@123213213213@')
        self.assertTrue(bool(anything_but_match))
        self.assertEqual(anything_but_match[0], '@12@')
        self.assertEqual(anything_but_match[1], '12')
        self.assertEqual(anything_but_match['x'], '12')

    def test_end_of_line(self):
        eof_match = HR().then('aaa', name='x').then('xxx', name='y').end_of_line()('aaaxxx')

        self.assertTrue(bool(eof_match))
        self.assertEqual(eof_match[0], 'aaaxxx')
        self.assertEqual(eof_match[1], 'aaa')
        self.assertEqual(eof_match[2], 'xxx')
        self.assertEqual(eof_match['x'], 'aaa')
        self.assertEqual(eof_match['y'], 'xxx')

        eof_match = (HR() & T('aaa', name='x') & T('xxx', name='y') & EOL())('aaaxxx')

        self.assertTrue(bool(eof_match))
        self.assertEqual(eof_match[0], 'aaaxxx')
        self.assertEqual(eof_match[1], 'aaa')
        self.assertEqual(eof_match[2], 'xxx')
        self.assertEqual(eof_match['x'], 'aaa')
        self.assertEqual(eof_match['y'], 'xxx')

    def test_add_hre(self):
        add_re = RE(T('@') & T('e') & T('$'))
        add_match = add_re('@e$')
        self.assertTrue(bool(add_match))
        self.assertEqual(add_match[0], '@e$')

    def test_br(self):
        br_re = HR() & T('a') & BR() & T('e')
        br_match = br_re('a\ne\nx')
        self.assertTrue(bool(br_match))
        self.assertEqual(br_match[0], 'a\ne')

    def test_group(self):
        g_re = HR() & T('a') & G(T('A') | T('B')) & T('e')
        g_match = g_re('aAe')
        self.assertTrue(bool(g_match))
        self.assertEqual(g_match[0], 'aAe')
        self.assertEqual(g_match[1], 'A')

        g_match = g_re('aBe')
        self.assertTrue(bool(g_match))
        self.assertEqual(g_match[0], 'aBe')
        self.assertEqual(g_match[1], 'B')

        g_match = g_re('aABe')
        self.assertFalse(bool(g_match))
        self.assertIsNone(g_match[0])
        self.assertIsNone(g_match[1])

        g_re = HR() & T('a') & G('12345') & T('e')
        g_match = g_re('a12345e')
        self.assertTrue(bool(g_match))
        self.assertEqual(g_match[0], 'a12345e')
        self.assertEqual(g_match[1], '12345')

    def test_int_or_decimal(self):
        br_re = HR() & T('a') & ID() & T('e')
        br_match = br_re('a3e4x')
        self.assertTrue(bool(br_match))
        self.assertEqual(br_match[0], 'a3e')

        br_re = HR() & T('a') & ID() & T('e')
        br_match = br_re('a3.5e4x')
        self.assertTrue(bool(br_match))
        self.assertEqual(br_match[0], 'a3.5e')

    def test_digit(self):
        d_re = HR() & T('a') & D() & T('e')
        d_match = d_re('a3e4x')
        self.assertTrue(bool(d_match))
        self.assertEqual(d_match[0], 'a3e')
        self.assertFalse(bool(d_re('a33e4x')))

    def test_digits(self):
        d_re = HR() & T('a') & DS() & T('e')
        d_match = d_re('a3e4x')
        self.assertTrue(bool(d_match))
        self.assertEqual(d_match[0], 'a3e')

        d_match = d_re('a323e4x')
        self.assertTrue(bool(d_match))
        self.assertEqual(d_match[0], 'a323e')

    def test_non_digit(self):
        d_re = HR() & T('a') & ND() & T('e')
        d_match = d_re('a@e4x')
        self.assertTrue(bool(d_match))
        self.assertEqual(d_match[0], 'a@e')
        self.assertFalse(bool(d_re('a3e4x')))
        self.assertFalse(bool(d_re('aWEe4x')))

    def test_non_digits(self):
        d_re = HR() & T('a') & NDS() & T('e')
        d_match = d_re('aRe4x')
        self.assertTrue(bool(d_match))
        self.assertEqual(d_match[0], 'aRe')

        d_match = d_re('aRTYe4x')
        self.assertTrue(bool(d_match))
        self.assertEqual(d_match[0], 'aRTYe')
        self.assertFalse(bool(d_re('a3e4x')))
        self.assertFalse(bool(d_re('a33e4x')))

    def test_multiple(self):
        m_re = T('@') & MTP()
        m_match = m_re('@@@@@@')
        self.assertTrue(bool(m_match))
        self.assertEqual(m_match[0], '@@@@@@')

    def test_word(self):
        m_re = T('@') & W()
        m_match = m_re('@palavra')
        self.assertTrue(bool(m_match))
        self.assertEqual(m_match[0], '@palavra')

    def test_non_word(self):
        m_re = T('@') & NW()
        m_match = m_re('@!!!')
        self.assertTrue(bool(m_match))
        self.assertEqual(m_match[0], '@!!!')

    def test_char(self):
        m_re = T('@') & C()
        m_match = m_re('@p')
        self.assertTrue(bool(m_match))
        self.assertEqual(m_match[0], '@p')

    def test_non_char(self):
        m_re = T('@') & NC()
        m_match = m_re('@!')
        self.assertTrue(bool(m_match))
        self.assertEqual(m_match[0], '@!')

    def test_whitespace(self):
        w_re = T('@') & WS() & T('orelha')
        w_match = w_re('@ orelha')
        self.assertTrue(bool(w_match))
        self.assertEqual(w_match[0], '@ orelha')

        w_match = w_re('@\torelha')
        self.assertTrue(bool(w_match))
        self.assertEqual(w_match[0], '@\torelha')

        w_match = w_re('@\norelha')
        self.assertTrue(bool(w_match))
        self.assertEqual(w_match[0], '@\norelha')

    def test_non_whitespace(self):
        w_re = T('@') & NWS() & T('orelha')
        w_match = w_re('@ orelha')
        self.assertFalse(bool(w_match))

        w_match = w_re('@#orelha')
        self.assertTrue(bool(w_match))
        self.assertEqual(w_match[0], '@#orelha')

    def test_tab(self):
        t_re = T('@') & TAB() & T('orelha')
        t_match = t_re('@\torelha')
        self.assertTrue(bool(t_match))
        self.assertEqual(t_match[0], '@\torelha')

    def test_range(self):
        my_re = HR() & R(['a', 'z'])
        my_match = my_re('3s234')
        self.assertTrue(bool(my_match))
        self.assertEqual(my_match[0], 's')

        my_re = HR() & R('abcedfghijklmnopqrsvuwxyz')
        my_match = my_re('3r234')
        self.assertTrue(bool(my_match))
        self.assertEqual(my_match[0], 'r')

    def test_something(self):
        my_re = T('x') & STB('123') & T('y')
        my_match = my_re('xeewy')
        self.assertTrue(bool(my_match))
        self.assertEqual(my_match[0], 'xeewy')

        my_re = T('x') & STB('123') & T('y')
        my_match = my_re('x123y')
        self.assertFalse(bool(my_match))
        self.assertIsNone(my_match[0])

    def test_something_but(self):
        my_re = T('x') & ST() & T('y')
        my_match = my_re('xeewy')
        self.assertTrue(bool(my_match))
        self.assertEqual(my_match[0], 'xeewy')

    def test_ranges(self):
        az = ['a', 'z']
        AZ = ['A', 'Z']
        _09 = ['0', '9']
        special = '_.+'
        my_re = HR() & RS(
            AZ, az,
            _09, special,
            name='account'
        ) & T('@') & RS(
            AZ, az, _09,
            name='provider'
        ) & T('.') & AT()
        my_match = my_re('my_email.1+github@Provider.com')
        self.assertTrue(bool(my_match))
        self.assertEqual(my_match['account'], 'my_email.1+github')
        self.assertEqual(my_match['provider'], 'Provider')

    def test_add_quantifier(self):
        add_re = RE('A', quantifier=1)
        self.assertEqual(str(add_re), r'A{1}')
        add_re = RE('A', quantifier=25)
        self.assertEqual(str(add_re), r'A{25}')
        add_re = RE('A', quantifier=(2,))
        self.assertEqual(str(add_re), r'A{2,}')
        add_re = RE('A', quantifier=(2, 5))
        self.assertEqual(str(add_re), r'A{2,5}')

    def test_maybe(self):
        maybe_re = HR().then('@').maybe('x').then('#')
        maybe_match = maybe_re('@x#')
        self.assertTrue(bool(maybe_match))
        self.assertEqual(maybe_match[0], '@x#')
        maybe_match = maybe_re('@#')
        self.assertTrue(bool(maybe_match))
        self.assertEqual(maybe_match[0], '@#')

        maybe_re = HR() & T('@') & MB('x') & T('#')
        maybe_match = maybe_re('@x#')
        self.assertTrue(bool(maybe_match))
        self.assertEqual(maybe_match[0], '@x#')
        maybe_match = maybe_re('@#')
        self.assertTrue(bool(maybe_match))
        self.assertEqual(maybe_match[0], '@#')


if __name__ == '__main__':
    unittest.main()
