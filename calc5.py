INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = ('INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'EOF')

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
        
class Interpreter(object):
    def __init__(self, lexer):
        # Example: "3+5", " 71 - 15 "
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
           facotr: INTEGER
        '''
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            result = token.value
            print("INTEGER " + str(token))
        elif token.type == LPAREN:
            print("LPAREN " + str(token))
            self.eat(LPAREN)
            result = self.expr()
            print("RPAREN " + str(self.current_token))
            self.eat(RPAREN)
        
        return result

        
    def term(self):
        '''
            term : factor ((MUL | DIV) factor)*
        '''
        
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()
            else:
                self.error('Unknow token in term()' + str(token))
            print("Op " + str(token))
        return result
        
    def expr(self):
        '''
            expr : term ((PLUS | MINUS) term)*
        '''
        result = self.term()
        
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()
            else:
                self.error('Unknow token in expr()' + str(token))
            print("Op " + str(token))
            
        return result
    
def main():
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)
        
if __name__ == '__main__':
    main()