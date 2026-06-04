# Curadoria dos documentos externos

## Critérios de inclusão dos documentos

A curadoria dos documentos externos priorizou a qualidade e a pertinência das fontes utilizadas no RAG. Assim, foram selecionados apenas documentos com relação direta com as questões analisadas, evitando a inserção de conteúdos genéricos ou pouco relevantes na base vetorial.

Os principais critérios de inclusão foram:

1. uso de fontes oficiais ou institucionalmente reconhecidas;
2. relação direta com o enunciado da questão;
3. capacidade do documento de fundamentar juridicamente a resposta correta;
4. análise da temporalidade do documento em relação ao lançamento dos modelos avaliados.

As buscas e coletas dos documentos foram realizadas em fontes jurídicas oficiais ou consolidadas, conforme apresentado na tabela a seguir.

## Questões avaliadas e arquivos presentes na base de conhecimento do RAG

| Questão                                    | Área                   | Tipo              | Status informado | Arquivo/documento associado                          | Situação para o RAG                                                              |
| ------------------------------------------ | ---------------------- | ----------------- | ---------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| `44_direito_administrativo_questao_1`      | Direito Administrativo | Questão           | Presente         | `L14133` — Lei nº 14.133/2021                        | Documento presente na base                                                       |
| `44_direito_administrativo_questao_2`      | Direito Administrativo | Questão           | Pendente         | Não identificado no texto                            | Necessário localizar/incluir documento                                           |
| `44_direito_administrativo_questao_3`      | Direito Administrativo | Questão           | Presente         | `L8429compilada` — Lei nº 8.429/1992                 | Documento presente na base                                                       |
| `44_direito_administrativo_questao_4`      | Direito Administrativo | Questão           | Presente         | `L13869` — Lei nº 13.869/2019                        | Documento presente na base                                                       |
| `44_direito_civil_peca_profissional`       | Direito Civil          | Peça profissional | Presente         | `L8078compilado` — Código de Defesa do Consumidor    | Documento presente na base                                                       |
| `44_direito_civil_questao_1`               | Direito Civil          | Questão           | Presente         | `L10406compilada` — Código Civil de 2002             | Documento presente na base                                                       |
| `44_direito_civil_questao_2`               | Direito Civil          | Questão           | Pendente         | `L13105compilada` — Código de Processo Civil de 2015 | O texto menciona documento associado, mas a lista marca como pendente; verificar |
| `44_direito_civil_questao_3`               | Direito Civil          | Questão           | Pendente         | `L13105compilada` — Código de Processo Civil de 2015 | O texto menciona documento associado, mas a lista marca como pendente; verificar |
| `44_direito_civil_questao_4`               | Direito Civil          | Questão           | Presente         | `L13146` — Lei nº 13.146/2015                        | Documento presente na base                                                       |
| `44_direito_do_trabalho_peca_profissional` | Direito do Trabalho    | Peça profissional | Presente         | `DEL5452` — Consolidação das Leis do Trabalho        | Documento presente na base                                                       |
| `44_direito_do_trabalho_questao_1`         | Direito do Trabalho    | Questão           | Pendente         | Não identificado no texto                            | Necessário localizar/incluir documento                                           |
| `44_direito_do_trabalho_questao_2`         | Direito do Trabalho    | Questão           | Presente         | `Constituicao` — Constituição Federal de 1988 e ADCT | Documento presente na base                                                       |

## Fontes utilizadas na curadoria dos documentos externos

