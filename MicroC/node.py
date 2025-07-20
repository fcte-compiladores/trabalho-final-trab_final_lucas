from .ast import *
from .ctx import *
from .errors import *

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def visit_bool_literal(self, node):
        return node.value

    def __init__(self, program):
        self.program = program

        self.env = Ctx()

        self.functions = {}
        self._register_functions(program)

    def _register_functions(self, program):
        for decl in program.declarations:
            if isinstance(decl, FunDecl):
                self.functions[decl.name] = decl
            elif isinstance(decl, VarDecl):
                if decl.init is not None:
                    value = decl.init.eval(self) if hasattr(decl.init, 'eval') else decl.init
                else:
                    value = 0
                self.env.set(decl.name, value)

    def run(self):
        if 'main' not in self.functions:
            raise KeyError('main')
        func = self.functions['main']
        try:
            result = self._eval_block(func.body, self.env)
        except ReturnValue as rv:
            result = rv.value
        return result

    def _call_function(self, name, args):
        func = self.functions.get(name)
        if not func:
            raise KeyError(name)
        
        if len(args) != len(func.params):
            raise KeyError(name, len(func.params), len(args))
            
        local_env = Ctx(self.env)
        for param, arg in zip(func.params, args):
            local_env.set(param.name, arg)
        try:
            result = self._eval_block(func.body, local_env)
            return result
        except ReturnValue as rv:
            return rv.value

    def _eval_block(self, block, env):
        prev_env = self.env
        self.env = env
        try:
            for stmt in block.stmts:
                stmt.eval(self)
        except ReturnValue as rv:
            raise rv
        finally:
            self.env = prev_env

    def visit_program(self, node):
        for decl in node.declarations:
            if isinstance(decl, FunDecl):
                self.functions[decl.name] = decl
            elif isinstance(decl, VarDecl):
                value = decl.init if decl.init is not None else 0
                self.env.set(decl.name, value)
            else:
                decl.eval(self)

        return self.run()

    def visit_var_decl(self, node):
        if node.init is not None:
            value = node.init.eval(self)
        else:
            value = 0  # valor padrão
        self.env.set(node.name, value)

    def visit_block(self, node):
        new_env = Ctx(self.env)
        try:
            self._eval_block(node, new_env)
        except ReturnValue as rv:
            raise rv

    def visit_expr_stmt(self, node):
        node.expr.eval(self)

    def visit_if_stmt(self, node):
        cond = node.condition.eval(self)
        if cond:
            node.then_stmt.eval(self)
        elif node.else_stmt:
            node.else_stmt.eval(self)

    def visit_while_stmt(self, node):
        while node.condition.eval(self):
            node.body.eval(self)

    def visit_return_stmt(self, node):
        value = node.expr.eval(self) if node.expr else 0
        raise ReturnValue(value)

    def visit_assignment(self, node):
        value = node.value.eval(self)
        self.env.update(node.name, value)
        return value

    def visit_binary_op(self, node):
        left = node.left.eval(self)
        right = node.right.eval(self)
        op = node.operator
        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/': return left // right
        if op == '==': return int(left == right)
        if op == '!=': return int(left != right)
        if op == '<': return int(left < right)
        if op == '>': return int(left > right)
        if op == '<=': return int(left <= right)
        if op == '>=': return int(left >= right)
        if op == '&&': return int(bool(left) and bool(right))
        if op == '||': return int(bool(left) or bool(right))
        raise Exception(f"Operador binário não suportado: {op}")

    def visit_unary_op(self, node):
        operand = node.operand.eval(self)
        op = node.operator
        if op == '-':
            return -operand
        if op == '+':
            return +operand
        if op == '!':
            return int(not bool(operand))
        raise Exception(f"Operador unário não suportado: {op}")

    def visit_function_call(self, node):
        args = [arg.eval(self) for arg in node.args]
        return self._call_function(node.name, args)
    
    def visit_print_call(self, node):
        value = node.expr.eval(self)
        print(value)
        return value

    def visit_variable(self, node):
        value = self.env.get(node.name)
        while hasattr(value, "eval"):
            value = value.eval(self)
        return value

    def visit_int_literal(self, node):
        return node.value