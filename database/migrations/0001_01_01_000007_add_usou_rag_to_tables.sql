-- Adiciona campo booleano usou_rag nas tabelas respostas_atividade_1 e avaliacoes_juiz
ALTER TABLE respostas_atividade_1 ADD COLUMN usou_rag BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE avaliacoes_juiz ADD COLUMN usou_rag BOOLEAN NOT NULL DEFAULT FALSE;
