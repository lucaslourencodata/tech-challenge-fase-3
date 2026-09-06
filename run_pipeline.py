from pathlib import Path
import json
import pandas as pd
import joblib
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from src.preprocessing.features import load_raw, build_student_dataset, build_municipal_training, UF_SIGLA, REGION_MAP
from src.modeling.pipelines import make_student_pipeline, make_municipal_pipeline
from src.evaluation.metrics import classification_metrics

ROOT=Path(__file__).resolve().parent
D=load_raw(ROOT)

# Modelo individual
s=build_student_dataset(D['students'],D['indicator'],D['metas'])
features=['uf','rede','taxa_alfabetizacao_2023_publica','media_portugues_2023_publica','meta_alfabetizacao_2024']
cat=['uf','rede']; num=['taxa_alfabetizacao_2023_publica','media_portugues_2023_publica','meta_alfabetizacao_2024']
X=s[features].copy(); y=s.alfabetizado.astype(int); g=s.id_municipio
for c in cat: X[c]=X[c].astype(str)
tr,te=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42).split(X,y,g))
model=make_student_pipeline(num,cat); model.fit(X.iloc[tr],y.iloc[tr])
p=model.predict(X.iloc[te]); prob=model.predict_proba(X.iloc[te])[:,1]
print('Modelo individual:', classification_metrics(y.iloc[te],p,prob))
joblib.dump(model,ROOT/'models'/'modelo_alfabetizacao_aluno_reexecucao.joblib')

# Modelo municipal
m=build_municipal_training(D['comparison'],D['evolution'],D['indicator'])
f=['uf','taxa_base','media_portugues_base','meta_alvo']; catm=['uf']; numm=['taxa_base','media_portugues_base','meta_alvo']
X=m[f]; y=m.risco_abaixo_meta
tr,te=train_test_split(range(len(m)),test_size=.2,random_state=42,stratify=y)
mm=make_municipal_pipeline(numm,catm,C=2.0); mm.fit(X.iloc[tr],y.iloc[tr]); p=mm.predict(X.iloc[te]); prob=mm.predict_proba(X.iloc[te])[:,1]
print('Modelo municipal:', classification_metrics(y.iloc[te],p,prob))
joblib.dump(mm,ROOT/'models'/'modelo_risco_meta_municipal_reexecucao.joblib')
