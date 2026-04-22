Português | [English](./README-EN.md)

<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/1/1c/Ufs_principal_positiva-nova.png" alt="ufs-logo" width="20%">

<h1>Tópicos Avançados ES e SI</h1>

<p>Atividade avaliativa 2: Implementação de framework "LLM-as-a-Judge" e persistência em banco de dados relacional</p>

<p align="center">
  <!-- Python version -->
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue.svg" alt="Python 3.12+">
  <!-- PostgreSQL -->
  <img src="https://img.shields.io/badge/PostgreSQL-17-336791.svg?logo=postgresql&logoColor=white" alt="PostgreSQL 17">
  <!-- License -->
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="Licença MIT">
  </a>
  <!-- Last commit -->
  <a href="https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2/commits/main">
    <img src="https://img.shields.io/github/last-commit/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2.svg" alt="Último commit">
  </a>
  <!-- Stars -->
  <a href="https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2/stargazers">
    <img src="https://img.shields.io/github/stars/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2.svg?style=social" alt="Stars">
  </a>
</p>

</div>

<details>
<summary>Sumário (Clique para expandir)</summary>

- [Sobre](#sobre)
- [Apresentação](#apresentação)
- [Colaboradores](#colaboradores)
- [Arquitetura do banco de dados](#arquitetura-do-banco-de-dados)
- [Instruções de execução](#instruções-de-execução)
  - [Pré-requisitos](#pré-requisitos)
  - [Restore do banco de dados](#restore-do-banco-de-dados)
- [Contribuições](#contribuições)
- [Licença](#licença)
- [Referências](#referências)

</details>

## Sobre

Este repositório contém as contribuições individuais do aluno **Reinan Gabriel** para a segunda atividade avaliativa da disciplina **Tópicos Avançados em Engenharia de Software e Sistemas de Informação I** (UFS 2026.1).

O projeto dá continuidade à [Atividade 1](https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1), avançando da inferência básica para uma avaliação estruturada das respostas dos modelos. As frentes principais são:

- **LLM-as-a-Judge:** implementação de um pipeline de julgamento automatizado com rubricas jurídicas (escala 1–5), extração de Chain-of-Thought e uso de modelos juízes para auditar acurácia técnica e fundamentação legal.
- **Persistência em PostgreSQL:** modelagem e implementação de um banco de dados relacional para armazenar o ciclo completo do experimento com datasets, respostas dos modelos candidatos e avaliações do juiz.
- **Análise estatística:** cálculo da correlação de Spearman entre as notas do Juiz-IA e o gabarito humano, com análise de erros e discussão dos resultados.

## Apresentação

> **Em breve.** O link do vídeo de apresentação (10–20 min) será adicionado aqui após a gravação.

O vídeo a seguir mostra os resultados coletados pela equipe para a segunda atividade avaliativa:

[![Vídeo no YouTube](https://gitlab.com/reinanhs/repo-slide-presentation/-/wikis/uploads/7cc03556931898d62b45b84b5006d119/image.png)](https://youtu.be/dQw4w9WgXcQ)

- **Assista ao vídeo completo:** [https://youtu.be/dQw4w9WgXcQ](https://youtu.be/dQw4w9WgXcQ)

## Colaboradores

<div align="center">
<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/ReinanHS">
        <img src="https://github.com/reinanhs.png" height="64" width="64" alt="Reinan Gabriel"/>
      </a><br/>
      <a href="https://github.com/ReinanHS">Reinan Gabriel</a>
    </td>
  </tr>
</table>
</div>

---

## Arquitetura do banco de dados

O esquema relacional segue a estrutura sugerida pelo professor, com cinco tabelas principais:

- [Acesse o link para visualizar o diagrama detalhado no DBDiagram.io](https://dbdiagram.io/d/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade2-69e940f2d80a958d1cb60703)

<img src="docs/assets/arquitetura-do-banco-de-dados.svg" alt="Diagrama de entidade-relacionamento" width="100%">

---

## Instruções de execução

### Pré-requisitos

| Requisito | Versão mínima | Descrição |
|-----------|---------------|-----------|
| [Python](https://www.python.org/downloads/) | 3.12+ | Linguagem principal do projeto |
| [PostgreSQL](https://www.postgresql.org/download/) | 15+ | Banco de dados relacional |
| [Git](https://git-scm.com/install) | 2.x | Controle de versão |

### Restore do banco de dados

Para recriar o ambiente de dados localmente a partir do backup:

```bash
TODO: Instruções detalhadas de restore serão incluídas
```

---

## Contribuições

Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

Este projeto utiliza a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para os termos completos.

## Referências

- [Atividade 1: Repositório da Equipe JUD_3](https://github.com/ReinanHS/Topicos_Avancados_2026_1_Equipe_JUD_3_atividade1)
- [OAB Bench](https://huggingface.co/datasets/maritaca-ai/oab-bench)
- [OAB Exams](https://huggingface.co/datasets/eduagarcia/oab_exams)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [LLM Evaluation: A Comprehensive Survey](https://arxiv.org/html/2504.21202v1)
- [SciPy: spearmanr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html)

---

<div align="center">
  <sub>Desenvolvido pela Equipe 3 (Domínio Jurídico) | UFS 2026.1</sub>
</div>
