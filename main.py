from lexer import Lexer 
from parser import JSONParser  

import pprint

def main():
    json_input = '{"name": "Felipe", "age": 20, "isMan": true, "languages": ["Python", "JavaScript"], "nullValue": null, "object": {"key": "value"}, "array": [1, 2, 3]}' #Exemplo de uma entrada

    lexer = Lexer(json_input)     # Criando o lexer, com objetivo de gerar tokens
    tokens = lexer.generate_tokens() # Gera os tokens a partir do texto de entrada

    print("Tokens gerados:")
    print("\033[93m") # Yellow
    for token in tokens:
        print("Token:", token)
    print("\033[0m") # Reset color

    parser = JSONParser(tokens)    # Criando o parser que vai validar e processar os tokens

    try:
        parsed_json = parser.parse() # Inicia a análise do valor JSON
        print("JSON interpretado com sucesso:")
        print(parsed_json)
        
        print('\n')
        print("\033[92m") # Green
        print("Imprimindo o JSON inteiro formatado:")
        pprint.pprint(parsed_json, indent=1, sort_dicts=False)
        print("\033[0m") # Reset color

        print('\n')
        print("\033[91m") # Red
        print("Imprimindo o valor do objeto 'key':")
        print("\033[90m->", parsed_json.get('object').get('key')) # Dark gray
        print("\033[0m") # Reset color

        print('\n')
        print("\033[91m") # Red
        print("Imprimindo o valor do array 'array':")
        print("\033[90m->", parsed_json.get('array')[1]) # Dark gray
        print("\033[0m") # Reset color
    except Exception as e:
        print(f"Erro ao interpretar o JSON: {e}")

if __name__ == "__main__":
    main()