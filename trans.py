from googletrans import Translator
def process(input):
    translator = Translator()
    translated=translator.translate(input).text
    return translated
