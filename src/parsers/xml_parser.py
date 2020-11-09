import xml.etree.ElementTree as et
from os import listdir
from os.path import isfile, join


class XmlParser(object):

    def __init__(self, path):
        self.root = et.parse(path).getroot()
        self.data = et.SubElement(self.root, "ProfessionalStandart")

    def get_name(self):
        return self.root.find(".//NameProfessionalStandart").text
    
    def get_relevant_text(self):
        return "\n".join({
            self.get_name(),
            self.root.find(".//KindProfessionalActivity").text,
            self.root.find(".//PurposeKindProfessionalActivity").text,
            "\n".join({el.text for el in self.root.findall(".//NameOKVED")}),
            "\n".join({el.text for el in self.root.findall(".//NameOTF")}),
            "\n".join({el.text for el in self.root.findall(".//PossibleJobTitle")}),
            "\n".join({el.text for el in self.root.findall(".//EducationalRequirement")}),
            "\n".join({el.text for el in self.root.findall(".//NameEKS")}),
            "\n".join({el.text for el in self.root.findall(".//NameOKSO")}),
            "\n".join({el.text for el in self.root.findall(".//LaborAction")}),
            "\n".join({el.text for el in self.root.findall(".//RequiredSkill")}),
            "\n".join({el.text for el in self.root.findall(".//NecessaryKnowledge")}),
            "\n".join({el.text for el in self.root.findall(".//RequirementsWorkExperience")})
        })
    
    """
    @staticmethod
    def extract_text_from_xmls_recursively(dir):
        '''
        получение содержимого всех xml документов в директории
        '''
        all_texts = []
        for root, dirs, files in os.walk(dir):
            for file in files:
                path_to_xml = os.path.join(root, file)
                [stem, ext] = os.path.splitext(path_to_xml)
                if ext == '.xml':
                    print("Processing " + path_to_xml)
                    XmlParser = XmlParser(path_to_xml)
                    text = XmlParser.get_relevant_text()
                    # xml_contents = XmlParser.get_relevant_text(path_to_xml)
                    # text = xml_contents['content']
                    all_texts.append(text)
        return all_texts
    """
    
    @staticmethod
    def extract_text_from_xmls(path):
        files = [f for f in listdir(path) if isfile(join(path, f))]
        # profstandards = [XmlParser(f"{path}/{f}").get_relevant_text() for f in files]
        profstandards = [XmlParser(join(path, f)).get_relevant_text() for f in files if f.endswith(".xml")]
        return profstandards