import os
import json

class Livro:
    def __init__(self, isbn, titulo, ano):
        self.isbn = isbn
        self.titulo = titulo
        self.ano = ano

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def load_data():
    try:
        with open('livro.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

def save_data(data):
    with open('livro.json', 'w') as file:
        json.dump(data, file, indent=4)

def insert_book(data, livro):
    data.append({'isbn': livro.isbn, 'titulo': livro.titulo, 'ano': livro.ano})
    save_data(data)
    print("\nLivro cadastrado com sucesso!\n")

def remove_book(data, isbn):
    for livro in data:
        if livro['isbn'] == isbn:
            data.remove(livro)
            save_data(data)
            print("\nLivro removido com sucesso!")
            return
    print("\nLivro não encontrado!\a")

def find_book(data, isbn):
    for livro in data:
        if livro['isbn'] == isbn:
            
            print(f"{livro['isbn']:9} | {livro['titulo']:<20} | {livro['ano']}")
    input("\nTecle Enter para voltar ao menu...")
        

def list_books(data):
    clear_screen()
    print("Biblioteca Unicap")
    print("_" * 80)
    print("\nListagem Geral\n")
    print("ISBN    |        Título        |   Ano")
    print("_" * 80)
    for livro in data:
        print(f"{livro['isbn']:9} | {livro['titulo']:<20} | {livro['ano']}")
    input("\nTecle Enter para voltar ao menu...")

def main():
    data = load_data()
    op = None
    while op != 0:
        clear_screen()
        print("Biblioteca Unicap")
        print("_" * 80)
        print("\nOpções:")
        print("1- Cadastrar novo livro")
        print("2- Remover livro")
        print("3- Consultar livro por ISBN")
        print("4- Listagem geral")
        print("0- Sair")
        op = input("\nInforme a opção desejada: ")
        if op == "1":
            livro = Livro(input("ISBN: "), input("Título: "), input("Ano: "))
            insert_book(data, livro)
        elif op == "2":
            isbn = input("ISBN: ")
            remove_book(data, isbn)
        elif op == "3":
            isbn = input("ISBN do livro: ")
            livro = find_book(data, isbn)
            if livro:
                print(f"\nISBN {livro['isbn']} | {livro['titulo']} | {livro['ano']}")
            else:
                print("\nISBN não encontrada!\n")
        elif op == "4":
            list_books(data)
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main()
