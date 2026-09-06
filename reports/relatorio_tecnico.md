# Relatório técnico — Tech Challenge Fase 3

**Aluno:** Lucas Lourenço  
**RM:** 371753

## 1. Objetivo

Construir uma solução analítica e preditiva para alfabetização no Brasil a partir das camadas Silver e Gold da Fase 2. A entrega contém dois modelos complementares:

1. **Modelo individual:** classificação de aluno alfabetizado/não alfabetizado.
2. **Modelo municipal:** probabilidade de um município ficar abaixo da meta de alfabetização no ano seguinte.

## 2. Bases

Foram utilizados os cinco CSVs exportados do BigQuery: Silver de alunos e quatro tabelas Gold (indicadores, metas, comparação e evolução).

A exportação Silver fornecida possui **62,767 registros**, enquanto a documentação da Fase 2 registra processamento de aproximadamente 3,87 milhões de registros. Portanto, os resultados do modelo individual devem ser interpretados como resultados da **exportação/amostra disponibilizada**, não como reprodução integral do universo processado na Fase 2.

## 3. Data leakage

A principal decisão metodológica foi excluir `proficiencia`. Na população avaliada, a variável `alfabetizado` coincide em **100.0%** dos registros com a regra `proficiencia >= 743`, logo usar proficiência como entrada entregaria a resposta ao modelo.

`presenca` e `preenchimento_caderno` também não são usadas como features. Elas são usadas apenas para restringir o modelo aos alunos efetivamente avaliados, pois alunos ausentes ou sem caderno preenchido aparecem sem proficiência e com classe 0 na exportação.

## 4. Modelo individual

A modelagem considera alunos de 2024 efetivamente avaliados e usa informações históricas de 2023 e metas previamente definidas. A separação treino/teste foi feita por município (`GroupShuffleSplit`), reduzindo o risco de o modelo memorizar o mesmo contexto municipal nos dois conjuntos.

**Modelo final:** HistGradientBoosting otimizado por GridSearchCV com GroupKFold.

- Accuracy: **0.650**
- Precision: **0.663**
- Recall: **0.781**
- F1-score: **0.717**
- ROC-AUC: **0.697**

As variáveis com maior importância por permutação foram: **media_portugues_2023_publica, uf, taxa_alfabetizacao_2023_publica**.

## 5. Modelo de risco municipal

O alvo é `Abaixo da meta` em 2024. O modelo recebe apenas variáveis conhecidas antes do resultado de 2024: desempenho de 2023, meta de 2024, gap histórico, UF e região.

**Modelo final:** Regressão Logística otimizada por validação cruzada.

- Accuracy: **0.708**
- Precision: **0.688**
- Recall: **0.685**
- F1-score: **0.686**
- ROC-AUC: **0.789**

Em 2024, a base registra **2,444 municípios abaixo da meta** e **2,788 com meta atingida**.

Ao reaplicar o modelo para 2025, usando desempenho de 2024 e metas de 2025, **2,911 de 5,352 municípios** são classificados como risco >= 50% de ficar abaixo da meta. Essa projeção é um sinal de priorização, não uma previsão causal.

A região com maior probabilidade média prevista é **Sul (71.9%)** e a menor é **Centro-Oeste (29.7%)**.

## 6. Perfis municipais

Foi aplicada uma clusterização exploratória K-Means com 4 perfis usando desempenho-base, média de português, meta, gap e risco previsto. O silhouette score foi **0.314**. Os clusters apoiam a segmentação de municípios em perfis de menor risco, desempenho favorável, pressão de meta e maior vulnerabilidade.

## 7. Aplicação em políticas públicas

A solução pode apoiar gestores a:

- priorizar municípios com maior probabilidade de não atingir metas;
- identificar territórios em que o desempenho histórico está distante da meta;
- direcionar monitoramento e apoio técnico;
- acompanhar redes com maior vulnerabilidade;
- combinar risco previsto com outras variáveis socioeconômicas em uma evolução futura.

## 8. Limitações

- A exportação Silver recebida é muito menor que o volume documentado na Fase 2, portanto o modelo individual usa uma amostra/exportação parcial.
- Não foram fornecidas variáveis socioeconômicas na exportação atual; elas são uma evolução prioritária para aderência máxima ao enunciado.
- O modelo municipal aprende o padrão 2023→2024 e o reaplica a 2024→2025; mudanças estruturais podem reduzir a validade dessa extrapolação.
- Probabilidade de risco não representa causalidade.
- Os CSVs Gold não contêm o nome do município; relatórios de risco usam código IBGE.

## 9. Reprodutibilidade

Execute:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run_pipeline.py
```

Os dados brutos devem estar em `data/raw/` com os nomes documentados em `data/README.md`.
