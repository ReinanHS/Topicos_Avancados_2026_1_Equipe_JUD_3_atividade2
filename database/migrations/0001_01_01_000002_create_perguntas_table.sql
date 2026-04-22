-- 3. Tabela de Perguntas (O Dataset Original)
CREATE TABLE perguntas (
    id_pergunta SERIAL PRIMARY KEY,
    id_dataset INTEGER REFERENCES datasets(id_dataset),
    enunciado TEXT NOT NULL,
    resposta_ouro TEXT NOT NULL, -- Gabarito oficial
    metadados JSONB -- Para guardar info extra como 'especialidade' ou 'ano'
);