| Fonte                                   | Endereço                                                            | Justificativa de uso                                                                                                                                                                                                                                        |
| --------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Legislação Federal — Planalto           | https://www4.planalto.gov.br/legislacao                             | Fonte principal para consulta de normas oficiais, como a Constituição Federal, códigos, estatutos e leis especiais. Sua utilização permite que o RAG recupere textos legais autênticos e diretamente relacionados às questões.                              |
| Súmulas Vinculantes do STF              | https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=26 | Relevantes para questões que exigem entendimento consolidado e obrigatório do STF, pois possuem efeito vinculante para o Poder Judiciário e a Administração Pública.                                                                                        |
| Súmulas não vinculantes do STF          | https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=30 | Utilizadas como orientação jurisprudencial consolidada do STF. Embora não tenham caráter obrigatório, auxiliam na fundamentação de respostas baseadas na interpretação predominante do Tribunal.                                                            |
| Informativos do STJ                     | https://scon.stj.jus.br/jurisprudencia/externo/informativo/         | Incluídos por reunirem entendimentos recentes do STJ. Essa fonte é especialmente importante para tratar o fator de temporalidade, pois ajuda a identificar atualizações jurisprudenciais que podem não estar presentes no conhecimento interno dos modelos. |
| Jurisprudência do STJ — Pesquisa Pronta | https://scon.stj.jus.br/SCON/pesquisa_pronta/listaPP.jsp            | Utilizada para localizar entendimentos organizados por temas jurídicos. Essa fonte facilita a seleção de documentos com pertinência direta ao enunciado das questões e contribui para reduzir respostas genéricas ou sem base jurisprudencial.              |

Além da origem dos documentos, também foi considerada a data de lançamento dos modelos avaliados. Essa análise é importante porque documentos posteriores ao lançamento dos modelos podem representar informações que não estavam disponíveis em seus pesos internos, enquanto documentos anteriores ainda podem contribuir para reduzir alucinações e ancorar as respostas em fontes oficiais.

## Modelos avaliados e datas de lançamento oficial

| # | Modelo       | Desenvolvedor | Parâmetros | Lançamento             |
| - | ------------ | ------------- | ---------- | ---------------------- |
| 1 | Llama 3.2 3B | Meta          | 3,21B      | 25 de setembro de 2024 |
| 2 | Gemma 2 2B   | Google        | 2,61B      | 31 de julho de 2024    |
| 3 | Qwen 2.5 3B  | Alibaba Cloud | 3,09B      | 19 de setembro de 2024 |

Conforme apresentado na tabela, todos os modelos avaliados foram lançados em 2024. Portanto, documentos jurídicos posteriores a essas datas foram considerados importantes para avaliar o possível ganho temporal do RAG. Já os documentos anteriores foram mantidos quando apresentavam valor fático, isto é, quando ajudavam a fundamentar corretamente a resposta e a reduzir erros de interpretação, citação normativa ou alucinação.

## Lei nº 14.133/2021 — curadoria de Reinan

**Arquivo:** `L14133`
**Fonte:** https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm
**Questão relacionada:** `44_direito_administrativo_questao_1`

### Justificativa de inclusão

O arquivo `L14133` foi incluído porque a questão de ID `44_direito_administrativo_questao_1` aborda um contrato administrativo de reforma de edifício público regido pela Lei nº 14.133/2021.

O enunciado envolve dois pontos centrais:

* a possibilidade de alteração unilateral quantitativa pela Administração;
* o direito ao ressarcimento de materiais já adquiridos.

Dessa forma, os dispositivos selecionados da norma oferecem a base legal necessária para a análise da questão:

* **Art. 124:** justifica a possibilidade de a Administração alterar unilateralmente o contrato quando houver necessidade de modificação do projeto. Esse dispositivo serve como base para a análise do item A, pois trata da prerrogativa administrativa de promover esse tipo de alteração.

* **Art. 125:** define os limites aplicáveis às alterações unilaterais do contrato. No caso analisado, esse artigo é essencial para o item A, pois estabelece o limite de 25% para acréscimos ou supressões e admite o limite de 50% apenas para acréscimos em contratos de reforma. Assim, como a supressão foi de 20%, ela permaneceu dentro do limite legal de 25%, sendo considerada regular. A distinção entre supressão e acréscimo é decisiva, já que o limite de 50% não se aplica à supressão.

