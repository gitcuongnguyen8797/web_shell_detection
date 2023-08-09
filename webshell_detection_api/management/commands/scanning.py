from django.core.management.base import BaseCommand, CommandParser
from core_detection.machine_learning.classifiers.random_forest import RandomForest
from core_detection.machine_learning.extract import *
import os
import pathlib

class Command(BaseCommand):
    help = 'Scanning Specific Folder to detect Webshells in PHP and ASP(X) languages'
    model_ps = RandomForest('./dataset/Q_dataset_ps_loctu_tfidf_200.csv')
    model_js = RandomForest('./dataset/Qdataset_js_loctu_tfidf_720.csv')
    benigns = 0

    def is_folder(self, path):
        if (os.path.isdir(path)):
            return True
        else:
            return False

    def read_file(self, path):
        if (self.is_folder(path)):
            for file in os.listdir(path):
                new_path = path+'/'+file
                if (self.is_folder(new_path)):
                    self.read_file(new_path)
                else:
                    filePath = path + '/' + file
                    ext = pathlib.Path(filePath).suffix
                    features = ExtractFeatures(filePath).extract_function_names()
                    if (ext == 'js'):   
                        prediction = self.model_js.predict_without_pca(features)
                    else:
                        prediction = self.model_ps.predict_without_pca(features)
                        
                    if (prediction[0] == 'malware'):
                        self.malware +=1
                    else:
                        self.benigns +=1
            

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-f', '--folder', type=str, help='Add your folder directory')

    def handle(self, *args, **kwargs):
        folder = kwargs['folder']
        self.stdout.write(self.style.SUCCESS('Starting Scanning with Folder %s' % folder))
        self.read_file(folder)
        self.stdout.write(self.style.ERROR('False Positive: %s' % self.malware))
        self.stdout.write(self.style.SUCCESS('True Negative: %s' % self.benigns))
        self.malware = 0 
        self.benigns = 0