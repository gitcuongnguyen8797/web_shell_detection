from django.core.management.base import BaseCommand, CommandParser
from core_detection.machine_learning.classifiers.random_forest import RandomForest
from core_detection.machine_learning.extract import *
import os
import pathlib

class Command(BaseCommand):
    help = 'Scanning Specific Folder to detect Webshells in PHP and ASP(X) languages'
    model_php = RandomForest('dataset/c_dataset_20.csv')
    model_php_2 = RandomForest('dataset/c_dataset_20_filtered.csv')
    model_asp = RandomForest('dataset/dataset_asp.csv')
    malware = 0
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
                    extractor = ExtractFeatures(filePath)
                    features = extractor.extract_function_names()
                    entropy = extractor.extract_entropy_file()
                    longest = extractor.extract_longest_string()
                    if (ext == 'asp' or ext == 'aspx'):   
                        prediction = self.model_asp.predict_without_pca(features, entropy, longest)
                    else: 
                        prediction = self.model_php.predict_without_pca(features, entropy, longest)
                        
                    if (prediction[0] == 'malware'):
                        self.stdout.write(self.style.ERROR('Malwares: %s' % filePath))
                        self.malware +=1
                    else:
                        self.benigns +=1
            

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-f', '--folder', type=str, help='Add your folder directory')

    def handle(self, *args, **kwargs):
        folder = kwargs['folder']
        self.stdout.write(self.style.SUCCESS('Starting Scanning with Folder %s' % folder))
        self.read_file(folder)
        self.stdout.write(self.style.ERROR('Malwares: %s' % self.malware))
        self.stdout.write(self.style.SUCCESS('Benigns: %s' % self.benigns))
        self.malware = 0 
        self.benigns = 0