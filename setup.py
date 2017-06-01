from setuptools import setup
from word_ladder import __version__


with open('README.rst') as f:
    long_description = f.read()

requirements = ['docopt']
dev_requirements = ['nose', 'sphinx', 'sphinxcontrib-napoleon', 'sphinx_rtd_theme']

setup(
    name='word_ladder',
    version=__version__,
    description='Find path between two words, changing one letter each step',
    long_description=long_description,
    url='https://github.com/snebel29/word_ladder',
    author='Sven Nebel',
    author_email='nebel.sven@gmail.com',
    license='GPL',
    packages=['word_ladder'],
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    zip_safe=False,
    entry_points={
        'console_scripts': ['word_ladder=word_ladder.cli:run']
    }
)