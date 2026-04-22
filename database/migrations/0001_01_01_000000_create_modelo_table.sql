-- 1. Tabela de Metadados dos Modelos (Candidatos e Juízes)
CREATE TABLE modelos (
    id_modelo SERIAL PRIMARY KEY,
    nome_modelo VARCHAR(100) NOT NULL, -- Ex: 'Llama-3-8B-4bit', 'GPT-4o'
    versao VARCHAR(50),
    parametro_precisao VARCHAR(20) -- Ex: 'INT4', 'FP16', 'N/A'
);