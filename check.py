from googletrans import Translator

translator = Translator()
translated= translator.translate("海贼王之吾为恶魔")
print(translated.text)
