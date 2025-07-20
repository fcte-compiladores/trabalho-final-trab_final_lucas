from .node import *

def eval(source):
    from .parser import parse_source
    from .transformer import MicroCTransformer

    tree = parse_source(source)
    if not tree:
        raise Exception("erro na sintaxe")
    
    ast = MicroCTransformer().transform(tree)

    interpreter = Interpreter(ast)

    result = interpreter.visit_program(ast)

    print(result)
    return result