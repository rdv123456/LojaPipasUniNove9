# Loja de Pipas - interface grafica com PySide6
# A tela foi feita no Qt Designer (loja.ui) e os dados ficam no banco SQLite LojaDePipasUni9.db

import os
import sys
import sqlite3

from PySide6.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

# pega a pasta onde esta este arquivo, para achar o .ui e o banco
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_UI = os.path.join(PASTA, "loja.ui")
ARQUIVO_BANCO = os.path.join(PASTA, "LojaDePipasUni9.db")


# ============================================================
# BANCO DE DADOS
# ============================================================

def conectar_banco():
    con = sqlite3.connect(ARQUIVO_BANCO)
    con.execute("PRAGMA foreign_keys = ON")  # liga a verificacao das chaves estrangeiras
    return con


def criar_tabelas():
    # so cria se ainda nao existir
    conexao.execute("""CREATE TABLE IF NOT EXISTS Fornecedor (
        id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT, contato TEXT, email TEXT, endereco TEXT)""")

    conexao.execute("""CREATE TABLE IF NOT EXISTS Produtos (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT, quantidade_estoque INTEGER, preco NUMERIC, id_fornecedor INTEGER,
        FOREIGN KEY (id_fornecedor) REFERENCES Fornecedor(id_fornecedor))""")

    conexao.execute("""CREATE TABLE IF NOT EXISTS Clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT, contato TEXT, email TEXT, endereco TEXT)""")

    conexao.execute("""CREATE TABLE IF NOT EXISTS Compras (
        id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produto INTEGER, id_cliente INTEGER, quantidade_comprada INTEGER, data_compra INTEGER,
        FOREIGN KEY (id_produto) REFERENCES Produtos(id_produto),
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente))""")

    conexao.execute("""CREATE TABLE IF NOT EXISTS Devedores (
        id_devedor INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER, valor_devendo NUMERIC, data_divida DATE, descricao TEXT,
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente))""")
    conexao.commit()


# ============================================================
# FUNCOES DE AJUDA
# ============================================================

def mostrar_mensagem(texto):
    QMessageBox.information(janela, "Loja de Pipas", texto)


def mostrar_erro(texto):
    QMessageBox.warning(janela, "Atencao", texto)


def perguntar(texto):
    resposta = QMessageBox.question(janela, "Confirmar", texto)
    return resposta == QMessageBox.StandardButton.Yes


def preencher_tabela(tabela, linhas):
    # coloca o resultado do SELECT dentro da QTableWidget
    tabela.setRowCount(0)
    for linha in linhas:
        numero_linha = tabela.rowCount()
        tabela.insertRow(numero_linha)
        for coluna, valor in enumerate(linha):
            tabela.setItem(numero_linha, coluna, QTableWidgetItem(str(valor)))
    tabela.resizeColumnsToContents()


def pegar_id_selecionado(tabela):
    # o ID sempre esta na primeira coluna da tabela
    linha = tabela.currentRow()
    if linha < 0 or tabela.item(linha, 0) is None:
        return None
    return int(tabela.item(linha, 0).text())


def dinheiro(valor):
    return f"R$ {valor:.2f}"


# ============================================================
# CARREGAR DADOS NAS TABELAS E COMBOBOX
# ============================================================

def carregar_fornecedores():
    dados = conexao.execute(
        "SELECT id_fornecedor, nome, contato, email, endereco FROM Fornecedor ORDER BY id_fornecedor"
    ).fetchall()
    preencher_tabela(janela.tabelaFornecedores, dados)

    # combobox de fornecedor na aba de produtos
    janela.cbProdFornecedor.clear()
    for f in dados:
        janela.cbProdFornecedor.addItem(f"{f[0]} - {f[1]}", f[0])


