import os
import os.path
from os import listdir
from os.path import isfile, join

from src.parsers.pdf_parser import PdfParser
from src.parsers.xml_parser import XmlParser


class Model:

    _MODEL_DIR = str(os.getcwd())

    def __init__(self, name):
        self.name = name
        self.model = self._load_model()
        self.pdf_parser = PdfParser()

    def _load_model(self):
        result = None
        if os.path.isfile(f"{self._MODEL_DIR}/{self.name}"):
            with open(f"{self._MODEL_DIR}/{self.name}", 'rb') as f:
                pass
        else:
            result = self._create_model()
        return result

    def _create_model(self):
        path = "../../data/RPD/5503_database_techologies_2019"
        rpds = [f for f in listdir(path) if isfile(join(path, f))]
        profstandards = [XmlParser(f"{path}/{f}").get_relevant_text() for f in rpds if f.endswith(".xml")]
        
        return None


if __name__ == "__main__":
    path = "../../data"
    rpds = [f for f in listdir(path) if isfile(join(path, f))]
    print(rpds)
    profstandards = [XmlParser(join(path, f)).get_relevant_text() for f in rpds if f.endswith(".xml")]
    print(profstandards)
