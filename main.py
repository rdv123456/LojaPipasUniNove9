"""Loja de Pipas - sistema de cadastro usando o banco SQLite LojaDePipasUni9.db.

Tabelas: Fornecedor, Produtos, Clientes, Compras e Devedores.
"""

import sqlite3
from pathlib import Path

# O banco fica na mesma pasta deste arquivo, independente de onde o programa e executado
CAMINHO_BANCO = Path(__file__).resolve().parent / "LojaDePipasUni9.db"


# ---------------------------------------------------------------------------
# Conexao e criacao das tabelas
# ---------------------------------------------------------------------------

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row          # permite acessar colunas pelo nome
    conexao.execute("PRAGMA foreign_keys = ON")  # o SQLite so valida chave estrangeira com isso ligado
    return conexao


def criar_tabelas(conexao):
    """Cria as tabelas caso o banco esteja vazio (se ja existirem, nada muda)."""
    conexao.executescript("""
        CREATE TABLE IF NOT EXISTS Fornecedor (
            id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            contato TEXT,
            email TEXT,
            endereco TEXT
        );
        CREATE TABLE IF NOT EXISTS Produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade_estoque INTEGER,
            preco NUMERIC,
            id_fornecedor INTEGER,
            FOREIGN KEY (id_fornecedor) REFERENCES Fornecedor(id_fornecedor)
        );
        CREATE TABLE IF NOT EXISTS Clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            contato TEXT,
            email TEXT,
            endereco TEXT
        );
        CREATE TABLE IF NOT EXISTS Compras (
            id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER,
            id_cliente INTEGER,
            quantidade_comprada INTEGER,
            data_compra INTEGER,
            FOREIGN KEY (id_produto) REFERENCES Produtos(id_produto),
            FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
        );
        CREATE TABLE IF NOT EXISTS Devedores (
            id_devedor INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            valor_devendo NUMERIC,
            data_divida DATE,
            descricao TEXT,
            FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
        );
    """)
    conexao.commit()


# ---------------------------------------------------------------------------
# Funcoes auxiliares de leitura do teclado
# ---------------------------------------------------------------------------

def ler_texto(mensagem, atual=None):
    """Le um texto. No modo alterar (atual informado), Enter vazio mantem o valor antigo."""
    while True:
        if atual is not None:
            valor = input(f"{mensagem} [{atual}]: ").strip()
            return valor if valor else atual
        valor = input(f"{mensagem}: ").strip()
        if valor:
            return valor
        print("Campo obrigatorio!")


def ler_inteiro(mensagem, atual=None, minimo=None):
    while True:
        texto = input(f"{mensagem}" + (f" [{atual}]" if atual is not None else "") + ": ").strip()
        if not texto and atual is not None:
            return atual
        try:
            valor = int(texto)
        except ValueError:
            print("Digite um numero inteiro valido!")
            continue
        if minimo is not None and valor < minimo:
            print(f"O valor deve ser no minimo {minimo}!")
            continue
        return valor


def ler_decimal(mensagem, atual=None):
    while True:
        texto = input(f"{mensagem}" + (f" [{atual:.2f}]" if atual is not None else "") + ": ").strip()
        if not texto and atual is not None:
            return atual
        try:
            valor = float(texto.replace(",", "."))  # aceita 10,50 ou 10.50
        except ValueError:
            print("Digite um valor valido!")
            continue
        if valor < 0:
            print("O valor nao pode ser negativo!")
            continue
        return valor


def buscar_por_id(conexao, tabela, coluna_id, id_registro):
    """Devolve o registro com o ID informado, ou None se nao existir."""
    return conexao.execute(
        f"SELECT * FROM {tabela} WHERE {coluna_id} = ?", (id_registro,)
    ).fetchone()


# ---------------------------------------------------------------------------
# FORNECEDORES e CLIENTES
# As duas tabelas tem os mesmos campos (nome, contato, email, endereco),
# entao usam as mesmas funcoes, mudando so o nome da tabela.
# ---------------------------------------------------------------------------

