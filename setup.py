# coding: utf-8
from setuptools import setup


setup(
    name='hre',
    version='0.1.0',
    description='helper for manipulating regex.',
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
