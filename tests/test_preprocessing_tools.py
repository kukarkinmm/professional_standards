import unittest

from src.preprocessing_tools.preprocessing_tools import preprocessing_tools


class TestPreprocessingTools(unittest.TestCase):

    def setUp(self):
        self.preprocessingTools = preprocessing_tools()

    # tests for clean_text()

    def test_clean_text_word_rus(self):
        self.assertEqual(self.preprocessingTools.clean_text("ДисциПлина"), "дисциплина")

    def test_clean_text_word_eng(self):
        self.assertEqual(self.preprocessingTools.clean_text("Bitcoin"), "bitcoin")

    def test_clean_text_numbers(self):
        self.assertEqual(self.preprocessingTools.clean_text("23 1 534"), "23 1 534")

    def test_clean_text_words_numbers(self):
        self.assertEqual(self.preprocessingTools.clean_text
                         ("По направлению 02.04.02"),
                         "по направлению 02.04.02"
                         )

    def test_clean_text_stop_words(self):
        self.assertEqual(self.preprocessingTools.clean_text
                         ("Ознакомить с основными тенденциями развития подходов"
                          + "в данной области и нерешенными задачами в ней"),
                         "ознакомить с основными тенденциями развития подходов"
                         + "в данной области и нерешенными задачами в ней"
                         )

    def test_clean_text_words_tab(self):
        self.assertEqual(self.preprocessingTools.clean_text
                         ("Дисциплина «Введение в блокчейн технологии» относится"
                          + "\t"
                          + "к циклу М.2 основной"
                          + "\n"
                          + "образовательной программы"),
                         "дисциплина «введение в блокчейн технологии» относится"
                         + " "
                         + "к циклу м.2 основной образовательной программы"
                         )

    # tests for def lemmatization()

    def test_lemmatization_word_rus(self):
        self.assertEqual(self.preprocessingTools.lemmatization("ДисциПлина"), ['дисциплина'])

    def test_lemmatization_word_eng(self):
        self.assertEqual(self.preprocessingTools.lemmatization("Bitcoin"), ['bitcoin'])

    def test_lemmatization_numbers(self):
        self.assertEqual(self.preprocessingTools.lemmatization("23 1 534"), ['23', '534'])

    def test_lemmatization_words_numbers(self):
        self.assertEqual(self.preprocessingTools.lemmatization
                         ("По направлению 02.04.02"),
                         ['направление', '02.04.02']
                         )

    def test_lemmatization_stop_words(self):
        self.assertEqual(self.preprocessingTools.lemmatization
                         ("Ознакомить с основными тенденциями развития подходов"
                          + "в данной области и нерешенными задачами в ней"),
                         ['ознакомить', 'основный', 'тенденция', 'развитие', 'подходовва', 'дать', 'область',
                          'нерешённый', 'задача']
                         )

    def test_lemmatization_words_tab(self):
        self.assertEqual(self.preprocessingTools.lemmatization
                         ("Дисциплина «Введение в блокчейн технологии» относится"
                          + "\t"
                          + "к циклу М.2 основной"
                          + "\n"
                          + "образовательной программы"),
                         ['дисциплина', 'введение', 'блокчейн', 'технология', 'относиться',
                          'цикл', 'основной', 'образовательный', 'программа']
                         )


if __name__ == '__main__':
    unittest.main()
