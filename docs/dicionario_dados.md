# Dicionário de dados utilizado na Fase 3

## Silver — alunos
- `ano`: ano da avaliação.
- `id_municipio`: código IBGE do município.
- `id_escola`: identificador da escola.
- `id_aluno`: identificador do aluno.
- `caderno`: caderno/prova aplicada.
- `serie`: série avaliada (na exportação, 2º ano).
- `rede`: código da rede de ensino.
- `presenca`: indicador de presença.
- `preenchimento_caderno`: indicador de preenchimento.
- `alfabetizado`: alvo binário do modelo individual.
- `proficiencia`: proficiência observada. **Não usada como feature por leakage**.
- `peso_aluno`: peso amostral. Não usado como feature.

## Gold — indicadores municipais
Inclui taxa de alfabetização, média de português, metas municipais, comparação resultado x meta e evolução 2023–2024.

## Features do modelo individual
O modelo usa apenas informações que não contêm o resultado de 2024: UF, rede, taxa pública municipal de alfabetização de 2023, média municipal de português de 2023 e meta municipal de 2024.

## Features do modelo municipal
Para prever o risco de 2024, usa taxa de 2023, média de português de 2023, meta de 2024 e UF. O gap é mantido apenas como indicador analítico nos relatórios, evitando multicolinearidade perfeita no modelo. O mesmo pipeline é reaplicado para 2025 usando 2024 como ano-base e a meta de 2025.
