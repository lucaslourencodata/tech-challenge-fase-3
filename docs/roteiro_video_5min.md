# Roteiro do vídeo executivo — até 5 minutos

## 0:00–0:35 — Problema
“Este projeto usa os dados de alfabetização preparados na Fase 2 para transformar indicadores históricos em inteligência preditiva. O objetivo é responder duas perguntas: quais alunos apresentam maior probabilidade de alfabetização e, principalmente para gestão pública, quais municípios apresentam maior risco de ficar abaixo das metas futuras.”

## 0:35–1:15 — Dados e preparação
“Utilizamos a camada Silver de alunos e quatro tabelas Gold: indicadores municipais, metas, comparação com metas e evolução temporal. Antes de modelar, tratamos um ponto crítico de data leakage. A variável proficiência não foi usada como entrada porque, na base avaliada, o rótulo de alfabetização coincide com o corte de 743 pontos. Também restringimos o modelo individual aos alunos efetivamente avaliados.”

**Tela sugerida:** `images/01_distribuicao_alvo_avaliados.png` e `images/03_status_meta_2024.png`.

## 1:15–2:20 — Modelo individual
“Para o modelo individual, usamos informações territoriais e educacionais conhecidas antes do resultado de 2024: UF, rede, taxa municipal de alfabetização de 2023, média de português de 2023 e meta de 2024. A separação treino e teste foi feita por município, evitando que o mesmo município aparecesse nos dois conjuntos. Foram comparados Regressão Logística, Random Forest e HistGradientBoosting. O modelo final obteve F1 de 0.717 e ROC-AUC de 0.697.”

**Tela sugerida:** `images/05_comparacao_modelos_aluno.png`, `images/06_matriz_confusao_aluno.png` e `images/09_shap_aluno.png`.

## 2:20–3:30 — Risco municipal
“Na camada estratégica, treinamos um modelo para prever se o município ficaria abaixo da meta de 2024 usando apenas o desempenho de 2023 e a meta já definida. A Regressão Logística apresentou ROC-AUC de 0.789. Depois reaplicamos a mesma lógica para 2025, usando 2024 como base. O resultado gera uma probabilidade de risco para cada município, permitindo priorização antes do fechamento do próximo ciclo.”

**Tela sugerida:** `images/10_comparacao_modelos_municipal.png`, `images/12_roc_municipal.png` e `images/15_top20_risco_2025.png`.

## 3:30–4:20 — Insights e aplicação
“Os resultados indicam que o desempenho histórico do território e a distância entre desempenho anterior e meta são fatores centrais. A região com maior risco médio previsto para 2025 é Sul. Também segmentamos municípios em quatro perfis, de melhor desempenho até maior vulnerabilidade, o que permite diferenciar estratégias de apoio.”

**Tela sugerida:** `images/16_risco_por_regiao_2025.png` e `images/17_clusters_municipais_2025.png`.

## 4:20–5:00 — Conclusão e limitações
“Mais do que buscar uma métrica alta, a proposta é oferecer um mecanismo replicável de priorização. O gestor pode usar o risco previsto para direcionar acompanhamento, apoio pedagógico e investigação dos fatores locais. Como evolução, o principal passo é incorporar variáveis socioeconômicas do IBGE, PNAD ou Censo Escolar e repetir a validação com a exportação completa dos microdados.”

**Fechamento:** “Assim, a solução conecta engenharia de dados, Machine Learning e inteligência analítica para apoiar decisões educacionais de forma antecipada.”