def cadastrar_pessoa(conexao, tabela, titulo):
    print(f"\n--- Cadastro de {titulo} ---")
    nome = ler_texto("Nome")
    contato = ler_texto("Contato (telefone)")
    email = ler_texto("Email")
    endereco = ler_texto("Endereco")
    cursor = conexao.execute(
        f"INSERT INTO {tabela} (nome, contato, email, endereco) VALUES (?, ?, ?, ?)",
        (nome, contato, email, endereco),
    )
    conexao.commit()
    print(f"{titulo} cadastrado com ID {cursor.lastrowid}!")
    return cursor.lastrowid


def listar_pessoas(conexao, tabela, coluna_id, titulo):
    registros = conexao.execute(f"SELECT * FROM {tabela} ORDER BY {coluna_id}").fetchall()
    print(f"\n--- Lista de {titulo} ---")
    if not registros:
        print("Nenhum registro cadastrado.")
        return False
    for r in registros:
        print(f"ID: {r[coluna_id]} | Nome: {r['nome']} | Contato: {r['contato']} | "
              f"Email: {r['email']} | Endereco: {r['endereco']}")
    return True


def alterar_pessoa(conexao, tabela, coluna_id, titulo):
    if not listar_pessoas(conexao, tabela, coluna_id, titulo):
        return
    id_alvo = ler_inteiro("\nDigite o ID para alterar")
    atual = buscar_por_id(conexao, tabela, coluna_id, id_alvo)
    if atual is None:
        print("ID nao encontrado!")
        return
    print("(Aperte Enter para manter o valor atual)")
    nome = ler_texto("Nome", atual["nome"])
    contato = ler_texto("Contato", atual["contato"])
    email = ler_texto("Email", atual["email"])
    endereco = ler_texto("Endereco", atual["endereco"])
    conexao.execute(
        f"UPDATE {tabela} SET nome = ?, contato = ?, email = ?, endereco = ? WHERE {coluna_id} = ?",
        (nome, contato, email, endereco, id_alvo),
    )
    conexao.commit()
    print(f"{titulo} alterado com sucesso!")


def deletar_pessoa(conexao, tabela, coluna_id, titulo):
    if not listar_pessoas(conexao, tabela, coluna_id, titulo):
        return
    id_alvo = ler_inteiro("\nDigite o ID para deletar")
    try:
        cursor = conexao.execute(f"DELETE FROM {tabela} WHERE {coluna_id} = ?", (id_alvo,))
        conexao.commit()
    except sqlite3.IntegrityError:
        # A chave estrangeira impede apagar quem ainda esta ligado a outros registros
        print("Nao e possivel deletar: existem produtos, compras ou dividas ligados a este registro.")
        return
    print(f"{titulo} removido!" if cursor.rowcount else "ID nao encontrado!")


# ---------------------------------------------------------------------------
# PRODUTOS
# ---------------------------------------------------------------------------

def escolher_fornecedor(conexao, atual=None):
    """Mostra os fornecedores e pede o ID. Permite cadastrar um novo na hora (digitando 0)."""
    while True:
        listar_pessoas(conexao, "Fornecedor", "id_fornecedor", "Fornecedores")
        print("0. Cadastrar novo fornecedor")
        id_fornecedor = ler_inteiro("ID do fornecedor", atual)
        if id_fornecedor == 0:
            return cadastrar_pessoa(conexao, "Fornecedor", "Fornecedor")
        if buscar_por_id(conexao, "Fornecedor", "id_fornecedor", id_fornecedor):
            return id_fornecedor
        print("Fornecedor nao encontrado!")


def cadastrar_produto(conexao):
    print("\n--- Cadastro de Produto ---")
    nome = ler_texto("Nome")
    preco = ler_decimal("Preco")
    estoque = ler_inteiro("Estoque", minimo=0)
    print("\nEscolha o fornecedor do produto:")
    id_fornecedor = escolher_fornecedor(conexao)
    cursor = conexao.execute(
        "INSERT INTO Produtos (nome, quantidade_estoque, preco, id_fornecedor) VALUES (?, ?, ?, ?)",
        (nome, estoque, preco, id_fornecedor),
    )
    conexao.commit()
    print(f"Produto salvo com ID {cursor.lastrowid}!")


