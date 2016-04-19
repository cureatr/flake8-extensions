"""Cureatrs extension for flake8 that finds usage of print."""
import re
import ast
import tokenize
from sys import stdin

__version__ = '1.0'


class CureatrPrintLinter(object):
    """Cureatr Flake8 Print checker."""
    name = 'cureatr-flake8-print'
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--ignore-dirs', default='', action='store',
                          type='string', help="Ignore Print Statement Directories")
        parser.config_options.append('ignore-dirs')

    @classmethod
    def parse_options(cls, options):
        cls.ignore_dirs = options.ignore_dirs.split(',') if options.ignore_dirs else []

    def run(self):
        if any([directory in self.filename for directory in self.ignore_dirs]):
            return
        if self.filename == stdin:
            noqa = get_noqa_lines(self.filename)
        else:
            with open(self.filename, 'r') as file_to_check:
                noqa = self.get_noqa_lines(file_to_check.readlines())

        errors = self.check_tree_for_debugger_statements(self.tree, noqa)
        for error in errors:
            yield (error.get("line"), error.get("col"), error.get("message"), type(self))

    def get_noqa_lines(self, code):
        tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
        noqa = [token[2][0] for token in tokens if token[0] == tokenize.COMMENT and (token[1].endswith('noqa') or (isinstance(token[0], str) and token[0].endswith('noqa')))]
        return noqa

    def check_code_for_debugger_statements(self, code):
        tree = ast.parse(code)
        noqa = self.get_noqa_lines(code.split("\n"))
        return self.check_tree_for_debugger_statements(tree, noqa)

    def format_debugger_message(self, error_code, message):
        return '{} {}'.format(error_code, message)

    def check_tree_for_debugger_statements(self, tree, noqa):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and hasattr(node.func, 'id'):
                if node.func.id == 'print':
                    errors.append({
                        'message': self.format_debugger_message('T003', 'print function found.'),
                        'line': node.lineno,
                        'col': node.col_offset,
                    })
            if isinstance(node, ast.Print):
                errors.append({
                    'message': self.format_debugger_message('T002', 'print statement found.'),
                    'line': node.lineno,
                    'col': node.col_offset,
                })
        return errors
