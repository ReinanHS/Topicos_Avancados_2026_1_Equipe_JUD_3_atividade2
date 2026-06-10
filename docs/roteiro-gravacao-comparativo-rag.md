# Roteiro de gravação — Comparativo Sem RAG × Com RAG

Anotações para gravar a execução do projeto. Os comandos estão divididos em
**(1) comandos primordiais** (preparam o ambiente e os dados) e
**(2) comandos de geração de comparativos** (a parte nova: análise + gráficos,
com filtro por aluno).

> **Dica para a gravação:** use sempre `uv run python main.py ...`. O `uv run`
> ativa o ambiente virtual automaticamente, então você não precisa rodar
> `.venv\Scripts\Activate.ps1` antes (evita o erro `ModuleNotFoundError`).

---

## 1. Comandos primordiais (setup do ambiente e dos dados)

Estes são os passos que deixam o banco pronto. Numa máquina que já baixou a
imagem Docker com o dump, muitos já vêm prontos — mas para a gravação vale
mostrar a sequência.

### 1.1 Subir o banco (Docker)

```bash
docker compose up -d --pull always
```
> Sobe o PostgreSQL 17 (porta 5432) e as ferramentas de visualização web.
> Conferir com `docker compose ps`.

### 1.2 Instalar dependências do projeto

```bash
uv sync
```
> Instala tudo o que está no `pyproject.toml`/`uv.lock` (inclui `scipy`,
> `psycopg2`, `typer` e o `matplotlib` usado nos gráficos).

### 1.3 Preparar o schema e popular o banco

```bash
# Recria as tabelas a partir das migrações
uv run python main.py db rollback
uv run python main.py db migrate

# Semeia dados base (modelos, categorias, datasets) + perguntas/respostas
uv run python main.py db seed all

# Importa perguntas/respostas e avaliações já processadas (evita refazer e pagar API)
uv run python main.py db seed import-all
uv run python main.py db judge import-all
```
> O `seed all` já inclui as respostas **com RAG** (`db seed respostas-rag`) — é
> isso que viabiliza o comparativo. O `judge import-all` traz as notas dos
> juízes que a equipe já gerou.

### 1.4 (Opcional) Rodar um juiz na hora

Só se quiser mostrar o pipeline LLM-as-a-Judge ao vivo. Exige credencial no
`.env` (ou Ollama local). Use `--limit` para um smoke test rápido:

```bash
uv run python main.py db judge list-available
uv run python main.py db judge evaluate -j openai:gpt-4o --limit 9 --workers 3
```

### 1.5 (Opcional) Análise estatística completa (Spearman base)

```bash
uv run python main.py db analysis run
```
> Imprime: resumo agregado, Spearman juiz × gabarito, correlação inter-juízes
> **e** o comparativo Sem RAG × Com RAG.

---

## 2. Comandos de geração de comparativos (parte nova)

A parte que responde "o RAG melhorou as notas?". Separa as avaliações pela flag
`usou_rag` da resposta avaliada e calcula o **ganho** (média com RAG − média sem
RAG) por `(dataset, candidato, juiz)`.

### 2.1 Comparativo no terminal (tabela)

```bash
uv run python main.py db analysis rag
```
> Mostra a tabela com **Média s/RAG**, **Média c/RAG**, **Ganho** (com `^`/`v`
> indicando subida/descida), o **N** de cada cenário, a linha **GERAL** (média
> ponderada) e o **Spearman juiz × gabarito** separado por cenário.

### 2.2 Comparativo + gráficos PNG

```bash
uv run python main.py db analysis rag --charts
```
> Faz tudo do item anterior **e** gera os gráficos em `database/charts/`.

### 2.3 Apenas os gráficos

```bash
uv run python main.py db analysis charts
```
> Gera, por juiz, um PNG com barras agrupadas (Sem RAG × Com RAG) + barras de
> ganho, e um PNG consolidado `comparativo-rag-geral.png`.

### 2.4 Filtrando por aluno (componente da equipe)

Use `--owner` para olhar **só as questões de um integrante**. Valores aceitos:
`ericles`, `julia`, `mikaela`, `fernanda`, `reinan`, `victor`.

```bash
# Tabela só com as questões do Ericles
uv run python main.py db analysis rag --owner ericles

# Gráficos só do Ericles (arquivos saem prefixados: ericles-comparativo-rag-*.png)
uv run python main.py db analysis charts --owner ericles

# Tabela + gráficos de um aluno de uma vez
uv run python main.py db analysis rag --charts --owner reinan
```
> O filtro usa o campo `metadados->>'source_file'` das perguntas (gravado na
> extração), então casa exatamente com o dono de cada questão.

### 2.5 Mudando a pasta de saída dos gráficos

```bash
uv run python main.py db analysis charts --owner ericles --output docs/assets/charts
```

---

## Resumo rápido (cola para a gravação)

| Etapa | Comando |
|---|---|
| Subir banco | `docker compose up -d --pull always` |
| Dependências | `uv sync` |
| Schema | `uv run python main.py db migrate` |
| Popular tudo | `uv run python main.py db seed all` |
| Importar avaliações | `uv run python main.py db judge import-all` |
| **Comparativo (tabela)** | `uv run python main.py db analysis rag` |
| **Comparativo + gráficos** | `uv run python main.py db analysis rag --charts` |
| **Só gráficos** | `uv run python main.py db analysis charts` |
| **Por aluno** | `uv run python main.py db analysis rag --charts --owner ericles` |

> Os gráficos ficam em `database/charts/` (essa pasta está no `.gitignore` por
> serem artefatos gerados). Para incluir no relatório, copie os PNGs ou use
> `--output` apontando para uma pasta versionada (ex.: `docs/assets/charts`).
