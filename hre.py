import re


from functools import reduce
from operator import or_


__title__ = 'HumanRegex'
__version__ = '1.0.0'
__author__ = 'Marcelo Fonseca Tambalo'


class HumanMatch(dict):
    def __getitem__(self, item):
        try:
            return super(HumanMatch, self).__getitem__(item)
        except KeyError:
            return None

    def get(self, key, default=None):
        r = super(HumanMatch, self).get(key, default)
        if r is None:
            return default
        return r


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

    def escape(self, value):
        return re.escape(value)

    def add(self, value=None, name=None, quantifier=None):
        if value is not None:
            if isinstance(value, HumanRegex):
                value = str(value)
            if quantifier is not None:
                if isinstance(quantifier, int):
                    value = "%s{%d}" % (value, quantifier)
                else:
                    if len(quantifier) == 1:
                        value = "%s{%d,}" % (value, quantifier[0])
                    else:
                        value = "%s{%d,%d}" % (value, quantifier[0], quantifier[1])
            if name is None:
                self.source += value
            else:
                self.source += '(?P<{name}>{value})'.format(name=name, value=value)
        self.pattern = self.prefixes + self.source + self.suffixes
        return self

    def any(self, value, name=None, quantifier=None):
        return self.add("[" + self.escape(value) + "]", name=name, quantifier=quantifier)

    def anything(self, name=None):
        return self.add(r"(?:.*)", name=name)

    def anything_but(self, value, name=None):
        return self.add("(?:[^" + self.escape(value) + "]*)", name=name)

    def br(self):
        return self.add(r"(?:\n|\r\n)")

    def int_or_decimal(self, name=None):
        return self.add(r"(?:\d*\.)?\d+", name=name)

    def digit(self, name=None, quantifier=None):
        return self.add(r"\d", name=name, quantifier=quantifier)

    def digits(self, name=None):
        return self.add(r"\d+", name=name)

    def group(self, value, name=None):
        if isinstance(value, HumanRegex):
            value = str(value)
        else:
            value = self.escape(value)
        return self.add("(" + value + ")", name=name)

    def non_digit(self, name=None, quantifier=None):
        return self.add(r"\D", name=name, quantifier=quantifier)

    def non_digits(self, name=None):
        return self.add(r"\D+", name=name)

    def end_of_line(self, enable=True):
        self.suffixes = "$" if enable else ""
        return self.add()

    def maybe(self, value, name=None):
        return self.add("(?:" + self.escape(value) + ")?", name=name)

    def multiple(self):
        return self.add(r"+")
    s = multiple

    def OR(self, value=None):
        self.add(r"|")
        return self.then(value) if value else self

    def range(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        quantifier = kwargs.pop('quantifier', None)
        r = []
        for arg in args:
            if isinstance(arg, str):
                r.append(self.escape(arg))
            else:
                r.append("-".join(arg))
        return self.add(r"[%s]" % ''.join(r), name=name, quantifier=quantifier)

    def ranges(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        r = []
        for arg in args:
            if isinstance(arg, str):
                r.append(self.escape(arg))
            else:
                r.append("-".join(arg))
        return self.add(r"[%s]+" % ''.join(r), name=name)

    def something(self, name=None, quantifier=None):
        return self.add(r"(?:.+)", name=name, quantifier=quantifier)

    def something_but(self, value, name=None, quantifier=None):
        return self.add("(?:[^" + self.escape(value) + "]+)", name=name, quantifier=quantifier)

    def start_of_line(self, enable=True):
        self.prefixes = "^" if enable else ""
        return self.add()

    def tab(self, quantifier=None):
        return self.add(r"\t", quantifier=quantifier)

    def whitespace(self, quantifier=None):
        return self.add(r"\s", quantifier=quantifier)

    def non_whitespace(self, quantifier=None):
        return self.add(r"\S", quantifier=quantifier)

    def then(self, value, name=None, quantifier=None):
        return self.add("(?:" + self.escape(value) + ")", name=name, quantifier=quantifier)
    find = then

    def word(self, name=None):
        return self.add(r"\w+", name=name)

    def non_word(self, name=None):
        return self.add(r"\W+")

    def char(self, name=None, quantifier=None):
        return self.add(r"\w", name=name, quantifier=quantifier)

    def non_char(self, name=None, quantifier=None):
        return self.add(r"\W", name=name, quantifier=quantifier)

    def dotall(self, enable=True):
        self._dotall = enable
        return self
    S = dotall

    def ignorecase(self, enable=True):
        self._ignorecase = enable
        return self
    I = ignorecase  # noqa

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

    def U(self, enable=True):
        return self.unicode(enable)

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
        if match:
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

    def __mul__(self, other):
        if isinstance(other, int):
            return HR().add(str(self) * other)
        raise TypeError(
            "unsupported operand type(s) for *: '%s' and '%s'" % (
                type(self).__name__,
                type(other).__name__
            )
        )

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

    def __int__(self):
        return reduce(or_, map(int, self or [0]))


class Flag(object):
    f_name = 'nill'

    def __init__(self, enable=True):
        self.enable = enable

    def f(self, hr):
        return getattr(HR, self.f_name)(hr, self.enable)

    def set(self, hr):
        self.f(hr)

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
        return self.f_name

    def __int__(self):
        return int(self.v)


class FS(Flag):
    v = re.S
    f_name = 'dotall'


class FI(Flag):
    v = re.I
    f_name = 'ignorecase'


class FL(Flag):
    v = re.L
    f_name = 'locale'


class FM(Flag):
    v = re.M
    f_name = 'multiline'


class FU(Flag):
    v = re.U
    f_name = 'unicode'


class FX(Flag):
    v = re.X
    f_name = 'verbose'


def ADD(value=None, name=None, quantifier=None):
    return HR().add(value, name=name, quantifier=quantifier)


RE = ADD


def T(value, name=None, quantifier=None):
    return HR().then(value, name=name, quantifier=quantifier)


def F(value, name=None, quantifier=None):
    return HR().find(value, name=name, quantifier=quantifier)


def G(value, name=None):
    return HR().group(value, name=name)


def A(value, name=None, quantifier=None):
    return HR().any(value, name=name, quantifier=quantifier)


def AT(name=None):
    return HR().anything(name=name)


def ATB(value, name=None):
    return HR().anything_but(value, name=name)


def EOL(enable=True):
    return HR().end_of_line(enable)


def MB(value, name=None):
    return HR().maybe(value)


def MTP():
    return HR().multiple()


def R(*args, **kwargs):
    return HR().range(*args, **kwargs)


def RS(*args, **kwargs):
    return HR().ranges(*args, **kwargs)


def ST(name=None):
    return HR().something(name=name)


def STB(value, name=None):
    return HR().something_but(value, name=name)


def SOL(enable=True):
    return HR().start_of_line(enable)


def BR():
    return HR().br()


def D(name=None, quantifier=None):
    return HR().digit(name=name, quantifier=quantifier)


def DS(name=None):
    return HR().digits(name=name)


def ID(name=None):
    return HR().int_or_decimal(name=name)


def ND(name=None, quantifier=None):
    return HR().non_digit(name=name, quantifier=quantifier)


def NDS(name=None):
    return HR().non_digits(name=name)


def TAB(quantifier=None):
    return HR().tab(quantifier=quantifier)


def WS(quantifier=None):
    return HR().whitespace(quantifier=quantifier)


def NWS(quantifier=None):
    return HR().non_whitespace(quantifier=quantifier)


def W(name=None):
    return HR().word(name=name)


def NW(name=None):
    return HR().non_word(name=name)


def C(name=None, quantifier=None):
    return HR().char(name=name, quantifier=quantifier)


def NC(name=None, quantifier=None):
    return HR().non_char(name=name, quantifier=quantifier)
