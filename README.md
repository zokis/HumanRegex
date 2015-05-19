Welcome to HumanRegex
=====================

Quickstart
==========


Test regex
```python
if bool(RE('[0-9]+')('number: 25')):
    print 'Regex Ok'
    # >> Regex Ok
if RE('[0-9]+')('number: 25')[0] == '25':
    print '25'
    # >> 25
if RE('[0-9]+', name='number')('number: 25')['number'] == '25':
    print 'number 25'
    # >> number 25
```

More complex regex
(?P<account>([A-Za-z0-9\+\_\.]+))(?:\@)(?P<provider>([A-Za-z0-9]+))(?:\.)(?:.+)

```python
email_re = RS(
        ['A', 'Z'], ['a', 'z'], ['0', '9'], '+_.',
        name='account'
    ) & T('@') & RS(
        ['A', 'Z'], ['a', 'z'], ['0', '9'],
        name='provider'
    ) & T('.') & ST()
email_match = email_re('my_email.1+github@Provider.com')
print email_re
# >> (?P<account>([A-Za-z0-9\+\_\.]+))(?:\@)(?P<provider>([A-Za-z0-9]+))(?:\.)(?:.+)
print email_match['account']
# >> my_email.1+github
print email_match['provider']
# >> Provider

# --- OR ---

email_re = HR().ranges(
        ['A', 'Z'], ['a', 'z'], ['0', '9'], '+_.',
        name='account'
    ).then('@').ranges(
        ['A', 'Z'], ['a', 'z'], ['0', '9'],
        name='provider'
    ).then('.').something()
email_match = email_re('my_email.2@provider.com.br')
print email_re
# >> (?P<account>([A-Za-z0-9\+\_\.]+))(?:\@)(?P<provider>([A-Za-z0-9]+))(?:\.)(?:.+)
print email_match['account']
# >> my_email.2
print email_match['provider']
# >> provider
```

Flags

```python
simple_email_re = FI() & W(name='account') & (
        FS() | FM() | FU()
    ) & T('@') & W(name='provider') & T('.') & W()
simple_email_match = simple_email_re('my_email_3@prOvider.com')
print simple_email_match['account']
# >> my_email_3
print simple_email_match['provider']
# >> prOvider

# --- OR ---

simple_email_re = HumanRegex().ignorecase().word(
        name='account'
    ).dotall().multiline().unicode().then('@').word(
        name='provider'
    ).then('.').word()
simple_email_match = simple_email_re('my_email_4@proVider.com')
print simple_email_match['account']
# >> my_email_4
print simple_email_match['provider']
# >> proVider

# --- OR ---

simple_email_re = HR().I().word(
        name='account'
    ).S().M().U().then('@').word(
        name='provider'
    ).then('.').word()
simple_email_match = simple_email_re('my_email_5@provIder.com')
print simple_email_match['account']
# >> my_email_3
print simple_email_match['provider']
# >> provIder
```


LIST:

    ADD .add
    RE  .add
    T   .then
    F   .find
    A   .any
    AT  .anything  
    ATB .anything_but
    EOL .end_of_line
    MB  .maybe
    MTP .multiple
    R   .range
    RS  .ranges
    ST  .something
    STB .something_but
    SOL .start_of_line
    BR  .br
    D   .digit
    DS  .digits
    ND  .non_digit
    NDS .non_digits
    TAB .tab
    WS  .whitespace
    NWS .non_whitespace
    W   .word
    NW  .non_word
    C   .char
    NC  .non_char

    FS .dotall      .S
    FI .ignorecase  .I
    FL .locale      .L
    FM .multiline   .M
    FU .unicode     .U
    FX .verbose     .X
