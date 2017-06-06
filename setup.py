import os
from setuptools import setup
from word_ladder import __version__

my_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(my_dir, 'README.rst')) as f:
    long_description = f.read()

with open(os.path.join(my_dir, 'docs/docs_requirements.txt')) as f:
    doc_requirements = f.read().splitlines()

requirements = ['docopt']
dev_requirements = ['nose'] + doc_requirements

setup(
    name='word-ladder',
    packages=['word_ladder'],
    version=__version__,
    description='Word ladder find path between two words, changing one letter each step',
    long_description=long_description,
    url='https://github.com/snebel29/word_ladder',
    author='Sven Nebel',
    author_email='nebel.sven@gmail.com',
    license='GPL',
    keywords=['word', 'ladder'],
    download_url='https://github.com/snebel29/word_ladder/archive/{0}.tar.gz'.format(__version__),
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    zip_safe=False,
    entry_points={
        'console_scripts': ['word_ladder=word_ladder.cli:run']
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX',
    ]
)
