import ast
from collections import defaultdict
import sys
import tokenize


def read_file(filename):
    with tokenize.open(filename) as fd:
        return fd.read()

class BaseChecker(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def check(self, paths):
        for filepath in paths:
            self.filename = filepath
            tree = ast.parse(read_file(filepath))
            self.visit(tree)

    def report(self):
        for violation in self.violations:
            filename, lineno, msg = violation
            print(f"{filename}:{lineno}: {msg}")

class CodeInjectionDefinitionChecker(BaseChecker):
    msg = "Usage of eval() or exec() detected. Possible code injection"
    codeInjectionCall = [eval.__name__, exec.__name__]       

    def visit_Call(self, node):
        # print("node", dir(node))
        name = getattr(node.func, "id", None)
        if name and name in self.codeInjectionCall and not node.args:
            self.violations.append((self.filename, node.lineno, self.msg))

    def visit_For(self, node):
        # print("node", dir(node))

        # self.visit_Call(node)
        print("a")
    
    # def visit_If(self, node):
    #     self.visit_Call(node)
    #     print("b")

if __name__ == '__main__':
    files = sys.argv[1:]
    checker = CodeInjectionDefinitionChecker()
    checker.check(files)
    checker.report()