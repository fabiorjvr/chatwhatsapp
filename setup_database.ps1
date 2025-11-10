# Definir a senha do PostgreSQL
$env:PGPASSWORD="vectra97"

# Obter o diretório do script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Caminho completo para o arquivo CSV
$CsvPath = Join-Path -Path $ScriptDir -ChildPath "vendas_smartphones.csv"

# Criar banco de dados
psql -U postgres -c "DROP DATABASE IF EXISTS vendas_smartphones_db;"
psql -U postgres -c "CREATE DATABASE vendas_smartphones_db;"

# Criar tabela
psql -U postgres -d vendas_smartphones_db -c @"
CREATE TABLE vendas_smartphones (
    id SERIAL PRIMARY KEY,
    modelo VARCHAR(100),
    fabricante VARCHAR(50),
    mes INTEGER,
    ano INTEGER,
    unidades_vendidas INTEGER,
    receita DECIMAL(12,2),
    regiao VARCHAR(50)
);
"@

# Importar dados do CSV
psql -U postgres -d vendas_smartphones_db -c @"
\copy vendas_smartphones(modelo, fabricante, mes, ano, unidades_vendidas, receita, regiao)
FROM '$CsvPath'
DELIMITER ','
CSV HEADER;
"@

Write-Host "✅ Banco configurado com sucesso!"