* **Art. 129:** fundamenta a resposta ao item B, pois trata dos efeitos da supressão contratual sobre materiais já adquiridos. De acordo com esse dispositivo, os materiais comprados e colocados no local da obra devem ser pagos pela Administração, desde que o custo de aquisição seja comprovado e devidamente reajustado.

### Temporalidade

A norma é de 01/04/2021, portanto anterior ao lançamento dos modelos analisados: Gemma 2 2B, Qwen 2.5 3B e Llama 3.2 3B, todos de 2024.

Assim, neste caso, o ganho proporcionado pelo RAG não está relacionado à atualização temporal da informação, e sim ao apoio fático e à redução de alucinações, ao ancorar a resposta no texto literal da norma e nos percentuais corretos. Embora o enunciado situe os fatos em janeiro de 2025, a norma aplicável continua sendo a Lei nº 14.133/2021, publicada em 2021.

## Lei nº 8.429/1992 — curadoria de Reinan

**Arquivo:** `L8429compilada`
**Fonte:** https://www.planalto.gov.br/ccivil_03/leis/l8429compilada.htm
**Questão relacionada:** `44_direito_administrativo_questao_3`

### Justificativa de inclusão

O arquivo `L8429compilada` foi incluído porque a questão de ID `44_direito_administrativo_questao_3` trata da responsabilização de pessoa jurídica por ato de improbidade administrativa, com fundamento na Lei nº 8.429/1992.

O enunciado envolve dois pontos centrais:

* a possibilidade de responsabilizar a sociedade empresária Bomcaminho independentemente da imputação de ato de improbidade ao deputado José;
* os limites da responsabilidade da sucessora em caso de fusão ou incorporação, quando não houver simulação ou fraude.

Dessa forma, os dispositivos selecionados da norma oferecem a base legal necessária para a análise da questão:

* **Art. 1º:** fundamenta que os atos de improbidade administrativa dependem de conduta dolosa e que o dolo exige vontade livre e consciente de alcançar o resultado ilícito previsto na lei. Esse dispositivo se conecta ao enunciado porque a questão informa a existência de dolo específico na conduta narrada.

* **Art. 3º:** estabelece que as disposições da Lei de Improbidade Administrativa também se aplicam, no que couber, a quem, mesmo não sendo agente público, induza ou concorra dolosamente para a prática do ato de improbidade. Esse dispositivo fundamenta o item A, pois permite analisar a responsabilização da sociedade empresária Bomcaminho como terceira envolvida na prática do ato.

### Temporalidade

Tanto a norma original quanto a alteração legislativa são anteriores ao lançamento dos modelos Gemma 2 2B, Qwen 2.5 3B e Llama 3.2 3B, todos de 2024.

Assim, o ganho do RAG neste caso não é temporal, mas fático e anti-alucinação, pois permite ancorar a resposta na redação atualizada da Lei de Improbidade Administrativa e evitar erros sobre a responsabilização da pessoa jurídica e os limites da responsabilidade da sucessora.

## Lei nº 13.869/2019 — curadoria de Reinan

**Arquivo:** `L13869`
**Fonte:** https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13869.htm
**Questão relacionada:** `44_direito_administrativo_questao_4`

### Justificativa de inclusão

O arquivo `L13869` foi incluído porque a questão de ID `44_direito_administrativo_questao_4` trata da responsabilização administrativa disciplinar de guarda municipal por conduta tipificada como abuso de autoridade.

O enunciado envolve dois pontos centrais:

* verificar se a aplicação de sanção administrativa depende de condenação criminal pelo mesmo fato;
* analisar se a sentença penal irrecorrível que reconhece o estrito cumprimento do dever legal produz efeitos no âmbito administrativo disciplinar.

Dessa forma, os dispositivos selecionados da norma oferecem a base legal necessária para a análise da questão:

