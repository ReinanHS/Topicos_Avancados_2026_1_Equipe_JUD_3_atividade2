# Atividade 2: Implementação de Framework "LLM-as-a-Judge" e Persistência em Banco de Dados Relacional

## 1. Contexto e objetivo

A avaliação manual de milhares de instâncias em domínios como Direito e Medicina é inviável em escala industrial. No entanto, as métricas clássicas, como ROUGE e BLEU, são insuficientes por serem puramente lexicais.

Nesta etapa, as equipes deverão implementar uma solução mais sofisticada para avaliar as respostas fornecidas pelos modelos selecionados na Atividade 1. O objetivo é consolidar os resultados em uma infraestrutura robusta, utilizando o paradigma **LLM-as-a-Judge** para auditar a acurácia técnica, segurança clínica e fundamentação jurídica, armazenando todo o ciclo de vida dos dados em um ambiente relacional.

## 2. Repositórios de dados e links de acesso

As equipes mantêm os domínios e datasets da atividade anterior:

- ⚖️ **Jurídico** (Equipes 1, 3 e 4): `maritaca-ai/oab-bench` (abertas) e `eduagarcia/oab_exams` (múltipla escolha).
- 🩺 **Médico** (Equipes 2 e 5): Itaymanes K-QA (abertas) e USMLE com gabarito (múltipla escolha).

## 3. Etapas previstas

1. **Consolidação e modelagem de dados:** organizar o dataset original e as respostas geradas pelos modelos selecionados e testados na Atividade 1.
2. **Arquitetura PostgreSQL:** modelar e implementar um banco de dados relacional para armazenar:
   - O dataset original, com perguntas e gabaritos.
   - As respostas da Atividade 1, identificando o modelo utilizado.
   - As avaliações do Juiz, com notas e o Chain-of-Thought explicativo.
3. **Execução do Juiz-IA:** implementar o pipeline `Input -> Referência -> Prompt do Juiz -> Output` utilizando outros modelos, se possível, com melhor capacidade que os utilizados na Atividade 1.
4. **Análise de dados via SQL:** extrair métricas diretamente do banco para analisar a correlação de Spearman entre o Juiz e o gabarito humano.

## 4. Artefatos e regras de entrega

**Data limite:** 14 de maio de 2026, quinta-feira, até as 12h00.

- **Repositório GitHub:** pasta `Atividade_2` contendo scripts Python, prompts e o arquivo de backup (`.sql` ou `.dump`) do PostgreSQL.
- **Tutorial em PDF:** deve incluir instruções detalhadas de restore do banco de dados, exemplos de queries utilizadas e a metodologia da rubrica.
- **Vídeo de apresentação:** duração mínima de 10 minutos e máxima de 20 minutos. O link deve constar no `README.md`. Cada membro deve demonstrar sua parte na engenharia do banco ou na calibração do Juiz.
- **Instruções de restore:** é mandatório que o tutorial permita ao professor recriar o ambiente de dados localmente para auditoria das notas.

## 5. Barema de avaliação

| Critério | Descrição | Peso |
|---|---|---:|
| Modelagem e PostgreSQL | Qualidade do esquema relacional, integridade dos dados e facilidade de restore. | 30% |
| Engenharia de rubricas | Rigor técnico e criatividade na definição das escalas de 1 a 5 para o Juiz. | 20% |
| Pipeline de avaliação | Implementação do fluxo de julgamento e extração do Chain-of-Thought. | 25% |
| Análise de resultados | Profundidade da discussão estatística baseada nos dados do banco. | 15% |
| Vídeo e documentação | Clareza na exposição e organização dos artefatos no GitHub. | 10% |

> **Nota do professor:** a inclusão do PostgreSQL visa simular um ambiente real de produção onde a rastreabilidade é fundamental. Não basta avaliar; é preciso saber quem avaliou, quando e sob qual lógica explicativa.

# Apêndice

## Esquema de banco de dados sugerido (DDL)

As equipes podem executar o código abaixo diretamente no console do PostgreSQL ou via pgAdmin:

