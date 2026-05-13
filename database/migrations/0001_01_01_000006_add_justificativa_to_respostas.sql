-- Adiciona campo justificativa para armazenar o raciocínio do modelo
-- candidato em questões de múltipla escolha. NULL para discursivas.
ALTER TABLE respostas_atividade_1
ADD COLUMN justificativa TEXT;