* **Art. 6º:** fundamenta o item A, pois estabelece que as penas previstas na Lei de Abuso de Autoridade são aplicadas independentemente das sanções civis ou administrativas cabíveis. Assim, a responsabilização administrativa disciplinar de José não depende, por si só, de prévia condenação criminal pelo mesmo fato.

* **Art. 8º:** fundamenta diretamente o item B, pois estabelece que faz coisa julgada no âmbito cível e administrativo-disciplinar a sentença penal que reconhece que o ato foi praticado em estrito cumprimento do dever legal. Portanto, se a sentença penal irrecorrível reconhecer essa causa de exclusão, tal conclusão deverá ser observada no processo administrativo disciplinar.

### Temporalidade

A Lei nº 13.869/2019 é de 05/09/2019, portanto anterior ao lançamento dos modelos Gemma 2 2B, Qwen 2.5 3B e Llama 3.2 3B, todos de 2024.

Assim, o ganho do RAG neste caso não é temporal, mas fático e anti-alucinação, pois permite ancorar a resposta nos dispositivos corretos da Lei de Abuso de Autoridade, especialmente quanto à independência entre as instâncias e aos efeitos da sentença penal no âmbito administrativo-disciplinar.

## Código de Defesa do Consumidor — curadoria de Reinan

**Arquivo:** `L8078compilado`
**Fonte:** https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm
**Questão relacionada:** `44_direito_civil_peca_profissional`

### Justificativa de inclusão

O arquivo `L8078compilado` foi incluído porque a questão de ID `44_direito_civil_peca_profissional` envolve relação de consumo entre Caroline, a agência de viagens e a companhia aérea Bons Voos S.A.

O enunciado exige enfrentar:

* a legitimidade da companhia aérea;
* a obrigatoriedade da promoção ofertada;
* a falha na prestação do serviço.

Dessa forma, os dispositivos selecionados do Código de Defesa do Consumidor oferecem a base material necessária para sustentar a pretensão da autora:

* **Arts. 2º e 3º:** fundamentam a existência de relação de consumo, identificando Caroline como consumidora e a companhia aérea como fornecedora de serviço de transporte aéreo.

* **Art. 6º, VI:** fundamenta o pedido de reparação pelos danos sofridos, incluindo o dano moral decorrente da perda do tempo útil na tentativa frustrada de resolver administrativamente o problema.

### Temporalidade

O Código de Defesa do Consumidor é de 11/09/1990, portanto anterior ao lançamento dos modelos Gemma 2 2B, Qwen 2.5 3B e Llama 3.2 3B, todos de 2024.

Assim, o ganho do RAG neste caso não é temporal, mas fático e anti-alucinação, pois permite ancorar a resposta nos dispositivos corretos sobre relação de consumo, vinculação da oferta, responsabilidade do fornecedor e cumprimento forçado da promoção.

## Código Civil de 2002 — curadoria de Reinan

**Arquivo:** `L10406compilada`
**Fonte:** https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm
**Questão relacionada:** `44_direito_civil_questao_1`

### Justificativa de inclusão

O arquivo `L10406compilada` foi incluído porque a questão de ID `44_direito_civil_questao_1` trata dos efeitos do regime de comunhão parcial de bens sobre automóvel recebido por herança pelo executado Fabiano.

O enunciado exige verificar se Maria, esposa de Fabiano, possui direito à comunicação patrimonial sobre o bem penhorado. Dessa forma, os dispositivos selecionados do Código Civil oferecem a base legal necessária para a análise do item A:

* **Art. 1.658:** estabelece a regra geral do regime de comunhão parcial, segundo a qual se comunicam os bens adquiridos na constância do casamento, ressalvadas as exceções previstas em lei. Esse dispositivo é útil para contextualizar o regime patrimonial do casamento de Maria e Fabiano.

* **Art. 1.659, I:** fundamenta diretamente o item A, pois exclui da comunhão os bens que sobrevierem a cada cônjuge por sucessão, bem como os sub-rogados em seu lugar. Assim, como o automóvel penhorado foi recebido por Fabiano em razão de herança, ele não se comunica com Maria no regime de comunhão parcial de bens.

