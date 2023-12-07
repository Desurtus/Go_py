CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = dict()

for cyrilic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrilic)] = latin
    TRANS[ord(cyrilic.upper())] = latin.upper()

def translate(translated_str):
    return translated_str.translate(TRANS)
    # result = ''
    
    # for symbol in translated_str:
    #     if symbol in TRANS.keys():
    #         result += TRANS.get(symbol)
    #     else:
    #         result += symbol
    # return result

print(translate("Дмитро Короб"))  # Dmitro Korob
print(translate("Олекса Івасюк"))  # Oleksa Ivasyuk