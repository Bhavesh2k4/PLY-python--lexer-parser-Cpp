import ply.lex as lex
import ply.yacc as yacc

reserved = {
   'while' : 'WHILE',
   'if' : 'IF',
   'else' : 'ELSE',
   'for' : 'FOR',
   'int' : 'INT',
   'char' : 'CHAR',
   'float' : 'FLOAT',
   'void' : 'VOID',
}
# List of token names. This is always required
tokens = (
   'NUMBER',
   'SEMICOLON',
   'PLUS',
   'MINUS',
   'MUL',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'WHILE',
   'IF',
   'ELSE',
   'FOR',
   'LBRACE',
   'RBRACE',
   'ID',
   'EQUALS',
   'DEQUALS',
   'LESSTHAN',
   'GREATERTHAN',
   'LESSTHANEQ',
   'GREATERTHANEQ',
   'INT',
   'CHAR',
   'FLOAT',
   'COMMA',
   'VOID',
)+ tuple(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MUL     = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQUALS = r'='
t_DEQUALS = r'=='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSTHANEQ = r'<='
t_GREATERTHANEQ = r'>='
t_COMMA = r','

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parser
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIVIDE'),
)

def p_program(p):
    '''program : statements
    '''

    p[0] = p[1]

def p_type_specifier(p):
    '''type_specifier : INT
                      | CHAR
                      | FLOAT
                      | VOID
    '''
    p[0] = p[1]

def p_params(p):
    '''params : type_specifier ID
              | type_specifier ID COMMA params
    '''
    if len(p) == 3:
        p[0] = [(p[1], p[2])]
    else:
        p[0] = [(p[1], p[2])] + p[4]

def p_declaration(p):
    '''declaration : type_specifier ID SEMICOLON
                   | type_specifier ID LPAREN params RPAREN SEMICOLON
                   | type_specifier ID LPAREN params RPAREN LBRACE program RBRACE
                   | type_specifier ID LBRACE program RBRACE
                   | type_specifier ID LBRACE program RBRACE SEMICOLON
                   | type_specifier ID LBRACE RBRACE
    '''
    if len(p) == 4:
        p[0] = ('declaration', p[1], [p[2]])
    elif len(p) == 7:
        p[0] = ('declaration', p[1], [p[2]], p[4], p[6])
    elif len(p) == 6:
        p[0] = ('declaration', p[1], [p[2]], [], p[5])
    else:
        p[0] = ('declaration', p[1], [p[2]])

def p_statements(p):
    '''statements : statement
                  | declaration
                  | statement statements
                  | declaration statements
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_statement(p):
    '''statement : IF LPAREN expression RPAREN LBRACE program RBRACE
                 | IF LPAREN expression RPAREN LBRACE program RBRACE ELSE LBRACE program RBRACE
                 | WHILE LPAREN expression RPAREN LBRACE program RBRACE
                 | FOR LPAREN assignment SEMICOLON expression SEMICOLON assignment RPAREN LBRACE program RBRACE
                 | ID EQUALS expression SEMICOLON
    '''
    if len(p) == 7 and p[1] == "if":
        p[0] = ('if', p[3], p[6])
    elif len(p) == 13:
        p[0] = ('if-else', p[3], p[6], p[12])
    elif len(p) == 7 and p[1] == "while":
        p[0] = ('while', p[3], p[6])
    elif len(p) == 13 and p[1] == "for":
        p[0] = ('for', p[3], p[5], p[7], p[12])
    else:
        p[0] = ('assignment', p[1], p[3])

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DIVIDE expression
                  | LPAREN expression RPAREN
                  | expression LESSTHAN expression
                  | expression GREATERTHAN expression
                  | expression LESSTHANEQ expression
                  | expression GREATERTHANEQ expression
                  | expression DEQUALS expression
                  | ID
                  | NUMBER
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_assignment(p):
    '''assignment : ID EQUALS expression
    '''
    p[0] = ('assignment', p[1], p[3])

def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()

# Test it out
lines = []
while True:
    line = input()
    if line:
        lines.append(line)
    else:
        lines.append('\n')
        break
input_code = '\n'.join(lines)
print("___________________________________________________________________________\n")
print(input_code)
result = parser.parse(input_code)
print(result)
print("\n")
if (result):
    print("Accepted! ")
else:
    print("Rejected !")
print("___________________________________________________________________________\n")