def listar_produtos(conexao):
    # LEFT JOIN para mostrar o nome do fornecedor junto com o produto
    produtos = conexao.execute("""
        SELECT p.id_produto, p.nome, p.preco, p.quantidade_estoque, f.nome AS fornecedor
        FROM Produtos p
        LEFT JOIN Fornecedor f ON f.id_fornecedor = p.id_fornecedor
        ORDER BY p.id_produto
    """).fetchall()
    print("\n--- Lista de Produtos ---")
    if not produtos:
        print("Nenhum produto cadastrado.")
        return False
    for p in produtos:
        print(f"ID: {p['id_produto']} | Nome: {p['nome']} | Preco: R$ {p['preco']:.2f} | "
              f"Estoque: {p['quantidade_estoque']} | Fornecedor: {p['fornecedor'] or '-'}")
    return True


def alterar_produto(conexao):
    if not listar_produtos(conexao):
        return
    id_alvo = ler_inteiro("\nDigite o ID para alterar")
    atual = buscar_por_id(conexao, "Produtos", "id_produto", id_alvo)
    if atual is None:
        print("ID nao encontrado!")
        return
    print("(Aperte Enter para manter o valor atual)")
    nome = ler_texto("Novo nome", atual["nome"])
    preco = ler_decimal("Novo preco", atual["preco"])
    estoque = ler_inteiro("Novo estoque", atual["quantidade_estoque"], minimo=0)
    print("\nFornecedor do produto:")
    id_fornecedor = escolher_fornecedor(conexao, atual["id_fornecedor"])
    conexao.execute(
        "UPDATE Produtos SET nome = ?, preco = ?, quantidade_estoque = ?, id_fornecedor = ? "
        "WHERE id_produto = ?",
        (nome, preco, estoque, id_fornecedor, id_alvo),
    )
    conexao.commit()
    print("Produto alterado com sucesso!")


def deletar_produto(conexao):
    if not listar_produtos(conexao):
        return
    id_alvo = ler_inteiro("\nDigite o ID para deletar")
    try:
        cursor = conexao.execute("DELETE FROM Produtos WHERE id_produto = ?", (id_alvo,))
        conexao.commit()
    except sqlite3.IntegrityError:
        print("Nao e possivel deletar: este produto ja possui compras registradas.")
        return
    print("Produto removido!" if cursor.rowcount else "ID nao encontrado!")


# ---------------------------------------------------------------------------
# COMPRAS
# ---------------------------------------------------------------------------

def registrar_compra(conexao):
    print("\n--- Registrar Compra ---")
    if not listar_pessoas(conexao, "Clientes", "id_cliente", "Clientes"):
        print("Cadastre um cliente antes de registrar uma compra.")
        return
    cliente = buscar_por_id(conexao, "Clientes", "id_cliente", ler_inteiro("ID do cliente"))
    if cliente is None:
        print("Cliente nao encontrado!")
        return

    if not listar_produtos(conexao):
        return
    produto = buscar_por_id(conexao, "Produtos", "id_produto", ler_inteiro("ID do produto"))
    if produto is None:
        print("Produto nao encontrado!")
        return

    quantidade = ler_inteiro("Quantidade", minimo=1)
    if quantidade > produto["quantidade_estoque"]:
        print(f"Estoque insuficiente! Disponivel: {produto['quantidade_estoque']}")
        return

    total = quantidade * produto["preco"]
    print(f"Total da compra: R$ {total:.2f}")
    fiado = input("Pagamento fiado? (s/n): ").strip().lower() == "s"

    # "with conexao" faz tudo numa transacao: ou grava tudo, ou nada
    with conexao:
        conexao.execute(
            "INSERT INTO Compras (id_produto, id_cliente, quantidade_comprada, data_compra) "
            "VALUES (?, ?, ?, date('now', 'localtime'))",
            (produto["id_produto"], cliente["id_cliente"], quantidade),
        )
        conexao.execute(
            "UPDATE Produtos SET quantidade_estoque = quantidade_estoque - ? WHERE id_produto = ?",
            (quantidade, produto["id_produto"]),
        )
        if fiado:
            conexao.execute(
                "INSERT INTO Devedores (id_cliente, valor_devendo, data_divida, descricao) "
                "VALUES (?, ?, date('now', 'localtime'), ?)",
                (cliente["id_cliente"], total, f"Compra de {quantidade}x {produto['nome']}"),
            )
    print("Compra registrada!" + (" Divida lancada para o cliente." if fiado else ""))


