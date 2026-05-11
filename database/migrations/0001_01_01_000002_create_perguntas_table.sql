-- 3. Tabela de Perguntas (O Dataset Original)
CREATE TABLE perguntas (
    id_pergunta INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_dataset INTEGER NOT NULL REFERENCES datasets (id_dataset) ON DELETE RESTRICT,
    id_categoria INTEGER NOT NULL REFERENCES categorias (id_categoria) ON DELETE RESTRICT,
    id_externo VARCHAR(150) NOT NULL,
    tipo_pergunta VARCHAR(30) NOT NULL,
    enunciado TEXT NOT NULL,
    resposta_ouro TEXT NOT NULL,
    nivel_dificuldade VARCHAR(30) NOT NULL,
    legislacao_basica TEXT,
    metadados JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT now (),
    CONSTRAINT ck_tipo_pergunta_p CHECK (
        tipo_pergunta IN ('discursiva', 'multipla_escolha')
    ),
    CONSTRAINT ck_nivel_dificuldade CHECK (
        nivel_dificuldade IN ('Nivel 1', 'Nivel 2', 'Nivel 3')
    ),
    CONSTRAINT uq_pergunta_dataset UNIQUE (id_dataset, id_externo)
);

COMMENT ON TABLE perguntas IS 'Perguntas base de todos os datasets.';

COMMENT ON COLUMN perguntas.id_externo IS 'ID original da pergunta no dataset de origem.';

COMMENT ON COLUMN perguntas.enunciado IS 'Texto principal da pergunta.';

COMMENT ON COLUMN perguntas.metadados IS 'Campos específicos do dataset não normalizados';

COMMENT ON COLUMN perguntas.resposta_ouro IS 'Resposta esperada pelo avaliador';

CREATE INDEX idx_perguntas_dataset ON perguntas (id_dataset);

CREATE INDEX idx_perguntas_categoria ON perguntas (id_categoria);