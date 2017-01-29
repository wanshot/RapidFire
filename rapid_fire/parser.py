import ast
import inspect

import __future__
PyCF_MASK = sum(v for k, v in vars(__future__).items() if k.startswith('CO_FUTURE'))


class ParsePyFile(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.functions = self.load_function()
        self.code_obj = None

    def load_pyfile(self):
        file_name = self.file_path
        with open(file_name, 'r') as f:
            code = f.read()
        return code

    def load_function(self):
        function_info = []

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                function_info.append((node.name, ast.get_docstring(node)))
        exprs = ast.parse(self.load_pyfile(), self.file_path)
        _Transform().visit(exprs)
        # TODO funcitons overlap raise
        return function_info

    def set_code_obj(self, func_name):

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                if node.name == func_name:
                    return node

        exprs = ast.parse(self.load_pyfile(), self.file_path)
        _Transform().visit(exprs)
        self.code_obj = compile(exprs, self.file_path, 'exec')

    def run(self):
        exec(self.code_obj)

    def set_rf_module(self, code_obj):
        """set import module code
        """
        source = self._uncompile(code_obj)
        s = ['from rapid_fire import render']
        s.extend(source)
        exprs = ''
        for line in s:
            exprs += line + '\n'
        self.code_obj = compile(exprs, '<rf>', 'exec')

    def _uncompile(self, code_obj):
        """uncompile(codeobj) -> source
        """
        if code_obj.co_flags & inspect.CO_NESTED or code_obj.co_freevars:
            # XXX
            raise TypeError('nested functions not supported')
        if code_obj.co_name == '<lambda>':
            raise TypeError('lambda functions not supported')
        if code_obj.co_filename == '<string>':
            raise TypeError('code without source file not supported')

        try:
            lines = inspect.getsourcelines(code_obj)[0]
        except IOError:
            # XXX
            raise TypeError('source code not available')

        return lines