def carregar_clientes():
    dados = conexao.execute(
        "SELECT id_cliente, nome, contato, email, endereco FROM Clientes ORDER BY id_cliente"
    ).fetchall()
    preencher_tabela(janela.tabelaClientes, dados)

    # combobox de clientes nas abas de compras e devedores
    janela.cbCompraCliente.clear()
    janela.cbDevCliente.clear()
    for c in dados:
        janela.cbCompraCliente.addItem(f"{c[0]} - {c[1]}", c[0])
        janela.cbDevCliente.addItem(f"{c[0]} - {c[1]}", c[0])


def carregar_produtos():
    # LEFT JOIN para mostrar o nome do fornecedor em vez so do numero
    dados = conexao.execute("""
        SELECT p.id_produto, p.nome, p.preco, p.quantidade_estoque, f.nome
        FROM Produtos p
        LEFT JOIN Fornecedor f ON f.id_fornecedor = p.id_fornecedor
        ORDER BY p.id_produto
    """).fetchall()

    linhas = []
    for p in dados:
        linhas.append((p[0], p[1], dinheiro(p[2]), p[3], p[4] or "-"))
    preencher_tabela(janela.tabelaProdutos, linhas)

    # combobox de produtos na aba de compras
    janela.cbCompraProduto.clear()
    for p in dados:
        janela.cbCompraProduto.addItem(f"{p[1]} - {dinheiro(p[2])} (estoque: {p[3]})", p[0])


def carregar_compras():
    dados = conexao.execute("""
        SELECT c.id_compra, c.data_compra, cl.nome, p.nome, c.quantidade_comprada, p.preco
        FROM Compras c
        LEFT JOIN Clientes cl ON cl.id_cliente = c.id_cliente
        LEFT JOIN Produtos p ON p.id_produto = c.id_produto
        ORDER BY c.id_compra DESC
    """).fetchall()

    linhas = []
    for c in dados:
        total = c[4] * (c[5] or 0)
        linhas.append((c[0], c[1], c[2], c[3], c[4], dinheiro(total)))
    preencher_tabela(janela.tabelaCompras, linhas)


def carregar_devedores():
    dados = conexao.execute("""
        SELECT d.id_devedor, c.nome, d.valor_devendo, d.data_divida, d.descricao
        FROM Devedores d
        LEFT JOIN Clientes c ON c.id_cliente = d.id_cliente
        ORDER BY d.id_devedor
    """).fetchall()

    linhas = []
    total = 0
    for d in dados:
        total = total + d[2]
        linhas.append((d[0], d[1], dinheiro(d[2]), d[3], d[4]))
    preencher_tabela(janela.tabelaDevedores, linhas)
    janela.labelDevTotal.setText("Total a receber: " + dinheiro(total))


def atualizar_tudo():
    carregar_fornecedores()
    carregar_clientes()
    carregar_produtos()
    carregar_compras()
    carregar_devedores()
    calcular_total_compra()


# ============================================================
# ABA PRODUTOS
# ============================================================

def limpar_produto():
    janela.txtProdNome.clear()
    janela.spinProdPreco.setValue(0)
    janela.spinProdEstoque.setValue(0)
    janela.tabelaProdutos.clearSelection()
    janela.tabelaProdutos.setCurrentCell(-1, -1)


def selecionar_produto():
    # quando clica numa linha da tabela, joga os dados nos campos
    id_produto = pegar_id_selecionado(janela.tabelaProdutos)
    if id_produto is None:
        return
    p = conexao.execute(
        "SELECT nome, preco, quantidade_estoque, id_fornecedor FROM Produtos WHERE id_produto = ?",
        (id_produto,)
    ).fetchone()
    janela.txtProdNome.setText(p[0])
    janela.spinProdPreco.setValue(p[1])
    janela.spinProdEstoque.setValue(p[2])
    janela.cbProdFornecedor.setCurrentIndex(janela.cbProdFornecedor.findData(p[3]))


def validar_produto():
    if janela.txtProdNome.text().strip() == "":
        mostrar_erro("Digite o nome do produto!")
        return False
    if janela.cbProdFornecedor.currentData() is None:
        mostrar_erro("Escolha um fornecedor! Se nao tiver nenhum, cadastre na aba Fornecedores.")
        return False
    return True


