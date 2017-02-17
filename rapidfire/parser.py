import ast
import inspect

import __future__
PyCF_MASK = sum(v for k, v in vars(__future__).items() if k.startswith('CO_FUTURE'))


class ParsePyFile(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.functions, self.modules = self.load_code()
        self.code_obj = None

    def load_pyfile(self):
        file_name = self.file_path
        with open(file_name, 'r') as f:
            code = f.read()
        return code

    def load_code(self):
        function_info = []
        module_names = []

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                function_info.append((node.name, ast.get_docstring(node)))

            def visit_ImportFrom(self, node):
                imp = node.names[0].asname if node.names[0].asname else node.names[0].name
                module_names.append('from %s import %s' % (node.module, imp))

            def visit_Import(self, node):
                module_names.append('import %s' % node.names[0].name)

        exprs = ast.parse(self.load_pyfile(), self.file_path)
        _Transform().visit(exprs)
        self.attribute_settings = compile(exprs, self.file_path, 'exec')
        # TODO funcitons overlap raise
        return function_info, module_names

    def set_code_obj(self, func_name):

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                if node.name == func_name:
                    return node

        exprs = ast.parse(self.load_pyfile(), self.file_path)
        _Transform().visit(exprs)
        self.code_obj = compile(exprs, self.file_path, 'exec')

    def run(self):
        try:
            exec(self.code_obj)
        except Exception as e:
            print(e)

    def set_rap_module(self, code_obj):
        """set import module code
        """
        source = self._uncompile(code_obj)
        code = self.modules
        code.extend(source)
        exprs = ''
        for line in code:
            exprs += line + '\n'
        self.code_obj = compile(exprs, '<rap>', 'exec')

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
