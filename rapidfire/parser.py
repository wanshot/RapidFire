import ast


class ParsePyFile(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.funcname2docstring = self.load_code()
        self.code_obj = None

    def load_pyfile(self):
        file_name = self.file_path
        with open(file_name, 'r') as f:
            code = f.read()
        return code

    def load_code(self):
        funcname2docstring = []

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                funcname2docstring.append((node.name, ast.get_docstring(node)))

        exprs = ast.parse(self.load_pyfile(), self.file_path)
        _Transform().visit(exprs)
        # TODO funcitons overlap raise
        return funcname2docstring

    def set_code_obj(self, func_name):

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                if node.name == func_name:
                    return node

        exprs = ast.parse(self.load_pyfile(), self.file_path)
        self.code_obj = compile(_Transform().visit(exprs), self.file_path, 'exec')

    def run(self, kwargs=None):
        _globals = globals()
        if kwargs:
            _globals.update(kwargs)
        try:
            exec(self.code_obj, _globals)
        except Exception as e:
            print(e)
