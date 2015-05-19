HumanRegex
=======================

API to make it easier to use regex

``RE('your regex here')``

Returns a Callable object that facilitates verification of matches

It allows the combination of regex to form new regex using the operators & and |

Flags Support

It has a verbose api to create regex and with shortcuts, both supported the combinations


## Examples

### Testing if the string contains digits
```python
from humanregex import RE

my_re = RE('[0-9]+')
if bool(my_re('number: 25')):
    print 'Regex Ok'
# >> Regex Ok
my_match = my_re('number: 25')
if my_match[0] == '25':
    print '25'
# >> 25
if RE('(?P<number>[0-9]+)')('number: 25')['number'] == '25':
    print 'number 25'
# >> number 25
```

### Tests if the email is valid and captures the account and the provider
```python
my_re = RE(r'(?P<account>[A-Za-z0-9+_.]+)\@(?P<provider>[A-Za-z0-9]+)\..+')
my_match = my_re('my_email.1+github@Provider.com')
print my_match['account']
# >> my_email.1+github
print my_match['provider']
# >> Provider
```

### Replacing strings
```python
from humanregex import RE

print RE('(?:red)').replace("violets are red", 'blue')
# >> violets are blue
```

### Using verbal expressions for the same examples
```python
from humanregex import HumanRegex as HR

my_re = HR().digits()
if bool(my_re('number: 25')):
    print 'Regex Ok'
# >> Regex Ok
my_match = my_re('number: 25')
if my_match[0] == '25':
    print '25'
# >> 25
if HR().digits(name='number')('number: 25')['number'] == '25':
    print 'number 25'
# >> number 25

```

```python
from humanregex import HumanRegex as HR

az = ['a', 'z']
AZ = ['A', 'Z']
_09 = ['0', '9']
special = '_.+'

my_re = HR().ranges(
    AZ, az,
    _09, special,
    name='account'
).then('@').ranges(
    AZ, az, _09,
    name='provider'
).then('.').anything()
my_match = my_re('my_email.1+github@Provider.com')
print my_re
# >> (?P<account>([A-Za-z0-9\_\.\+]+))(?:\@)(?P<provider>([A-Za-z0-9]+))(?:\.)(?:.*)
print my_match['account']
# >> my_email.1+github
print my_match['provider']
# >> Provider
```

```python
from humanregex import HR

print HR().find('red').replace("violets are red", 'blue')
# >> violets are blue
```

### Combinations

```python
my_combination = RE('([0-9]{2})') | RE('([a-z]{2})')
print "regex: ", my_combination
# >> regex:  ([0-9]{2})|([a-z]{2})
print "av: ", my_combination('av: 159')[0]
# >> av:  av
print "01: ", my_combination('01: avsb')[0]
# >> 01:  01

x = HR().then('@').word(name='p')
y = HR().char(name='c').then('.')
my_combination = y & x
my_match = my_combination('x.@zokis')
print "regex: ", my_combination
# >> regex:  (?P<c>\w)(?:\.)(?:\@)(?P<p>\w+)
print "c: ", my_match['c']
# >> c:  x
print "p: ", my_match['p']
# >> p:  zokis
```


### Examples using shortcuts and combinations

```python
from humanregex import RS

my_re = DS()
print my_re
# >> \d+

if bool(my_re('number: 25')):
    print 'Regex Ok'
# >> Regex Ok
my_match = my_re('number: 25')
if my_match[0] == '25':
    print '25'
# >> 25

my_named_regex = DS(name='number')
print my_named_regex
# >> (?P<number>\d+)
if my_named_regex('number: 25')['number'] == '25':
    print 'number 25'
# >> number 25
```

```python
from humanregex import RS, T, AT

az = ['a', 'z']
AZ = ['A', 'Z']
_09 = ['0', '9']
special = '_.+'

my_re = RS(
    AZ, az, _09, special,
    name='account'
) & T('@') & RS(
    AZ, az, _09,
    name='provider'
) & AT()
my_match = my_re('my_email.1+github@Provider.com')
print my_re
# >> (?P<account>([A-Za-z0-9\_\.\+]+))(?:\@)(?P<provider>([A-Za-z0-9]+))(?:.*)
print my_match['account']
# >> my_email.1+github
print my_match['provider']
# >> Provider
```

```python
from humanregex import F

print F('red').replace("violets are red", 'blue')
# >> violets are blue
```

### FLAGs

