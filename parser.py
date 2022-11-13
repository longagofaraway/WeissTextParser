import traceback
import sys

import parse_ability


CONT=1
AUTO=2
ACT=3
EVENT=4
ABILITY_TYPES={'A': AUTO, 'S': ACT, 'C': CONT}

KEYWORDS=['ENCORE', 'CX COMBO']
KEYWORDS_MAP={'ENCORE': 1, 'CX COMBO': 2}

abilities_prefix = 'TEXT: '


def GetAblityType(text):
    if text[0] != '[' or text[2] != ']':
        raise Exception("error parsing " + text)
    if text[1] not in ABILITY_TYPES:
        raise Exception("error parsing " + text)
    return ABILITY_TYPES[text[1]]


def GetKeywords(text):
    keywords = []
    while (True):
        for keyword in KEYWORDS:
            if text.startswith(keyword):
                keywords.append(KEYWORDS_MAP[keyword])
                text = text[len(keyword) + 1:]
                break
        else:
            break

    return keywords, text


def ParseAbility(text):
    ability_type = GetAblityType(text[:3])
    pos = 4 #[A]_
    keywords, text = GetKeywords(text[pos:])
    text = text[0].lower() + text[1:]
    if ability_type == AUTO:
        ability = parse_ability.ParseAutoAbility(text, keywords)
    elif ability_type == CONT:
        ability = parse_ability.ParseContAbility(text, keywords)
    return ability


def GetCurrentLine(text, pos):
    next_new_line = text.find('\n', pos)
    line = text[pos:next_new_line]
    return line, next_new_line + 1


def GetNextLine(text, pos):
    next_line_start = text.find('\n', pos) + 1
    next_line_end = text.find('\n', next_line_start)
    line = text[next_line_start:next_line_end]
    return line, next_line_end


def SkipSpaces(text, pos):
    while text[pos] == ' ':
        pos += 1
    return pos


def StartsWithAbility(line):
    if (line.startswith('[A]') or line.startswith('[C]') or
        line.startswith('[S]')):
        return True
    return False


def GetAbilitiesText(text, pos):
    abilities = []
    pos = text.find(abilities_prefix, pos)
    pos += len(abilities_prefix)
    ability = ''
    while True:
        line, pos = GetCurrentLine(text, pos)
        if (not len(line) or StartsWithAbility(line)) and ability:
            abilities.append(ability.strip())
            ability = ''
        if not len(line):
            break
        ability += line + ' '

    return abilities, pos


f = open("text.txt", "r", encoding='utf-8')
text = f.read()

card_no_prefix = 'Card No.: '

pos = text.find(card_no_prefix)
card_count = 0
while pos != -1:
    card_count += 1
    #if len(sys.argv) > 2 and sys.argv[1] != card_count:
    #    continue

    pos += len(card_no_prefix)
    code_end = text.find(' ', pos)
    code = text[pos:code_end]

    line, next_line_end = GetNextLine(text, code_end)
    card_type = line.split()[-1]

    abilities, pos = GetAbilitiesText(text, next_line_end)
    count = 0
    for ability in abilities:
        count += 1
        try:
            json = ParseAbility(ability)
            print(code, count, ':')
            print(json)
        except Exception:
            print('skipping', code, count)
            traceback.print_exc()
            continue

    pos = text.find(card_no_prefix, pos)
    if card_count > 2:
        break
