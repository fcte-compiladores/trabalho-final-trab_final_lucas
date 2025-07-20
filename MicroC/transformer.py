from lark import Transformer, Token
from .ast import *


class MicroCTransformer(Transformer):
    def ast_converter(self, item):
        if isinstance(item, (Node, list)):
            return item
        if isinstance(item, int):
            return Int(item)
        elif isinstance(item, str):
            if item == 'true':
                return Bool(True)
            elif item == 'false':
                return Bool(False)
            return Var(item)
        elif isinstance(item, Token):
            if item.type == 'INT':
                return Int(int(item))
            elif item.type == 'BOOL':
                return Bool(str(item) == 'true')
            elif item.type == 'ID':
                return Var(str(item))
        return item
    
    def program(self, items):
        return Program(items)
    
    def var_decl(self, items):
        type_str = items[0]
        name = items[1]
        if isinstance(name, Token):
            name = str(name)

        init = items[2] if len(items) > 2 else None
        return VarDecl(type_str, name, init)
    
    def fun_decl(self, items):
        type_str, name, params, body = items
        if isinstance(name, Token):
            name = str(name)
        return FunDecl(type_str, name, params, body)
    
    def params(self, items):
        return items if items else []
    
    def param(self, items):
        type_str, name = items
        if isinstance(name, Token):
            name = str(name)
        return Param(type_str, name)
    
    def type(self, items):
        if items and len(items) > 0:
            item = items[0]
            if isinstance(item, Token):
                return str(item.value)
            return str(item)
        print("valor em type não reconhecido")
        return "void"
    
    def block(self, items):
        return Block(items)
    
    def expr_stmt(self, items):
        expr = self.ast_converter(items[0])
        return ExprStmt(expr)
    
    def if_stmt(self, items):
        if len(items) == 2:
            cond, then_stmt = items
            cond = self.ast_converter(cond)
            return IfStmt(cond, then_stmt)
        else:
            cond, then_stmt, else_stmt = items
            cond = self.ast_converter(cond)
            return IfStmt(cond, then_stmt, else_stmt)
    
    def while_stmt(self, items):
        cond, body = items
        cond = self.ast_converter(cond)
        return WhileStmt(cond, body)
    
    def return_stmt(self, items):
        if items:
            expr = self.ast_converter(items[0])
            return Return(expr)
        return Return()
    
    def assignment(self, items):
        if len(items) == 2:
            name, value = items
            if isinstance(name, Token):
                name = str(name)
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
            value = self.ast_converter(value)
            return Assign(name, value)
        else:
            expr = items[0]
            if isinstance(expr, list) and len(expr) == 1:
                expr = expr[0]
            return expr
    
    def logic_or(self, items):
        return self._create_binary_op(items, "||")
    
    def logic_and(self, items):
        return self._create_binary_op(items, "&&")
    
    def equality(self, items):
        return self._create_binary_op(items, ["==", "!="])
    
    def relational(self, items):
        if len(items) == 1:
            return items[0]
        result = self.ast_converter(items[0])
        i = 1
        while i + 1 < len(items):
            op = items[i]
            right = self.ast_converter(items[i + 1])
            result = BinOp(result, op, right)
            i += 2
        return result
        
    def sum(self, items):
        return self._create_binary_op(items, ["+", "-"])
    
    def term(self, items):
        return self._create_binary_op(items, ["*", "/"])
    
    def factor(self, items):
        if len(items) == 1:
            item = items[0]
            result = self.ast_converter(item)
            return result
        elif len(items) == 2:
            if items[0] == '!':
                operand = self.ast_converter(items[1])
                return UnaryOp('!', operand)
            else:
                name, args = items
                if isinstance(name, Token):
                    name = str(name)
                result = Function(name, args)
                return result
        else:
            return items[0]
        
    def fun_call(self, items):
        name = str(items[0])
        args = items[1] if len(items) > 1 else []
        return Function(name=name, args=args)
    
    def print_call(self, items):
        expr = self.ast_converter(items[0])
        return Print(expression=expr)
        
    
    def args(self, items):
        result = [self.ast_converter(item) for item in items] if items else []
        return result
    
    def _create_binary_op(self, items, operators):
        if len(items) == 1:
            return items[0]
        if len(items) == 2:
            left = self.ast_converter(items[0])
            right = self.ast_converter(items[1])
            op = operators[0] if isinstance(operators, str) else operators[0]
            result = BinOp(left, op, right)
            return result
        result = self.ast_converter(items[0])
        i = 1
        while i + 1 < len(items):
            op = str(items[i])
            right = items[i + 1]
            right = self.ast_converter(right)
            result = BinOp(result, op, right)
            i += 2
        return result
    
    def INT(self, token):
        return int(token)

    def ID(self, token):
        return str(token)

    def NOT(self, token):
        return str(token)
    
    def BOOL(self, token):
        return Bool(token == 'true')

    def PLUS(self, token):
        return str(token)

    def MINUS(self, token):
        return str(token)

    def TIMES(self, token):
        return str(token)

    def DIVIDE(self, token):
        return str(token)

    def EQ(self, token):
        return str(token)

    def NE(self, token):
        return str(token)

    def LT(self, token):
        return str(token)

    def GT(self, token):
        return str(token)

    def LE(self, token):
        return str(token)

    def GE(self, token):
        return str(token)

    def OR(self, token):
        return str(token)

    def AND(self, token):
        return str(token)