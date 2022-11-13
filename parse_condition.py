import utils
import parse_card

EXACT_MATCH = 1
AT_LEAST = 3


def PrintBool(value):
    if value:
        return 'true'
    else:
        return 'false'


def ParseNumModifier(text):
    modifier = EXACT_MATCH
    text = utils.SkipSpacesAndCommas(text)
    if text.startswith('or more'):
        modifier = AT_LEAST
        text = text[len('or more'):]
        text = utils.SkipSpacesAndCommas(text)
    return modifier, text

def ParseConditionHaveCards(text):
    text = utils.SkipSpacesAndCommas(text)
    condition = None
    if text[0].isdigit():
        num = int(text[0])
        modifier, text = ParseNumModifier(text[1:])
        card, excluding_this, text = parse_card.ParseCard(text)
        place='{"pos":0,"zone":1,"owner":1}'
        condition = '{"type":2,"cond":{"invert":false,'\
        '"who":1,'\
        '"howMany":{"mod":'+str(modifier)+',"value":'+str(num)+'},'\
        '"whichCards":'+card+','\
        '"where":'+place+','\
        '"excludingThis":'+PrintBool(excluding_this)+'}}'
    return condition, text


def ParseConditionDuring(text):
    if not text.startswith('during battles'):
        raise Exception('during battles not parsed')
    text = text[len('during battles'):]
    text = utils.SkipSpacesAndCommas(text)
    if text.startswith('involving this'):
        text = text[len('involving this'):]
    elif text.startswith('with this'):
        text = text[len('with this'):]
    else:
        raise Exception('during battles_ not parsed')
    text = utils.SkipSpacesAndCommas(text)
    condition = '{"type":5}'
    return condition, text


def ParseCondition(text):
    condition = None
    if text.startswith('if you have'): 
        text = text[len('if you have'):]
        condition, text = ParseConditionHaveCards(text)
    elif text.startswith('during'):
        condition, text = ParseConditionDuring(text)
    return condition, text