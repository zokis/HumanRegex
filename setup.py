# coding: utf-8
from setuptools import setup

version = __import__('hre').__version__

setup(
    name='hre',
    version=version,
    description='hre (Human Regex) is an API to make it easier to use Regex.',
    long_description='''hre (Human Regex) is an API to make it easier to use Regex.
DOCS: https://github.com/zokis/HumanRegex/blob/master/README.md
DOCS RAW: https://raw.githubusercontent.com/zokis/HumanRegex/master/README.md''',
    url='https://github.com/zokis/HumanRegex/',
    author='Marcelo Fonseca Tambalo',
    author_email='marcelo.zokis@gmail.com',
    license='MIT',
    py_modules=['hre'],
    scripts=['hre.py'],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
