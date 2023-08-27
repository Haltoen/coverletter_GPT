from deep_translator import GoogleTranslator
import database
db = database.db()
csv_h = database.CSVHandler()



class DeepTrans():
    """
    Handles large translation calls.
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

    def translate(self, src: str = "auto", dst: str = "english", txt: str = "Hello") -> str:
        """
        Translates text using google translate API.

        Parameters:
        src (str): Source language. 
        dst (str): Destination language.
        txt (str): Text to be translated.

        Returns:
        str: Translated text.
        """
        print("dst:", dst)
        translator = GoogleTranslator(source=src.lower(), target=dst.lower())
        translation = translator.translate(txt)
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
        