def cadastrar_produto():
    if not validar_produto():
        return
    conexao.execute(
        "INSERT INTO Produtos (nome, preco, quantidade_estoque, id_fornecedor) VALUES (?, ?, ?, ?)",
        (janela.txtProdNome.text().strip(), janela.spinProdPreco.value(),
         janela.spinProdEstoque.value(), janela.cbProdFornecedor.currentData())
    )
    conexao.commit()
    mostrar_mensagem("Produto cadastrado!")
    limpar_produto()
    atualizar_tudo()


def alterar_produto():
    id_produto = pegar_id_selecionado(janela.tabelaProdutos)
    if id_produto is None:
        mostrar_erro("Selecione um produto na tabela!")
        return
    if not validar_produto():
        return
    conexao.execute(
        "UPDATE Produtos SET nome = ?, preco = ?, quantidade_estoque = ?, id_fornecedor = ? WHERE id_produto = ?",
        (janela.txtProdNome.text().strip(), janela.spinProdPreco.value(),
         janela.spinProdEstoque.value(), janela.cbProdFornecedor.currentData(), id_produto)
    )
    conexao.commit()
    mostrar_mensagem("Produto alterado!")
    limpar_produto()
    atualizar_tudo()


def excluir_produto():
    id_produto = pegar_id_selecionado(janela.tabelaProdutos)
    if id_produto is None:
        mostrar_erro("Selecione um produto na tabela!")
        return
    if not perguntar("Deseja mesmo excluir este produto?"):
        return
    try:
        conexao.execute("DELETE FROM Produtos WHERE id_produto = ?", (id_produto,))
        conexao.commit()
    except sqlite3.IntegrityError:
        mostrar_erro("Nao da para excluir: esse produto ja tem compras registradas.")
        return
    mostrar_mensagem("Produto excluido!")
    limpar_produto()
    atualizar_tudo()


# ============================================================
# ABA FORNECEDORES
# ============================================================

def limpar_fornecedor():
    janela.txtFornNome.clear()
    janela.txtFornContato.clear()
    janela.txtFornEmail.clear()
    janela.txtFornEndereco.clear()
    janela.tabelaFornecedores.clearSelection()
    janela.tabelaFornecedores.setCurrentCell(-1, -1)


def selecionar_fornecedor():
    id_fornecedor = pegar_id_selecionado(janela.tabelaFornecedores)
    if id_fornecedor is None:
        return
    f = conexao.execute(
        "SELECT nome, contato, email, endereco FROM Fornecedor WHERE id_fornecedor = ?",
        (id_fornecedor,)
    ).fetchone()
    janela.txtFornNome.setText(f[0])
    janela.txtFornContato.setText(f[1])
    janela.txtFornEmail.setText(f[2])
    janela.txtFornEndereco.setText(f[3])


def cadastrar_fornecedor():
    if janela.txtFornNome.text().strip() == "":
        mostrar_erro("Digite o nome do fornecedor!")
        return
    conexao.execute(
        "INSERT INTO Fornecedor (nome, contato, email, endereco) VALUES (?, ?, ?, ?)",
        (janela.txtFornNome.text().strip(), janela.txtFornContato.text().strip(),
         janela.txtFornEmail.text().strip(), janela.txtFornEndereco.text().strip())
    )
    conexao.commit()
    mostrar_mensagem("Fornecedor cadastrado!")
    limpar_fornecedor()
    atualizar_tudo()


