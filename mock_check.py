from __future__ import with_statement
from __future__ import print_function

import itertools
import sys
from collections import defaultdict
try:
    import ast
    from ast import iter_child_nodes
except ImportError:   # Python 2.5
    from flake8.util import ast, iter_child_nodes

__version__ = '0.1'


class FuncMockArgsDecoratorsChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def _get_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return self._get_name(node.value) + "." + node.attr
        return ""

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

        mock_decs = [
            decorator.args[0].s.split(".")[-1]
            for decorator in reversed(node.decorator_list)
            if (isinstance(decorator, ast.Call) and
                self._get_name(decorator.func) == "mock.patch")
        ]

        mock_args = [arg.id[len("mock_"):] for arg in node.args.args
                     if arg.id.startswith("mock_")]

        for arg, dec in itertools.izip_longest(mock_args, mock_decs):
            if arg is None or dec is None or not dec.startswith(arg):
                self.errors.append((node.lineno, mock_args, mock_decs))
                break


class MockChecker(object):
    """Check that mock arguments are correct against decorators."""
    name = 'mock-checker'
    version = __version__
    _error_tmpl = "C902 Invalid mocks and/or args (args: %r, mocks: %r)"

    def __init__(self, tree, filename=None):
        self.tree = tree

    def run(self):
        visitor = FuncMockArgsDecoratorsChecker()
        visitor.visit(self.tree)
        for lineno, args, decs in visitor.errors:
            text = self._error_tmpl % (args, decs)
            yield lineno, 0, text, type(self)
