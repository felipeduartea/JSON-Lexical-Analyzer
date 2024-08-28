### Detailed Explanation of the Lexer Code
This document provides a detailed explanation of a lexer (lexical analyzer) code that converts an input string into a sequence of tokens. The lexer appears to be designed to parse a JSON-like data structure.

Import Statements and Basic Class Definitions
```
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
```


import re: Imports the regular expressions module, although it is not currently used in the code.
class TokenType: Defines constants for each type of token the lexer can recognize, such as strings, numbers, booleans (TRUE, FALSE), and JSON symbols (LBRACE, RBRACE, etc.).
```
class Token:
    def __init__(self, type_, value, position):
        self.type = type_
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, position={self.position})"
```


class Token: Defines an object representing a token.
__init__: Initializes a token with its type (type_), value (value), and position in the input string.
__repr__: Returns a textual representation of the token, useful for debugging.
Lexer Class: Lexical Analyzer

```
class Lexer:
    def __init__(self, input_text):
        self.text = input_text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
```


class Lexer: Defines the lexer responsible for converting the input string into tokens.
__init__: Initializes the lexer with the input text, sets the current position to 0, and sets the current character.
Basic Methods of the Lexer
```
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
```


advance: Moves the lexer’s position to the next character in the input.
```
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
```


skip_whitespace: Skips over all whitespace characters until it finds a non-space character.
Methods to Recognize Different Token Types
python
Copy code
    def string(self):
        result = ''
        self.advance()  
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  
        return Token(TokenType.STRING, result, self.pos)


string: Recognizes and returns a string that starts and ends with quotation marks (").
```
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
```


number: Recognizes integer and decimal numbers.
```
    def identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
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
```


identifier: Recognizes identifiers like true, false, and null.
Method to Get the Next Token
```
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
```


get_next_token: Identifies the next token in the input string, generating tokens based on the current character.
Helper Methods and Token Generation
python
Copy code
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        else:
            return None


peek: Looks at the next character without advancing in the string.
```
    def generate_tokens(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
```


generate_tokens: Generates and returns a list of all tokens from the input string.
```
def run_tests():
    lexer = Lexer('{"name": "Felipe", "age": 20, "isMan": true, "languages": ["Python", "JavaScript"], "nullValue": null}')
    tokens = lexer.generate_tokens()
    for token in tokens:
        print(token)

if __name__ == "__main__":
    run_tests()
```


run_tests: Creates a lexer with a sample JSON string and prints all generated tokens.
if __name__ == "__main__": run_tests(): Executes the tests if the script is run directly.
