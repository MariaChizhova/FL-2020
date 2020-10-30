from ply import lex

tokens = [
  'IDENTIFIER',
  'TURNSTILE',
  'COMMA',
  'SEMICOLON',
  'LPAREN',
  'RPAREN',
  'DOT'
]

t_ignore = ' \t\n'

t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_TURNSTILE = r':-'
t_COMMA = '\,'
t_SEMICOLON = '\;'
t_LPAREN = '\('
t_RPAREN = '\)'
t_DOT = '\.'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise SyntaxError(str(t))


lexer = lex.lex() 