```python
my_re = HR().find('cat')
my_match = my_re('CAT or dog')
print bool(my_match)
# >> False
my_re = my_re.ignorecase()
my_match = my_re('CAT or dog')
print bool(my_match)
# >> True

my_re = SOL() & F('DOG')
my_match = my_re('CAT or \ndog')
print bool(my_match)
# >> False
my_re = my_re & FI() | FM()
my_match = my_re('CAT or \ndog')
print bool(my_match)
# >> True
```


### Full API

 - column Shortcut: Shortcut Function or Flag Class
 - column Verbose: Verbose method => HR().x
 - column Example Shortcut: Example using the shortcut functions
 - column Resulting: resulting regex
 - column V: receives "value" as a parameter
 - column N: receives "name" as named parameter => Named groups

| Shortcut | Verbose         | Example Shortcut | Resulting                | V | N |
|----------|-----------------|------------------|--------------------------|---|---|
| ADD      | .add            | ADD('[0-9]+')    | ``[0-9]+              `` | ✓ | ✓ |
| RE       | .add            | RE('[0-9]+')     | ``[0-9]+              `` | ✓ | ✓ |
| T        | .then           | T('@')           | ``(?:\@)              `` | ✓ | ✓ |
| F        | .find           | F('blue')        | ``(?:blue)            `` | ✓ | ✓ |
| A        | .any            | A('0258qaz')     | ``[0258qaz]           `` | ✓ | ✓ |
| AT       | .anything       | AT()             | ``(?:.*)              `` | ✗ | ✓ |
| ATB      | .anything_but   | ATB('0258zaq')   | ``(?:[^0258zaq]*)     `` | ✓ | ✓ |
| EOL      | .end_of_line    | EOL()            | ``$                   `` | ✗ | ✗ |
| MB       | .maybe          | MB('s')          | ``(?:s)?              `` | ✓ | ✓ |
| MTP      | .multiple       | MTP()            | ``+                   `` | ✗ | ✗ |
| R        | .range          | R(['a', 'z'])    | ``([a-z])             `` | ✓ | ✓ |
| RS       | .ranges         | RS(['a', 'z'])   | ``([a-z]+)            `` | ✓ | ✓ |
| ST       | .something      | ST()             | ``(?:.+)              `` | ✗ | ✓ |
| STB      | .something_but  | STB('0258qaz')   | ``(?:[^0258qaz]+)     `` | ✓ | ✓ |
| SOL      | .start_of_line  | SOL()            | ``^                   `` | ✗ | ✗ |
| BR       | .br             | BR()             | ``(?:(?:\n)|(?:\r\n)) `` | ✗ | ✗ |
| D        | .digit          | D()              | ``\d                  `` | ✗ | ✓ |
| DS       | .digits         | DS()             | ``\d+                 `` | ✗ | ✓ |
| ND       | .non_digit      | ND()             | ``\D                  `` | ✗ | ✓ |
| NDS      | .non_digits     | NDS()            | ``\D+                 `` | ✗ | ✓ |
| TAB      | .tab            | TAB()            | ``\t                  `` | ✗ | ✗ |
| WS       | .whitespace     | WS()             | ``\s                  `` | ✗ | ✗ |
| NWS      | .non_whitespace | NWS()            | ``\S                  `` | ✗ | ✗ |
| W        | .word           | W()              | ``\w+                 `` | ✗ | ✓ |
| NW       | .non_word       | NW()             | ``\W+                 `` | ✗ | ✓ |
| C        | .char           | C()              | ``\w                  `` | ✗ | ✓ |
| NC       | .non_char       | NC()             | ``\W                  `` | ✗ | ✓ |
| FS       | .dotall/.S      | FS()             | Flag dotall enabled      | ✗ | ✗ |
| FI       | .ignorecase/.I  | FI()             | Flag ignorecase enabled  | ✗ | ✗ |
| FL       | .locale/.L      | FL()             | Flag locale enabled      | ✗ | ✗ |
| FM       | .multiline/.M   | FM()             | Flag multiline enabled   | ✗ | ✗ |
| FU       | .unicode/.U     | FU()             | Flag unicode enabled     | ✗ | ✗ |
| FX       | .verbose/.X     | FX()             | Flag verbose enabled     | ✗ | ✗ |

Other methods of regex object

| Method     | Description
|------------|---------------
| .get_flags | returns an integer with the value of the flags
| .compile   | same as re.compile
| .findall   | same as re.findall
| .groups    | same as re.groups
| .groupdict | return a match object => a defaultdict(None) Like that contains all the results of a match
| .match     | same as re.match
| .replace   | return the string obtained by replacing
| .search    | same as re.search
| .split     | same as re.split
| .test      | returns true if the result of .findall have size greater than 0
