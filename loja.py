# Loja de Pipas: este arquivo cuida da parte visual e das acoes do sistema.
# A tela foi montada no Qt Designer em "loja.ui".
# O cadastro dos dados fica guardado no banco SQLite "LojaDePipasUni9.db".

# Biblioteca padrao do Python para trabalhar com pastas e arquivos.
import os
# Usada para acessar coisas da execucao do programa.
import sys
# Usada para conectar e manipular o banco SQLite.
import sqlite3

# Classes do PySide6 que criam janelas, botoes, caixas de texto e tabelas.
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
# Este arquivo foi criado a partir de loja.ui pelo pyside6-uic.
# Ele ja vem com todos os botoes e campos dentro do executavel.
from loja_ui import Ui_JanelaPrincipal

# Aqui definimos onde cada arquivo sera procurado.
# Rodando pelo Python: tudo fica na pasta do projeto.
# Rodando pelo executavel: a tela ja esta dentro do codigo e o banco fica ao lado do .exe.
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else PASTA_PROJETO
ARQUIVO_BANCO = os.path.join(PASTA_DADOS, "LojaDePipasUni9.db")


# ============================================================
# BANCO DE DADOS
# ============================================================

def conectar_banco():
    # Garante que a pasta local exista. Se o .exe estiver em uma pasta nova, o banco pode ser criado ali.
    os.makedirs(PASTA_DADOS, exist_ok=True)
    # sqlite3 cria o arquivo automaticamente quando ele ainda nao existe.
    con = sqlite3.connect(ARQUIVO_BANCO)
    # Liga a verificacao das chaves estrangeiras, evitando apagar registros ligados a outros dados.
    con.execute("PRAGMA foreign_keys = ON")
    return con


def criar_tabelas():
    # CREATE TABLE IF NOT EXISTS nao apaga os dados: ele apenas cria a tabela quando ainda nao existe.
    # Esta tabela guarda os fornecedores.
    conexao.execute("""CREATE TABLE IF NOT EXISTS Fornecedor (
        id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT, contato TEXT, email TEXT, endereco TEXT)""")

    # Esta tabela guarda os produtos e liga cada produto a um fornecedor.
    conexao.execute("""CREATE TABLE IF NOT EXISTS Produtos (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT, quantidade_estoque INTEGER, preco NUMERIC, id_fornecedor INTEGER,
        FOREIGN KEY (id_fornecedor) REFERENCES Fornecedor(id_fornecedor))""")

    # Esta tabela guarda os clientes cadastrados.
    conexao.execute("""CREATE TABLE IF NOT EXISTS Clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT, contato TEXT, email TEXT, endereco TEXT)""")

    # Esta tabela guarda as compras feitas por clientes.
    conexao.execute("""CREATE TABLE IF NOT EXISTS Compras (
        id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produto INTEGER, id_cliente INTEGER, quantidade_comprada INTEGER, data_compra INTEGER,
        FOREIGN KEY (id_produto) REFERENCES Produtos(id_produto),
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente))""")

    # Esta tabela guarda dividas ou compras feitas no fiado.
    conexao.execute("""CREATE TABLE IF NOT EXISTS Devedores (
        id_devedor INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER, valor_devendo NUMERIC, data_divida DATE, descricao TEXT,
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente))""")
    conexao.commit()


# ============================================================
# FUNCOES DE AJUDA
# ============================================================

def mostrar_mensagem(texto):
    # Caixa verde? Nao e verde; aqui usamos uma caixa simples de informacao para avisar o usuario.
    QMessageBox.information(janela, "Loja de Pipas", texto)


def mostrar_erro(texto):
    # Caixa de aviso usada quando falta algum dado ou existe um problema no cadastro.
    QMessageBox.warning(janela, "Atencao", texto)


def perguntar(texto):
    # Pergunta ao usuario antes de uma exclusao ou cancelamento importante.
    resposta = QMessageBox.question(janela, "Confirmar", texto)
    return resposta == QMessageBox.StandardButton.Yes


def preencher_tabela(tabela, linhas):
    # Limpa a tabela antes de preencher, porque precisamos mostrar somente os dados atuais do banco.
    tabela.setRowCount(0)
    for linha in linhas:
        numero_linha = tabela.rowCount()
        tabela.insertRow(numero_linha)
        for coluna, valor in enumerate(linha):
            # QTableWidget precisa receber um objeto de texto em cada celula.
            tabela.setItem(numero_linha, coluna, QTableWidgetItem(str(valor)))
    # Ajusta a largura das colunas automaticamente para o conteudo aparecer melhor.
    tabela.resizeColumnsToContents()


def pegar_id_selecionado(tabela):
    # O ID sempre fica na primeira coluna. Se nada estiver selecionado, devolvemos None.
    linha = tabela.currentRow()
    if linha < 0 or tabela.item(linha, 0) is None:
        return None
    return int(tabela.item(linha, 0).text())


def dinheiro(valor):
    # Coloca o valor no padrao brasileiro mostrado pela interface.
    return f"R$ {valor:.2f}"


