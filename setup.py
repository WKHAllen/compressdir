from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'compressdir',
    packages = ['compressdir'],
    version = '0.1.0',
    license = 'MIT',
    description = 'File/Directory compression',
    long_description = long_description,
    author = 'Will Allen',
    author_email = 'wkhallen@gmail.com',
    url = 'https://github.com/WKHAllen/compressdir',
    keywords = ['compression', 'decompression', 'files', 'directories'],
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: System :: Archiving :: Compression',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
