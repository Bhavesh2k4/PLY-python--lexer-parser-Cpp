# PLY-python--lexer-parser-Cpp
This project is a simple  parser for C++ language, implemented using PLY (Python Lex-Yacc). It includes a lexer and parser to analyze the syntax of input code, supporting features like conditional statements, loops, variable assignments, and expressions. Provides a foundation for understanding lexical analysis and parsing concepts.

*pip install ply*

*Lexer (ply.lex):*

The lexer defines a set of tokens, which are the building blocks of the programming language. Tokens include numbers, operators, keywords, etc.
Regular expressions are used to define the patterns for each token, such as numbers, arithmetic operators, parentheses, etc.
Reserved keywords like 'while,' 'if,' 'else,' etc., are specified in a dictionary called reserved.
The t_ID function identifies identifiers and checks if they are reserved words.
The lexer also handles comments and ignores whitespace.

*Parser (ply.yacc):*

The parser specifies the grammar of the language using a set of production rules.
Precedence rules are defined for operators like +, -, *, and /.
Productions are defined for the program, type specifiers, parameters, declarations, statements, expressions, assignments, and error handling.
The p_program rule starts the parsing process, defining a program as a set of statements.
The p_type_specifier rule defines the type specifier for variables and functions.
The p_params rule handles function parameters.
The p_declaration rule defines variable and function declarations.
The p_statements rule handles program statements, including both declarations and other statements.
The p_statement rule defines various types of statements such as if, if-else, while, for, and assignments.
The p_expression rule defines expressions with different operators and operands.
The p_assignment rule handles variable assignments.
The p_error function handles syntax errors.

*Test and Output:*

The code includes a simple test loop where the user can input lines of code.
The input code is then parsed using the defined parser.
If the parsing is successful, the parsed result is printed, and "Accepted!" is displayed. Otherwise, a syntax error message is printed, and "Rejected!" is displayed.
