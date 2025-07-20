from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any

class Node(ABC):

    @abstractmethod
    def eval(self, visitor):
        pass


@dataclass
class Program(Node):


    declarations: List['Decl']
    
    def eval(self, visitor):
        return visitor.visit_program(self)


class Decl(Node):
    pass


@dataclass
class VarDecl(Decl):


    type: str
    name: str
    init: Optional[Node] = None  
    
    def eval(self, visitor):
        return visitor.visit_var_decl(self)


@dataclass
class FunDecl(Decl):


    type: str
    name: str
    params: List['Param']
    body: 'Block'
    
    def eval(self, visitor):
        return visitor.visit_fun_decl(self)


@dataclass
class Param(Node):


    type: str
    name: str
    
    def eval(self, visitor):
        return visitor.visit_param(self)


class Stmt(Node):
    pass


@dataclass
class Block(Stmt):


    stmts: List[Stmt]
    
    def eval(self, visitor):
        return visitor.visit_block(self)


@dataclass
class ExprStmt(Stmt):


    expr: 'Expr'
    
    def eval(self, visitor):
        return visitor.visit_expr_stmt(self)


@dataclass
class IfStmt(Stmt):


    condition: 'Expr'
    then_stmt: Stmt
    else_stmt: Optional[Stmt] = None
    
    def eval(self, visitor):
        return visitor.visit_if_stmt(self)


@dataclass
class WhileStmt(Stmt):


    condition: 'Expr'
    body: Stmt
    
    def eval(self, visitor):
        return visitor.visit_while_stmt(self)


@dataclass
class Return(Stmt):


    expr: Optional['Expr'] = None
    
    def eval(self, visitor):
        return visitor.visit_return_stmt(self)


class Expr(Node):
    pass


@dataclass
class Assign(Expr):


    name: str
    value: Expr
    
    def eval(self, visitor):
        return visitor.visit_assignment(self)


@dataclass
class BinOp(Expr):


    left: Expr
    operator: str
    right: Expr
    
    def eval(self, visitor):
        return visitor.visit_binary_op(self)


@dataclass
class UnaryOp(Expr):


    operator: str
    operand: Expr
    
    def eval(self, visitor):
        return visitor.visit_unary_op(self)


@dataclass
class Function(Expr):


    name: str
    args: List[Expr]
    
    def eval(self, visitor):
        return visitor.visit_function_call(self)


@dataclass
class Print(Expr):


    expr: Expr
    
    def eval(self, visitor):
        return visitor.visit_print_call(self)


@dataclass
class Var(Expr):


    name: str
    
    def eval(self, visitor):
        return visitor.visit_variable(self)



@dataclass
class Int(Expr):


    value: int
    
    def eval(self, visitor):
        return visitor.visit_int_literal(self)

@dataclass
class Bool(Expr):


    value: bool

    def eval(self, visitor):
        return visitor.visit_bool_literal(self)


class Printer:
    def __init__(self):
        self.indent_level = 0

    def visit_bool_literal(self, node):
        return f"Bool({str(node.value).lower()})"

    def _indent(self):
        return "  " * self.indent_level

    def visit_program(self, node: Program):
        result = "Program:\n"
        self.indent_level += 1
        for decl in node.declarations:
            result += self._indent() + str(decl.eval(self)) + "\n"
        self.indent_level -= 1
        return result.rstrip()

    def visit_var_decl(self, node: VarDecl):
        return f"VarDecl({node.type} {node.name})"

    def visit_fun_decl(self, node: FunDecl):
        params_str = ", ".join([param.eval(self) for param in node.params])
        result = f"FunDecl({node.type} {node.name}({params_str}))"
        self.indent_level += 1
        result += "\n" + self._indent() + node.body.eval(self)
        self.indent_level -= 1
        return result

    def visit_param(self, node: Param):
        return f"{node.type} {node.name}"

    def visit_block(self, node: Block):
        result = "Block:"
        self.indent_level += 1
        for stmt in node.stmts:
            result += "\n" + self._indent() + str(stmt.eval(self))
        self.indent_level -= 1
        return result

    def visit_expr_stmt(self, node: ExprStmt):
        return f"ExprStmt({node.expr.eval(self)})"

    def visit_if_stmt(self, node: IfStmt):
        result = f"IfStmt({node.condition.eval(self)})"
        self.indent_level += 1
        result += "\n" + self._indent() + "Then: " + node.then_stmt.eval(self)
        if node.else_stmt:
            result += "\n" + self._indent() + "Else: " + node.else_stmt.eval(self)
        self.indent_level -= 1
        return result

    def visit_while_stmt(self, node: WhileStmt):
        result = f"WhileStmt({node.condition.eval(self)})"
        self.indent_level += 1
        result += "\n" + self._indent() + node.body.eval(self)
        self.indent_level -= 1
        return result

    def visit_return_stmt(self, node: Return):
        if node.expr:
            return f"Return({node.expr.eval(self)})"
        return "Return()"

    def visit_assignment(self, node: Assign):
        return f"Assign({node.name} = {node.value.eval(self)})"

    def visit_binary_op(self, node: BinOp):
        return f"BinOp({node.left.eval(self)} {node.operator} {node.right.eval(self)})"

    def visit_unary_op(self, node: UnaryOp):
        return f"UnaryOp({node.operator} {node.operand.eval(self)})"

    def visit_function_call(self, node: Function):
        args_str = ", ".join([arg.eval(self) for arg in node.args])
        return f"Function({node.name}({args_str}))"
    
    def visit_print_call(self, node: Print):
        return f"Print({node.expr.eval(self)})"

    def visit_variable(self, node: Var):
        return f"Var({node.name})"

    def visit_int_literal(self, node: Int):
        return f"Int({node.value})"