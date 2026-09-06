from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier

def make_preprocessor(numeric, categorical):
    return ColumnTransformer([
        ('num', Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler())]), numeric),
        ('cat', Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]), categorical),
    ])

def make_student_pipeline(numeric, categorical):
    return Pipeline([('preprocessor',make_preprocessor(numeric,categorical)),('model',HistGradientBoostingClassifier(max_iter=200,learning_rate=0.1,max_leaf_nodes=31,min_samples_leaf=50,l2_regularization=1.0,random_state=42))])

def make_municipal_pipeline(numeric, categorical, C=1.0):
    return Pipeline([('preprocessor',make_preprocessor(numeric,categorical)),('model',LogisticRegression(max_iter=1000,class_weight='balanced',C=C,random_state=42))])
