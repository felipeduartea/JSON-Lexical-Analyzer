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
        """Move o ponteiro de posição e atualiza o caractere atual."""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        """Ignora espaços em branco."""
        while self.current_char and self.current_char.isspace():
            self.advance()

    def string(self):
        """Trata tokens de string, incluindo caracteres escapados."""
        result = ''
        self.advance()  # Skip the initial quote
        while self.current_char:
            if self.current_char == '"':  # Detect closing quote
                break
            if self.current_char == '\\':  # Handle escape sequences
                self.advance()
                escape_sequences = {
                    '"': '"', '\\': '\\', '/': '/', 'b': '\b',
                    'f': '\f', 'n': '\n', 'r': '\r', 't': '\t'
                }
                result += escape_sequences.get(self.current_char, self.current_char)
            else:
                result += self.current_char
            self.advance()
        if self.current_char != '"':
            raise ValueError(f'String not closed properly at position {self.pos}')
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, result, self.pos)

    def number(self):
        """Trata tokens de número, incluindo decimais e notação científica."""
        result = ''
        if self.current_char == '-':
            result += self.current_char
            self.advance()
        while self.current_char and (self.current_char.isdigit() or self.current_char in '.eE'):
            result += self.current_char
            self.advance()
        try:
            if '.' in result or 'e' in result or 'E' in result:
                return Token(TokenType.NUMBER, float(result), self.pos)
            else:
                return Token(TokenType.NUMBER, int(result), self.pos)
        except ValueError:
            raise ValueError(f'Formato de número inválido: {result}')

    def identifier(self):
        """Trata identificadores como 'true', 'false' e 'null'."""
        result = ''
        while self.current_char and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        keywords = {'true': TokenType.TRUE, 'false': TokenType.FALSE, 'null': TokenType.NULL}
        if result in keywords:
            value = True if result == 'true' else False if result == 'false' else None
            return Token(keywords[result], value, self.pos)
        raise ValueError(f'Identificador inválido: {result}')

    def get_next_token(self):
        """Retorna o próximo token."""
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '"':
                return self.string()
            if self.current_char.isdigit() or (self.current_char == '-' and self.peek().isdigit()):
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

            raise ValueError(f'Caractere inválido: {self.current_char}')

        return Token(TokenType.EOF, None, self.pos)

    def peek(self):
        """Olha o próximo caractere sem avançar a posição."""
        return self.text[self.pos + 1] if self.pos + 1 < len(self.text) else None

    def generate_tokens(self):
        """Gera uma lista de tokens a partir do texto de entrada."""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
    
    
#Removemos a forma de execução do lexer, pois não é mais necessário.