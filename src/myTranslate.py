
from translate import Translator
import os

import database
Db = database.db()
csv_h = database.CSVHandler()
#print(Translator.LANGUAGES)
class Trans():
    def __init__(self) -> None:
        self.languages = self.language_dict()
        self.lang_list = self.language_lst()
        print(self.lang_list)

    def language_dict (self) -> dict:
        dict_lst = csv_h.read_dicts_from_csv("Language_Codes.csv")
        return {dic["Language"]: dic["ISO_code"]  for dic in dict_lst}
    
    def language_lst (self) -> list:
        return list(self.languages.keys())

    def translate(self, src, dst, txt):
        translator = Translator(to_lang=dst, from_lang=src)
        translation = translator.translate(txt)
        print(translation)
        return translation
    
    def translate_resume(self, res: tuple) -> None:
        print ("res", res)
        from_l = res[0]
        to_l = res[1]
        resume = str(Db.get_resume(from_l))
        translation = self.translate(from_l, to_l, resume)
        return translation
        

