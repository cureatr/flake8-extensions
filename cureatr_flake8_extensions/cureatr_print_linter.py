"""Cureatrs extension for flake8 that finds usage of print."""
import re
import ast
import tokenize
from sys import stdin

__version__ = '1.4'


class CureatrPrintLinter(object):
    """Cureatr Flake8 Print checker."""
    name = 'cureatr-flake8-print'
    version = __version__
    print_statement_code = 'T002'
    print_function_code = 'T003'

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--ignore-path-regex', default='', action='store', parse_from_config=True,
                          type='string', help="Ignore Print Statement Directories")
        parser.add_option('--enable-extension', default='', action='store', parse_from_config=True,
                          type='string', help="Enables print check extension.")

    @classmethod
    def parse_options(cls, options):
        cls.ignore_path_regex = re.compile(options.ignore_path_regex) if options.ignore_path_regex else None
        cls.enable_extension = [option for option in options.enable_extension.split(',')] if options.enable_extension else list()

    def run(self):
        if self.ignore_path_regex:
            if re.search(self.ignore_path_regex, self.filename):
                return
        if self.filename == stdin:
            noqa = self.get_noqa_lines(self.filename)
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
            if isinstance(node, ast.Call) and hasattr(node.func, 'id') and self.print_function_code in self.enable_extension:
                if node.func.id == 'print':
                    errors.append({
                        'message': self.format_debugger_message(self.print_function_code, 'print function found.'),
                        'line': node.lineno,
                        'col': node.col_offset,
                    })
            if isinstance(node, ast.Print) and self.print_statement_code in self.enable_extension:
                errors.append({
                    'message': self.format_debugger_message(self.print_statement_code, 'print statement found.'),
                    'line': node.lineno,
                    'col': node.col_offset,
                })
        return errors
