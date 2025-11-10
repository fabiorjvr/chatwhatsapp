CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);

CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER REFERENCES produtos(id),
    data_venda DATE NOT NULL,
    quantidade INTEGER NOT NULL
);

INSERT INTO produtos (nome, preco) VALUES
    ('iPhone 15', 7999.00),
    ('Samsung Galaxy S24', 6999.00),
    ('Xiaomi 14', 3499.00),
    ('Motorola G54', 1799.00),
    ('OnePlus 12', 3299.00),
    ('Google Pixel 8', 6499.00),
    ('Redmi Note 13', 1499.00),
    ('Poco F5', 2499.00),
    ('iPhone 14', 5999.00),
    ('Samsung Galaxy A50', 999.00);