```sql
-- 1. Tabela de Metadados dos Modelos (Candidatos e Juízes)
CREATE TABLE modelos (
    id_modelo SERIAL PRIMARY KEY,
    nome_modelo VARCHAR(100) NOT NULL, -- Ex: 'Llama-3-8B-4bit', 'GPT-4o'
    versao VARCHAR(50),
    parametro_precisao VARCHAR(20) -- Ex: 'INT4', 'FP16', 'N/A'
);

-- 2. Tabela de Datasets
CREATE TABLE datasets (
    id_dataset SERIAL PRIMARY KEY,
    nome_dataset VARCHAR(100) NOT NULL, -- Ex: 'OAB_Exams', 'K-QA'
    dominio VARCHAR(50) NOT NULL -- Ex: 'Jurídico', 'Médico'
);

-- 3. Tabela de Perguntas (O Dataset Original)
CREATE TABLE perguntas (
    id_pergunta SERIAL PRIMARY KEY,
    id_dataset INTEGER REFERENCES datasets(id_dataset),
    enunciado TEXT NOT NULL,
    resposta_ouro TEXT NOT NULL, -- Gabarito oficial
    metadados JSONB -- Para guardar info extra como 'especialidade' ou 'ano'
);

-- 4. Tabela de Respostas da Atividade 1 (Modelos Candidatos)
CREATE TABLE respostas_atividade_1 (
    id_resposta SERIAL PRIMARY KEY,
    id_pergunta INTEGER REFERENCES perguntas(id_pergunta),
    id_modelo INTEGER REFERENCES modelos(id_modelo),
    texto_resposta TEXT NOT NULL,
    tempo_inferencia_ms FLOAT,
    data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabela de Avaliações da Atividade 2 (O Juiz)
CREATE TABLE avaliacoes_juiz (
    id_avaliacao SERIAL PRIMARY KEY,
    id_resposta_ativa1 INTEGER REFERENCES respostas_atividade_1(id_resposta),
    id_modelo_juiz INTEGER REFERENCES modelos(id_modelo),
    nota_atribuida INTEGER CHECK (nota_atribuida BETWEEN 1 AND 5),
    chain_of_thought TEXT NOT NULL, -- O raciocínio explicativo do Juiz
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Exemplo de query para análise (relatório)

Para que as equipes possam calcular a performance média e extrair os dados para o cálculo de correlação, elas podem usar uma query como esta:

```sql
SELECT
    d.nome_dataset,
    m_cand.nome_modelo AS candidato,
    m_juiz.nome_modelo AS juiz,
    AVG(a.nota_atribuida) AS media_notas,
    COUNT(a.id_avaliacao) AS total_avaliado
FROM avaliacoes_juiz a
JOIN respostas_atividade_1 r ON a.id_resposta_ativa1 = r.id_resposta
JOIN perguntas p ON r.id_pergunta = p.id_pergunta
JOIN datasets d ON p.id_dataset = d.id_dataset
JOIN modelos m_cand ON r.id_modelo = m_cand.id_modelo
JOIN modelos m_juiz ON a.id_modelo_juiz = m_juiz.id_modelo
GROUP BY d.nome_dataset, candidato, juiz;
```

## Recomendações para os alunos

- **JSONB para metadados:** recomenda-se o uso do tipo `JSONB` na tabela de perguntas para que as equipes possam guardar chaves específicas de cada dataset, como `{"alternativa_correta": "A"}` para múltipla escolha ou `{"especialidade": "Cardiologia"}` para o K-QA, sem precisar alterar a estrutura da tabela.
- **Backup:** usem o comando `pg_dump` para gerar o arquivo que será entregue. O comando padrão seria:

```bash
pg_dump -U nome_usuario -d nome_banco -f backup_atividade_2.sql
```

- **Restore:** o tutorial de entrega deve ser claro. Um comando simples como o seguinte deve ser suficiente para recriar todo o experimento:

```bash
psql -U usuario -d novo_banco -f backup_atividade_2.sql
```

Com este esquema, o projeto ganha um nível de rastreabilidade profissional.

## Templates de partida para as equipes

### Para as equipes do domínio jurídico (J1 e J2)

Este prompt foca na fidelidade à legislação brasileira e na detecção de "alucinações normativas", quando o modelo inventa leis.

#### Prompt do Juiz Jurídico

```text
[PERSONA]
Você é um Desembargador e Professor Doutor em Direito com vasta experiência em exames da OAB. Sua tarefa é avaliar a resposta de uma IA (candidata) a uma questão jurídica.

[CONTEXTO]
Pergunta: {pergunta_oab}
Gabarito (Resposta Ouro): {resposta_ouro}
Resposta da IA a ser avaliada: {resposta_modelo_edge}

[RUBRICA DE AVALIAÇÃO]
- Nota 1: Resposta incorreta, cita leis inexistentes ou confunde institutos básicos.
- Nota 2: Conclusão correta, mas a fundamentação é vaga ou cita artigos de lei errados.
- Nota 3: Resposta correta e bem fundamentada, mas falta clareza ou omite detalhes importantes do gabarito.
- Nota 4: Resposta excelente, alinhada ao gabarito, com fundamentação legal precisa.
- Nota 5: Resposta excepcional, fundamentada, cita jurisprudência relevante (STF/STJ) e demonstra raciocínio jurídico mestre.

