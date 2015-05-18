import itertools
import re

__title__ = 'HumanRegex'
__version__ = '0.1.0'
__author__ = 'Marcelo Fonseca Tambalo'


class HumanMatch(dict):
    def __getitem__(self, y):
        try:
            return super(HumanMatch, self).__getitem__(y)
        except KeyError:
            return None

    def get(self, k, d=None):
        ret = super(HumanMatch, self).get(k, d)
        return d if ret is None else ret


class HumanRegex(str):
    _AND = 'AND'
    _OR = 'OR'

    def __init__(self):
        self.pattern = ''
        self.prefixes = ''
        self.source = ''
        self.suffixes = ''

        self._dotall = False
        self._ignorecase = False
        self._locale = False
        self._multiline = False
        self._unicode = False
        self._verbose = False

    def add(self, value=None, name=None):
        if value:
            if name is None:
                self.source += value
            else:
                self.source += '(?P<{name}>{value})'.format(name=name, value=value)
        self.pattern = self.prefixes + self.source + self.suffixes
        return self

    def any(self, value):
        return self.add("[" + re.escape(value) + "]")

    def anything(self):
        return self.add("(?:.*)")

    def anything_but(self, value):
        return self.add("(?:[^" + re.escape(value) + "]*)")

    def br(self):
        return self.add(r"(?:(?:\n)|(?:\r\n))")

    def digit(self):
        return self.add(r"\d")

    def digits(self):
        return self.add(r"\d+")

    def non_digit(self):
        return self.add(r"\D")

    def non_digits(self):
        return self.add(r"\D+")

    def end_of_line(self, enable=True):
        self.suffixes = "$" if enable else ""
        return self.add()

    def maybe(self, value):
        return self.add("(?:" + re.escape(value) + ")?")

    def multiple(self):
        return self.add("+")
    s = multiple

    def OR(self, value=None):
        self.add("|")
        return self.then(value) if value else self

    def range(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        if name is None:
            f = r"([%s])"
        else:
            f = r"(?P<{name}>([%s]))".format(name=name)
        r = []
        for arg in args:
            if isinstance(arg, basestring):
                r.append(re.escape(arg))
            else:
                r.append("-".join(arg))
        return self.add(f % ''.join(r))

    def ranges(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        if name is None:
            f = r"([%s]+)"
        else:
            f = r"(?P<{name}>([%s]+))".format(name=name)
        r = []
        for arg in args:
            if isinstance(arg, basestring):
                r.append(re.escape(arg))
            else:
                r.append("-".join(arg))
        return self.add(f % ''.join(r))

    def something(self):
        return self.add("(?:.+)")

    def something_but(self, value):
        return self.add("(?:[^" + re.escape(value) + "]+)")

    def start_of_line(self, enable=True):
        self.prefixes = "^" if enable else ""
        return self.add()

    def tab(self):
        return self.add(r"\t")

    def whitespace(self):
        return self.add(r"\s")

    def non_whitespace(self):
        return self.add(r"\S")

    def then(self, value):
        return self.add("(?:" + re.escape(value) + ")")
    find = then

    def word(self):
        return self.add(r"\w+")

    def non_word(self):
        return self.add(r"\W+")

    def char(self):
        return self.add(r"\w")

    def non_char(self):
        return self.add(r"\W")

    def dotall(self, enable=True):
        self._dotall = enable
        return self
    S = dotall

    def ignorecase(self, enable=True):
        self._ignorecase = enable
        return self
    I = ignorecase

    def locale(self, enable=True):
        self._locale = enable
        return self
    L = locale

    def multiline(self, enable=True):
        self._multiline = enable
        return self
    M = multiline

    def unicode(self, enable=True):
        self._unicode = enable
        return self

    def U(self, enable=True): return self.unicode(enable)

    def verbose(self, enable=True):
        self._verbose = enable
        return self
    X = verbose

    def get_flags(self):
        flag = 0
        flag = flag | re.S if self._dotall else flag | 0
        flag = flag | re.I if self._ignorecase else flag | 0
        flag = flag | re.L if self._locale else flag | 0
        flag = flag | re.M if self._multiline else flag | 0
        flag = flag | re.U if self._unicode else flag | 0
        flag = flag | re.X if self._verbose else flag | 0
        return flag

    def compile(self):
        return re.compile(str(self), self.get_flags())

    def findall(self, string):
        return self.compile().findall(string)

    def groups(self, string):
        return self.search(string).groups()

    def groupdict(self, string):
        result = HumanMatch()
        match = self.search(string)
        result[0] = match.group()
        result.update(enumerate(match.groups(), start=1))
        result.update(match.groupdict())
        return result

    def match(self, string):
        return self.compile().match(string)

    def replace(self, string, repl):
        return self.compile().sub(repl, string)
    sub = replace

    def search(self, string):
        return self.compile().search(string)

    def split(self, string):
        return re.split(str(self), string, flags=self.get_flags())

    def test(self, string):
        return True if len(self.findall(string)) else False

    def __str__(self):
        return r"%s" % self.pattern

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self

    def __repr__(self):
        return repr(str(self))

    def __call__(self, string):
        return self.groupdict(string)

    def _combine(self, other, op=_AND):
        if isinstance(other, Flag):
            Flag.set(other, self)
            return self
        elif isinstance(other, Flags):
            for flag in other:
                flag.set(self)
            return self

        hr = HumanRegex()

        hr._dotall = self._dotall | other._dotall
        hr._ignorecase = self._ignorecase | other._ignorecase
        hr._locale = self._locale | other._locale
        hr._multiline = self._multiline | other._multiline
        hr._unicode = self._unicode | other._unicode
        hr._verbose = self._verbose | other._verbose

        hr.prefixes = self.prefixes if self.prefixes else other.prefixes
        hr.suffixes = other.suffixes if other.suffixes else self.suffixes
        hr.add(self.source)
        if op == 'OR':
            hr.OR()
        return hr.add(other.source)

    def __or__(self, other):
        return self._combine(other, self._OR)

    def __and__(self, other):
        return self._combine(other, self._AND)


HR = HumanRegex


class Flags(set):
    def __or__(self, other):
        if isinstance(other, (Flag, HR)):
            return other | self
        return super(Flags, self).__or__(other)

    def __and__(self, other):
        if isinstance(other, HR):
            return other & self
        return super(Flags, self).__and__(other)


class Flag(object):
    def __init__(self, enable=True):
        self.enable = enable

    def set(self, hr):
        self.f(hr, self.enable)

    def __or__(self, other):
        if isinstance(other, Flag):
            return Flags([self, other])
        elif isinstance(other, Flags):
            flgs = Flags(other)
            flgs.add(self)
            return flgs
        else:
            return other | self

    def __and__(self, other):
        if isinstance(other, HR):
            return other & self
        raise TypeError(
            "unsupported operand type(s) for |: '%s' and '%s'" % (
                type(self).__name__,
                type(other).__name__
            )
        )

    def __repr__(self):
        return self.f.__name__


class FS(Flag):
    f = HR.dotall


class FI(Flag):
    f = HR.ignorecase


class FL(Flag):
    f = HR.locale


class FM(Flag):
    f = HR.multiline


class FU(Flag):
    f = HR.unicode


class FX(Flag):
    f = HR.verbose


def ADD(value, name=None): return HR().add(value, name=name)
RE = ADD


def T(value, name=None): return HR().then(value)


def F(value, name=None): return HR().find(value)


def A(value, name=None): return HR().any(value)


def AT(): return HR().anything()


def ATB(value, name=None): return HR().anything_but(value)


def EOL(): return HR().end_of_line()


def MB(value, name=None): return HR().maybe(value)


def MTP(): return HR().multiple()


def R(*args, **kwargs): return HR().range(*args, **kwargs)


def RS(*args, **kwargs): return HR().ranges(*args, **kwargs)


def ST(value, name=None): return HR().something(value)


def STB(value, name=None): return HR().something_but(value)


def SOL(): return HR().start_of_line()


def BR(): return HR().br()


def D(): return HR().digit()


def DS(): return HR().digits()


def ND(): return HR().non_digit()


def NDS(): return HR().non_digits()


def TAB(): return HR().tab()


def WS(): return HR().whitespace()


def NWS(): return HR().non_whitespace()


def W(): return HR().word()


def NW(): return HR().non_word()


def C(): return HR().char()


def NC(): return HR().non_char()


if __name__ == '__main__':
    print (FI() & F("CAT")).replace("this is a cat", "dog")

    if F('dog').test('This is a dog'):
        print 'Oh yeah'

    re09 = RS(('0', '9'))
    if re09.test('My lucky 25 number'):
        print '1: Number found'
    if re09.findall('My lucky 25 number')[0] == '25':
        print '2: Number found'
    re09_number = RS(('0', '9'), name='number')
    if re09_number.groupdict('My lucky 25 number')['number'] == '25':
        print '3: Number found'
    print re09_number.groupdict('My lucky 25 number')['no_such_group']
    # None

    if bool(re09_number('My lucky 25 number')):
        print '4: Number found'
    if re09_number('My lucky 25 number')[0] == '25':
        print '5: Number found'
    if re09_number('My lucky 25 number')['number'] == '25':
        print '6: Number found'
    print re09_number('My lucky 25 number')['no_such_group']
    # None

    print bool(RE('[0-9]+', name='number')('My lucky 25 number'))
    # True
    print RE('[0-9]+', name='number')('My lucky 25 number')[0]
    # 25
    print RE('[0-9]+', name='number')('My lucky 25 number')['number']
    # 25
