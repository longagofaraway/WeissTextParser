import utils

CARD_TYPE_CHARACTER = 1

CARD_TYPE = 1
TRAITS = 3


def ParseCard(text):
    text = utils.SkipSpacesAndCommas(text)
    excluding_this = False
    traits = []
    card_types = []
    card = None
    while True:
        if text.startswith('other'):
            excluding_this = True
            text = text[len('other'):]
            text = utils.SkipSpacesAndCommas(text)
        elif text.startswith('::'):
            trait_end = text.find('::', 2)
            trait = text[2:trait_end]
            traits.append(trait)
            text = text[trait_end+2:]
            text = utils.SkipSpacesAndCommas(text)
        elif text.startswith('Character'):
            card_types.append(CARD_TYPE_CHARACTER)
            text = text[len('Character'):]
            if text[0] == 's':
                text = text[1:]
            text = utils.SkipSpacesAndCommas(text)
        else:
            break

    card = '{"cardSpecifiers":['
    specifiers_num = 0
    if card_types:
        card += '{"type":'+str(CARD_TYPE)+',"specifier":'+str(CARD_TYPE_CHARACTER)+'}'
        specifiers_num += 1
    for trait in traits:
        if specifiers_num > 0:
            card += ','
        card += '{"type":'+str(TRAITS)+',"specifier":{"value":"'+trait+'"}}'
        specifiers_num += 1
    card += ']}'

    return card, excluding_this, text