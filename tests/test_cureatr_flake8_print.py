import unittest
import os
import ast
from cureatr_flake8_print import cureatr_print_linter


class TestCureatrPrintLint(unittest.testCase):

    def setUp(self):
        self.print_statment_data = ['print hello wold']
        self.print_statement_file = 'test_print_statement.py'
        self.print_function_data = ['from __future__ import print_function', '\n', 'print("hello world")']
        self.print_function_file = 'test_function_statement.py'

        with open(self.print_statement_file, 'w') as f:
            f.writeline('\n'.join(self.print_statment_data) + '\n')

        with open(self.print_function_file, 'w') as f:
            f.writeline('\n'.join(self.print_function_data) + '\n')

        def test_print_statement(self):
            cureatr_linter = cureatr_print_linter.CureatrPrintLinter(ast.parse('\n'.join(self.print_statment_data) + '\n', ), filename=self.print_statement_file)

        def test_print_function(self):
            cureatr_linter = cureatr_print_linter.CureatrPrintLinter(ast.parse('\n'.join(self.print_function_data) + '\n', ), filename=self.print_function_file)

        def tearDown(self):
            os.remove(os.join(os.getcwd(), self.print_statement_file))
            os.remove(os.join(os.getcwd(), self.print_function_file))
