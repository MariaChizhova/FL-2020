import argparse
import os
from parsita import *

class BaseParsers(TextParsers, whitespace=r'[ \t\n\r]*'):
    dot = lit('.')
    comma = lit(',')
    colon = lit(':')
    id = reg(r'[A-Za-z_][A-Za-z0-9_]*')
    mod = lit('module')
    t = lit('type')
    lparen = lit('(')
    rparen = lit(')')
    var = reg(r'[A-Z][A-Za-z0-9_]*')
    maybe = reg(r'[a-z_][a-zA-Z_0-9]*')
    not_var = pred(maybe, lambda x: x != "module" and x != "type", 'another id')
    # atom
    subatom = id | helper | lst
    helper = (lparen & atom & rparen) | (lparen & subatom & rparen)
    atom = not_var & rep(subatom) > (lambda x: "(" + "ID " + x[0] + ")")
    # module
    module = mod & id & dot > (lambda x: "MODULE " + x[1])
    # type
    elem = atom | subbody | id
    body = repsep(elem, '->') > (lambda x:"(" + " ARROW ".join(x) + ")")
    subbody = lparen & body & rparen > (lambda x: "(" + x[1] + ")")
    type = t & not_var & body & dot > (lambda x: "(TYPE " + "(NAME(" + x[1] + "))" + x[2] + ")(DOT)")
    # list
    optional = var | lst | atom
    helper2 = comma & optional & opt(helper2)
    lst = (lit('[') & optional & lit('|') & var & ']') | (lit('[') & opt(optional & opt(helper2)) & lit(']'))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=str, help='Path to program file')
    parser.add_argument('--module', help='Parse module', action='store_true')
    parser.add_argument('--variable', help='Parse variable', action='store_true')
    parser.add_argument('--type', help='Parse type', action='store_true')
    parser.add_argument('--list', help='Parse list', action='store_true')
    parser.add_argument('--atom', help='Parse atom', action='store_true')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    lines = []
    with open(args.input, 'r') as file:
        lines = file.read()
    if args.module:
        tree = BaseParsers.module.parse(lines).value
    elif args.variable:
        tree = "VAR " + BaseParsers.var.parse(lines).value
    elif args.type:
        tree = BaseParsers.type.parse(lines).value
    elif args.list:
        tree = BaseParsers.lst.parse(lines).value
    elif args.atom:
        tree = BaseParsers.atom.parse(lines).value
    with open(os.path.basename(args.input) + '.out', 'w') as ans_file:
        ans_file.write(str(tree))


if __name__ == '__main__':
    try:
     main()
    except Exception as e:
        print('Failed to parse')
        exit(1)
        
