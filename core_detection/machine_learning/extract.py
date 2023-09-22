import re
from collections import Counter
from .helper import *

class ExtractFeatures:
    
    def __init__(self, file) -> None:
        self.resource = file
        self._sensitive_functions = ['exec', 'shell_exec', 'passthru', 'system', 'show_source', 'proc_open', 'pcntl_exec', 'eval', 'assert']
        self._df = None

    def extract_function_names(self):
        filter = [
            'if', 'while', 'die', 'elseif', 'go', 'back', 'sort', 'foreach', 'switch', 'trim', 'array', 'count',
            'session_start', 'header', 'try', 'catch', 'floor', 'round', 'max', 'min', 'session_destroy', 'css', 'pagination',
            'add', 'pop', 'shift', 'edit', 'int32', 'end', 'prev','next', 'for'
        ]
        regex = re.compile(r"\b[_A-Za-z]+[_0-9A-Za-z]*\b")
        with open(self.resource, 'r', encoding='ISO-8859-1') as file:
          results = [x.lower().strip() for x in regex.findall(file.read())]
          return Counter([result for result in results if result not in filter])
    
    def extract_entropy_file(self):
        return calc_entropy(self.resource)

    def extract_longest_string(self):
        longest_string = ''
        with open(self.resource, 'r', encoding='ISO-8859-1') as file:
            lines = file.readlines()
            longest_string = max(lines, key=len)
            return len(longest_string)

    def extract_by_word2vec(self):
        return None
    