### Temporalidade

O Código Civil é de 10/01/2002, portanto anterior ao lançamento dos modelos Gemma 2 2B, Qwen 2.5 3B e Llama 3.2 3B, todos de 2024.

Assim, o ganho do RAG neste caso não é temporal, mas fático e anti-alucinação, pois permite ancorar a resposta na regra correta sobre exclusão dos bens recebidos por sucessão no regime de comunhão parcial.

## Código de Processo Civil de 2015 — curadoria de Reinan

**Arquivo:** `L13105compilada`
**Fonte:** https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105compilada.htm
**Questões relacionadas:** `44_direito_civil_questao_2` e `44_direito_civil_questao_3`

### Justificativa de inclusão

O arquivo `L13105compilada` foi incluído porque foi utilizado em mais de uma questão de Direito Civil com conteúdo processual.

Na questão de ID `44_direito_civil_questao_2`, o Código de Processo Civil fundamenta a possibilidade de intervenção da seguradora no processo por meio da denunciação da lide.

Já na questão de ID `44_direito_civil_questao_3`, a norma fundamenta o recurso cabível contra a decisão que rejeitou os embargos monitórios.

Dessa forma, os dispositivos selecionados oferecem a base processual necessária para ambas as análises:

* **Art. 125, II:** fundamenta a questão `44_direito_civil_questao_2`, pois admite a denunciação da lide àquele que, por lei ou contrato, esteja obrigado a indenizar a parte que vier a perder a demanda. No caso, esse dispositivo permite chamar a seguradora ao processo, em razão do contrato de seguro firmado por Maria.

* **Art. 702, § 9º:** fundamenta a questão `44_direito_civil_questao_3`, pois prevê o cabimento de apelação contra a sentença que acolhe ou rejeita os embargos monitórios. Assim, diante da rejeição dos embargos apresentados pela Suinocultura Ltda., o recurso cabível é a apelação.

### Temporalidade

O Código de Processo Civil é de 16/03/2015, portanto anterior ao lançamento dos modelos Gemma 2 2B, Qwen 2.5 3B e Llama 3.2 3B, todos de 2024.

Assim, o ganho do RAG neste caso não é temporal, mas fático e anti-alucinação, pois permite ancorar as respostas nos dispositivos processuais corretos sobre denunciação da lide e embargos monitórios.

> **Observação:** apesar de o texto indicar o uso do Código de Processo Civil para as questões `44_direito_civil_questao_2` e `44_direito_civil_questao_3`, a lista de controle marca essas duas questões como pendentes. Recomenda-se verificar se o arquivo já foi efetivamente inserido na base vetorial do RAG.

## Lei nº 13.146/2015 — curadoria de Reinan

**Arquivo:** `L13146`
**Fonte:** https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm
**Questão relacionada:** `44_direito_civil_questao_4`

### Justificativa de inclusão

O arquivo `L13146` foi incluído porque a questão de ID `44_direito_civil_questao_4` trata da possibilidade de decretação de curatela de pessoa maior de idade diagnosticada com Transtorno do Espectro Autista (TEA).

O enunciado informa que o laudo médico reconhece que Thomaz tem discernimento necessário para gerir seu patrimônio, mas, ainda assim, a curatela foi deferida com base na existência de deficiência.

Dessa forma, os dispositivos selecionados do Estatuto da Pessoa com Deficiência oferecem a base legal necessária para a análise do item A:

* **Art. 6º:** fundamenta que a deficiência não afeta, por si só, a plena capacidade civil da pessoa. Esse dispositivo é central para o item A, pois demonstra que o diagnóstico de TEA, isoladamente, não autoriza a decretação da curatela de Thomaz.

