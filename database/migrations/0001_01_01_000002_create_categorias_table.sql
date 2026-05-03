-- 3. Tabela de Categorias
CREATE TABLE categorias (
    id_categoria INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now (),
    CONSTRAINT uq_categoria_nome UNIQUE (nome)
);

COMMENT ON TABLE categorias IS 'Categorias das perguntas.';

COMMENT ON COLUMN categorias.nome IS 'Nome da categoria.';

CREATE INDEX idx_categorias_nome ON categorias (nome);