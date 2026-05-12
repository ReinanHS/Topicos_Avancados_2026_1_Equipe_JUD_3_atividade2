-- Garante idempotência: cada (resposta, juiz) só pode ter uma avaliação
ALTER TABLE avaliacoes_juiz
ADD CONSTRAINT uq_avaliacoes_resposta_juiz
UNIQUE (id_resposta_ativa1, id_modelo_juiz);