def alterar_fornecedor():
    id_fornecedor = pegar_id_selecionado(janela.tabelaFornecedores)
    if id_fornecedor is None:
        mostrar_erro("Selecione um fornecedor na tabela!")
        return
    if janela.txtFornNome.text().strip() == "":
        mostrar_erro("Digite o nome do fornecedor!")
        return
    conexao.execute(
        "UPDATE Fornecedor SET nome = ?, contato = ?, email = ?, endereco = ? WHERE id_fornecedor = ?",
        (janela.txtFornNome.text().strip(), janela.txtFornContato.text().strip(),
         janela.txtFornEmail.text().strip(), janela.txtFornEndereco.text().strip(), id_fornecedor)
    )
    conexao.commit()
    mostrar_mensagem("Fornecedor alterado!")
    limpar_fornecedor()
    atualizar_tudo()


def excluir_fornecedor():
    id_fornecedor = pegar_id_selecionado(janela.tabelaFornecedores)
    if id_fornecedor is None:
        mostrar_erro("Selecione um fornecedor na tabela!")
        return
    if not perguntar("Deseja mesmo excluir este fornecedor?"):
        return
    try:
        conexao.execute("DELETE FROM Fornecedor WHERE id_fornecedor = ?", (id_fornecedor,))
        conexao.commit()
    except sqlite3.IntegrityError:
        mostrar_erro("Nao da para excluir: esse fornecedor tem produtos cadastrados.")
        return
    mostrar_mensagem("Fornecedor excluido!")
    limpar_fornecedor()
    atualizar_tudo()


# ============================================================
# ABA CLIENTES
# ============================================================

def limpar_cliente():
    janela.txtCliNome.clear()
    janela.txtCliContato.clear()
    janela.txtCliEmail.clear()
    janela.txtCliEndereco.clear()
    janela.tabelaClientes.clearSelection()
    janela.tabelaClientes.setCurrentCell(-1, -1)


def selecionar_cliente():
    id_cliente = pegar_id_selecionado(janela.tabelaClientes)
    if id_cliente is None:
        return
    c = conexao.execute(
        "SELECT nome, contato, email, endereco FROM Clientes WHERE id_cliente = ?",
        (id_cliente,)
    ).fetchone()
    janela.txtCliNome.setText(c[0])
    janela.txtCliContato.setText(c[1])
    janela.txtCliEmail.setText(c[2])
    janela.txtCliEndereco.setText(c[3])


def cadastrar_cliente():
    if janela.txtCliNome.text().strip() == "":
        mostrar_erro("Digite o nome do cliente!")
        return
    conexao.execute(
        "INSERT INTO Clientes (nome, contato, email, endereco) VALUES (?, ?, ?, ?)",
        (janela.txtCliNome.text().strip(), janela.txtCliContato.text().strip(),
         janela.txtCliEmail.text().strip(), janela.txtCliEndereco.text().strip())
    )
    conexao.commit()
    mostrar_mensagem("Cliente cadastrado!")
    limpar_cliente()
    atualizar_tudo()


def alterar_cliente():
    id_cliente = pegar_id_selecionado(janela.tabelaClientes)
    if id_cliente is None:
        mostrar_erro("Selecione um cliente na tabela!")
        return
    if janela.txtCliNome.text().strip() == "":
        mostrar_erro("Digite o nome do cliente!")
        return
    conexao.execute(
        "UPDATE Clientes SET nome = ?, contato = ?, email = ?, endereco = ? WHERE id_cliente = ?",
        (janela.txtCliNome.text().strip(), janela.txtCliContato.text().strip(),
         janela.txtCliEmail.text().strip(), janela.txtCliEndereco.text().strip(), id_cliente)
    )
    conexao.commit()
    mostrar_mensagem("Cliente alterado!")
    limpar_cliente()
    atualizar_tudo()


def excluir_cliente():
    id_cliente = pegar_id_selecionado(janela.tabelaClientes)
    if id_cliente is None:
        mostrar_erro("Selecione um cliente na tabela!")
        return
    if not perguntar("Deseja mesmo excluir este cliente?"):
        return
    try:
        conexao.execute("DELETE FROM Clientes WHERE id_cliente = ?", (id_cliente,))
        conexao.commit()
    except sqlite3.IntegrityError:
        mostrar_erro("Nao da para excluir: esse cliente tem compras ou dividas registradas.")
        return
    mostrar_mensagem("Cliente excluido!")
    limpar_cliente()
    atualizar_tudo()


