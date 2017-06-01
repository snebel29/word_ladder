"""
Word ladder

Usage:
  word_ladder from <from> using <dict_file> [-a]
  word_ladder from <from> to <to> using <dict_file> [-a]
  word_ladder -h | --help
  word_ladder -v | --version

Subcommands:
  from              The initial word
  to                The word to stop [Optional]

Options:
  -a, --all-paths    Print all paths
  -h, --help         Show this screen
  -v, --version      Show version

Examples:
  word_ladder from word1 using /english.dict
  word_ladder from word1 using /english.dict --all-paths
  word_ladder from word1 to word2 using /english.dict -a
"""

import sys
from docopt import docopt
from word_ladder import WordLadder, __version__

def _run(args):
    result = WordLadder(
        args['<dict_file>']).find_path(
            args['<from>'],
            args['<to>'],
            bool(args['--all-paths']
        )
    )

    return result

def _parse_args(args=sys.argv[1:]):
    return docopt(__doc__, args, version=__version__)

def run():
    print('path: {0}'.format(_run(_parse_args())))

if __name__ == '__main__':
    run()

