from analisador_lexico import lexer
from analisador_sintatico import parser, parse_file
from analisador_semantico import Semantico

def main():
    caminho_do_arquivo = 'codigo_teste.txt'

    with open(caminho_do_arquivo, 'r') as file:
        lexer.input(file.read())
        for token in lexer:
            print(token)

    print("analise lexica bem sucedida.")

    ast = parse_file(caminho_do_arquivo)

    semantico = Semantico()
    semantico.analyze(ast)
    print("analise semantica bem sucedida.")

if __name__ == "__main__":
    main()