# ============================================================
# ABA COMPRAS
# ============================================================

def calcular_total_compra():
    id_produto = janela.cbCompraProduto.currentData()
    if id_produto is None:
        janela.labelCompraTotal.setText(dinheiro(0))
        return
    preco = conexao.execute("SELECT preco FROM Produtos WHERE id_produto = ?", (id_produto,)).fetchone()[0]
    total = preco * janela.spinCompraQtd.value()
    janela.labelCompraTotal.setText(dinheiro(total))


def registrar_compra():
    id_cliente = janela.cbCompraCliente.currentData()
    id_produto = janela.cbCompraProduto.currentData()
    quantidade = janela.spinCompraQtd.value()

    if id_cliente is None:
        mostrar_erro("Cadastre um cliente primeiro!")
        return
    if id_produto is None:
        mostrar_erro("Cadastre um produto primeiro!")
        return

    nome, preco, estoque = conexao.execute(
        "SELECT nome, preco, quantidade_estoque FROM Produtos WHERE id_produto = ?", (id_produto,)
    ).fetchone()

    if quantidade > estoque:
        mostrar_erro(f"Estoque insuficiente! So tem {estoque} unidade(s).")
        return

    total = preco * quantidade

    # salva a compra
    conexao.execute(
        "INSERT INTO Compras (id_produto, id_cliente, quantidade_comprada, data_compra) "
        "VALUES (?, ?, ?, date('now', 'localtime'))",
        (id_produto, id_cliente, quantidade)
    )
    # tira do estoque
    conexao.execute(
        "UPDATE Produtos SET quantidade_estoque = quantidade_estoque - ? WHERE id_produto = ?",
        (quantidade, id_produto)
    )
    # se for fiado, cria a divida do cliente
    if janela.checkCompraFiado.isChecked():
        conexao.execute(
            "INSERT INTO Devedores (id_cliente, valor_devendo, data_divida, descricao) "
            "VALUES (?, ?, date('now', 'localtime'), ?)",
            (id_cliente, total, f"Compra de {quantidade}x {nome}")
        )
    conexao.commit()

    if janela.checkCompraFiado.isChecked():
        mostrar_mensagem(f"Compra registrada! Total: {dinheiro(total)}\nA divida foi lancada para o cliente.")
    else:
        mostrar_mensagem(f"Compra registrada! Total: {dinheiro(total)}")

    janela.spinCompraQtd.setValue(1)
    janela.checkCompraFiado.setChecked(False)
    atualizar_tudo()


def cancelar_compra():
    id_compra = pegar_id_selecionado(janela.tabelaCompras)
    if id_compra is None:
        mostrar_erro("Selecione uma compra na tabela!")
        return
    if not perguntar("Deseja cancelar esta compra? Os produtos voltam para o estoque."):
        return

    id_produto, quantidade = conexao.execute(
        "SELECT id_produto, quantidade_comprada FROM Compras WHERE id_compra = ?", (id_compra,)
    ).fetchone()

    # devolve pro estoque e apaga a compra
    conexao.execute(
        "UPDATE Produtos SET quantidade_estoque = quantidade_estoque + ? WHERE id_produto = ?",
        (quantidade, id_produto)
    )
    conexao.execute("DELETE FROM Compras WHERE id_compra = ?", (id_compra,))
    conexao.commit()
    mostrar_mensagem("Compra cancelada! Se ela foi fiado, lembre de ajustar a divida na aba Devedores.")
    atualizar_tudo()


# ============================================================
# ABA DEVEDORES
# ============================================================

