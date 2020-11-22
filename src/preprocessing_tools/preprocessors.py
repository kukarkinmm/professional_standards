import re
import stop_words
import snowballstemmer as snb

from .preprocessing_tools import preprocessing_tools


class Preprocessor:

    def __init__(self, preprocess_=True, stop_words_=True, stemming_=True, lang='english'):
        self.preprocess = preprocess_
        self.stop_words = stop_words_
        self.stemming = stemming_
        self.language = lang

    def __call__(self, line):
        return self._stem(self._stop_words(self._preprocess(line)))

    def _preprocess(self, line):
        line = line.lower()
        if self.preprocess:
            line = re.sub(r'&quot;.*?&quot;|&quot|http?\w+', '', line)
            line = re.sub(r'@\w+', '', line)
            line = re.sub(
                r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
                '', line)
            line = re.sub(r'[^\w\s]', '', line)
            line = re.sub(r'\d+', '', line)
        return line

    def _stop_words(self, line):
        if self.stop_words:
            stopwords = stop_words.get_stop_words(self.language)
            return [word for word in line.split() if word not in stopwords]
        return line.split()

    def _stem(self, words):
        if self.stemming:
            stemmer = snb.stemmer(self.language)
            return stemmer.stemWords(words)
        return words


class ToolsPreprocessor:

    def __init__(self):
        self.prep_tools = preprocessing_tools()

    def __call__(self, text):
        result = self.prep_tools.clean_text(text)
        result = self.prep_tools.stop_words_remove(result)
        return result