# ============================================================
# CARREGAR DADOS NAS TABELAS E COMBOBOX
# ============================================================

def carregar_fornecedores():
    # SELECT pega os dados; fetchall() transforma o resultado em uma lista.
    dados = conexao.execute(
        "SELECT id_fornecedor, nome, contato, email, endereco FROM Fornecedor ORDER BY id_fornecedor"
    ).fetchall()
    preencher_tabela(janela.tabelaFornecedores, dados)

    # combobox de fornecedor na aba de produtos
    janela.cbProdFornecedor.clear()
    for f in dados:
        janela.cbProdFornecedor.addItem(f"{f[0]} - {f[1]}", f[0])


def carregar_clientes():
    # Busca os clientes e deixa os dados prontos para tabela e comboboxes.
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
    # LEFT JOIN conecta a tabela Produtos com Fornecedor.
    # Assim mostramos o nome do fornecedor em vez de aparecer apenas o id dele.
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
    # Faz a leitura das compras ligando os dados de produto e cliente pelo id.
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
    # Aqui buscamos as dividas e somamos tudo que ainda esta pendente.
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
    # Atualiza todas as partes da tela depois que algo muda no banco.
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
    # Volta os campos do produto para o estado inicial e remove a selecao da tabela.
    janela.txtProdNome.clear()
    janela.spinProdPreco.setValue(0)
    janela.spinProdEstoque.setValue(0)
    janela.tabelaProdutos.clearSelection()
    janela.tabelaProdutos.setCurrentCell(-1, -1)


def selecionar_produto():
    # Quando o usuario clica em uma linha, o programa procura esse id no banco.
    # Depois envia os dados encontrados para os campos da aba Produtos.
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
    # Verifica os campos obrigatorios antes de cadastrar ou alterar.
    if janela.txtProdNome.text().strip() == "":
        mostrar_erro("Digite o nome do produto!")
        return False
    if janela.cbProdFornecedor.currentData() is None:
        mostrar_erro("Escolha um fornecedor! Se nao tiver nenhum, cadastre na aba Fornecedores.")
        return False
    return True


def cadastrar_produto():
    # Primeiro valida; se estiver tudo certo, monta o INSERT com os valores digitados.
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
    # Precisa selecionar um produto antes de tentar alterar seus dados.
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
    # Busca o id selecionado e pede confirmacao antes de excluir.
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
    # Limpa os campos e deixa a tabela sem linha selecionada.
    janela.txtFornNome.clear()
    janela.txtFornContato.clear()
    janela.txtFornEmail.clear()
    janela.txtFornEndereco.clear()
    janela.tabelaFornecedores.clearSelection()
    janela.tabelaFornecedores.setCurrentCell(-1, -1)


def selecionar_fornecedor():
    # Ao clicar em um fornecedor, consulta seus dados e preenche o formulario.
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
    # O nome e obrigatorio. Os outros dados podem ser preenchidos livremente.
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
    # O UPDATE muda somente o fornecedor identificado pelo id selecionado.
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
    # Se houver produtos ligados a ele, o banco impede a exclusao para nao quebrar os relacionamentos.
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
    # Deixa o formulario pronto para cadastrar um novo cliente.
    janela.txtCliNome.clear()
    janela.txtCliContato.clear()
    janela.txtCliEmail.clear()
    janela.txtCliEndereco.clear()
    janela.tabelaClientes.clearSelection()
    janela.tabelaClientes.setCurrentCell(-1, -1)


def selecionar_cliente():
    # Coloca os dados da linha selecionada dentro dos campos da aba Clientes.
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
    # Faz a verificacao do nome e salva os dados com um INSERT.
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
    # Atualiza os dados do cliente que esta selecionado na tabela.
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
    # Nao permite excluir cliente que ainda possui compras ou dividas.
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
    # Consulta o preco do produto escolhido e multiplica pela quantidade selecionada.
    id_produto = janela.cbCompraProduto.currentData()
    if id_produto is None:
        janela.labelCompraTotal.setText(dinheiro(0))
        return
    preco = conexao.execute("SELECT preco FROM Produtos WHERE id_produto = ?", (id_produto,)).fetchone()[0]
    total = preco * janela.spinCompraQtd.value()
    janela.labelCompraTotal.setText(dinheiro(total))


