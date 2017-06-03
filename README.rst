Word Ladder
===========

Find path from one word to another, changing one letter each step, and
each intermediate word must be in the dictionary, the dictionary is a
text file with words separated by a line break like the one found in
``/usr/share/dict/words``

Prerequisites
-------------

-  Python 3.4 and Linux
-  List of words separated by newlines
-  Virtual environment is recommended

Documentation
-------------

- http://word-ladder.readthedocs.io/en/latest/

Installing
----------

Clone the repository (Pypi package comming soon)

.. code:: bash

    $ git clone git@github.com:snebel29/word_ladder.git
    $ cd word_ladder

Production
~~~~~~~~~~

.. code:: bash

    $ pip install .

Development
~~~~~~~~~~~

.. code:: bash

    $ pip install -e .[dev]

Getting started
---------------

The word\_ladder packges commes with both, a command line tool and a
module that can be used to find word ladder paths

Command line tool
~~~~~~~~~~~~~~~~~

Once installed you can use the command line interface

.. code:: bash

    $ word_ladder -h


Python module
~~~~~~~~~~~~~

You can import and use the module directly as well

.. code:: python

    >>> from word_ladder import WordLadder
    >>> wl = WordLadder('tests/word_lists/linux_english_words')
    >>> wl.find_path('fear', 'sail')
    ['fear', 'hear', 'heir', 'hair', 'hail', 'sail']
    >>> wl.find_path('Abe', 'sail')
    ['Abe', 'be', 'bed', 'bid', 'aid', 'said', 'sail']
    >>> wl.find_path('Am', 'sail')
    ['Am', 'am', 'aim', 'ail', 'sail']

Running the tests
-----------------

You will have to use nose to run the tests

.. code:: bash

    $ nosetests

References
----------

-  https://bradfieldcs.com/algos/graphs/word-ladder/