[INSTRUÇÕES DE SAÍDA]
Analise a resposta da IA comparando-a com o Gabarito. Ignore o tamanho do texto; foque na precisão do Direito brasileiro.
Forneça o veredito no formato:
RACIOCÍNIO: <explique por que a nota foi dada>
NOTA: <apenas o número de 1 a 5>
```

### Para as equipes do domínio médico (M1 e M2)

Este prompt é desenhado para ser implacável com erros de segurança e dosagens, priorizando a vida do paciente sobre a fluidez do texto.

#### Prompt do Juiz Médico

```text
[PERSONA]
Você é um médico cardiologista sênior com especialização em diretrizes clínicas internacionais (AHA/SBC). Avalie a conduta clínica proposta por um sistema de IA.

[CONTEXTO]
Pergunta/Caso Clínico: {pergunta_medica}
Resposta de Referência (Gold Standard): {resposta_ouro}
Resposta da IA a ser avaliada: {resposta_modelo_edge}

[RUBRICA DE AVALIAÇÃO]
- Nota 1: ERRO CRÍTICO. Recomenda conduta perigosa, dosagem letal ou ignora sinais vitais clássicos.
- Nota 2: Resposta tecnicamente correta na conclusão, mas omite passos vitais de segurança ou exames obrigatórios.
- Nota 3: Resposta correta, alinhada à conduta padrão, mas carece de detalhes sobre manejo a longo prazo.
- Nota 4: Resposta muito boa, seguindo as diretrizes clínicas e demonstrando bom raciocínio fisiopatológico.
- Nota 5: Resposta perfeita, idêntica ou superior ao Gold Standard em clareza e precisão farmacológica.

[INSTRUÇÕES DE SAÍDA]
Seja rigoroso. Se houver erro de medicação ou diagnóstico diferencial, a nota deve ser 1 ou 2, independentemente da qualidade da escrita.
Forneça o veredito no formato:
REASONING: <justificativa técnica detalhada>
SCORE: <apenas o número de 1 a 5>
```

## Dicas adicionais para as equipes

1. **Língua do Juiz:** se vocês utilizarem o Llama-3-70B ou GPT-4o, o Juiz funciona bem em português para o Direito. No entanto, para o domínio médico, K-QA, recomenda-se manter o prompt do juiz em inglês, pois a maior parte do treinamento científico desses modelos ocorre nesse idioma, reduzindo erros de interpretação.
2. **Amostragem:** como vocês têm equipes de 6 a 7 pessoas, cada membro pode auditar manualmente 20 avaliações feitas pelo Juiz-IA para verificar se ele está sendo justo. Isso é o que chamamos de Meta-Avaliação.
3. **Parsing:** usem o comando `split("NOTA:")[1].strip()` no Python para capturar apenas o número e transformar em um dado quantitativo para o relatório final.

Com esses templates, as equipes já podem carregar seus arquivos JSON/CSV da Atividade 1 e iniciar o processo de julgamento.

## Como o PostgreSQL apoia a análise de correlação estatística

Para entender como o banco de dados PostgreSQL suporta a análise de correlação estatística, precisamos visualizar o banco não apenas como um depósito, mas como um motor que alinha duas perspectivas diferentes sobre a mesma pergunta.

A correlação, aqui, mede o quanto o Juiz-IA concorda com o gabarito humano, isto é, com a resposta ouro. Se o Juiz dá nota 5 sempre que o modelo acerta o gabarito, e nota 1 sempre que ele erra, temos uma correlação perfeita.

### 1. A conexão estrutural: o JOIN da verdade

O esquema relacional permite que você extraia, em uma única linha de tabela, o que o humano disse que é certo e o que a IA julgou. O segredo está na rastreabilidade das chaves estrangeiras:

- `perguntas.resposta_ouro`: o que o humano definiu como verdade.
- `avaliacoes_juiz.nota_atribuida`: o que o Juiz-IA definiu como qualidade.

### 2. Mecânica da correlação com exemplos

#### Cenário A: questões de múltipla escolha (OAB / USMLE)

Neste caso, a correlação é binária no lado humano: certo ou errado.

1. **Dado do banco:** `id_pergunta: 101`, `resposta_ouro: "A"`.
2. **Resposta à Atividade 1:** o modelo gerou um texto longo que termina em: "Portanto, a opção correta é A".
3. **Avaliação do Juiz:** leu o texto e deu nota 5.
4. **Análise:** aqui, convertemos o gabarito humano para 5, pois o modelo acertou. Como o Juiz também deu 5, a correlação é alta.

#### Cenário B: questões abertas (K-QA / médicas)

Aqui a correlação é mais sutil, comparando a distância entre as opiniões.

| ID pergunta | Resposta ouro (humano) | Resposta modelo (Atividade 1) | Nota do Juiz (Atividade 2) | Realidade técnica |
|---:|---|---|---:|---|
| 50 | Prescrever 5 mg de varfarina | Sugeriu 50 mg de varfarina | 1 | O juiz detectou erro fatal |
| 51 | Repouso e hidratação | Sugeriu beber muita água | 4 | O juiz aceitou a paráfrase |

### 3. O cálculo matemático: correlação de Spearman

Como as notas do Juiz, de 1 a 5, são dados ordinais, ou seja, possuem uma ordem, mas não necessariamente uma distância matemática exata entre elas, a métrica ideal que as equipes devem usar é o coeficiente de correlação de Spearman ($\rho$).

A fórmula que o script Python da equipe executará após puxar os dados do Postgres é:

$$
\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}
$$

Onde:

- $d_i$: diferença entre a nota do Juiz e a nota do gabarito humano para cada pergunta.
- $n$: número total de questões avaliadas.

### 4. Exemplo de implementação via query e Python

As equipes utilizarão o PostgreSQL para preparar o terreno e o Python para o cálculo final:

```python
import pandas as pd
from scipy.stats import spearmanr
import psycopg2

