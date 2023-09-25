import os
import json

class Livro:
    def __init__(self, isbn, titulo, ano, autor):
        self.isbn = isbn
        self.titulo = titulo
        self.ano = ano
        self.autor = autor

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def load_data():
    try:
        with open('livro.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def save_data(data):
    with open('livro.json', 'w') as file:
        json.dump(data, file, indent=4)

def insert_book(data, livro):
    data.append({'isbn': livro.isbn, 'titulo': livro.titulo, 'ano': livro.ano, 'autor': livro.autor})
    save_data(data)
    print("\nLivro cadastrado com sucesso!\n")

def remove_book(data, isbn):
    for livro in data:
        if livro['isbn'] == isbn:
            data.remove(livro)
            save_data(data)
            print("\nLivro removido com sucesso!")
            return
    print("\nLivro não encontrado!\n")

def update_book(data, isbn, field, new_value):
    for livro in data:
        if livro['isbn'] == isbn:
            livro[field] = new_value
            save_data(data)
            print(f"\nInformação '{field}' atualizada com sucesso!\n")
            return
    print("\nLivro não encontrado!\n")

def find_book(data, isbn):
    for livro in data:
        if livro['isbn'] == isbn:
            return livro
    input("\nTecle Enter para voltar ao menu...")

def list_books(data):
    clear_screen()
    print("Biblioteca Unicap")
    print("_" * 80)
    print("\nListagem Geral\n")
    print("ISBN            |              Título                   | Ano  |     Autor     ")
    print("_" * 80)
    for livro in data:
        print(f"{livro['isbn']:15} | {livro['titulo']:25} | {livro['ano']} | {livro['autor']:<15}")
    input("\nTecle Enter para voltar ao menu...")

def main():
    data = load_data()
    op = None
    while op != '0':
        clear_screen()
        print("Biblioteca Unicap")
        print("_" * 80)
        print("\nOpções:")
        print("1- Cadastrar novo livro")
        print("2- Remover livro")
        print("3- Consultar livro por ISBN")
        print("4- Listagem geral")
        print("5- Atualizar informação do livro")
        print("0- Sair")
        op = input("\nInforme a opção desejada: ")
        if op == "1":
            livro = Livro(input("ISBN: "), input("Título: "), input("Ano: "), input("Autor: "))
            insert_book(data, livro)
        elif op == "2":
            isbn = input("ISBN: ")
            remove_book(data, isbn)
        elif op == "3":
            isbn = input("ISBN do livro: ")
            livro = find_book(data, isbn)
            if livro:
                print(f"{livro['isbn']:15} | {livro['titulo']:<20} | {livro['ano']} | {livro['autor']:<15}")
            else:
                print("\nISBN não encontrada!\n")
        elif op == "4":
            list_books(data)
        elif op == "5":
            isbn = input("ISBN do livro que deseja atualizar: ")
            field = input("Campo que deseja atualizar (ISBN, Título, Ano, Autor): ").lower()
            new_value = input(f"Novo valor para o campo '{field}': ")
            update_book(data, isbn, field, new_value)
        elif op == "0":
            exit()
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main()
