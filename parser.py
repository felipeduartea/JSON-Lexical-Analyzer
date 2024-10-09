class JSONParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        """Avança para o próximo token."""
        self.current_token = self.tokens.pop(0) if self.tokens else None

    def parse(self):
        """Inicia a análise do valor JSON."""
        return self.value()

    def value(self):
        """Analisa os valores: objeto, array, número, string, true, false, null."""
        if self.current_token.type == 'LBRACE':
            return self.object()
        elif self.current_token.type == 'LBRACKET':
            return self.array()
        elif self.current_token.type == 'NUMBER':
            return self.number()
        elif self.current_token.type == 'STRING':
            return self.string()
        elif self.current_token.type == 'TRUE':
            self.next_token()
            return True
        elif self.current_token.type == 'FALSE':
            self.next_token()
            return False
        elif self.current_token.type == 'NULL':
            self.next_token()
            return None
        else:
            raise SyntaxError(f"Token inesperado: {self.current_token}")

    def object(self):
        """Analisa um objeto JSON."""
        obj = {}
        self.next_token()  # Consome '{'
        while self.current_token.type != 'RBRACE':
            key = self.string()
            self.expect('COLON')
            value = self.value()
            obj[key] = value
            if self.current_token.type == 'COMMA':
                self.next_token()  # Consome ','
            elif self.current_token.type != 'RBRACE':
                raise SyntaxError(f"Esperado ',' ou '}}', mas encontrado {self.current_token}")
        self.next_token()  # Consome '}'
        return obj

    def array(self):
        """Analisa um array JSON."""
        arr = []
        self.next_token()  # Consome '['
        while self.current_token.type != 'RBRACKET':
            arr.append(self.value())
            if self.current_token.type == 'COMMA':
                self.next_token()  # Consome ','
            elif self.current_token.type != 'RBRACKET':
                raise SyntaxError(f"Esperado ',' ou ']', mas encontrado {self.current_token}")
        self.next_token()  # Consome ']'
        return arr

    def number(self):
        """Analisa números (inteiros ou fracionários)."""
        num_value = self.current_token.value
        self.next_token()
        return num_value

    def string(self):
        """Analisa strings JSON."""
        str_value = self.current_token.value
        self.next_token()
        return str_value

    def expect(self, token_type):
        """Verifica se o token atual é o esperado e avança para o próximo."""
        if self.current_token.type != token_type:
            raise SyntaxError(f"Esperado '{token_type}', mas encontrado {self.current_token}")
        self.next_token()