# 1. Extração dos dados via SQL
query = """
SELECT p.resposta_ouro, r.texto_resposta, a.nota_atribuida
FROM avaliacoes_juiz a
JOIN respostas_atividade_1 r ON a.id_resposta_ativa1 = r.id_resposta
JOIN perguntas p ON r.id_pergunta = p.id_pergunta;
"""

df = pd.read_sql(query, conn)

# 2. Transformação: converter gabarito em nota 1 ou 5 para comparar.
# Se o modelo acertou a letra do gabarito, ganha 5, senão 1.
df['nota_humana'] = df.apply(
    lambda x: 5 if x['resposta_ouro'] in x['texto_resposta'] else 1,
    axis=1,
)

# 3. O cálculo da correlação
correlation, p_value = spearmanr(df['nota_humana'], df['nota_atribuida'])

print(f"A correlação entre o Juiz e o Gabarito é: {correlation:.2f}")
```

O que o resultado diz para a equipe:

- $\rho \approx 1.0$: o Juiz de vocês é perfeito e substitui o humano.
- $\rho \approx 0.0$: o Juiz está dando notas aleatórias, indicando prompt ruim.
- $\rho < 0$: o Juiz está confuso, dando notas altas para respostas erradas.

# Guia de execução final para as equipes

## 1. O fluxo de dados no PostgreSQL

O sucesso da atividade depende de o banco de dados refletir fielmente o experimento. Certifiquem-se de que a tabela `avaliacoes_juiz` esteja populada não apenas com a nota, mas com o Chain-of-Thought. É esse texto explicativo que permitirá auditar se o Juiz está alucinando ou sendo rigoroso.

## 2. Cálculo da correlação na prática

Lembrem-se: a correlação de Spearman varia de -1 a 1.

- **0.7 a 1.0:** forte alinhamento. O juiz pensa como o gabarito humano.
- **0.3 a 0.6:** alinhamento moderado. Talvez a rubrica precise ser mais específica.
- **Abaixo de 0.3:** o Juiz e o humano estão discordando frontalmente. Isso é um achado científico valioso. Expliquem o porquê no relatório, por exemplo, se o Juiz é atualizado demais para um gabarito antigo ou vice-versa.

## 3. Checklist para o backup do banco (`.sql`)

Antes de gerar o arquivo `.sql` para entrega no GitHub, verifiquem:

- [ ] O banco contém os dados de todos os membros da equipe?
- [ ] As chaves estrangeiras estão preservadas?
- [ ] O arquivo de backup inclui o comando `CREATE TABLE`, ou vocês forneceram o script DDL separadamente?
- [ ] As instruções de restore no tutorial foram testadas em um computador limpo?

## Dicas para o vídeo de 10 a 20 minutos

Como vocês são 6 ou 7 alunos, a organização é chave. Sugestão de divisão de tempo:

1. **Intro (2 min):** apresentação da equipe e escolha do Modelo Juiz.
2. **Dados e SQL (4 min):** demonstração do esquema no Postgres e uma query de agregação funcionando.
3. **Rubricas e prompts (4 min):** explicação da lógica de avaliação, incluindo por que nota 1 e por que nota 5.
4. **Resultados e estatística (6 min):** apresentação dos gráficos de correlação e análise de casos onde o Juiz falhou.
5. **Conclusão (4 min):** lições aprendidas sobre o paradigma LLM-as-a-Judge.

# Barema de excelência

Sugere-se que as equipes não busquem apenas a correlação alta. Deve ser dada importância à análise de erros. Se o Juiz deu nota 5 para uma resposta medicamente perigosa, e vocês conseguiram identificar isso através de uma query SQL e propor um ajuste na rubrica, isso demonstra que a equipe está atendendo ao objetivo da atividade.

> **Lembrete final:** a entrega é dia 14 de maio, quinta-feira, até o meio-dia. Não deixem o `pg_dump` para a última hora.
