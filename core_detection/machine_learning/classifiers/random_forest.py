from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
from config import *
from .pca import PCA_Model
from sklearn.preprocessing import StandardScaler

class RandomForest:
    def __init__(self) -> None:
        self.df = pd.read_csv(ROOT_DIR + '/dataset.csv')
        self.defined_function_names = self.df.drop(columns=['no', 'class']).columns
        self.x_train = self.x_test = self.y_train = self.y_test= None
        self.pca = None
        self.config()
        self.pca_random_forest = self.train_model_with_pca()
        self.random_forest = self.train_model_without_pca()

    def config(self):
        X = self.df.drop(columns=['no', 'class'])
        Y = self.df['class']
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

    def train_model_without_pca(self):
        random_forest = RandomForestClassifier(max_depth=10, random_state=0)
        random_forest.fit(self.x_train, self.y_train)
        y_pre = random_forest.predict(self.x_test)

        print( '-------------------------------------Random Forest without PCA --------------------------------------------------------------')
        print ('Current accuracy of Random Forest without PCA is: %3f' % metrics.accuracy_score(self.y_test, y_pre))
        print ('Current recall of Random Forest without PCA is: %3f' % metrics.recall_score(self.y_test, y_pre, average="binary", pos_label="malware"))
        print ('Current f1_score of Random Forest without PCA is: %3f' % metrics.f1_score(self.y_test, y_pre, average="binary", pos_label="malware"))
        print( '-------------------------------------Random Forest without PCA --------------------------------------------------------------')
        return random_forest

    def train_model_with_pca(self):
        pca = PCA_Model()
        features = self.df.drop(columns=['no', 'class'])
        pca_model = pca.train(features)
        
        post_x_train = pca_model.fit_transform(self.x_train)
        post_x_test = pca_model.transform(self.x_test)

        random_forest = RandomForestClassifier(max_depth=10, random_state=0)
        random_forest.fit(post_x_train, self.y_train)
        y_pre = random_forest.predict(post_x_test)
        print( '-------------------------------------Random Forest with PCA --------------------------------------------------------------')
        print ('Current accuracy of Random Forest with PCA is: %3f' % metrics.accuracy_score(self.y_test, y_pre))
        print ('Current recall of Random Forest with PCA is: %3f' % metrics.recall_score(self.y_test, y_pre, average="binary", pos_label="malware"))
        print ('Current f1_score of Random Forest with PCA is: %3f' % metrics.f1_score(self.y_test, y_pre, average="binary", pos_label="malware"))
        print( '-------------------------------------Random Forest with PCA --------------------------------------------------------------')
        self.pca = pca_model
        return random_forest

    def predict_with_pca(self, extracted_features):
        tmp = []
        tmp.append(extracted_features)
        new_df = pd.DataFrame(tmp, columns=self.defined_function_names).fillna(0)
        return self.pca_random_forest.predict(self.pca.transform(new_df))
    
    def predict_without_pca(self, extracted_features):
        tmp = []
        tmp.append(extracted_features)
        new_df = pd.DataFrame(tmp, columns=self.defined_function_names).fillna(0)
        return self.random_forest.predict(new_df)

