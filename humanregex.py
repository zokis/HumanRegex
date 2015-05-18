import re

__title__ = 'HumanRegex'
__version__ = '0.1.0'
__author__ = 'Marcelo Fonseca Tambalo'


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

    def add(self, value=None):
        if value:
            self.source += value
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

    def range(self, *args):
        f = r"([%s])"
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

    def groups(self, string):
        return self.search().groups()

    def groupdict(self, string):
        return self.search().groupdict()

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
        return True if self.match(string) else False

    def __str__(self):
        return r"%s" % self.pattern

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self

    def _combine(self, other, op='AND'):
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
        return super(Flag, self).__and__(other)

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


def ADD(value): return HR().add(value)


def T(value): return HR().then(value)


def F(value): return HR().then(value)


def A(value): return HR().any(value)


def AT(): return HR().anything()


def ATB(value): return HR().anything_but(value)


def EOL(): return HR().end_of_line()


def MB(value): return HR().maybe(value)


def MTP(): return HR().multiple()


def R(*args): return HR().range(*args)


def ST(value): return HR().something(value)


def STB(value): return HR().something_but(value)


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

    # with HR().then('cat').OR('dog') as expression:
    #     print expression.test('cat')
    #     print expression.test('dog')
    #     print expression.test('rat')

    # print T('cat') | T('dog')

    # print HR().find("red").replace("violets are red", "blue")

    # print (FI() | F("RED")).replace("violets are red", "blue")

    # print HR().add(r'\W+').split('Words, words, words.')

    # x = (SOL() & T('http') & MB('S') & FI() | FS() & T('://') & MB('www.') & ATB(' ') & EOL())
    # print x.get_flags()
    # print x
    # x = (HR().start_of_line().then('http').maybe('s').I().S().then('://').maybe('www.').anything_but(' ').end_of_line())
    # print x.get_flags()
    # print x

    # print (FI() | FS() | FX()) & T('g')

    # email1 = HR().I().range(['A', 'Z'], ['0', '9'], '.', '_').multiple().then('@').range(['A', 'Z'], ['0', '9']).multiple().then('.').anything()
    # print email1
    # print email1.test("marcelo@Zokis.com")

    az09s = R(['A', 'Z'], ['0', '9'], '.', '_') & MTP()
    email2 = FI() & az09s & T('@') & az09s & T('.') & az09s
    print email2
    print email2.test("marcelo.zokis@gmail.com")
