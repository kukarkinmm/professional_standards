from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as et


class XmlParser(object):

    def __init__(self, path):
        self.root = et.parse(path).getroot()

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
    
    @staticmethod
    def extract_text_from_xmls(path):
        files = [f for f in listdir(path) if isfile(join(path, f))]
        return [XmlParser(f"{path}/{f}").lol() for f in files if f.endswith(".xml")]

    def get_name_text(self):
        return self.get_name(), et.tostring(self.root, encoding='utf-8', method='text').decode('utf-8')
