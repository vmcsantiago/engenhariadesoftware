from tkinter import *
from functools import partial
import sqlite3

conn = sqlite3.connect('C:\sqlite\DB\esofdb.db')
c = conn.cursor()

def consulta_estoque():
    resposta = input("Deseja pesquisar algum produto por nome ou codigo? (S/N): ")

    if(resposta == 'S'):
        resposta2 = input("Deseja pesquisar por nome ou por codigo? (N/C): ")
        if(resposta2 == 'N'):
            resposta3 = input("Digite o nome do produto: ")
            print(resposta3)
            c.execute("SELECT id, nomeP, quantP, valorP FROM produtos WHERE nomeP = ?", (resposta3, ))
            print("[ID][NOME PRODUTO][QUANTIDADE][PREÇO]")
            for linha in c.fetchall():
                print(linha)
        else:
            resposta3 = input("Digite o codigo do produto: ")
            resposta3 = int(resposta3)
            c.execute("SELECT * FROM produtos WHERE id = ?", (resposta3, ))
            print("[ID][NOME PRODUTO][QUANTIDADE][PREÇO]")
            for linha in c.fetchall():
                print(linha)
    else:
        print("Lista de todos produtos cadastrados:")
        print("[ID][NOME PRODUTO][QUANTIDADE][PREÇO]\n")
        c.execute("SELECT * FROM produtos")

        for linha in c.fetchall():
            print(linha)

    c.execute("SELECT valorcaixa FROM caixa")
    total = c.fetchall()
    total = float(total[0][0])

    print("\nValor monetário disponível no caixa: %f" % total)


def bt_adicionar(idp, nomep, quantp, valorp, jan2):
    idp = idp.get()
    nomep = nomep.get()
    quantp = quantp.get()
    valorp = valorp.get()
    c.execute("INSERT INTO produtos VALUES(?, ?, ?, ?)",
              (idp, nomep, quantp, valorp))
    conn.commit()
    lbadicionado = Label(jan2, text="Adicionado com sucesso!!!")
    lbadicionado.place(x=150, y=215)

def add_produto():
    jan2 = Tk()
    jan2.title("Adicionar Produto")
    jan2.geometry("500x245+636+120")
    lab1 = Label(jan2, text="Digite o id do produto: ")
    lab1.place(x=15, y=55)
    idp = Entry(jan2)
    idp.place(x=330, y=55)
    nomep = Entry(jan2)
    nomep.place(x=330, y=85)
    lab2 = Label(jan2, text="Digite o nome do produto:")
    lab2.place(x=15, y=85)
    lab3 = Label(jan2, text="Digite a quantidade do produto: ")
    lab3.place(x=15, y=115)
    quantp = Entry(jan2)
    quantp.place(x=330, y=115)
    lab4 = Label(jan2, text="Digite o valor do produto: ")
    lab4.place(x=15, y=145)
    valorp = Entry(jan2)
    valorp.place(x=330, y=145)
    but = Button(jan2, width=25, text="Adicionar")
    but["command"] = partial(bt_adicionar, idp, nomep, quantp, valorp, jan2)
    but.place(x=150, y=185)
    jan2.mainloop()


def bt_cadastrar(nomec, idc, contatoc, jan1):
    idc = idc.get()
    nomec = nomec.get()
    contatoc = contatoc.get()
    c.execute("INSERT INTO clientes VALUES(?, ?, ?)", (idc, nomec, contatoc))
    conn.commit()
    lbcadastrado = Label(jan1, text="Cadastrado com sucesso!!!")
    lbcadastrado.place(x=150,y=200)

