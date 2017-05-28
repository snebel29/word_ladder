import unittest
from nose.tools import raises
from nose.tools import ok_, eq_
from word_ladder.cli import main, run, parse_args


class TestCli(unittest.TestCase):

    @raises(SystemExit)
    def test_cli_with_no_arguments_should_fail(self):
        parse_args()

    @raises(SystemExit)
    def test_main_as_seen_from_setup_tools(self):
        main()

    def test_cli_with_arguments_should_parse(self):
        args = parse_args(['from', 'fear', 'to' , 'sail', 'using', 'file'])
        ok_(isinstance(args, dict))
        eq_(args['<from>'], 'fear')
        eq_(args['<to>'], 'sail')
        eq_(args['<dict_file>'], 'file')

    def test_cli_triggers_find_path_method(self):
        args = {
          "--all-paths": False,
          "--help": False,
          "--version": False,
          "<dict_file>": ['ola', 'olo'],
          "<from>": "ola",
          "<to>": "olo",
          "from": True,
          "to": True,
          "using": True
        }

        eq_(run(args), ['ola', 'olo'])







