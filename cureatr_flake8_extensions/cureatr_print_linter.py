"""Cureatrs extension for flake8 that finds usage of print."""
import re
import ast
import tokenize
import re
from sys import stdin

__version__ = '1.3'


class CureatrPrintLinter(object):
    """Cureatr Flake8 Print checker."""
    name = 'cureatr-flake8-print'
    version = __version__
    off_by_default = True

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--ignore-path-regex', default='', action='store',
                          type='string', help="Ignore Print Statement Directories")
        parser.config_options.append('ignore-path-regex')

    @classmethod
    def parse_options(cls, options):
        cls.ignore_path_regex = re.compile(options.ignore_path_regex) if options.ignore_path_regex else None

    def run(self):
        if self.ignore_path_regex:
            if re.search(self.ignore_path_regex, self.filename):
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
