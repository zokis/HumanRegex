# coding: utf-8
from setuptools import setup

version = __import__('hre').__version__

setup(
    name='hre',
    version=version,
    description='hre (Human Regex) is an API to make it easier to use Regex.',
    long_description='hre (Human Regex) is an API to make it easier to use Regex.',
    url='https://github.com/zokis/HumanRegex/',
    author='Marcelo Fonseca Tambalo',
    author_email='marcelo.zokis@gmail.com',
    license='MIT',
    py_modules=['hre'],
    scripts=['hre.py'],
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
