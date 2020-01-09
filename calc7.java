/*
https://ruslanspivak.com/lsbasi-part7/

Writtent with AST and Visitor pattern

Visitor Pattern: https://www.baeldung.com/java-visitor-pattern

Old Case:
"1+1"
"27 + 3"
"27  - 7"
"100"
"7 - 3 + 2 - 1"
"10 /2 * 3" ==> 15
"14 + 2 * 3 - 6 / 2" ==> 17

New Case:
"7 + 3 * (10 / (12 / (3 + 1) - 1))" ==> 22


Parser / Interpreter

expr -> term ((PLUS|MINUS) term)*
term -> factor ((MUL|DIV) factor)*
factor -> INTEGER | LPAREN expr RPAREN

*/
class Solution {
    //==== Lexer: String -> Token =====
    public enum Type {
            PLUS, MINUS,
            MUL, DIV,
            LPAREN, RPAREN,
            INTEGER,
            EOF //End of file  
    }
    
    class Token {
        private Type type;
        private int value;
        private static final int NAN = 0;
        
        Token(Type type) {
            this.type = type;
            this.value = NAN;
        }
        
        Token(Type type, int value) {
            this.type = type;
            this.value = value;
        }
        
        public String toString() { 
            return "(" + type + "," + value + ")"; 
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
            currentChar = pos < text.length() ? text.charAt(pos) : NONE;
        }
        
                
        private void skipWhitespace() {
            while (currentChar != NONE && Character.isSpace(currentChar)) {
                advance();
            }
        }
        
        private int integer() {
            int result = 0;
            while (currentChar != NONE && Character.isDigit(currentChar)) {
                result = result * 10 + (currentChar - '0');
                advance();
            }
            return result;
        }
        
        public Token getNextToken() {
            while (currentChar != NONE) {
                if (Character.isSpace(currentChar)) {
                    skipWhitespace();
                    continue;
                } else if (Character.isDigit(currentChar)) {
                    return new Token(Type.INTEGER, integer());
                } else if (currentChar == '+') {
                    advance();
                    return new Token(Type.PLUS);
                } else if (currentChar == '-') {
                    advance();
                    return new Token(Type.MINUS);
                } else if (currentChar == '*') {
                    advance();
                    return new Token(Type.MUL);
                } else if (currentChar == '/') {
                    advance();
                    return new Token(Type.DIV);
                } else if (currentChar == '(') {
                    advance();
                    return new Token(Type.LPAREN);
                } else if (currentChar == ')') {
                    advance();
                    return new Token(Type.RPAREN);
                } else {
                    System.out.println("LEXER: Invalid Character: " + currentChar);
                }
                
            }
            return new Token(Type.EOF);
        }
    }
    
    //==== Parser: Token -> TreeNode =====
    public abstract class Node {
        public Token token;
        
        public Node(Token token) {
            this.token = token;
        }
        
        public abstract int accept(Visitor v);
    }
    
    public class BinOpNode extends Node {
        public Node left;
        public Node right;
        private Token op;
        
        public BinOpNode(Node left, Token op, Node right) {
            super(op);
            this.left = left;
            this.right = right;
            this.op = op;
        }
        
        public int accept(Visitor v) {
            return v.visit(this);
        }
        
    }
    
    public class NumNode extends Node {
        public NumNode(Token token) {
            super(token);
        }
        
        public int accept(Visitor v) {
            return v.visit(this);
        }
    }
    
    class Parser {
        private Lexer lexer;
        private Token currentToken;
        
        Parser(Lexer lexer) {
            this.lexer = lexer;
            this.currentToken = lexer.getNextToken();
        }
        
        private void eat(Type tokenType) {
            System.out.println(currentToken);
            if (currentToken.type != tokenType) {
               System.out.println("Invalid Syntax: Expected token: " + tokenType + ", actual token " + currentToken.type);
            }
            currentToken = lexer.getNextToken();
        }
        
        private Node factor() {
            Token token = currentToken;
            /*
            if (token.type == Type.PLUS) {
                eat(Type.PLUS);
                return factor();
            } else if (token.type == Type.MINUS) {
                eat(Type.MINUS);
                return -1 * factor();
            } else */
            if (token.type == Type.INTEGER) {
                eat(Type.INTEGER);
                return new NumNode(token);
            } else if (token.type == Type.LPAREN) {
                eat(Type.LPAREN);
                Node node = expr();
                eat(Type.RPAREN);
                return node;
            }
            System.out.println("Invalid Syntax in factor()");
            return null; //Should never reach here
        }
        
        private Node term() {
            Node node = factor();
            while (currentToken.type == Type.MUL || currentToken.type == Type.DIV) {
                Token token = currentToken;
                if (token.type == Type.MUL) {
                    eat(Type.MUL);
                } else if (token.type == Type.DIV) {
                    eat(Type.DIV);
                }
                 node = new BinOpNode(node, token, factor());
            }
            return node;
        }
        
        private Node expr() {
            //set current token to the first token taken from the input
            Node node = term();

            while (currentToken.type == Type.PLUS || currentToken.type == Type.MINUS) {
                Token token = currentToken;
                if (token.type == Type.PLUS) {
                    eat(Type.PLUS);
                } else if (token.type == Type.MINUS) {
                    eat(Type.MINUS);
                }
                node = new BinOpNode(node, token, term());
            }
            return node;
        }
        
        public Node parse() {
            return expr();
        }
    }
    
    //------Interpreter---------
    public interface Visitor {
        int visit(BinOpNode binOp);
        int visit(NumNode num);
    }
    
    public class Interpreter implements Visitor {
        private Parser parser;
        
        Interpreter(Parser parser) {
            this.parser = parser;
        }
        
        @Override
        public int visit(BinOpNode binOp) {
            switch (binOp.op.type) {
                case PLUS:
                    return binOp.left.accept(this) + binOp.right.accept(this);
                case MINUS:
                    return binOp.left.accept(this) - binOp.right.accept(this);
                case MUL:
                    return binOp.left.accept(this) * binOp.right.accept(this);
                case DIV:
                    return binOp.left.accept(this) / binOp.right.accept(this);
            }
            System.out.println("Interpreter Error: Should not reach here");
            return 0;
        }

        @Override
        public int visit(NumNode num) {
            System.out.println("processing NumNode");
            return num.token.value;
        }
        
        public int interpret() {
            Node tree = parser.parse();
            return tree.accept(this);
        }
    }
    
    public int calculate(String text) {
        Lexer lexer = new Lexer(text);
        Parser parser = new Parser(lexer);
        Interpreter interpreter = new Interpreter(parser);
        int result = interpreter.interpret();
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