* **Art. 84:** reforça que a pessoa com deficiência tem assegurado o direito ao exercício de sua capacidade legal em igualdade de condições com as demais pessoas. Esse dispositivo também estabelece que a curatela somente deve ser adotada quando necessária, o que não foi demonstrado no caso narrado, especialmente diante do laudo que reconheceu o discernimento de Thomaz.

* **Art. 85:** delimita a curatela aos atos relacionados aos direitos de natureza patrimonial e negocial. Esse dispositivo é relevante porque mostra que a curatela não pode ser decretada de forma automática ou ampla apenas em razão do diagnóstico de deficiência, devendo observar a necessidade concreta e a proporcionalidade da medida.

### Temporalidade

A Lei nº 13.146/2015 é de 06/07/2015, portanto anterior ao lançamento dos modelos Gemma 2 2B, Qwen 2.5 3B e Llama 3.2 3B, todos de 2024.

Assim, o ganho do RAG neste caso não é temporal, mas fático e anti-alucinação, pois permite ancorar a resposta na regra correta de que a deficiência não retira automaticamente a capacidade civil e de que a curatela é medida excepcional.

## Consolidação das Leis do Trabalho — curadoria de Reinan

**Arquivo:** `DEL5452`
**Fonte:** https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452compilado.htm
**Questão relacionada:** `44_direito_do_trabalho_peca_profissional`

### Justificativa de inclusão

O arquivo `DEL5452` foi incluído porque a questão de ID `44_direito_do_trabalho_peca_profissional` exige a elaboração da peça processual adequada para a defesa de uma empresa fictícia e de seus sócios em uma reclamação trabalhista.

Por esse motivo, o documento reúne informações relevantes sobre a Consolidação das Leis do Trabalho, de modo a fornecer uma base consistente para a elaboração dessa peça processual.

### Temporalidade

A Consolidação das Leis do Trabalho é de 01/05/1943, mas os dispositivos atualmente aplicáveis foram considerados em sua versão compilada e vigente.

A norma é anterior ao lançamento dos modelos Gemma 2 2B, Qwen 2.5 3B e Llama 3.2 3B, todos de 2024.

Assim, o ganho do RAG neste caso não é temporal, mas fático e anti-alucinação, pois permite ancorar a defesa nos dispositivos trabalhistas corretos sobre contestação, prescrição, sócios, norma coletiva, aviso prévio, periculosidade, perícia, honorários e ônus da prova.

## Constituição Federal de 1988 e ADCT — curadoria de Reinan

**Arquivo:** `Constituicao`
**Fonte:** https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm
**Questão relacionada:** `44_direito_do_trabalho_questao_2`

### Justificativa de inclusão

O arquivo `Constituicao` foi incluído porque a questão de ID `44_direito_do_trabalho_questao_2` trata do direito à estabilidade gestante após dispensa imotivada ocorrida durante a gravidez.

O enunciado informa que Lúcia engravidou no curso do contrato de trabalho, mas foi dispensada sem que ela ou o empregador soubessem da gestação.

Dessa forma, o dispositivo selecionado do Ato das Disposições Constitucionais Transitórias oferece a base constitucional necessária para a análise do item A:

* **Art. 10, II, b, do ADCT:** fundamenta diretamente o item A, pois veda a dispensa arbitrária ou sem justa causa da empregada gestante desde a confirmação da gravidez até cinco meses após o parto. Esse dispositivo permite sustentar que o direito à estabilidade decorre do fato objetivo de a gravidez ter ocorrido durante o contrato de trabalho, e não do conhecimento prévio do empregador sobre o estado gestacional da empregada.

### Temporalidade

A Constituição Federal é de 05/10/1988, portanto anterior ao lançamento dos modelos Gemma 2 2B, Qwen 2.5 3B e Llama 3.2 3B, todos de 2024.

Assim, o ganho do RAG neste caso não é temporal, mas fático e anti-alucinação, pois permite ancorar a resposta no fundamento constitucional correto da estabilidade gestante e evitar o erro de condicionar o direito ao conhecimento prévio do empregador.
