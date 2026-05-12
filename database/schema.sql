--
-- PostgreSQL database dump
--

\restrict d7PD8sunoHJbvv7uJdvkFv0Up47KPhfxlt23ts0R2yGLvBrmXEgvRfW3BR5HjlT

-- Dumped from database version 17.9 (Debian 17.9-1.pgdg13+1)
-- Dumped by pg_dump version 17.9 (Debian 17.9-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: _yoyo_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public._yoyo_log (
    id character varying(36) NOT NULL,
    migration_hash character varying(64),
    migration_id character varying(255),
    operation character varying(10),
    username character varying(255),
    hostname character varying(255),
    comment character varying(255),
    created_at_utc timestamp without time zone
);


ALTER TABLE public._yoyo_log OWNER TO admin;

--
-- Name: _yoyo_migration; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public._yoyo_migration (
    migration_hash character varying(64) NOT NULL,
    migration_id character varying(255),
    applied_at_utc timestamp without time zone
);


ALTER TABLE public._yoyo_migration OWNER TO admin;

--
-- Name: _yoyo_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public._yoyo_version (
    version integer NOT NULL,
    installed_at_utc timestamp without time zone
);


ALTER TABLE public._yoyo_version OWNER TO admin;

--
-- Name: avaliacoes_juiz; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.avaliacoes_juiz (
    id_avaliacao integer NOT NULL,
    id_resposta_ativa1 integer,
    id_modelo_juiz integer,
    nota_atribuida integer,
    chain_of_thought text NOT NULL,
    data_avaliacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT avaliacoes_juiz_nota_atribuida_check CHECK (((nota_atribuida >= 1) AND (nota_atribuida <= 5)))
);


ALTER TABLE public.avaliacoes_juiz OWNER TO admin;

--
-- Name: avaliacoes_juiz_id_avaliacao_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.avaliacoes_juiz_id_avaliacao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.avaliacoes_juiz_id_avaliacao_seq OWNER TO admin;

--
-- Name: avaliacoes_juiz_id_avaliacao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.avaliacoes_juiz_id_avaliacao_seq OWNED BY public.avaliacoes_juiz.id_avaliacao;


--
-- Name: categorias; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.categorias (
    id_categoria integer NOT NULL,
    nome character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.categorias OWNER TO admin;

--
-- Name: TABLE categorias; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON TABLE public.categorias IS 'Categorias das perguntas.';


--
-- Name: COLUMN categorias.nome; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.categorias.nome IS 'Nome da categoria.';


--
-- Name: categorias_id_categoria_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.categorias ALTER COLUMN id_categoria ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.categorias_id_categoria_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: datasets; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.datasets (
    id_dataset bigint NOT NULL,
    nome text NOT NULL,
    url_origem text,
    dominio text NOT NULL,
    tipo_tarefa text NOT NULL,
    versao text,
    descricao text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT datasets_tipo_tarefa_check CHECK ((tipo_tarefa = ANY (ARRAY['discursiva'::text, 'multipla_escolha'::text])))
);


ALTER TABLE public.datasets OWNER TO admin;

--
-- Name: TABLE datasets; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON TABLE public.datasets IS 'Conjuntos de dados de avaliação (benchmarks).';


--
-- Name: COLUMN datasets.id_dataset; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.datasets.id_dataset IS 'Identificador único do dataset.';


--
-- Name: COLUMN datasets.nome; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.datasets.nome IS 'Nome do dataset.';


--
-- Name: COLUMN datasets.url_origem; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.datasets.url_origem IS 'URL da origem do dataset.';


--
-- Name: COLUMN datasets.dominio; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.datasets.dominio IS 'Domínio do dataset.';


--
-- Name: COLUMN datasets.tipo_tarefa; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.datasets.tipo_tarefa IS 'Tipo de tarefa: discursiva ou múltipla escolha.';


--
-- Name: COLUMN datasets.versao; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.datasets.versao IS 'Versão do dataset.';


--
-- Name: COLUMN datasets.descricao; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.datasets.descricao IS 'Descrição do dataset.';


--
-- Name: COLUMN datasets.created_at; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.datasets.created_at IS 'Data de criação do dataset.';


--
-- Name: datasets_id_dataset_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.datasets ALTER COLUMN id_dataset ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.datasets_id_dataset_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: modelos; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.modelos (
    id_modelo integer NOT NULL,
    nome_modelo character varying(100) NOT NULL,
    versao character varying(50),
    provedor character varying(20),
    familia character varying(50),
    parametro_precisao character varying(20)
);


ALTER TABLE public.modelos OWNER TO admin;

--
-- Name: modelos_id_modelo_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.modelos_id_modelo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.modelos_id_modelo_seq OWNER TO admin;

--
-- Name: modelos_id_modelo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.modelos_id_modelo_seq OWNED BY public.modelos.id_modelo;


--
-- Name: perguntas; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.perguntas (
    id_pergunta integer NOT NULL,
    id_dataset integer NOT NULL,
    id_categoria integer NOT NULL,
    id_externo character varying(150) NOT NULL,
    tipo_pergunta character varying(30) NOT NULL,
    enunciado text NOT NULL,
    resposta_ouro text NOT NULL,
    nivel_dificuldade character varying(30) NOT NULL,
    legislacao_basica text,
    metadados jsonb,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_nivel_dificuldade CHECK (((nivel_dificuldade)::text = ANY ((ARRAY['Nivel 1'::character varying, 'Nivel 2'::character varying, 'Nivel 3'::character varying])::text[]))),
    CONSTRAINT ck_tipo_pergunta_p CHECK (((tipo_pergunta)::text = ANY ((ARRAY['discursiva'::character varying, 'multipla_escolha'::character varying])::text[])))
);


ALTER TABLE public.perguntas OWNER TO admin;

--
-- Name: TABLE perguntas; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON TABLE public.perguntas IS 'Perguntas base de todos os datasets.';


--
-- Name: COLUMN perguntas.id_externo; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.perguntas.id_externo IS 'ID original da pergunta no dataset de origem.';


--
-- Name: COLUMN perguntas.enunciado; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.perguntas.enunciado IS 'Texto principal da pergunta.';


--
-- Name: COLUMN perguntas.resposta_ouro; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.perguntas.resposta_ouro IS 'Resposta esperada pelo avaliador';


--
-- Name: COLUMN perguntas.metadados; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.perguntas.metadados IS 'Campos específicos do dataset não normalizados';


--
-- Name: perguntas_id_pergunta_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.perguntas ALTER COLUMN id_pergunta ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.perguntas_id_pergunta_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: respostas_atividade_1; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.respostas_atividade_1 (
    id_resposta integer NOT NULL,
    id_pergunta integer,
    id_modelo integer,
    texto_resposta text NOT NULL,
    tempo_inferencia_ms double precision,
    data_geracao timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.respostas_atividade_1 OWNER TO admin;

--
-- Name: respostas_atividade_1_id_resposta_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.respostas_atividade_1_id_resposta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.respostas_atividade_1_id_resposta_seq OWNER TO admin;

--
-- Name: respostas_atividade_1_id_resposta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.respostas_atividade_1_id_resposta_seq OWNED BY public.respostas_atividade_1.id_resposta;


--
-- Name: yoyo_lock; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.yoyo_lock (
    locked integer DEFAULT 1 NOT NULL,
    ctime timestamp without time zone,
    pid integer NOT NULL
);


ALTER TABLE public.yoyo_lock OWNER TO admin;

--
-- Name: avaliacoes_juiz id_avaliacao; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.avaliacoes_juiz ALTER COLUMN id_avaliacao SET DEFAULT nextval('public.avaliacoes_juiz_id_avaliacao_seq'::regclass);


--
-- Name: modelos id_modelo; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.modelos ALTER COLUMN id_modelo SET DEFAULT nextval('public.modelos_id_modelo_seq'::regclass);


--
-- Name: respostas_atividade_1 id_resposta; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.respostas_atividade_1 ALTER COLUMN id_resposta SET DEFAULT nextval('public.respostas_atividade_1_id_resposta_seq'::regclass);


--
-- Name: _yoyo_log _yoyo_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public._yoyo_log
    ADD CONSTRAINT _yoyo_log_pkey PRIMARY KEY (id);


--
-- Name: _yoyo_migration _yoyo_migration_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public._yoyo_migration
    ADD CONSTRAINT _yoyo_migration_pkey PRIMARY KEY (migration_hash);


--
-- Name: _yoyo_version _yoyo_version_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public._yoyo_version
    ADD CONSTRAINT _yoyo_version_pkey PRIMARY KEY (version);


--
-- Name: avaliacoes_juiz avaliacoes_juiz_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.avaliacoes_juiz
    ADD CONSTRAINT avaliacoes_juiz_pkey PRIMARY KEY (id_avaliacao);


--
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (id_categoria);


--
-- Name: datasets datasets_nome_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_nome_key UNIQUE (nome);


--
-- Name: datasets datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_pkey PRIMARY KEY (id_dataset);


--
-- Name: modelos modelos_nome_modelo_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.modelos
    ADD CONSTRAINT modelos_nome_modelo_key UNIQUE (nome_modelo);


--
-- Name: modelos modelos_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.modelos
    ADD CONSTRAINT modelos_pkey PRIMARY KEY (id_modelo);


--
-- Name: perguntas perguntas_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.perguntas
    ADD CONSTRAINT perguntas_pkey PRIMARY KEY (id_pergunta);


--
-- Name: respostas_atividade_1 respostas_atividade_1_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.respostas_atividade_1
    ADD CONSTRAINT respostas_atividade_1_pkey PRIMARY KEY (id_resposta);


--
-- Name: avaliacoes_juiz uq_avaliacoes_resposta_juiz; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.avaliacoes_juiz
    ADD CONSTRAINT uq_avaliacoes_resposta_juiz UNIQUE (id_resposta_ativa1, id_modelo_juiz);


--
-- Name: categorias uq_categoria_nome; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT uq_categoria_nome UNIQUE (nome);


--
-- Name: perguntas uq_pergunta_dataset; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.perguntas
    ADD CONSTRAINT uq_pergunta_dataset UNIQUE (id_dataset, id_externo);


--
-- Name: yoyo_lock yoyo_lock_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.yoyo_lock
    ADD CONSTRAINT yoyo_lock_pkey PRIMARY KEY (locked);


--
-- Name: idx_categorias_nome; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_categorias_nome ON public.categorias USING btree (nome);


--
-- Name: idx_perguntas_categoria; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_perguntas_categoria ON public.perguntas USING btree (id_categoria);


--
-- Name: idx_perguntas_dataset; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_perguntas_dataset ON public.perguntas USING btree (id_dataset);


--
-- Name: avaliacoes_juiz avaliacoes_juiz_id_modelo_juiz_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.avaliacoes_juiz
    ADD CONSTRAINT avaliacoes_juiz_id_modelo_juiz_fkey FOREIGN KEY (id_modelo_juiz) REFERENCES public.modelos(id_modelo);


--
-- Name: avaliacoes_juiz avaliacoes_juiz_id_resposta_ativa1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.avaliacoes_juiz
    ADD CONSTRAINT avaliacoes_juiz_id_resposta_ativa1_fkey FOREIGN KEY (id_resposta_ativa1) REFERENCES public.respostas_atividade_1(id_resposta);


--
-- Name: perguntas perguntas_id_categoria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.perguntas
    ADD CONSTRAINT perguntas_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria) ON DELETE RESTRICT;


--
-- Name: perguntas perguntas_id_dataset_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.perguntas
    ADD CONSTRAINT perguntas_id_dataset_fkey FOREIGN KEY (id_dataset) REFERENCES public.datasets(id_dataset) ON DELETE RESTRICT;


--
-- Name: respostas_atividade_1 respostas_atividade_1_id_modelo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.respostas_atividade_1
    ADD CONSTRAINT respostas_atividade_1_id_modelo_fkey FOREIGN KEY (id_modelo) REFERENCES public.modelos(id_modelo);


--
-- Name: respostas_atividade_1 respostas_atividade_1_id_pergunta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.respostas_atividade_1
    ADD CONSTRAINT respostas_atividade_1_id_pergunta_fkey FOREIGN KEY (id_pergunta) REFERENCES public.perguntas(id_pergunta);


--
-- PostgreSQL database dump complete
--

\unrestrict d7PD8sunoHJbvv7uJdvkFv0Up47KPhfxlt23ts0R2yGLvBrmXEgvRfW3BR5HjlT