def registrar_compra():
    # Junta cliente, produto e quantidade antes de cadastrar a compra.
    # Essa funcao tambem confere o estoque e cria uma divida quando a compra e fiado.
    id_cliente = janela.cbCompraCliente.currentData()
    id_produto = janela.cbCompraProduto.currentData()
    quantidade = janela.spinCompraQtd.value()

    if id_cliente is None:
        # O combobox nao tera id quando nao houver nenhum cliente cadastrado.
        mostrar_erro("Cadastre um cliente primeiro!")
        return
    if id_produto is None:
        # O mesmo ocorre quando ainda nao existe nenhum produto.
        mostrar_erro("Cadastre um produto primeiro!")
        return

    nome, preco, estoque = conexao.execute(
        "SELECT nome, preco, quantidade_estoque FROM Produtos WHERE id_produto = ?", (id_produto,)
    ).fetchone()

    if quantidade > estoque:
        # Esta validacao evita vender mais unidades do que existem no estoque.
        mostrar_erro(f"Estoque insuficiente! So tem {estoque} unidade(s).")
        return

    # Preco vezes quantidade informa quanto a compra custou no total.
    total = preco * quantidade

    # Salva o registro da compra no banco.
    conexao.execute(
        "INSERT INTO Compras (id_produto, id_cliente, quantidade_comprada, data_compra) "
        "VALUES (?, ?, ?, date('now', 'localtime'))",
        (id_produto, id_cliente, quantidade)
    )
    # Desconta a quantidade vendida do estoque.
    conexao.execute(
        "UPDATE Produtos SET quantidade_estoque = quantidade_estoque - ? WHERE id_produto = ?",
        (quantidade, id_produto)
    )
    # Se o usuario marcou Fiado, cria uma divida para o mesmo cliente.
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
    # Ao cancelar, devolvemos ao estoque exatamente a quantidade que havia sido vendida.
    id_compra = pegar_id_selecionado(janela.tabelaCompras)
    if id_compra is None:
        mostrar_erro("Selecione uma compra na tabela!")
        return
    if not perguntar("Deseja cancelar esta compra? Os produtos voltam para o estoque."):
        return

    id_produto, quantidade = conexao.execute(
        "SELECT id_produto, quantidade_comprada FROM Compras WHERE id_compra = ?", (id_compra,)
    ).fetchone()

    # Primeiro devolve os produtos ao estoque.
    conexao.execute(
        "UPDATE Produtos SET quantidade_estoque = quantidade_estoque + ? WHERE id_produto = ?",
        (quantidade, id_produto)
    )
    # Depois apaga o registro da compra.
    conexao.execute("DELETE FROM Compras WHERE id_compra = ?", (id_compra,))
    conexao.commit()
    mostrar_mensagem("Compra cancelada! Se ela foi fiado, lembre de ajustar a divida na aba Devedores.")
    atualizar_tudo()


# ============================================================
# ABA DEVEDORES
# ============================================================

def registrar_divida():
    # Cria manualmente uma divida para um cliente selecionado.
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
    # Busca a divida selecionada e confere quanto o cliente esta pagando.
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
        # Pagamento igual ou maior que a divida significa que ela foi quitada.
        # Se passou do valor, o programa mostra o troco.
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

# QApplication representa a aplicacao grafica completa.
app = QApplication(sys.argv)

# Cria a janela principal e configura todos os campos usando a classe gerada a partir do .ui.
janela = QMainWindow()
interface = Ui_JanelaPrincipal()
interface.setupUi(janela)
# Os controles ficam guardados em "interface"; copiamos as referencias para
# a janela porque as funcoes abaixo acessam os campos usando janela.nomeDoCampo.
for nome, componente in vars(interface).items():
    setattr(janela, nome, componente)

# Aqui conectamos o codigo ao banco e garantimos que todas as tabelas existam.
conexao = conectar_banco()
criar_tabelas()

# Ligamos cada botao a sua funcao. Assim, ao clicar no botao, o metodo correspondente sera executado.
# Produtos
janela.btnProdSalvar.clicked.connect(cadastrar_produto)
janela.btnProdAlterar.clicked.connect(alterar_produto)
janela.btnProdExcluir.clicked.connect(excluir_produto)
janela.btnProdLimpar.clicked.connect(limpar_produto)
janela.tabelaProdutos.itemSelectionChanged.connect(selecionar_produto)

# Fornecedores
janela.btnFornSalvar.clicked.connect(cadastrar_fornecedor)
janela.btnFornAlterar.clicked.connect(alterar_fornecedor)
janela.btnFornExcluir.clicked.connect(excluir_fornecedor)
janela.btnFornLimpar.clicked.connect(limpar_fornecedor)
janela.tabelaFornecedores.itemSelectionChanged.connect(selecionar_fornecedor)

# Clientes
janela.btnCliSalvar.clicked.connect(cadastrar_cliente)
janela.btnCliAlterar.clicked.connect(alterar_cliente)
janela.btnCliExcluir.clicked.connect(excluir_cliente)
janela.btnCliLimpar.clicked.connect(limpar_cliente)
janela.tabelaClientes.itemSelectionChanged.connect(selecionar_cliente)

# Compras
janela.btnCompraRegistrar.clicked.connect(registrar_compra)
janela.btnCompraCancelar.clicked.connect(cancelar_compra)
janela.cbCompraProduto.currentIndexChanged.connect(calcular_total_compra)
janela.spinCompraQtd.valueChanged.connect(calcular_total_compra)

# Devedores
janela.btnDevRegistrar.clicked.connect(registrar_divida)
janela.btnDevPagar.clicked.connect(pagar_divida)

# Ao iniciar, carregamos todos os dados ja existentes no banco.
atualizar_tudo()
janela.statusbar.showMessage("Banco de dados: " + ARQUIVO_BANCO)
# Exibe a janela principal na tela.
janela.show()
# Mantem o aplicativo aberto enquanto a janela estiver ativa.
sys.exit(app.exec())
