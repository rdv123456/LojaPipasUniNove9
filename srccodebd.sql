CREATE TABLE Fornecedor (
    id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    contato TEXT,
    email TEXT,
    endereco TEXT
);

CREATE TABLE Produtos (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    quantidade_estoque INTEGER,
    preco NUMERIC,
    id_fornecedor INTEGER,
    FOREIGN KEY (id_fornecedor) REFERENCES Fornecedor(id_fornecedor)
);

CREATE TABLE Clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    contato TEXT,
    email TEXT,
    endereco TEXT
);

CREATE TABLE Compras (
    id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto INTEGER,
    id_cliente INTEGER,
    quantidade_comprada INTEGER,
    data_compra INTEGER,
    FOREIGN KEY (id_produto) REFERENCES Produtos(id_produto),
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);

CREATE TABLE Devedores (
    id_devedor INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    valor_devendo NUMERIC,
    data_divida DATE,
    descricao TEXT,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);


-- Inserindo Fornecedores
INSERT INTO Fornecedor (nome, contato, email, endereco) VALUES
('Atacado das Pipas SP', '(11) 98765-4321', 'contato@atacadopipassp.com.br', 'Rua das Varetas, 120 - Brás, SP'),
('Fábrica Linha Pura', '(11) 91234-5678', 'vendas@linhapura.com.br', 'Av. dos Ventos, 450 - Mooca, SP'),
('Artesanato Papel & Bambu', '(11) 99887-7665', 'artesanato@papelbambu.com', 'Rua da Seda, 88 - Tatuapé, SP');

-- Inserindo Produtos
INSERT INTO Produtos (nome, quantidade_estoque, preco, id_fornecedor) VALUES
('Pipa Raia 50cm Colorida', 80, 3.50, 1),
('Pipa Peixinho Tradicional', 120, 2.00, 3),
('Linha de Algodão 500 Jardas', 45, 8.00, 2),
('Carretilha de Madeira 12 Polegadas', 15, 35.00, 1),
('Rabiola Pronta 10 Metros', 60, 2.50, 3);

-- Inserindo Clientes
INSERT INTO Clientes (nome, contato, email, endereco) VALUES
('João Pedro Silva', '(11) 97777-1111', 'joaopedro@email.com', 'Rua das Flores, 45'),
('Carlos Eduardo Souza', '(11) 96666-2222', 'cadu.souza@email.com', 'Travessa do Sol, 12'),
('Mariana Costa', '(11) 95555-3333', 'mari.costa@email.com', 'Rua Nova, 300');

-- Inserindo Compras (Data no formato DD/MM/AAAA)
INSERT INTO Compras (id_produto, id_cliente, quantidade_comprada, data_compra) VALUES
(1, 1, 5, '20/11/2026'),
(3, 1, 1, '20/11/2026'),
(4, 2, 1, '21/11/2026'),
(2, 3, 10, '22/11/2026');

-- Inserindo Devedores (Data no formato DD/MM/AAAA)
INSERT INTO Devedores (id_cliente, valor_devendo, data_divida, descricao) VALUES
(2, 35.00, '21/11/2026', 'Compra a prazo: 1 Carretilha de Madeira 12 Polegadas'),
(1, 15.50, '20/11/2026', 'Saldo restante de 5 Pipas Raia e 1 Linha');


SELECT * FROM Fornecedor;
SELECT * FROM Produtos;
SELECT * FROM Clientes;
SELECT * FROM Compras;
SELECT * FROM Devedores;


SELECT 
    Compras.id_compra AS 'ID Venda',
    Clientes.nome AS 'Cliente',
    Produtos.nome AS 'Produto',
    Compras.quantidade_comprada AS 'Qtd',
    Produtos.preco AS 'Preço Unit. (R$)',
    (Compras.quantidade_comprada * Produtos.preco) AS 'Total (R$)',
    Compras.data_compra AS 'Data'
FROM Compras
INNER JOIN Clientes ON Compras.id_cliente = Clientes.id_cliente
INNER JOIN Produtos ON Compras.id_produto = Produtos.id_produto;