def listar_compras(conexao):
    compras = conexao.execute("""
        SELECT c.id_compra, c.data_compra, c.quantidade_comprada,
               cl.nome AS cliente, p.nome AS produto, p.preco
        FROM Compras c
        LEFT JOIN Clientes cl ON cl.id_cliente = c.id_cliente
        LEFT JOIN Produtos p ON p.id_produto = c.id_produto
        ORDER BY c.id_compra
    """).fetchall()
    print("\n--- Lista de Compras ---")
    if not compras:
        print("Nenhuma compra registrada.")
        return
    for c in compras:
        total = c["quantidade_comprada"] * (c["preco"] or 0)
        print(f"ID: {c['id_compra']} | Data: {c['data_compra']} | Cliente: {c['cliente']} | "
              f"Produto: {c['produto']} | Qtd: {c['quantidade_comprada']} | Total: R$ {total:.2f}")


def cancelar_compra(conexao):
    listar_compras(conexao)
    compra = buscar_por_id(conexao, "Compras", "id_compra", ler_inteiro("\nDigite o ID da compra para cancelar"))
    if compra is None:
        print("ID nao encontrado!")
        return
    with conexao:
        # Devolve os itens ao estoque antes de apagar a compra
        conexao.execute(
            "UPDATE Produtos SET quantidade_estoque = quantidade_estoque + ? WHERE id_produto = ?",
            (compra["quantidade_comprada"], compra["id_produto"]),
        )
        conexao.execute("DELETE FROM Compras WHERE id_compra = ?", (compra["id_compra"],))
    print("Compra cancelada e estoque devolvido!")


# ---------------------------------------------------------------------------
# DEVEDORES
# ---------------------------------------------------------------------------

def listar_devedores(conexao):
    dividas = conexao.execute("""
        SELECT d.id_devedor, d.valor_devendo, d.data_divida, d.descricao, c.nome AS cliente
        FROM Devedores d
        LEFT JOIN Clientes c ON c.id_cliente = d.id_cliente
        ORDER BY d.id_devedor
    """).fetchall()
    print("\n--- Lista de Devedores ---")
    if not dividas:
        print("Nenhuma divida registrada.")
        return False
    total = 0
    for d in dividas:
        total += d["valor_devendo"]
        print(f"ID: {d['id_devedor']} | Cliente: {d['cliente']} | Valor: R$ {d['valor_devendo']:.2f} | "
              f"Data: {d['data_divida']} | Descricao: {d['descricao']}")
    print(f"Total a receber: R$ {total:.2f}")
    return True


def registrar_divida(conexao):
    print("\n--- Registrar Divida ---")
    if not listar_pessoas(conexao, "Clientes", "id_cliente", "Clientes"):
        print("Cadastre um cliente antes de registrar uma divida.")
        return
    id_cliente = ler_inteiro("ID do cliente")
    if buscar_por_id(conexao, "Clientes", "id_cliente", id_cliente) is None:
        print("Cliente nao encontrado!")
        return
    valor = ler_decimal("Valor devendo")
    descricao = ler_texto("Descricao")
    conexao.execute(
        "INSERT INTO Devedores (id_cliente, valor_devendo, data_divida, descricao) "
        "VALUES (?, ?, date('now', 'localtime'), ?)",
        (id_cliente, valor, descricao),
    )
    conexao.commit()
    print("Divida registrada!")


