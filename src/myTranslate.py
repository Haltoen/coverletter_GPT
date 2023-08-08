
from translate import Translator
import os

import database
db = database.db()
csv_h = database.CSVHandler()
#print(Translator.LANGUAGES)
class Trans():
    """
    Handles google translate calls.
    """
    def __init__(self) -> None:
        self.languages = self.language_dict()
        self.lang_list = self.language_lst()
        print(self.lang_list)

    def language_dict (self) -> dict:
        """
        Creates a dictionary containing languages & their codes. 

        Returns:
        dict: With language codes as items and languages as keys. 
        """
        dict_lst = csv_h.read_dicts_from_csv("Language_Codes.csv")
        return {dic["Language"]: dic["ISO_code"]  for dic in dict_lst}
    
    def language_lst (self) -> list[str]:
        """
        Creates a list containing all languages.

        Returns:
        list[str]: Languages. 
        """
        return list(self.languages.keys())

    def translate(self, src: str, dst: str, txt: str) -> str:
        """
        Translates text using google translate API.

        Parameters:
        src (str): Source language. 
        dst (str): Destination language.
        txt (str): Text to be translated.

        Returns:
        str: Translated text.
        """
        translator = Translator(to_lang=dst, from_lang=src)
        translation = translator.translate(txt)
        print(translation)
        return translation
    
    def translate_resume(self, src_dst: tuple) -> None:
        """
        Translates a resume and adds it to the database.
        
        Parameters: 
        src_dst (tuple): Source and destination languages, expects (src, dst)
        """
        from_l = src_dst[0]
        to_l = src_dst[1]
        resume = str(db.get_resume(from_l))
        translation = self.translate(from_l, to_l, resume)
        db.add_resume((to_l, translation))
        return None
        

