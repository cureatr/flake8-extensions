import unittest
import os
import ast
import re
from cureatr_flake8_extensions import cureatr_print_linter


class TestCureatrPrintLint(unittest.TestCase):

    def setUp(self):
        self.print_statement_data = ['print "hello world"']
        self.print_statement_file = 'test_print_statement.py'
        self.print_function_data = ['from __future__ import print_function', '\n', 'print("hello world")']
        self.print_function_file = 'test_function_statement.py'
        self.print_ignore_file = 'reporting/tests_ignore.py'
        self.ignore_argument = 'tests,tools,reporting'
        os.mkdir('reporting')

        with open(self.print_statement_file, 'w') as f:
            f.writelines('\n'.join(self.print_statement_data) + '\n')

        with open(self.print_function_file, 'w') as f:
            f.writelines('\n'.join(self.print_function_data) + '\n')

        with open(self.print_ignore_file, 'w') as f:
            f.writelines('\n'.join(self.print_statement_data) + '\n')

    def test_print_statement(self):
        cureatr_linter = cureatr_print_linter.CureatrPrintLinter(ast.parse('\n'.join(self.print_statement_data) + '\n', ), filename=self.print_statement_file)
        cureatr_linter.ignore_printcheck_dirs = re.compile('|'.join(['^{}|/{}/'.format(option, option) for option in self.ignore_argument.split(',')])) if self.ignore_argument else None
        self.assertIn('T002 print statement found.', next(cureatr_linter.run()))

    def test_print_function(self):
        cureatr_linter = cureatr_print_linter.CureatrPrintLinter(ast.parse('\n'.join(self.print_function_data) + '\n', ), filename=self.print_function_file)
        cureatr_linter.ignore_printcheck_dirs = re.compile('|'.join(['^{}|/{}/'.format(option, option) for option in self.ignore_argument.split(',')])) if self.ignore_argument else None
        self.assertIn('T003 print function found.', next(cureatr_linter.run()))

    def test_ignore_dirs(self):
        cureatr_linter = cureatr_print_linter.CureatrPrintLinter(ast.parse('\n'.join(self.print_function_data) + '\n', ), filename=self.print_ignore_file)
        cureatr_linter.ignore_printcheck_dirs = re.compile('|'.join(['^{}|/{}/'.format(option, option) for option in self.ignore_argument.split(',')])) if self.ignore_argument else None
        self.assertEqual(len(list(cureatr_linter.run())), 0)

    def test_no_arg(self):
        self.ignore_argument = ''
        cureatr_linter = cureatr_print_linter.CureatrPrintLinter(ast.parse('\n'.join(self.print_statement_data) + '\n', ), filename=self.print_ignore_file)
        cureatr_linter.ignore_printcheck_dirs = re.compile('|'.join(['^{}|/{}/'.format(option, option) for option in self.ignore_argument.split(',')])) if self.ignore_argument else None
        self.assertIn('T002 print statement found.', next(cureatr_linter.run()))

    def tearDown(self):
        os.remove(os.path.join(os.getcwd(), self.print_statement_file))
        os.remove(os.path.join(os.getcwd(), self.print_function_file))
        os.remove(os.path.join(os.getcwd(), self.print_ignore_file))
        os.rmdir(os.path.join(os.getcwd(), 'reporting'))

if __name__ == '__main__':
    unittest.main()
