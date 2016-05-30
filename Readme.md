# Let's build a simple interpreter 
Simple interpreter/compiler for Pascal in Python

## Part I: [Two Terms, Single Digit Addition with No Whitespace](https://ruslanspivak.com/lsbasi-part1/)
Evaluate: `3+4`
Token: an object with a type and a value
Lexical analysis: the process of breaking the input string into tokens
Lexical analyser (lexer/scanner/tokenizer): the part of interpreter that performs lexical analysis

## [Part II: Two Terms, Multiple Digits Addition/Substraction with Whitespace](https://ruslanspivak.com/lsbasi-part2/)
Evaluate: `123 + 456`
Lexeme: a sequence of characters that form a token
Parsing: the process of recognizing a phrase in the stream of token
Parser: the part of interpreter that performs parsing

## Part III: [Multiple Terms, Multiple Digits Addition and Subtraction](https://ruslanspivak.com/lsbasi-part3/)
Evaluate: `7 - 12 + 5 -45`
Syntax Diagram: a graphical representation of a programming language's syntax rules
Syntax analysis: parsing
Syntax analyser: parser

## Part IV: [Multiple Terms, Multiple Digits Multiplication and Division](https://ruslanspivak.com/lsbasi-part4/)
Evaluate: `7 * 4 / 2 * 3`
Context-free Grammars: also known as Grammars / Backus-Naur Form/ BNF 
Grammars: consists of a sequence of rules, also known as productions.
Rules: consists of a non-terminal (called the head of left-hand-side of the production), a colon, and a sequence of terminals and/or non-terminals (called body or right hand side of the production)  
Terminals: tokens like MUL, DIV and INTEGER
Non-terminals: variables like expr and factor
Start symbol: the non-terminal symbol on the left side of first rule
Grammar Example:
	expr: factor ((MUL | DIV) factor )*
	factor: INTEGER
	
Translation:
	(1) expr: body
	def expr(self):
		body()
		
	(2) (MUL | DIV)
	if token.type == MUL:
	elif token.type == DIV:
	else:
	
	(3) ((MUL | DIV) factor)*
	while token.type in (MUL, DIV):
	
	(4) INTEGER
	self.eat(INTEGER)
	
## Part V: [Basic Arithmetic](https://ruslanspivak.com/lsbasi-part5/)
Evaluate: `2 + 3 * 5 -8 / 2`
Left associativity
Precedence of operators

## Part VI: [Arithmetic with Parenthesis - Recursion](https://ruslanspivak.com/lsbasi-part6/)
Evaluate: `7 + 3 * (10 / (12 / (3 + 1) - 1))` using recursion
Recursive-descent parser

## Part VII: [Arithmetic with Parenthesis - AST](https://ruslanspivak.com/lsbasi-part7/)
Evaluate: `7 + 3 * (10 / (12 / (3 + 1) - 1))` using AST
Parse tree (Concrete syntax tree)
Abstract syntax tree (AST)
Intermediate Representation (IR)
Depth-first traversal: preorder, inorder, postorder
Visitor design pattern

## Part VIII: [Unary operator](https://ruslanspivak.com/lsbasi-part8/)
Evaluate: `-3 + 8`
Unary operator

## Part IX: [Sequence Code Block](https://ruslanspivak.com/lsbasi-part9/)
Evaluate: 
```pascal
BEGIN
    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number / 4;
        c := a - - b
    END;
    x := 11;
END.
```
Reserved Keywords
Symbol table
