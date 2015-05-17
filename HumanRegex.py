__title__ = 'HumanRegex'
__version__ = '0.1.0'
__author__ = 'Marcelo Fonseca Tambalo'


import re


class HumanRegex(object):
    def __init__(self):
        self.pattern = ''
        self.prefixes = ''
        self.source = ''
        self.suffixes = ''

        self.end_of_line_called = False
        self.start_of_line_called = False

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

    def any(self):
        return self.add("[" + re.escape(value) + "]");

    def anything(self):
        return self.add("(?:.*)")

    def anything_but(self, value):
        return self.add("(?:[^" + re.escape(value) + "]*)")

    def br(self):
        return self.add(r"(?:(?:\n)|(?:\r\n))")

    def end_of_line(self, enable=True):
        if not self.end_of_line_called:
            self.end_of_line_called = True
            self.suffixes = enable and "$" or "";
            return self.add()
        raise Exception()

    def find(self, value):
        return self.then(value)

    def maybe(self, value):
        return self.add("(?:" + re.escape(value) + ")?")

    def multiple(self, value):
        if not value.startswith('*') or not value.startssith('*'):
            self.add("+")
        return self.add(value)

    def something(self):
        return self.add("(?:.+)")

    def something_but(self, value):
        return self.add("(?:[^" + re.escape(value) + "]+)")

    def start_of_line(self, enable=True):
        if not self.start_of_line_called:
            self.start_of_line_called = True
            self.prefixes = enable and "^" or "";
            return self.add()
        raise Exception()

    def tab(self):
        return self.add(r"\t")

    def then(self, value):
        return self.add("(?:" + re.escape(value) + ")")

    def word(self):
        return self.add(r"\w+")

    def dotall(self, enable=True):
        self._dotall = enable

    def ignorecase(self, enable=True):
        self._ignorecase = enable

    def locale(self, enable=True):
        self._locale = enable

    def multiline(self, enable=True):
        self._multiline = enable

    def unicode(self, enable=True):
        self._unicode = enable

    def verbose(self, enable=True):
        self._verbose = enable

    def get_flags(self):
        flag = 0
        if self._dotall:
            flag = flag | re.DOTALL
        if self._ignorecase:
            flag = flag | re.IGNORECASE
        if self._locale:
            flag = flag | re.LOCALE
        if self._multiline:
            flag = flag | re.MULTILINE
        if self._unicode:
            flag = flag | re.UNICODE
        if self._verbose:
            flag = flag | re.VERBOSE
        return flag

    def compile(self):
        return re.compile(str(self), self.get_flags())

    def groups(self, string):
        return self.search().groups()

    def groupdict(self, string):
        return self.search().groupdict()

    def match(self, string):
        return self.compile().match(string)

    def search(self, string):
        return self.compile().search(string)

    def test(self, string):
        return True if self.match(string) else False


    def __str__(self):
        return r"%s" % self.pattern


if __name__ == '__main__':
    expression = HumanRegex()\
      .start_of_line()\
      .then("http")\
      .maybe("s")\
      .then("://")\
      .maybe("www.")\
      .anything_but(" ")\
      .end_of_line()
    print str(expression)
