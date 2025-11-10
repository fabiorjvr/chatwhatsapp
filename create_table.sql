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