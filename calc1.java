/*
https://ruslanspivak.com/lsbasi-part1/
*/

class Solution {
    public enum Type {
            PLUS,
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
        private Token currentToken;
        
        Interpreter(String text) {
            this.text = text;
            this.pos = 0; //Current position to be consumed
            this.currentToken = null;
        }
        
        Token getNextToken() throws Exception {
            if (pos == text.length()) {
                return new Token(Type.EOF, 0);
            }
            
            char currentChar = text.charAt(pos);
            if (Character.isDigit(currentChar)) {
                pos++;
                return new Token(Type.INTEGER, currentChar - '0');
            } else if (currentChar == '+') {
                pos++;
                return new Token(Type.PLUS, 0);
            } 
            throw new Exception("Unregonized Character: " + currentChar);
            
        }
        
        void eat(Type tokenType) throws Exception {
            if (currentToken.type != tokenType) {
               throw new Exception("Expected token: " + tokenType + ", actual token " + currentToken.type);
            }
            this.currentToken = getNextToken();
        }
        
        int expr() throws Exception {
            currentToken = getNextToken();
            Token left = this.currentToken;
            eat(Type.INTEGER);
            
            Token op = currentToken;
            eat(Type.PLUS);
            
            Token right = currentToken;
            eat(Type.INTEGER);
            
            int result =  left.value + right.value;
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
            
            System.out.print(out);
        }
    }
}