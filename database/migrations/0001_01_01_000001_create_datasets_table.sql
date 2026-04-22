-- 2. Tabela de Datasets
CREATE TABLE datasets (
    id_dataset SERIAL PRIMARY KEY,
    nome_dataset VARCHAR(100) NOT NULL, -- Ex: 'OAB_Exams', 'K-QA'
    dominio VARCHAR(50) NOT NULL -- Ex: 'Jurídico', 'Médico'
);
