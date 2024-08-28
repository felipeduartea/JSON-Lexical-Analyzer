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
        """Move the position pointer and update the current character."""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        """Skip over any whitespace characters."""
        while self.current_char and self.current_char.isspace():
            self.advance()

    def string(self):
        """Handle string tokens."""
        result = ''
        self.advance()  
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance() 
        return Token(TokenType.STRING, result, self.pos)

    def number(self):
        """Handle numeric tokens including integers and decimals."""
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, float(result), self.pos)

    def identifier(self):
        """Handle boolean and null identifiers."""
        result = ''
        while self.current_char and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        keywords = {'true': TokenType.TRUE, 'false': TokenType.FALSE, 'null': TokenType.NULL}
        if result in keywords:
            value = True if result == 'true' else False if result == 'false' else None
            return Token(keywords[result], value, self.pos)
        raise ValueError(f'Invalid identifier: {result}')

    def get_next_token(self):
        """Retrieve the next token from the input text."""
        while self.current_char:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '"':
                return self.string()

            if self.current_char.isdigit() or (self.current_char == '-' and self.peek() and self.peek().isdigit()):
                return self.number()

            if self.current_char.isalpha():
                return self.identifier()

            token_map = {
                '{': TokenType.LBRACE, '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
                ':': TokenType.COLON, ',': TokenType.COMMA
            }

            if self.current_char in token_map:
                char = self.current_char
                self.advance()
                return Token(token_map[char], char, self.pos)

            raise ValueError(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF, None, self.pos)

    def peek(self):
        """Look at the next character without advancing the position."""
        return self.text[self.pos + 1] if self.pos + 1 < len(self.text) else None

    def generate_tokens(self):
        """Generate a list of tokens from the input text."""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
    
def run_tests():
    """Run a series of test cases including valid and invalid inputs."""

    test_cases = [
        ('{"name": "Felipe", "age": 20, "isMan": true, "languages": ["Python", "JavaScript"], "nullValue": null}',
         "Valid JSON with strings, numbers, booleans, arrays, and null values."),

        ('{"emptyObject": {}, "emptyArray": []}', 
         "Valid JSON with empty object and empty array."),

        ('{"negativeNumber": -42, "decimal": 3.14}', 
         "Valid JSON with negative number and decimal."),

        ('{"name": Felipe, "age": 20, "isMan": true}', 
         "Missing quotes around the string 'Felipe'."),

        ('{"age": @20}', 
         "Invalid character '@' before the number."),

        ('{"isValid": maybe}', 
         "Unrecognized identifier 'maybe' which is not true, false, or null."),

        ('{"languages": [Python, JavaScript]}', 
         "Missing quotes around strings inside the array."),

        ('{"unterminatedString": "hello}', 
         "Unterminated string, missing closing quote."),

        ('{"colonError" "missingColonValue"}', 
         "Missing colon between key and value."),

        ('{name: "Felipe"}', 
         "Key 'name' without quotes."),

        ('{"numberWithLetters": 123abc}', 
         "Number followed by unexpected letters."),

        ('{}', 
         "Valid empty JSON object."),

        ('[]', 
         "Valid empty JSON array."),

        ('{"key": "value", "number": 0.0}', 
         "Valid JSON with a float number zero."),
    ]

    for input_text, description in test_cases:
        print(f"Test: {description}")
        lexer = Lexer(input_text)
        try:
            tokens = lexer.generate_tokens()
            for token in tokens:
                print(token)
            print("Test passed.\n")
        except Exception as e:
            print(f"Test failed as expected with error: {e}\n")

if __name__ == "__main__":
    run_tests()
