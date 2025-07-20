import argparse

from lark import Lark
from . import parser as microc_parser
from .parser import parse_source
from . import eval as MicroC_eval

def make_argparser():
    parser = argparse.ArgumentParser(description="Compilador Lox")
    parser.add_argument(
        "file",
        help="Arquivo de entrada",
    )
    parser.add_argument(
        "-t",
        "--ast",
        action="store_true",
        help="Imprime a árvore sintática.",
    )
    parser.add_argument(
        "-c",
        "--cst",
        action="store_true",
        help="Imprime a árvore sintática concreta produzida pelo Lark.",
    )
    return parser

def main():
    parser = make_argparser()
    args = parser.parse_args()
    try:
        with open(args.file, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Arquivo {args.file} não encontrado.")
        exit(1)

    if not args.ast and not args.cst:
            MicroC_eval(source)

    if args.cst:
        tree = parse_source(source)
        if tree:
            print(tree.pretty())
        return

    if args.ast:
        from .transformer import MicroCTransformer
        tree = parse_source(source)
        if tree:
            ast = MicroCTransformer().transform(tree)
            from .ast import Printer
            content = Printer()
            print(ast.eval(content))
        return