English | [Português](./README.md)

<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/1/1c/Ufs_principal_positiva-nova.png" alt="ufs-logo" width="20%">

<h1>Advanced Topics in SE and IS</h1>

<p>Assessment activity 2: Implementation of the "LLM-as-a-Judge" framework and persistence in a relational database</p>

<p align="center">
  <!-- Python version -->
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue.svg" alt="Python 3.12+">
  <!-- PostgreSQL -->
  <img src="https://img.shields.io/badge/PostgreSQL-17-336791.svg?logo=postgresql&logoColor=white" alt="PostgreSQL 17">
  <!-- License -->
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  </a>
  <!-- Last commit -->
  <a href="https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2/commits/main">
    <img src="https://img.shields.io/github/last-commit/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2.svg" alt="Last commit">
  </a>
  <!-- Stars -->
  <a href="https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2/stargazers">
    <img src="https://img.shields.io/github/stars/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2.svg?style=social" alt="Stars">
  </a>
</p>

</div>

<details>
<summary>Table of contents (Click to expand)</summary>

- [About](#about)
- [Presentation](#presentation)
- [Contributors](#contributors)
- [Database architecture](#database-architecture)
- [Execution instructions](#execution-instructions)
  - [Prerequisites](#prerequisites)
  - [Starting the environment with Docker](#starting-the-environment-with-docker)
  - [Accessing CloudBeaver](#accessing-cloudbeaver)
  - [Running SQL queries in the browser](#running-sql-queries-in-the-browser)
- [LLM-as-a-Judge pipeline](#llm-as-a-judge-pipeline)
  - [Supported judges](#supported-judges)
  - [Credential configuration](#credential-configuration)
  - [Running the evaluator](#running-the-evaluator)
- [Statistical analysis (Spearman)](#statistical-analysis-spearman)
- [Contributions](#contributions)
- [License](#license)
- [References](#references)

</details>

## About

This repository contains the group's collective contributions to the second assessment activity of the course Advanced Topics in Software Engineering and Information Systems I (UFS 2026.1). In addition to the implemented features, the material presents the consolidated information and results that the team, as a whole, was able to develop during the activity.

The project continues the work from [Activity 1](https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1), advancing from basic inference to a structured evaluation of model responses. The main workstreams are:

- **LLM-as-a-Judge:** implementation of an automated judgment pipeline with legal rubrics (1–5 scale), Chain-of-Thought extraction, and the use of judge models to audit technical accuracy and legal grounding.
- **Persistence in PostgreSQL:** modeling and implementation of a relational database to store the complete experiment lifecycle, including datasets, candidate-model responses, and judge evaluations.
- **Statistical analysis:** calculation of Spearman correlation between the AI Judge scores and the human answer key, with error analysis and discussion of the results.

## Presentation

> **Coming soon.** The presentation video link (10–20 min) will be added here after recording.

The following video shows the results collected by the team for the second assessment activity:

[![YouTube video](https://gitlab.com/reinanhs/repo-slide-presentation/-/wikis/uploads/7cc03556931898d62b45b84b5006d119/image.png)](https://youtu.be/YiBB6kJq82w)

- **Watch the full video:** [https://youtu.be/YiBB6kJq82w](https://youtu.be/YiBB6kJq82w)

## Contributors

<div align="center">
<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/ReinanHS">
        <img src="https://github.com/reinanhs.png" height="64" width="64" alt="Reinan Gabriel"/>
      </a><br/>
      <a href="https://github.com/ReinanHS">Reinan Gabriel</a>
    </td>
    <td align="center">
      <a href="https://github.com/Ericles-Porty">
        <img src="https://github.com/Ericles-Porty.png" height="64" width="64" alt="Ericles Dos Santos"/>
      </a><br/>
      <a href="https://github.com/Ericles-Porty">Ericles Dos Santos</a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/Leomascarenhas91">
        <img src="https://github.com/Leomascarenhas91.png" height="64" width="64" alt="Victor Mascarenhas"/>
      </a><br/>
      <a href="https://github.com/Leomascarenhas91">Victor Mascarenhas</a>
    </td>
    <td align="center">
      <a href="https://github.com/safira1344">
        <img src="https://github.com/safira1344.png" height="64" width="64" alt="Ericles Dos Santos"/>
      </a><br/>
      <a href="https://github.com/safira1344">Fernanda Mirely</a>
    </td>
  </tr>
</table>
</div>

---

## Database architecture

The relational schema follows the structure suggested by the professor, with five main tables:

- [Open the link to view the detailed diagram on DBDiagram.io](https://dbdiagram.io/d/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2-69e940f2d80a958d1cb60703)

<img src="docs/assets/arquitetura-do-banco-de-dados.svg" alt="Entity-relationship diagram" width="100%">

---

## 🚀 How to start the project (Step by step)

Welcome! To make the setup process easier to understand, we organized the environment configuration into simple stages. Follow them in order to get everything working properly.

### 1. Prerequisites

Before getting started, make sure you have the following tools installed:

| Tool | Minimum version | Why do we need it? |
|-----------|---------------|-----------|
| [Python](https://www.python.org/downloads/) | 3.12+ | Main programming language of the project. |
| [Docker](https://docs.docker.com/get-docker/) | 24+ | Runs the database and supporting tools without cluttering your machine. |
| [Docker Compose](https://docs.docker.com/compose/install/) | 2.x | Starts all Docker containers with a single command. |
| [Git](https://git-scm.com/install) | 2.x | Downloads the code and manages version control. |
| [Make](https://www.gnu.org/software/make/) | (Optional) | Runs helpful shortcuts, but we also provide the raw commands in case it is not installed. |

> **💡 Tip:** PostgreSQL (version 17) is already configured inside Docker. You do not need to install it separately on your machine!

### 2. Starting the environment with Docker

With Docker installed and running on your computer, open a terminal at the project root and start the services:

```bash
docker pull ghcr.io/reinanhs/jud-db:latest
docker compose down -v
docker compose up -d
```

> **🐳 Golden Docker tips (Avoiding headaches):**
> 
> - **Always pull the latest version:** To make sure you have the newest database or tool image, add the `--pull always` tag:
>   `docker compose up -d --pull always`
> - **Cache problems?** If something looks strange or a configuration is not updating, force image recreation while ignoring the cache:
>   `docker compose build --no-cache`
> - **Starting completely from scratch:** To fully reset the database and delete all data, remove the *volumes* when stopping the containers:
>   `docker compose down -v`

The `up -d` command will quietly run two main services:
- **PostgreSQL 17** (Port `5432`): The relational database.
- **CloudBeaver** (Port `8978`): Browser-based interface for managing the database (details in the next section).

To check whether they are running: `docker compose ps`
To shut everything down at the end of the day: `docker compose down`

### 3. Installing the project dependencies

Now let us prepare the Python environment. The project uses the `uv` tool for a very fast installation:

```bash
# 1. Create the virtual environment, a safe space for the project's libraries
python -m venv .venv

# 2. Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows (PowerShell):
# .venv\Scripts\activate

# 3. Install all dependencies at once
uv sync
```

### 4. Populating the database

For the project to work properly, you will need data. Running the extractions from scratch can be a slow process because of the large number of requests and the processing of dense texts.

#### Easy way (Recommended)

To simplify the process, **our CI/CD automatically updates the database image**. This means the data is already prepared inside the image, and you may not need to run the manual commands below.

This automatic *dump* process ensures that the information is processed by CI/CD, reducing the local workload. When downloading the image, the database is already initialized and populated.

The only required action is to download the image, as shown in the previous sections, and verify that there are no cache conflicts.

```shell
docker pull ghcr.io/reinanhs/jud-db:latest
docker compose down -v
docker compose up -d --pull always

```

#### Advanced way

In some scenarios, you may prefer to import everything manually. To do this, use the procedure below to delete your current database and recreate it using the import scripts and the preprocessed configurations:

```bash
# 1. Recreate the tables from scratch using the migration files
uv run python main.py db rollback
uv run python main.py db migrate

# 2. Import the seed data, i.e., the initial data
uv run python main.py db seed all

# 3. Import all questions and responses from the datasets
uv run python main.py db seed import-all

# 4. Import all evaluations already performed by the AI Judges
uv run python main.py db judge import-all

```

> **Why do this?** The import process is smart and resolves references by natural names, making it idempotent. This avoids redundant network calls, saving time and possible API costs.

#### Manual import via pg_dump

```shell
make db-restore-full
```

If you do not have **make** installed, you can copy the instructions directly from the `Makefile`.

### Sharing new extractions

```bash
uv run python main.py db seed export --type all
```

Quick table of manual commands:

| Command | What it does |
|---|---|
| `db seed export --type perguntas` | Exports only questions. |
| `db seed export --type respostas` | Exports only responses. |
| `db seed export --type all` | Exports both, which is the default. |
| `db seed import <arquivo.json>` | Imports one file and detects the type automatically. |
| `db seed import-all` | Imports questions and responses from the default folder. |

### Accessing CloudBeaver

[CloudBeaver](https://dbeaver.com/docs/cloudbeaver/) is a web-based database administration tool. It is already configured automatically with the project's PostgreSQL connection.

1. Open the browser and access: [http://localhost:8978](http://localhost:8978)
2. Anonymous access is already enabled, so **you do not need to log in**.
3. In the left sidebar, you will see the **jud_db** connection already available.
4. Click the connection to expand it and view the database tables.

> **Administrative access:** If you need administrator permissions, use the credentials `cbadmin` / `Admin123`.

### Running SQL queries in the browser

To execute SQL queries directly through CloudBeaver:

1. In the left sidebar, click the **jud_db** connection to select it.
2. Click the **SQL** button in the top bar, or press `Ctrl + Enter` after opening the editor.
3. In the SQL editor that opens, enter your query. For example:

```sql
SELECT * FROM modelos;
```

4. Click the **▶ Run** button, or press `Ctrl + Enter`, to execute the query.
5. The results will be displayed at the bottom of the editor in table format.

See the example in the image below:

![Example of executing an SQL query in CloudBeaver](docs/assets/executando-consultas-sql-no-navegador.png)

---

### Accessing Grafana

[Grafana](https://grafana.com/docs/grafana/latest/) is a data visualization tool. It is already configured automatically with the project's PostgreSQL connection.

1. Open the browser and access: [http://localhost:3000](http://localhost:3000)
2. Anonymous access is already enabled, so **you do not need to log in**.
3. In the left sidebar, you will see the **jud_db** connection already available.
4. Click the connection to expand it and view the database tables.

> **Administrative access:** If you need administrator permissions, use the credentials `admin` / `admin`.

![Example of a Grafana dashboard](docs/assets/dashboard-no-grafana.png)

---

## LLM-as-a-Judge pipeline

The evaluator, or AI Judge, reads the responses generated in Activity 1 (table `respostas_atividade_1`), submits each one to a judge model with the OAB Appellate Judge rubric (1–5 scale), and persists the verdict, namely score + Chain-of-Thought, in `avaliacoes_juiz`.

Modular architecture: `BaseJudge` (contract) → `JudgeFactory` (resolves `provider:model` into the correct instance) → concrete implementations for [Ollama](src/services/judges/ollama_judge.py), [Anthropic](src/services/judges/anthropic_judge.py), and [OpenAI](src/services/judges/openai_judge.py). The prompt is in [prompts.py](src/services/judges/prompts.py), and the verdict parser is in [parser.py](src/services/judges/parser.py). Idempotency is guaranteed in the database through a unique constraint on `(id_resposta_ativa1, id_modelo_juiz)`.

### Supported judges

| CLI spec | Type | Model in the database |
|---|---|---|
| `ollama:llama3.1:8b` | Local (Ollama) | Llama 3.1 |
| `ollama:qwen2.5:7b` | Local (Ollama) | Qwen 2.5 |
| `anthropic:claude-sonnet-4-6` | API | Claude Sonnet 4.6 |
| `openai:gpt-4o` | API | GPT-4o |

To list them dynamically:

```bash
uv run python main.py db judge list-available
```

### Credential configuration

Copy `.env.example` to `.env` and fill it in according to the judge or judges you intend to use:

```env
# For API-based judges, optional, fill in only what you will use
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# For local judges through Ollama, the default is http://localhost:11434
OLLAMA_HOST=http://localhost:11434
```

For Ollama judges, make sure the model has already been downloaded:

```bash
ollama pull llama3.1:8b
ollama pull qwen2.5:7b
```

### Running the evaluator

The command accepts from 1 to 3 judges per execution. Repeat `-j` to use multiple judges:

```bash
# Only one local judge, with no API cost
uv run python main.py db judge evaluate -j ollama:llama3.1:8b --limit 9 --workers 3
uv run python main.py db judge evaluate -j google:gemini-2.5-flash --limit 9 --workers 3
uv run python main.py db judge evaluate -j openai:gpt-4o --limit 9 --workers 3
uv run python main.py db judge evaluate -j openai:gpt-5-mini-2025-08-07 --limit 9 --workers 3

# Smoke test with a limit, useful for validating the pipeline
uv run python main.py db judge evaluate -j ollama:llama3.1:8b --limit 5

# Multi-judge, up to 3
uv run python main.py db judge evaluate \
  -j ollama:llama3.1:8b \
  -j anthropic:claude-sonnet-4-6 \
  -j openai:gpt-4o
```

The pipeline automatically skips responses that the specified judge has already evaluated, so you can interrupt and resume as needed without duplicating API costs.

### Sharing evaluations without reprocessing

To prevent each team member from paying for the API again, after running `judge evaluate`, perform the export and commit the file:

```bash
uv run python main.py db judge export -j openai:gpt-4o
uv run python main.py db judge export -j google:gemini-2.5-flash
uv run python main.py db judge export -j openai:gpt-5-mini-2025-08-07
```

Other members, after running `git pull`, can load the data without calling the API:

```bash
uv run python main.py db judge import database/backup/avaliacoes-gpt-4o-mini.json
```

Available commands:

| Command | What it does |
|---|---|
| `db judge export -j <spec>` | Exports a specific judge to `database/backup/avaliacoes-<slug>.json`. |
| `db judge export --all` | Generates one file for each judge that already has evaluations in the database. |
| `db judge export -j <spec> --output <path>` | Exports to a custom path. |
| `db judge import <arquivo.json>` | Imports a specific file, idempotently. |
| `db judge import-all` | Imports all `avaliacoes-*.json` files from the default folder. |

The file format is portable JSON with natural keys, namely dataset name, question `id_externo`, and candidate model name, instead of auto-incremented IDs. Therefore, it works even if a teammate's database has different IDs from yours. The import is idempotent at two levels: `AvaliacoesExporter.import_file` checks whether each `(response, judge)` pair already exists, and the `uq_avaliacoes_resposta_juiz` database constraint acts as a safety belt.

---

## Statistical analysis (Spearman)

After populating `avaliacoes_juiz`, the analysis module calculates the **Spearman correlation (ρ)** between the AI Judge and the human answer key. This section explains what the metric is, why we chose it, and how to interpret the results generated by the project.

### Why Spearman instead of Pearson?

The scores assigned by the AI Judge, on a 1 to 5 scale, are **ordinal data**: there is a clear order, since 5 is better than 4, which is better than 3, and so on, but the *distance* between values is not necessarily uniform. The qualitative difference between "Score 1 — severe hallucination" and "Score 2 — vague grounding" may be much greater than the difference between "Score 4 — excellent" and "Score 5 — exceptional".

- **Pearson correlation** measures the *linear* relationship between continuous variables and assumes that distances are meaningful, which **does not hold** for our scale.
- **Spearman correlation** operates on *ranks*: each value is transformed into its relative position in the sample. It captures any **monotonic relationship**, whether increasing or decreasing, regardless of whether the function is linear. For this reason, it is the recommended metric when the data are ordinal, as in rubric-based scores. It is also the metric explicitly suggested in the activity instructions.

### The formula

When there are no ties among the scores, Spearman has the classic closed form:

$$\rho = 1 - \frac{6 \sum_{i=1}^{n} d_i^2}{n(n^2 - 1)}$$

Where:
- $d_i$ is the difference between the rank of the AI Judge score and the rank of the human score, for the i-th question;
- $n$ is the total number of evaluated questions.

When ties occur, which is common on a 1–5 scale, the implementation in `scipy.stats.spearmanr` calculates Pearson correlation over average ranks. The result is equivalent and robust. For this reason, we use `scipy` in [spearman_service.py](src/services/analysis/spearman_service.py) instead of implementing the formula manually.

The function also returns a **p-value**, which indicates the probability of obtaining a correlation as strong as the observed one *purely by chance*. Low values, typically $p < 0.05$, indicate that the correlation is statistically significant.

### Methodology applied in the project

The `db analysis run` command produces three output blocks:

```bash
uv run python main.py db analysis run
```

#### 1. Aggregated summary (descriptive statistics)

For each `(dataset, candidate model, judge)` combination, the system calculates the mean, standard deviation, and count of scores. This serves as a sanity check before examining the correlation: if a judge only assigns score 5, any ρ will be degenerate.

The underlying SQL query is in [avaliacao_repository.py](src/repositories/avaliacao_repository.py#L121-L156) and follows the example from the activity instructions:

```sql
SELECT d.nome AS dataset, m_cand.nome_modelo AS candidato,
       m_juiz.nome_modelo AS juiz,
       AVG(a.nota_atribuida) AS media,
       STDDEV_SAMP(a.nota_atribuida) AS desvio,
       COUNT(a.id_avaliacao) AS total
FROM avaliacoes_juiz a
JOIN respostas_atividade_1 r ON r.id_resposta = a.id_resposta_ativa1
JOIN perguntas p ON p.id_pergunta = r.id_pergunta
JOIN datasets d ON d.id_dataset = p.id_dataset
JOIN modelos m_cand ON m_cand.id_modelo = r.id_modelo
JOIN modelos m_juiz ON m_juiz.id_modelo = a.id_modelo_juiz
GROUP BY d.nome, candidato, juiz;
```

#### 2. Scenario A — Judge × Human Answer Key (multiple choice)

For **multiple-choice** questions (`oab_exams`), the human answer key is discrete, namely letter A, B, C, D, or E. We follow the strategy described in the activity instructions:

1. Extract the `answerKey` from the question metadata;
2. Check whether the model response text contains the correct letter, using a regex heuristic `\b<letter>\b`;
3. Convert the human answer key into a **binarized score**: `5` if the model chose the correct alternative, `1` if it did not;
4. Calculate Spearman between this binarized series and the judge scores for the same set of questions.

The intuition is direct: if the judge assigns high scores whenever the model selects the correct alternative and low scores when it gets the answer wrong, ρ approaches 1.

#### 3. Scenario B — Inter-judge agreement (open-ended questions)

For **discursive** questions (`oab_bench`), there is no human numeric score. The reference answer is a text guideline, not a number. Here, we use a common complementary technique in LLM-as-a-Judge studies: **inter-judge agreement** (`inter-rater agreement`).

When at least two judges have evaluated the same responses, we calculate Spearman pairwise. This answers two important questions:

- **Convergence:** If GPT-4o and Claude Sonnet 4.6 agree, with high ρ, there is evidence that the rubric is robust and the signal is not random.
- **Bias detection:** If a low-cost local judge, such as Llama 3.1 8B, has high ρ with a premium judge, such as GPT-4o, it may be a viable substitute. If ρ is low, the cost × quality trade-off becomes evident.

### Interpreting ρ

The Spearman range is $\rho \in [-1, 1]$. The interpretation recommended by the activity instructions is:

| ρ range | Interpretation | Recommended action |
|---|---|---|
| 0.7 – 1.0 | **Strong alignment** | The judge "thinks" like the answer key; viable for use at scale. |
| 0.3 – 0.6 | **Moderate alignment** | The rubric needs to be more specific; review the criteria. |
| 0.0 – 0.3 | **Weak alignment** | The judge is inconsistent; change the model or refine the prompt. |
| < 0 | **Systematic disagreement** | Scientific finding — investigate bias, since the judge may be more up to date than the answer key, or vice versa. Document it in the report. |

Special cases handled in [spearman_service.py](src/services/analysis/spearman_service.py):

- **Insufficient sample** (n < 2): ρ is undefined; the report prints `motivo` instead of breaking.
- **Constant scores** (the judge always assigns the same score): variance is zero, ρ is undefined; this is reported explicitly.
- **Missing answer key** (`answerKey` absent from metadata): the question is skipped and counted in `skipped(sem gabarito)`.

### Known limitation: answer key in multiple-choice questions

The "Judge × Human Answer Key" block depends on `answerKey` being present in `metadados.jsonb` for multiple-choice questions. [base_extractor.py](src/services/extractors/base_extractor.py) was updated to capture this field, but the insertions use `ON CONFLICT DO NOTHING`. Therefore, if the database was populated **before** this update, older rows will not receive `answerKey`.

To solve this:

```bash
uv run python main.py db rollback   # roll back migrations
uv run python main.py db migrate    # recreate the tables
uv run python main.py db seed all   # recapture everything with answerKey already present
```

### Reference

- [SciPy: scipy.stats.spearmanr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html) — implementation used.
- Spearman, C. (1904). *The Proof and Measurement of Association between Two Things*. American Journal of Psychology.

---

## Contributions

See the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project uses the MIT License. See the [LICENSE](LICENSE) file for the full terms.

## References

- [Activity 1: Team JUD_3 repository](https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1)
- [OAB Bench](https://huggingface.co/datasets/maritaca-ai/oab-bench)
- [OAB Exams](https://huggingface.co/datasets/eduagarcia/oab_exams)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [LLM Evaluation: A Comprehensive Survey](https://arxiv.org/html/2504.21202v1)
- [SciPy: spearmanr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html)

---

<div align="center">
  <sub>Developed by Team 3 (Legal Domain) | UFS 2026.1</sub>
</div>
