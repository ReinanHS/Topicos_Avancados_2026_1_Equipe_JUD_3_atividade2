-- 4. Tabela de Respostas da Atividade 1 (Modelos Candidatos)
CREATE TABLE respostas_atividade_1 (
    id_resposta SERIAL PRIMARY KEY,
    id_pergunta INTEGER REFERENCES perguntas(id_pergunta),
    id_modelo INTEGER REFERENCES modelos(id_modelo),
    texto_resposta TEXT NOT NULL,
    tempo_inferencia_ms FLOAT,
    data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
