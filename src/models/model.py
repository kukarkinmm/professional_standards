import os
import os.path
from os import listdir
from os.path import isfile, join

from src.parsers.pdf_parser import PdfParser
from src.parsers.xml_parser import XmlParser

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Model:

    _MODEL_DIR = str(os.getcwd())
    _path = "../../data/professional_standarts"

    def __init__(self, name=""):
        self.name = name
        self.files = self._get_files()
        self.vectorizer, self.profst_vecs = self._create_model()
        self.pdf_parser = PdfParser()

    def _load_model(self):
        result = None
        if os.path.isfile(f"{self._MODEL_DIR}/{self.name}"):
            with open(f"{self._MODEL_DIR}/{self.name}", 'rb') as f:
                pass
        else:
            result = self._create_model()
        return result

    def _get_files(self):
        files = [f for f in listdir(self._path) if isfile(join(self._path, f))]
        return files

    def _create_model(self):
        tfidf = TfidfVectorizer()
        profstandards = [XmlParser(f"{self._path}/{f}").lol() for f in self.files if f.endswith(".xml")]
        vals = tfidf.fit_transform(profstandards)
        return tfidf, vals

    def closest_standards(self, text):
        vals = self.vectorizer.transform([text])
        sim = cosine_similarity(self.profst_vecs, vals)
        result = sorted(zip(self.files, sim), key=lambda x: -x[1])
        return result


if __name__ == "__main__":

    model = Model()
    model.closest_standards("Написание")
