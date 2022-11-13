

def SkipSpacesAndCommas(text):
    while text[0] in (' ', ',', '.'):
        text=text[1:]
        if not len(text):
            break
    return text

def GetNumber(text):
    i = 0
    value = ''
    while text[i].isdigit():
        value += text[i]
        i += 1
    return value, text[i:]