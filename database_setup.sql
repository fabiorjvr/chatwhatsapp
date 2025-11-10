-- Remove tabelas existentes, se houver, para evitar conflitos
DROP TABLE IF EXISTS vendas;
DROP TABLE IF EXISTS produtos;

-- Tabela de Vendas
-- Armazena todos os dados de vendas de forma denormalizada
CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL,
    fabricante VARCHAR(100),
    mes INT NOT NULL,
    ano INT NOT NULL,
    unidades_vendidas INT NOT NULL,
    receita DECIMAL(15, 2) NOT NULL,
    regiao VARCHAR(50)
);

-- Índices para melhorar a performance das consultas
CREATE INDEX idx_vendas_modelo ON vendas(modelo);
CREATE INDEX idx_vendas_data ON vendas(ano, mes);