from io import StringIO

from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfdocument import PDFDocument
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfparser import PDFParser


class PdfParser(object):

    def __init__(self):
        self.rsrcmgr = PDFResourceManager()
        self.laparams = LAParams()

    def extract_string(self, path):
        output_string = StringIO()

        with open(path, "rb") as pdf:
            parser = PDFParser(pdf)
            doc = PDFDocument(parser)
            device = TextConverter(self.rsrcmgr, output_string, laparams=self.laparams)
            interpreter = PDFPageInterpreter(self.rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        return output_string.getvalue()

    def get_lines(self, path):
        return self.extract_string(path).split('\n')

    def extract_volumes(self, path):
        lines = self.get_lines(path)
        volumes = [(line, i) for i, line in enumerate(lines) if line.startswith(f"Раздел ")]
        return volumes

    def extract_relevant(self, path):
        flag = False
        content = ""
        lines = self.get_lines(path)
        for line in lines:
            if line.startswith("1.1") or line.startswith("1.3"):
                flag = True
                continue
            if line.startswith("1.2") or line.startswith("1.4"):
                flag = False
            if flag:
                content += line + '\n'
        return content
