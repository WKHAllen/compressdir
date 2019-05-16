import os
from setuptools import setup

setup(
    name = 'compressdir',
    packages = ['compressdir'],
    version = '0.1.2',
    license = 'MIT',
    description = 'File/directory compression',
    long_description = ''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type = 'text/markdown',
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
