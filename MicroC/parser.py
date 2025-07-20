from lark import Lark, UnexpectedInput
import os

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), 'grammar.lark')

with open(GRAMMAR_PATH, encoding='utf-8') as f:
    GRAMMAR = f.read()

parser = Lark(GRAMMAR, parser='lalr', start='start', propagate_positions=True)

def parse_source(source: str):
    try:
        tree = parser.parse(source)
        return tree
    except UnexpectedInput as e:
        print('Erro de sintaxe:', e)
        return None