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
        """Mova o ponteiro de posição e atualize o caractere atual."""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        """Pule os espaços sem nada"""
        while self.current_char and self.current_char.isspace():
            self.advance()

    def string(self):
        """Tratar os tokens da string, incluindo caracteres escapados"""
        result = ''
        self.advance()
        while self.current_char:
            if self.current_char == '"':
                break
            if self.current_char == '\\':
                self.advance()
                if self.current_char in '"\\/bfnrt':
                    escape_sequences = {
                        '"': '"', '\\': '\\', '/': '/', 'b': '\b',
                        'f': '\f', 'n': '\n', 'r': '\r', 't': '\t'
                    }
                    result += escape_sequences.get(self.current_char, self.current_char)
                else:
                    raise ValueError(f'Invalid escape character: \\{self.current_char}')
            else:
                result += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return Token(TokenType.STRING, result, self.pos)

    def number(self):
        """Tratar os tokens dos números, incluindo os decimais e notação científica"""
        result = ''
        if self.current_char == '-':
            result += self.current_char
            self.advance()
        while self.current_char and (self.current_char.isdigit() or self.current_char in '.eE'):
            if self.current_char in 'eE':
                result += self.current_char
                self.advance()
                if self.current_char in '+-':
                    result += self.current_char
                    self.advance()
            else:
                result += self.current_char
                self.advance()
        try:
            if '.' in result or 'e' in result or 'E' in result:
                return Token(TokenType.NUMBER, float(result), self.pos)
            else:
                return Token(TokenType.NUMBER, int(result), self.pos)
        except ValueError:
            raise ValueError(f'Invalid number format: {result}')

    def identifier(self):
        """Tratar nulos e boolenaos"""
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
        """Pegar o próximo caractere"""
        while self.current_char:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '"':
                return self.string()

            if self.current_char.isdigit() or (
                    self.current_char == '-' and self.peek() and (self.peek().isdigit() or self.peek() == '.')):
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
        """OLhar pro próximo caractere sem pular de posição"""
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
    """Test cases para testarmos o código feito"""

    test_cases = [
        ('{"name": "Felipe", "age": 20, "isMan": true, "languages": ["Python", "JavaScript"], "nullValue": null}',
         "Teste todo funcional e válido"),

        ('{"emptyObject": {}, "emptyArray": []}',
         "Válido vazio"),

        ('{"negativeNumber": -42, "decimal": 3.14, "scientific": 1.23e4}',
         "Json válido com decimal, negativo e notação científica"),

        ('{"name": "Felipe\\nSilva", "quote": "He said, \\"Hello!\\""}',
         "Strings com caracteres escapados"),

        ('{"name": Felipe, "age": 20, "isMan": true}',
         "'Felipe' sem aspas"),

        ('{"age": @20}',
         "@ que não deveria estar antes de um número"),

        ('{"isValid": maybe}',
         "Identificador desconhecido"),

        ('{"languages": [Python, JavaScript]}',
         "String sem aspas."),

        ('{"unterminatedString": "hello}',
         "String inacabada"),

        ('{name: "Felipe"}',
         "Nome sem a chave com aspas."),

        ('{"numberWithLetters": 123abc}',
         "Número seguido por caracteres"),

        ('{}',
         "JSON válido e vazio"),

        ('[]',
         "JSON vazio válido"),

        ('{"key": "value", "number": 0.0}',
         "Válido com float 0"),
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
