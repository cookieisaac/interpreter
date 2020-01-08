/*
https://ruslanspivak.com/lsbasi-part5/

Old Case:
"1+1"
"27 + 3"
"27  - 7"
"100"
"7 - 3 + 2 - 1"

New Case:
"10 /2 * 3" ==> 15
"14 + 2 * 3 - 6 / 2" ==> 17


Parser / Interpreter

expr -> term ((PLUS|MINUS) term)*
term -> factor ((MUL|DIV) factor)*
factor -> INTEGER

*/

class Solution {
    public enum Type {
            PLUS, MINUS,
            MUL, DIV,
            INTEGER,
            EOF //End of file  
    }
    
    class Token {
        private Type type;
        private int value;
        
        Token(Type type, int value) {
            this.type = type;
            this.value = value;
        }
        
        public String toString() { 
            return "("+type+","+value+")"; 
        }
    }
    
    class Lexer {
        private String text;
        private int pos;
        private char currentChar;
        private static final char NONE = '$';
        
        Lexer(String text) {
            this.text = text;
            this.pos = 0; //Current position to be consumed
            this.currentChar = text.charAt(pos);
        }
        
        private void advance() {
            pos++;
            if (pos == text.length()) {
                currentChar = NONE;
            } else {
                currentChar = text.charAt(pos);
            }
        }
        
                
        private void skipWhitespace() {
            while (currentChar != NONE && Character.isSpace(currentChar)) {
                advance();
            }
        }
        
        private int integer() {
            StringBuilder sb = new StringBuilder();
            while (currentChar != NONE && Character.isDigit(currentChar)) {
                sb.append(currentChar);
                advance();
            }
            return Integer.parseInt(sb.toString());
        }
        
        public Token getNextToken() throws Exception {
            while (currentChar != NONE) {
                if (Character.isSpace(currentChar)) {
                    skipWhitespace();
                    continue;
                } else if (Character.isDigit(currentChar)) {
                    return new Token(Type.INTEGER, integer());
                } else if (currentChar == '+') {
                    advance();
                    return new Token(Type.PLUS, 0);
                } else if (currentChar == '-') {
                    advance();
                    return new Token(Type.MINUS, 0);
                } else if (currentChar == '*') {
                    advance();
                    return new Token(Type.MUL, 0);
                } else if (currentChar == '/') {
                    advance();
                    return new Token(Type.DIV, 0);
                } else {
                    throw new Exception("LEXER: Invalid Character: " + currentChar);
                }
                
            }
            return new Token(Type.EOF, 0);
        }
    }
    
    class Interpreter {
        private Lexer lexer;
        private Token currentToken;
        
        Interpreter(Lexer lexer) throws Exception {
            this.lexer = lexer;
            this.currentToken = lexer.getNextToken();
        }
        
        private void eat(Type tokenType) throws Exception {
            if (currentToken.type != tokenType) {
               throw new Exception("Invalid Syntax: Expected token: " + tokenType + ", actual token " + currentToken.type);
            }
            currentToken = lexer.getNextToken();
        }
        
        private int factor() throws Exception {
            Token token = currentToken;
            eat(Type.INTEGER);
            return token.value;
        }
        
        private int term() throws Exception {
            int result = factor();
            while (currentToken.type == Type.MUL || currentToken.type == Type.DIV) {
                Token token = currentToken;
                if (token.type == Type.MUL) {
                    eat(Type.MUL);
                    result = result * factor();
                } else if (token.type == Type.DIV) {
                    eat(Type.DIV);
                    result = result / factor();
                } 
            }
            return result;
        }
        
        private int expr() throws Exception {
            //set current token to the first token taken from the input
            int result = term();

            while (currentToken.type == Type.PLUS || currentToken.type == Type.MINUS) {
                Token token = currentToken;
                if (token.type == Type.PLUS) {
                    eat(Type.PLUS);
                    result =  result + term();
                } else if (token.type == Type.MINUS) {
                    eat(Type.MINUS);
                    result =  result - term();
                }
            }
            return result;
        }
    }
    
    public int calculate(String text) {
        Lexer lexer = new Lexer(text);
        int result = 0;
        try {
            Interpreter interpreter = new Interpreter(lexer);
            result = interpreter.expr();
        } catch (Exception e) {
            System.out.println(e);
        }
        return result;
    }
}

public class MainClass {
    public static String stringToString(String input) {
        return JsonArray.readFrom("[" + input + "]").get(0).asString();
    }
    
    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        String line;
        while ((line = in.readLine()) != null) {
            String s = stringToString(line);
            
            int ret = new Solution().calculate(s);
            
            String out = String.valueOf(ret);
            
            System.out.println(out);
        }
    }
}