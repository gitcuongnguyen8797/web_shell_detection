from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from config import *

class RandomForest:
    def __init__(self, dataset) -> None:
        self.df = pd.read_csv(ROOT_DIR + '/' + dataset)
        self.defined_function_names = self.df.drop(columns=['class']).columns
        self.x_train = self.x_test = self.y_train = self.y_test= None
        self.pca = None
        self.config()
        self.random_forest = self.train_model_without_pca()

    def config(self):
        X = self.df.drop(columns=['class'])
        Y = self.df['class']
        self.x_train = X
        self.y_train = Y

    def train_model_without_pca(self):
        random_forest = RandomForestClassifier(n_estimators=1000, max_depth=10, random_state=0)
        random_forest.fit(self.x_train, self.y_train)
        return random_forest
    
    def predict_without_pca(self, extracted_features):
        tmp = []
        tmp.append(extracted_features)
        new_df = pd.DataFrame(tmp, columns=self.defined_function_names).fillna(0)
        return self.random_forest.predict(new_df)

