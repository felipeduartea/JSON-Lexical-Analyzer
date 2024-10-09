from lexer import Lexer 
from parser import JSONParser  

def main():
    json_input = '{"name": "Felipe", "age": 20, "isMan": true, "languages": ["Python", "JavaScript"], "nullValue": null}' #Exemplo de uma entrada

    lexer = Lexer(json_input)     # Criando o lexer, com objetivo de gerar tokens
    tokens = lexer.generate_tokens() # Gera os tokens a partir do texto de entrada

    parser = JSONParser(tokens)    # Criando o parser que vai validar e processar os tokens

    try:
        parsed_json = parser.parse() # Inicia a análise do valor JSON
        print("JSON interpretado com sucesso:")
        print(parsed_json)
    except Exception as e:
        print(f"Erro ao interpretar o JSON: {e}")

if __name__ == "__main__":
    main()