def pagar_divida(conexao):
    if not listar_devedores(conexao):
        return
    id_alvo = ler_inteiro("\nDigite o ID da divida")
    divida = buscar_por_id(conexao, "Devedores", "id_devedor", id_alvo)
    if divida is None:
        print("ID nao encontrado!")
        return
    valor = ler_decimal(f"Valor pago (devendo R$ {divida['valor_devendo']:.2f})")
    restante = round(divida["valor_devendo"] - valor, 2)
    if restante <= 0:
        conexao.execute("DELETE FROM Devedores WHERE id_devedor = ?", (id_alvo,))
        print("Divida quitada!" + (f" Troco: R$ {-restante:.2f}" if restante < 0 else ""))
    else:
        conexao.execute("UPDATE Devedores SET valor_devendo = ? WHERE id_devedor = ?", (restante, id_alvo))
        print(f"Pagamento parcial registrado. Ainda deve R$ {restante:.2f}")
    conexao.commit()


# ---------------------------------------------------------------------------
# Menus
# ---------------------------------------------------------------------------

def submenu(titulo, opcoes):
    """Mostra um menu com as opcoes [(texto, funcao), ...] ate o usuario escolher Voltar."""
    while True:
        print(f"\n--- {titulo} ---")
        for i, (texto, _) in enumerate(opcoes, start=1):
            print(f"{i}. {texto}")
        print("0. Voltar")
        op = input("Opcao: ").strip()
        if op == "0":
            return
        if op.isdigit() and 1 <= int(op) <= len(opcoes):
            opcoes[int(op) - 1][1]()
        else:
            print("Opcao invalida!")


def main():
    conexao = conectar()
    criar_tabelas(conexao)

    menus = {
        "1": ("Produtos", [
            ("Cadastrar produto", lambda: cadastrar_produto(conexao)),
            ("Listar produtos", lambda: listar_produtos(conexao)),
            ("Alterar produto", lambda: alterar_produto(conexao)),
            ("Deletar produto", lambda: deletar_produto(conexao)),
        ]),
        "2": ("Fornecedores", [
            ("Cadastrar fornecedor", lambda: cadastrar_pessoa(conexao, "Fornecedor", "Fornecedor")),
            ("Listar fornecedores", lambda: listar_pessoas(conexao, "Fornecedor", "id_fornecedor", "Fornecedores")),
            ("Alterar fornecedor", lambda: alterar_pessoa(conexao, "Fornecedor", "id_fornecedor", "Fornecedor")),
            ("Deletar fornecedor", lambda: deletar_pessoa(conexao, "Fornecedor", "id_fornecedor", "Fornecedor")),
        ]),
        "3": ("Clientes", [
            ("Cadastrar cliente", lambda: cadastrar_pessoa(conexao, "Clientes", "Cliente")),
            ("Listar clientes", lambda: listar_pessoas(conexao, "Clientes", "id_cliente", "Clientes")),
            ("Alterar cliente", lambda: alterar_pessoa(conexao, "Clientes", "id_cliente", "Cliente")),
            ("Deletar cliente", lambda: deletar_pessoa(conexao, "Clientes", "id_cliente", "Cliente")),
        ]),
        "4": ("Compras", [
            ("Registrar compra", lambda: registrar_compra(conexao)),
            ("Listar compras", lambda: listar_compras(conexao)),
            ("Cancelar compra", lambda: cancelar_compra(conexao)),
        ]),
        "5": ("Devedores", [
            ("Listar devedores", lambda: listar_devedores(conexao)),
            ("Registrar divida", lambda: registrar_divida(conexao)),
            ("Pagar divida", lambda: pagar_divida(conexao)),
        ]),
    }

    while True:
        print("\n===== LOJA DE PIPAS =====")
        for chave, (titulo, _) in menus.items():
            print(f"{chave}. {titulo}")
        print("0. Sair")
        op = input("Opcao: ").strip()
        if op == "0":
            print("Saindo...")
            break
        if op in menus:
            submenu(*menus[op])
        else:
            print("Opcao invalida!")

    conexao.close()


if __name__ == "__main__":
    main()
