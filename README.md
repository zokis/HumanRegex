HumanRegex
=======================


## Examples

### Testing if the string contains digits
```python
from humanregex import RE

my_regex = RE('[0-9]+')
if bool(my_regex('number: 25')):
    print 'Regex Ok'
# >> Regex Ok
my_match = my_regex('number: 25')
if my_match[0] == '25':
    print '25'
# >> 25
if RE('(?P<number>[0-9]+)')('number: 25')['number'] == '25':
    print 'number 25'
# >> number 25
```
### Tests if the email is valid and captures the account and the provider
```python
my_regex = RE(r'(?P<account>([A-Za-z0-9\+\_\.]+))(?:\@)(?P<provider>([A-Za-z0-9]+))(?:\.)(?:.+)')
my_match = my_regex('my_email.1+github@Provider.com')
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

my_regex = HR().digits()
if bool(my_regex('number: 25')):
    print 'Regex Ok'
    # >> Regex Ok
my_match = my_regex('number: 25')
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

my_regex = HR().ranges(
    AZ, az,
    _09, special,
    name='account'
).then('@').ranges(
    AZ, az, _09,
    name='provider'
).then('.').anything()
my_match = my_regex('my_email.1+github@Provider.com')
print my_regex
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

### Os mesmos exemplos mas usando atalhos e combinações

```python
from humanregex import RS

my_regex = RS(['0', '9'])
print my_regex
# >> ([0-9]+)

if bool(my_regex('number: 25')):
    print 'Regex Ok'
    # >> Regex Ok
my_match = my_regex('number: 25')
if my_match[0] == '25':
    print '25'
    # >> 25

my_named_regex = RS(['0', '9'], name='number')
print my_named_regex
# >> (?P<number>([0-9]+))
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

my_regex = RS(
    AZ, az, _09, special,
    name='account'
) & T('@') & RS(
    AZ, az, _09,
    name='provider'
) & AT()
my_match = my_regex('my_email.1+github@Provider.com')
print my_regex
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
