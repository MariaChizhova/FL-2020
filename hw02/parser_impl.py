import ply.yacc as yacc
from lex_impl import tokens


def p_program(p):
    'program : relation_list'
    p[0] = 'Program (' + p[1] + ')'


def p_relation_list(p):
    '''relation_list : relation
                     | relation relation_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ', ' + p[2]


def p_relation(p):
    '''relation : head DOT
                | head TURNSTILE body DOT'''
    if len(p) == 3:
        p[0] = 'Relation (' + p[1] + ')'
    elif len(p) == 5:
        p[0] = 'Relation (' + p[1] + ', ' + p[3] + ')'


def p_head(p):
    'head : atom'
    p[0] = 'Head (' + p[1] + ')'


def p_body(p):
    'body : disjunction'
    p[0] = 'Body (' + p[1] + ')'


def p_disjunction(p):
    '''disjunction : conjunction
                   | conjunction SEMICOLON disjunction'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = 'Disjunction (' + p[1] + ', ' + p[3] + ')'


def p_conjunction(p):
    '''conjunction : operand
                   | operand COMMA conjunction'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = 'Conjunction (' + p[1] + ', ' + p[3] + ')'


def p_operand(p):
    '''operand : atom
               | LPAREN disjunction RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_atom(p):
    '''atom : IDENTIFIER
            | IDENTIFIER atom_list'''
    if len(p) == 2:
        p[0] = 'Atom (' + p[1] + ')'
    elif len(p) == 3:
        p[0] = 'Atom (' + p[1] + ', ' + 'Atom list (' + p[2] + '))'


def p_atom_list(p):
    '''atom_list : atom
                 | LPAREN atom RPAREN
                 | LPAREN atom_list RPAREN
                 | LPAREN atom RPAREN atom_list'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]
    elif len(p) == 5:
        p[0] = 'Atom list (' + p[2] + ', ' + p[4] + ')'


def p_error(p):
    raise SyntaxError(str(p))


parser = yacc.yacc()


def parse(expr):
    return parser.parse(expr)