def registrar_divida():
    id_cliente = janela.cbDevCliente.currentData()
    valor = janela.spinDevValor.value()
    descricao = janela.txtDevDescricao.text().strip()

    if id_cliente is None:
        mostrar_erro("Cadastre um cliente primeiro!")
        return
    if valor <= 0:
        mostrar_erro("Digite um valor maior que zero!")
        return
    if descricao == "":
        mostrar_erro("Digite uma descricao!")
        return

    conexao.execute(
        "INSERT INTO Devedores (id_cliente, valor_devendo, data_divida, descricao) "
        "VALUES (?, ?, date('now', 'localtime'), ?)",
        (id_cliente, valor, descricao)
    )
    conexao.commit()
    mostrar_mensagem("Divida registrada!")
    janela.spinDevValor.setValue(0)
    janela.txtDevDescricao.clear()
    atualizar_tudo()


def pagar_divida():
    id_devedor = pegar_id_selecionado(janela.tabelaDevedores)
    if id_devedor is None:
        mostrar_erro("Selecione uma divida na tabela!")
        return
    pago = janela.spinDevPagamento.value()
    if pago <= 0:
        mostrar_erro("Digite o valor que foi pago!")
        return

    devendo = conexao.execute(
        "SELECT valor_devendo FROM Devedores WHERE id_devedor = ?", (id_devedor,)
    ).fetchone()[0]
    restante = round(devendo - pago, 2)

    if restante <= 0:
        # pagou tudo, entao apaga a divida
        conexao.execute("DELETE FROM Devedores WHERE id_devedor = ?", (id_devedor,))
        texto = "Divida quitada!"
        if restante < 0:
            texto = texto + " Troco: " + dinheiro(-restante)
    else:
        conexao.execute(
            "UPDATE Devedores SET valor_devendo = ? WHERE id_devedor = ?", (restante, id_devedor)
        )
        texto = "Pagamento registrado! Ainda falta " + dinheiro(restante)
    conexao.commit()

    mostrar_mensagem(texto)
    janela.spinDevPagamento.setValue(0)
    atualizar_tudo()


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

app = QApplication(sys.argv)

# carrega a tela feita no Qt Designer
arquivo = QFile(ARQUIVO_UI)
arquivo.open(QFile.OpenModeFlag.ReadOnly)
loader = QUiLoader()
janela = loader.load(arquivo)
arquivo.close()

conexao = conectar_banco()
criar_tabelas()

# ligando os botoes nas funcoes
janela.btnProdSalvar.clicked.connect(cadastrar_produto)
janela.btnProdAlterar.clicked.connect(alterar_produto)
janela.btnProdExcluir.clicked.connect(excluir_produto)
janela.btnProdLimpar.clicked.connect(limpar_produto)
janela.tabelaProdutos.itemSelectionChanged.connect(selecionar_produto)

janela.btnFornSalvar.clicked.connect(cadastrar_fornecedor)
janela.btnFornAlterar.clicked.connect(alterar_fornecedor)
janela.btnFornExcluir.clicked.connect(excluir_fornecedor)
janela.btnFornLimpar.clicked.connect(limpar_fornecedor)
janela.tabelaFornecedores.itemSelectionChanged.connect(selecionar_fornecedor)

janela.btnCliSalvar.clicked.connect(cadastrar_cliente)
janela.btnCliAlterar.clicked.connect(alterar_cliente)
janela.btnCliExcluir.clicked.connect(excluir_cliente)
janela.btnCliLimpar.clicked.connect(limpar_cliente)
janela.tabelaClientes.itemSelectionChanged.connect(selecionar_cliente)

janela.btnCompraRegistrar.clicked.connect(registrar_compra)
janela.btnCompraCancelar.clicked.connect(cancelar_compra)
janela.cbCompraProduto.currentIndexChanged.connect(calcular_total_compra)
janela.spinCompraQtd.valueChanged.connect(calcular_total_compra)

janela.btnDevRegistrar.clicked.connect(registrar_divida)
janela.btnDevPagar.clicked.connect(pagar_divida)

atualizar_tudo()
janela.statusbar.showMessage("Banco de dados: " + ARQUIVO_BANCO)
janela.show()
sys.exit(app.exec())
