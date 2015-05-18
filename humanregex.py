import re

__title__ = 'HumanRegex'
__version__ = '0.1.0'
__author__ = 'Marcelo Fonseca Tambalo'


class HumanRegex(object):
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

    def end_of_line(self, enable=True):
        self.suffixes = "$" if enable else ""
        return self.add()

    def maybe(self, value):
        return self.add("(?:" + re.escape(value) + ")?")

    def multiple(self, value):
        if not value.startswith('*') or not value.startswith('*'):
            self.add("+")
        return self.add(value)

    def OR(self, value=None):
        self.add("|")
        return self.then(value) if value else self

    def range(self, *args):
        for args in args:
            self.add("([" + '-'.join(args) + "])")
        return self

    def something(self):
        return self.add("(?:.+)")

    def something_but(self, value):
        return self.add("(?:[^" + re.escape(value) + "]+)")

    def start_of_line(self, enable=True):
        self.prefixes = "^" if enable else ""
        return self.add()

    def tab(self):
        return self.add(r"\t")

    def then(self, value):
        return self.add("(?:" + re.escape(value) + ")")
    find = then

    def word(self):
        return self.add(r"\w+")

    def dotall(self, enable=True):
        self._dotall = enable
    S = dotall

    def ignorecase(self, enable=True):
        self._ignorecase = enable
    I = ignorecase

    def locale(self, enable=True):
        self._locale = enable
    L = locale

    def multiline(self, enable=True):
        self._multiline = enable
    M = multiline

    def unicode(self, enable=True):
        self._unicode = enable

    def U(self, enable=True): return self.unicode(enable)

    def verbose(self, enable=True):
        self._verbose = enable
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

    def test(self, string):
        return True if self.match(string) else False

    def __str__(self):
        return r"%s" % self.pattern


HR = HumanRegex

if __name__ == '__main__':
    expression = HR()\
        .start_of_line()\
        .then("http")\
        .maybe("s")\
        .then("://")\
        .maybe("www.")\
        .anything_but(" ")\
        .end_of_line()

    e1 = HR()\
        .start_of_line()\
        .then('b')\
        .any('aeiou')\
        .then('t')\
        .end_of_line()

    e2 = HR().then('cat').OR('dog')
    print str(e2)

    print HR().find("roses").replace(
        HR().find("red").replace(
            "roses are red",
            "blue"
        ),
        'violets'
    )

    print str(HR().start_of_line().range(['a', 'b'], ['X', 'Z']))
