import re

class TokenType:
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    NULL = 'NULL'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    COLON = 'COLON'
    COMMA = 'COMMA'
    EOF = 'EOF'

class Token:
    def __init__(self, type_, value, position):
        self.type = type_
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, position={self.position})"

class Lexer:
    def __init__(self, input_text):
        self.text = input_text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def string(self):
        result = ''
        self.advance()  
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  
        return Token(TokenType.STRING, result, self.pos)

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        return Token(TokenType.NUMBER, float(result), self.pos)

    def identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        if result == 'true':
            return Token(TokenType.TRUE, True, self.pos)
        elif result == 'false':
            return Token(TokenType.FALSE, False, self.pos)
        elif result == 'null':
            return Token(TokenType.NULL, None, self.pos)
        else:
            raise Exception(f'Invalid identifier: {result}')

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '"':
                return self.string()

            if self.current_char.isdigit() or (self.current_char == '-' and self.peek().isdigit()):
                return self.number()

            if self.current_char.isalpha():
                return self.identifier()

            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{', self.pos)

            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}', self.pos)

            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET, '[', self.pos)

            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET, ']', self.pos)

            if self.current_char == ':':
                self.advance()
                return Token(TokenType.COLON, ':', self.pos)

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.pos)

            raise Exception(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF, None, self.pos)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        else:
            return None

    def generate_tokens(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
    
def run_tests():
    lexer = Lexer('{"name": "Felipe", "age": 20, "isMan": true, "languages": ["Python", "JavaScript"], "nullValue": null}')
    tokens = lexer.generate_tokens()
    for token in tokens:
        print(token)

if __name__ == "__main__":
    run_tests()
