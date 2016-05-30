INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = ('INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'EOF')

#=================Lexer=============================
class Token(object):
    def __init__(self, type, value):
        #token type: INTEGER, PLUS, or EOF
        self.type = type
        #token value: 0-9, '+'
        self.value = value
        
    def __str__(self):
        """
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )
        
    def __repre__(self):
        return self.__str__()
   
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        
    def error(self, msg='Lexical analysis error'):
        raise Exception(msg)
        
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
        
    def get_next_token(self):
        '''
        Lexical analyzer
        '''
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            elif self.current_char.isdigit():
                return Token(INTEGER, self.integer())
                
            elif self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
                
            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            
            elif self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
                
            elif self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
                
            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
                
            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
                
            else:               
                self.error("Current_char is " + self.current_char)
            
        return Token(EOF, None)
 
#================Parser============================
class AST(object):
    pass
    
class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
   
class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr
        
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        
    def error(self, msg='Syntax analysis error'):
        raise Exception(msg)
        
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error('self.current_token:'+str(self.current_token)+', expected token_type is ' + token_type)
    
    def factor(self):
        '''
            factor: INTEGER | LPAREN expr RPAREN
        '''
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            print("INTEGER " + str(token))
            return Num(token)
        elif token.type == LPAREN:
            print("LPAREN " + str(token))
            self.eat(LPAREN)
            node = self.expr()
            print("RPAREN " + str(self.current_token))
            self.eat(RPAREN)
            return node
        elif token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        else:
            self.error("Unknown token in factor(): " + str(token))
        
    def term(self):
        '''
            term: factor ((MUL | DIV) factor ) *
        '''
        node = self.factor()
        
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            else:
                self.error("Unknown token in term(): " + str(token))
            
            node = BinOp(left=node, op=token, right=self.factor())
                
        return node
        
    def expr(self):
        '''
            expr : term ((PLUS | MINUS) term)*
            term : factor((MUL|DIV) factor)*
            factor: INTEGER | LPAREN expr RPAREN
        '''
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            else:
                self.error("Unknown token in expr(): " + str(token))
            node = BinOp(left=node, op=token, right=self.term())
            
        return node
        
    def parse(self):
        return self.expr()


#=======================Interpreter===============================        
class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
        
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
 
class Interpreter(NodeVisitor):
    def __init__(self, parser):
        # Example: "3+5", " 71 - 15 "
        self.parser = parser
      
    def error(self, msg='Interpreter error'):
        raise Exception(msg)
        
    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        else:
            self.erorr("Unknown node op type: " + str(self.node.type))
    
    def visit_Num(self, node):
        return node.value
        
    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
    
    
def main():
    while True:
        try:
            text = raw_input('calc > ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)

def main2():
    tests = [  '7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)',
               '7 + (((3 + 2)))',
               '7 + 3 * (10 / (12 / (3 + 1) - 1))' ]
    results = [10, 12, 22]
    
    for text in tests:
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
        print ('='*20)
        
if __name__ == '__main__':
    main()