from pathlib import Path
import pandas as pd

REGION_MAP = {11:'Norte',12:'Norte',13:'Norte',14:'Norte',15:'Norte',16:'Norte',17:'Norte',21:'Nordeste',22:'Nordeste',23:'Nordeste',24:'Nordeste',25:'Nordeste',26:'Nordeste',27:'Nordeste',28:'Nordeste',29:'Nordeste',31:'Sudeste',32:'Sudeste',33:'Sudeste',35:'Sudeste',41:'Sul',42:'Sul',43:'Sul',50:'Centro-Oeste',51:'Centro-Oeste',52:'Centro-Oeste',53:'Centro-Oeste'}
UF_SIGLA = {11:'RO',12:'AC',13:'AM',14:'RR',15:'PA',16:'AP',17:'TO',21:'MA',22:'PI',23:'CE',24:'RN',25:'PB',26:'PE',27:'AL',28:'SE',29:'BA',31:'MG',32:'ES',33:'RJ',35:'SP',41:'PR',42:'SC',43:'RS',50:'MS',51:'MT',52:'GO',53:'DF'}

def load_raw(root: Path):
    raw=root/'data'/'raw'
    return {
        'students': pd.read_csv(raw/'alunos_silver.csv'),
        'indicator': pd.read_csv(raw/'indicador_alfabetizacao_municipio.csv'),
        'metas': pd.read_csv(raw/'metas_alfabetizacao_municipio.csv'),
        'comparison': pd.read_csv(raw/'comparacao_meta_resultado_municipio.csv'),
        'evolution': pd.read_csv(raw/'evolucao_alfabetizacao_municipio.csv'),
    }

def build_student_dataset(students, indicator, metas):
    df=students[(students.ano==2024)&(students.presenca==1)&(students.preenchimento_caderno==1)&students.proficiencia.notna()].copy()
    df['id_uf']=(df['id_municipio']//100000).astype(int)
    df['uf']=df['id_uf'].map(UF_SIGLA); df['regiao']=df['id_uf'].map(REGION_MAP)
    hist=indicator[(indicator.ano==2023)&(indicator.codigo_rede==5)][['id_municipio','taxa_alfabetizacao','media_portugues']].drop_duplicates('id_municipio').rename(columns={'taxa_alfabetizacao':'taxa_alfabetizacao_2023_publica','media_portugues':'media_portugues_2023_publica'})
    meta=metas[metas.ano_meta==2024][['id_municipio','meta_alfabetizacao']].drop_duplicates('id_municipio').rename(columns={'meta_alfabetizacao':'meta_alfabetizacao_2024'})
    return df.merge(hist,on='id_municipio',how='left').merge(meta,on='id_municipio',how='left')

def build_municipal_training(comparison, evolution, indicator):
    df=comparison[comparison.codigo_rede==3].copy()
    evo=evolution[evolution.codigo_rede==3][['id_municipio','taxa_alfabetizacao_2023']].drop_duplicates('id_municipio')
    ind=indicator[(indicator.ano==2023)&(indicator.codigo_rede==3)][['id_municipio','media_portugues']].drop_duplicates('id_municipio').rename(columns={'media_portugues':'media_portugues_base'})
    df=df.merge(evo,on='id_municipio',how='left').merge(ind,on='id_municipio',how='left')
    df['taxa_base']=df['taxa_alfabetizacao_2023']; df['meta_alvo']=df['meta_alfabetizacao']; df['gap_base_meta']=df['taxa_base']-df['meta_alvo']; df['risco_abaixo_meta']=(df.status_meta=='Abaixo da meta').astype(int); df['uf']=df.id_uf.map(UF_SIGLA); df['regiao']=df.id_uf.map(REGION_MAP)
    return df
