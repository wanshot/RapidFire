import ast
import inspect
from collections import namedtuple

import __future__
PyCF_MASK = sum(v for k, v in vars(__future__).items() if k.startswith('CO_FUTURE'))


class ParsePyFile(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.funcname2docstring, self.imports = self.load_code()
        self.code_obj = None

    def load_pyfile(self):
        file_name = self.file_path
        with open(file_name, 'r') as f:
            code = f.read()
        return code

    def load_code(self):
        Import = namedtuple('Import', ['module', 'name', 'asname'])
        imports = []
        funcname2docstring = []

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                funcname2docstring.append((node.name, ast.get_docstring(node)))

            def visit_ImportFrom(self, node):
                for n in node.names:
                    imports.append(Import(node.module.split('.'),
                                          n.name.split('.'),
                                          n.asname))

            def visit_Import(self, node):
                for n in node.names:
                    imports.append(Import([],
                                          n.name.split('.'),
                                          n.asname))

        exprs = ast.parse(self.load_pyfile(), self.file_path)
        _Transform().visit(exprs)
        # TODO funcitons overlap raise
        return funcname2docstring, imports

    def set_code_obj(self, func_name):

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                if node.name == func_name:
                    return node

        exprs = ast.parse(self.load_pyfile(), self.file_path)
        self.code_obj = compile(_Transform().visit(exprs), self.file_path, 'exec')

    def run(self, kwargs=None):
        try:
            exec(self.code_obj, kwargs)
        except Exception as e:
            print(e)

    def set_rap_module(self, code_obj=None):
        """set import module code
        """
        code_obj = code_obj if code_obj else self.code_obj
        code = self._imports_to_str()
        print(self._uncompile(code_obj))
        code.extend(self._uncompile(code_obj))
        line = ''
        for c in code:
            line += c + '\n'
        self.code_obj = compile(line, '<rf>', 'exec')

    def _uncompile(self, code_obj):
        """uncompile from codeobj to sourcecode
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

    def _imports_to_str(self):
        imports_str = []
        for i in self.imports:
            line = ''
            if i.module:
                line += 'from ' + '.'.join(i.module) + ' '
            line += 'import ' + '.'.join(i.name)
            if i.asname:
                line += ' as ' + i.asname
            imports_str.append(line)
        return imports_str
