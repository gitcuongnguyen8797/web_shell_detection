from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone
import os

class Command(BaseCommand):
    help = 'Displays current time'

    def is_folder(self, path):
        if (os.path.isdir(path)):
            return True
        else:
            return False

    def read_file(self, path):
        if (self.is_folder(path)):
            for file in os.listdir(path):
                new_path = path+'\\'+file
                if (self.is_folder(new_path)):
                    self.read_file(new_path)
                else:
                    print(path + '\\' + file)

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-f', '--folder', type=str, help='Add your folder directory')

    def handle(self, *args, **kwargs):
        folder = kwargs['folder']
        self.read_file(folder)