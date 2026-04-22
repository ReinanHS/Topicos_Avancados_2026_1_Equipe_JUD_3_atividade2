-- 5. Tabela de Avaliações da Atividade 2 (O Juiz)
CREATE TABLE avaliacoes_juiz (
    id_avaliacao SERIAL PRIMARY KEY,
    id_resposta_ativa1 INTEGER REFERENCES respostas_atividade_1(id_resposta),
    id_modelo_juiz INTEGER REFERENCES modelos(id_modelo),
    nota_atribuida INTEGER CHECK (nota_atribuida BETWEEN 1 AND 5),
    chain_of_thought TEXT NOT NULL, -- O raciocínio explicativo do Juiz
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
