INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

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
        self.text = text
        self.pos = 0
        self.current_token = None
        
    def error(self, msg='Error parsing input'):
        raise Exception(msg)
    
    def nextCharIsInt(self):
        if self.pos + 1 > len(self.text) - 1:
            return False
        
        return self.text[self.pos+1].isdigit()
        
    def get_next_token(self):
        """
        Lexical analyzer
        """
        text = self.text
        
        if self.pos > len(text) - 1:
            return Token(EOF, None)
            
        current_char = text[self.pos]
        
        if current_char.isdigit():
            buffer = int(current_char)
            while self.nextCharIsInt():
                self.pos += 1
                current_char = text[self.pos]
                buffer = buffer * 10 + int(current_char)        
            token = Token(INTEGER, int(buffer))
            self.pos += 1
            return token
            
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
            
        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token
        
        if current_char == ' ':
            self.pos += 1
            return self.get_next_token()
        
        self.error("Current_char is " + current_char)
        
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error('self.current_token:'+str(self.current_token)+', token_type is ' + token_type)
            
    def expr(self):
        """
            expr -> INTEGER PLUS INTEGER
        """
        self.current_token = self.get_next_token()
        
        left = self.current_token
        self.eat(INTEGER)
        print("Left " + str(left))
        
        op = self.current_token
        if op.value == '+':
            self.eat(PLUS)
        elif op.value == '-':
            self.eat(MINUS)
        else:
            self.error('Unknow op ' + str(op))
        print("Op " + str(op))
        
        
        right = self.current_token
        self.eat(INTEGER)
        print("Right " + str(right))
        
        if op.value == '+':
            result = left.value + right.value
        elif op.value == '-':
            result = left.value - right.value
        return result
    
def main():
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)
        
if __name__ == '__main__':
    main()