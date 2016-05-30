INTEGER, PLUS, MINUS, MUL, DIV, EOF = ('INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF')

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
    
    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        print("INTEGER " + str(token))
        return token.value
        
    def expr(self):
        '''
        Parser / Interpreter
            expr -> INTEGER
            expr -> INTEGER PLUS INTEGER
            expr -> INTEGER MINUS INTEGER
            expr -> INTEGER MUL INTEGER
            expr -> INTEGER DIV INTEGER
            expr -> INTEGER op INTEGER op INTEGER ...
        '''
        
        result = self.term()

        while self.current_token.type != EOF:
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif op.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()
            elif op.type == MUL:
                self.eat(MUL)
                result = result * self.term()
            elif op.type == DIV:
                self.eat(DIV)
                result = result / self.term()
            else:
                self.error('Unknow op ' + str(op))
            print("Op " + str(op))
        return result
    
def main():
    while True:
        try:
            text = raw_input('calc > ')
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