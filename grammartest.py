import nltk
from nltk import CFG
nltk.download('punkt_tab', quiet=True)

# Define a context-free grammar for a subset of TypeScript
# Model 3: No ambiguity, no left recursion — LL(1) ready
grammar = CFG.fromstring("""
    Program  -> Stmt ProgramR
    ProgramR -> Stmt ProgramR
    ProgramR -> Empty
    Stmt     -> Decl SEMI
    Decl     -> Kw ID DeclTail
    DeclTail -> COLON Type ASSIGN Expr
    DeclTail -> ASSIGN Expr
    Kw       -> CONST
    Kw       -> LET
    Type     -> TNUM
    Type     -> TSTR
    Type     -> TBOOL
    Expr     -> Term ExprR
    ExprR    -> PLUS Term ExprR
    ExprR    -> MINUS Term ExprR
    ExprR    -> Empty
    Term     -> Factor TermR
    TermR    -> TIMES Factor TermR
    TermR    -> DIV Factor TermR
    TermR    -> Empty
    Factor   -> LPAREN Expr RPAREN
    Factor   -> Literal
    Factor   -> ID
    Literal  -> INTLIT
    Literal  -> STRLIT
    Literal  -> TRUE
    Literal  -> FALSE
    Empty    ->

    CONST  -> 'const'
    LET    -> 'let'

    TNUM   -> 'number'
    TSTR   -> 'string'
    TBOOL  -> 'boolean'

    TRUE   -> 'true'
    FALSE  -> 'false'

    SEMI   -> ';'
    COLON  -> ':'
    ASSIGN -> '='
    PLUS   -> '+'
    MINUS  -> '-'
    TIMES  -> '*'
    DIV    -> '/'
    LPAREN -> '('
    RPAREN -> ')'

    ID     -> 'x' | 'y' | 'z' | 'a' | 'b' | 'result' | 'name' | 'flag' | 'total' | 'count' | 'value'
    INTLIT -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '42' | '100'
    STRLIT -> '"hello"' | '"world"' | '"typescript"' | '"foo"'
""")

# Create a parser with the defined grammar
parser = nltk.ChartParser(grammar)

# Input sentences to be parsed.
# Tokens must be separated by spaces — each token corresponds to a terminal in the grammar.
# Note: identifiers and literals are restricted to the fixed sets defined above.
original_sentences = [
    # --- Part of the language ---
    "const x = 5 ;",                              # Simple integer declaration
    "let y = 10 + 3 ;",                           # Addition expression
    'const name : string = "hello" ;',            # Typed string declaration
    "let result : number = 5 + 3 * 2 ;",          # Precedence: * before +
    "const flag : boolean = true ;",              # Boolean literal
    "const z = ( 5 + 3 ) * 2 ;",                 # Parenthesized expression
    "let a = x + y ;",                            # Identifier in expression
    "const x = 5 ; let y = x * 2 ;",             # Multiple statements
    "const total : number = ( x + y ) / 2 ;",    # Complex typed declaration
    # --- Not part of the language ---
    "x = 5 ;",                                    # Missing keyword
    "const = 5 ;",                                # Missing identifier
    "const x = 5 + ;",                            # Incomplete expression
    "const x = ;",                                # Missing expression after =
    "const x = ( 5 + 3 ;",                        # Unclosed parenthesis
    "let x : number ;",                           # Missing = and expression
]

# Parse each sentence and print the parse tree or "Unable to parse"
for sentence in original_sentences:
    print()
    print("Input:", sentence)
    tokens = sentence.split()
    trees = list(parser.parse(tokens))
    if trees:
        print("Parse Tree (LL(1) compatible grammar, NLTK ChartParser):")
        for tree in trees:
            tree.pretty_print()
    else:
        print("Unable to parse")
