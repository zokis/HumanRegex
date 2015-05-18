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
        for args in args:
            self.add("([" + "-".join(args) + "])")
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


HR = HumanRegex

if __name__ == '__main__':

    with HR().then('cat').OR('dog') as expression:
        print expression.test('cat')
        print expression.test('dog')
        print expression.test('rat')

    print HR().find("red").replace("violets are red", "blue")

    print HR().add(r'\W+').split('Words, words, words.')
