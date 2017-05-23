from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='word_ladder',
    version='0.0.1',
    description='Find path between two words, changing one letter each step',
    long_description=long_description,
    url='https://github.com/snebel29/word_ladder',
    author='Sven Nebel',
    author_email='nebel.sven@gmail.com',
    license='GPL',
    packages=['word_ladder'],
    tests_require=['nose'],
    zip_safe=False
)