def add_cliente():
    jan1 = Tk()
    jan1.title("Cadastro de Clientes/Fornecedor")
    jan1.geometry("500x230+636+120")
    lb2 = Label(jan1, text="Digite o nome do cliente/fornecedor: ")
    lb2.place(x=15, y=55)
    nomec = Entry(jan1)
    nomec.place(x=330, y=55)
    idc = Entry(jan1)
    idc.place(x=330, y=85)
    lb1 =  Label(jan1, text="Digite a identificação do cliente/fornecedor (CPF/CNPJ):")
    lb1.place(x=15, y=85)
    lb3 = Label(jan1, text="Digite o email do cliente/fornecedor: ")
    lb3.place(x=15, y=115)
    contatoc = Entry(jan1)
    contatoc.place(x=330,y=115)
    but = Button(jan1, width=25, text="Cadastrar")
    but["command"] = partial(bt_cadastrar, nomec, idc, contatoc, jan1)
    but.place(x=150, y=170)
    jan1.mainloop()

def vender_produto():
    idp = input('Digite o id do produto: ')
    vendaq = input('Digite a quantidade do produto que foi vendida: ')
    c.execute("SELECT quantP FROM produtos WHERE id = ?",(idp))
    antigaq = c.fetchall()
    antigaq = int(antigaq[0][0])
    atualq = - int(vendaq) + antigaq
    c.execute("UPDATE produtos SET quantP = ? WHERE id = ?",(atualq, idp))
    c.execute("SELECT quantP FROM produtos WHERE id = ?", (idp))
    posq = c.fetchall()
    posq = int(posq[0][0])
    print("A quantidade atual do produto é: %d." % posq)
    c.execute("SELECT valorP FROM produtos WHERE id = ?", (idp))
    valor = c.fetchall()
    valor = float(valor[0][0])
    valorcaixaadd = int(vendaq)*valor
    print("O valor adicionado ao caixa foi de %f reais." % valorcaixaadd)
    c.execute("SELECT valorcaixa FROM caixa")
    total = c.fetchall()
    total = float(total[0][0])
    total = total + valorcaixaadd
    c.execute("UPDATE caixa SET valorcaixa = ? WHERE id = ?", (total, 1))
    print("Valor total do caixa é: %f" % total)
    conn.commit()

def repor_produto():
    idp = input('Digite o id do produto: ')
    addq = input('Digite a quantidade a ser adicionada: ')
    c.execute("SELECT quantP FROM produtos WHERE id = ?",(idp))
    antigaq = c.fetchall()
    antigaq = int(antigaq[0][0])
    atualq = int(addq) + antigaq
    c.execute("UPDATE produtos SET quantP = ? WHERE id = ?",(atualq, idp))
    c.execute("SELECT quantP FROM produtos WHERE id = ?", (idp))
    posq = c.fetchall()
    posq = int(posq[0][0])
    print("A quantidade atual do produto é: %d." % posq)
    c.execute("SELECT valorP FROM produtos WHERE id = ?", (idp))
    valor = c.fetchall()
    valor = float(valor[0][0])
    valorcaixaret = int(addq) * valor
    print("O valor retirado do caixa foi de %f reais." % valorcaixaret)
    c.execute("SELECT valorcaixa FROM caixa")
    total = c.fetchall()
    total = float(total[0][0])
    total = total - valorcaixaret
    c.execute("UPDATE caixa SET valorcaixa = ? WHERE id = ?", (total, 1))
    print("Valor total do caixa é: %f" % total)
    conn.commit()

janela = Tk()
janela.title("Projeto Eng. Software v.1")
janela.geometry("220x250+400+120")
lb = Label(janela, text="Menu de Controle")
lb.place(x=55, y=35)

bt1 = Button(janela, width=25, text="Cadastrar Cliente/Fornecedor", command=add_cliente)
bt1.place(x=15, y=80)
bt2 = Button(janela, width=25, text="Adicionar Produto", command=add_produto)
bt2.place(x=15, y=110)
bt3 = Button(janela, width=25, text="Repor Produto", command=repor_produto)
bt3.place(x=15, y=140)
bt4 = Button(janela, width=25, text="Vender Produto", command=vender_produto)
bt4.place(x=15, y=170)
bt5 = Button(janela, width=25, text="Abrir/Fechar Estoque", command=consulta_estoque)
bt5.place(x=15, y=200)

janela.mainloop()

conn.close()
