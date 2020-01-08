/*
https://ruslanspivak.com/lsbasi-part3/

Old Case:
"1+1"
"27 + 3"
"27  - 7"

New Case:
"100"
"7 - 3 + 2 - 1"


Parser / Interpreter

expr -> term ((PLUS|MINUS) term)*
term -> INTEGER

*/

class Solution {
    public enum Type {
            PLUS,
            MINUS,
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
    
    class Interpreter {
        private String text;
        private int pos;
        private char currentChar;
        private Token currentToken;
        private static final char NONE = '$';
        
        Interpreter(String text) {
            this.text = text;
            this.pos = 0; //Current position to be consumed
            this.currentToken = null;
            this.currentChar = text.charAt(pos);
        }
        
        void advance() {
            pos++;
            if (pos == text.length()) {
                currentChar = NONE;
            } else {
                currentChar = text.charAt(pos);
            }
        }
        
        void skipWhitespace() {
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
        
        private int term() throws Exception {
            Token token = currentToken;
            eat(Type.INTEGER);
            return token.value;
        }
        
        private Token getNextToken() throws Exception {
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
                } else {
                    throw new Exception("Unregonized Character: " + currentChar);
                }
                
            }
            return new Token(Type.EOF, 0);
        }
        
        private void eat(Type tokenType) throws Exception {
            if (currentToken.type != tokenType) {
               throw new Exception("Expected token: " + tokenType + ", actual token " + currentToken.type);
            }
            this.currentToken = getNextToken();
        }
        
        public int expr() throws Exception {
            //set current token to the first token taken from the input
            currentToken = getNextToken();
            
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
    
    int calculate(String text) {
        int result = 0;
        Interpreter interpreter = new Interpreter(text);
        try {
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