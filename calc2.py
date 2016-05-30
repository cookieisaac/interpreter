INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EOF'

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
        
class Interpreter(object):
    def __init__(self, text):
        # Example: "3+5", " 71 - 15 "
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]
        
    def error(self, msg='Error parsing input'):
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
                return Token(MULTIPLY, '*')
                
            elif self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')
            else:               
                self.error("Current_char is " + self.current_char)
            
        return Token(EOF, None)
        
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error('self.current_token:'+str(self.current_token)+', token_type is ' + token_type)
            
    def expr(self):
        '''
        Parser / Interpreter
            expr -> INTEGER
            expr -> INTEGER PLUS INTEGER
            expr -> INTEGER MINUS INTEGER
            expr -> INTEGER MULTIPLY INTEGER
            expr -> INTEGER DIVIDE INTEGER
            expr -> INTEGER op INTEGER op INTEGER ...
        '''
        self.current_token = self.get_next_token()
        
        left = self.current_token
        self.eat(INTEGER)
        print("Left " + str(left))
        
        result = left.value
        while self.current_token.type != EOF:
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
            elif op.type == MINUS:
                self.eat(MINUS)
            elif op.type == MULTIPLY:
                self.eat(MULTIPLY)
            elif op.type == DIVIDE:
                self.eat(DIVIDE)
            else:
                self.error('Unknow op ' + str(op))
            print("Op " + str(op))
            
            
            right = self.current_token
            self.eat(INTEGER)
            print("Right " + str(right))
            
            if op.type == PLUS:
                result = left.value + right.value
            elif op.type == MINUS:
                result = left.value - right.value
            elif op.type == MULTIPLY:
                result = left.value * right.value
            elif op.type == DIVIDE:
                result = left.value / right.value
            
            left = Token(INTEGER, result)
        return result
    
def main():
    while True:
        try:
            text = raw_input('calc > ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)
        
if __name__ == '__main__':
    main()