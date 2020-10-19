# coding: utf-8
import re
import os
from tika import parser
#from nltk.corpus import stopwords
from razdel import tokenize # pip install razdel # https://github.com/natasha/razdel
import pymorphy2 # pip install pymorphy2

class preprocessing_tools:
    morph = pymorphy2.MorphAnalyzer()
    
    stopword_ru = [] #stopwords.words('russian')
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        for w in f.readlines():
            stopword_ru.append(re.sub('\n','',w))
    
    cache = {}  # для кеша лемм
    
    def __init__(self):
        self.stopwords = stopword_ru
    
    
    def clean_text(text):
        '''
        очистка текста
            
        на выходе - очищенный текст
        '''
        
        if not isinstance(text, str):
            text = str(text)
        
        text = text.lower()
        text = text.strip('\n').strip('\r').strip('\t')
    
        text = re.sub("-\s\r\n\|-\s\r\n|\r\n", '', str(text))
    
        text = re.sub("[0-9]|[-—.,:;_%©«»?*!@#№$^•·&()]|[+=]|[[]|[]]|[/]|[\"]", '', text)
        text = re.sub(r"\r\n\t|\n|\\s|\r\t|\\n", ' ', text)
        text = re.sub(r'[\xad]|[\s+]', ' ', text.strip())
    
        return text
    
    
    def lemmatization(text):
        '''
        лемматизация
            [0] если зашел тип не `str` делаем его `str`
            [1] токенизация предложения через razdel
            [2] проверка есть ли в начале слова '-'
            [3] проверка токена с одного символа
            [4] проверка есть ли данное слово в кэше
            [5] лемматизация слова
            [6] проверка на стоп-слова
            
        на выходе - лист отлемматизированых токенов
        '''
        
        # [0]
        if not isinstance(text, str):
            text = str(text)
        
        # [1]
        tokens = list(tokenize(text))
        words = [_.text for _ in tokens]
    
        words_lem = []
        for w in words:
            if w[0] == '-': # [2]
                w = w[1:]
            if len(w)>1: # [3]
                if w in cache: # [4]
                    words_lem.append(cache[w])
                else: # [5]
                    temp_cach = cache[w] = morph.parse(w)[0].normal_form
                    words_lem.append(temp_cach)
    
        words_lem_without_stopwords = [i for i in words_lem if not i in stopword_ru] # [6]
    
        return words_lem_without_stopwords
    
    
    def stop_words_remove(text):
        '''
        очистка текста от стоп-слов
        
        на выходе - очищенный от стоп-слов текст
        '''
        # [0]
        if not isinstance(text, str):
            text = str(text)
        
        # [1]
        tokens = list(tokenize(text))
        words = [_.text for _ in tokens]
    
        words_lem = []
        for w in words:
            if w[0] == '-': # [2]
                w = w[1:]
            if len(w)>1: # [3]
                if w in cache: # [4]
                    words_lem.append(cache[w])
                else: # [5]
                    temp_cach = cache[w] = morph.parse(w)[0].normal_form
                    words_lem.append(temp_cach)
    
        words_lem_without_stopwords = [i for i in words_lem if not i in stopword_ru] # [6]
        
        words_lem_without_stopwords_string = str(words_lem_without_stopwords)
    
        return words_lem_without_stopwords_string
    
    
    def extract_text_from_pdfs_recursively(dir):
        '''
        получение содержимого всех pdf документов в директории
        '''
        all_texts = []
        for root, dirs, files in os.walk(dir):
            for file in files:
                path_to_pdf = os.path.join(root, file)
                [stem, ext] = os.path.splitext(path_to_pdf)
                if ext == '.pdf':
                    print("Processing " + path_to_pdf)
                    pdf_contents = parser.from_file(path_to_pdf)
                    text = pdf_contents['content']
                    all_texts.append(text)
        return all_texts    