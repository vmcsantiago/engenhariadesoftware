import tkinter
import sqlite3

conn = sqlite3.connect('C:\sqlite\DB\esofdb.db')
c = conn.cursor()


def add_produto():
    idp = input('Digite o id do produto: ')
    nomep = input('Digite o nome do produto: ')
    quantp = input('Digite a quantidade do produto: ')
    valorp = input('Digite o valor do produto: ')
    c.execute("INSERT INTO produtos VALUES(?, ?, ?, ?)",
              (idp, nomep, quantp, valorp))
    conn.commit()


def add_cliente():
    idc = input('Digite o id do cliente: ')
    nomec = input('Digite o nome do cliente: ')
    contatoc = input('Digite o email do cliente: ')
    c.execute("INSERT INTO clientes VALUES(?, ?, ?)", (idc, nomec, contatoc))
    conn.commit()

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


conn.close()