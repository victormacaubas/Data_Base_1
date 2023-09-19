import os
import struct

class Livro:
    def __init__(self, isbn, titulo, ano):
        self.isbn = isbn
        self.titulo = titulo
        self.ano = ano

def linha():
    for _ in range(80):
        print("_", end="")
    print("\n")

def cabec():
    os.system("cls" if os.name == "nt" else "clear")
    print("Biblioteca Unicap")
    linha()

def abre_arquivo():
    try:
        plivro = open("livro.dat", "r+b")
    except FileNotFoundError:
        plivro = open("livro.dat", "w+b")
    return plivro

def inserir(plivro):
    resp = 1
    while resp == 1:
        cabec()
        print("\n\nCadastrar novo livro\n\n")
        isbn = int(input("ISBN: "))
        titulo = input("Titulo: ")
        ano = int(input("Ano: "))
        livro = Livro(isbn, titulo, ano)
        plivro.seek(0, os.SEEK_END)
        data = struct.pack('i', livro.isbn) + livro.titulo.encode('utf-8') + struct.pack('i', livro.ano)
        plivro.write(data)
        print("\n\nLivro cadastrado com sucesso!\n")
        resp = int(input("Deseja cadastrar outro Livro (1-sim/0-nao)? "))

def procura(plivro, isbnp):
    p = 0
    plivro.seek(0)
    while True:
        data = plivro.read(60)  # Assuming 4 bytes for int, 52 bytes for str, and 4 bytes for int
        if not data:
            break
        livro = Livro(*struct.unpack('i52si', data))
        if livro.isbn == isbnp:
            return p
        p += 1
    return -1

def mostre(plivro, pos):
    plivro.seek(pos * 60)
    data = plivro.read(60)  # Assuming 4 bytes for int, 52 bytes for str, and 4 bytes for int
    isbn = struct.unpack('i', data[:4])[0]
    titulo = data[4:56].decode('utf-8', errors='replace').strip()
    ano = struct.unpack('i', data[-4:])[0]

    print("\n\n")
    linha()
    print("ISBN titulo ano")
    linha()
    print(f"{isbn:9} | {titulo:<20} | {ano}")
    linha()

def consultar(plivro):
    resp = 1
    while resp == 1:
        cabec()
        print("\n\nConsultar livro\n\n")
        isbncon = int(input("ISBN do livro: "))
        posicao = procura(plivro, isbncon)
        if posicao == -1:
            print("\n\nISBN nao encontrada!\n")
        else:
            mostre(plivro, posicao)
        resp = int(input("Deseja consultar outro (1-sim/0-nao)? "))

def remover(plivro):
    resp = 1
    while resp == 1:
        cabec()
        print("\n\nRemover livro\n\n")
        isbnrem = int(input("ISBN: "))
        posicao = procura(plivro, isbnrem)
        if posicao == -1:
            print("\nlivro nao encontrado!!\a")
        else:
            mostre(plivro, posicao)
            conf = int(input("\n\nDeseja remover o livro (1-sim/0-nao)? "))
            if conf == 1:
                plivro.seek(posicao * 60)
                plivro.write(b'\x00' * 60)  # Writing 60 bytes of null bytes
                print("\n\nlivro removido com sucesso!")
            else:
                print("\nRemocao cancelada!")
        resp = int(input("\n\n\nDeseja remover outro (1-sim/0-nao)? "))

def alterar(plivro):
    resp = 1
    while resp == 1:
        cabec()
        print("\n\nAlterar ano do livro\n\n")
        isbnalt = int(input("ISBN: "))
        posicao = procura(plivro, isbnalt)
        if posicao == -1:
            print("\nlivro nao encontrado!!\a")
        else:
            mostre(plivro, posicao)
            conf = int(input("\n\nAlterar o ano do livro (1-sim/0-nao)? "))
            if conf == 1:
                novo_ano = int(input("\nNovo ano: "))
                plivro.seek(posicao * 60 + 56)  # Positioning at the 'ano' field in the record
                plivro.write(struct.pack('i', novo_ano))  # Writing the new 'ano' value
                print("\nAno do livro alterado com sucesso!\n")
                mostre(plivro, posicao)
            else:
                print("\n\nAlteracao cancelada!\n")
        resp = int(input("\n\nDeseja alterar outro (1-sim/0-nao)? "))

def listagem(plivro):
    resp = 0
    while resp == 0:
        cabec()
        print("\n\nListagem Geral\n\n")
        linha()
        print("ISBN    |        titulo        |   ano")
        linha()
        plivro.seek(0)
        while True:
            data = plivro.read(60)  # Assuming 4 bytes for int, 52 bytes for str, and 4 bytes for int
            if not data:
                break
            isbn = struct.unpack('i', data[:4])[0]
            titulo = data[4:56].decode('utf-8', errors='replace').strip()
            ano = struct.unpack('i', data[-4:])[0]
            if isbn != 0:
                print(f"{isbn:9} | {titulo:<20} | {ano}")
        linha()
        resp = int(input("Tecle 1 para voltar ao menu..."))

def main():
    plivro = abre_arquivo()
    while True:
        cabec()
        print("\n\nOpcoes: \n\n\n")
        print(" 1- Cadastrar novo livro\n\n")
        print(" 2- Remover livro\n\n")
        print(" 3- Consultar livro por ISBN\n\n")
        print(" 4- Alterar ano do livro\n\n")
        print(" 5- Listagem geral\n\n")
        print(" 0- Sair\n\n")
        linha()
        op = int(input("Informe a opcao desejada: "))
        if op == 1:
            inserir(plivro)
        elif op == 2:
            remover(plivro)
        elif op == 3:
            consultar(plivro)
        elif op == 4:
            alterar(plivro)
        elif op == 5:
            listagem(plivro)
        elif op == 0:
            plivro.close()
            break
        else:
            print("\n\nOpcao invalida!")

if __name__ == "__main__":
    main()
