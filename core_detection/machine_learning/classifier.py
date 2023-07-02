import pickle
from config import *

class Classifier:
    def __init__(self) -> None:
        self.model = pickle.load('./random_forest.pkl', 'w')

    def detect(self, file):
        pass