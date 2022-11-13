import parse_effect
import parse_condition
import utils

ON_ATTACK='when this attacks'

JSON_THIS_CARD='{"type":1}'


def ParseTrigger(text):
    trigger = None
    if (text.startswith(ON_ATTACK)):
        trigger = '{"type":4,"trigger":{"target":'+JSON_THIS_CARD+'}}'
        text = text[len(ON_ATTACK)+1:]
        text = utils.SkipSpacesAndCommas(text)
    return trigger, text


def ParseAutoAbility(text, keywords):
    json='{"type":2,"ability":'
    print('parsing auto', text[:10])
    condition = None
    if text.startswith('when'):
        trigger, text = ParseTrigger(text)
        if not trigger:
            raise Exception('trigger not parsed')
    if text.startswith('if'):
        condition, text = parse_condition.ParseCondition(text)
        if not condition:
            raise Exception('condition not parsed')
    effects, text = parse_effect.ParseEffects(text, condition)
    if not effects:
        raise Exception('effects not parsed')
    if not trigger:
        raise Exception('trigger not parsed')
    auto_ability = '{"keywords":'+str(keywords)+',"triggers":['+trigger+'],'\
        '"effects":['
    count = 0
    for effect in effects:
        if count > 0:
            auto_ability += ','
        auto_ability += effect
    auto_ability += ']}'
    json+=auto_ability+'}'
    return json


def ParseContAbility(text, keywords):
    json='{"type":1,"ability":'
    condition = None
    if text.startswith('if') or text.startswith('during'):
        condition, text = parse_condition.ParseCondition(text)
        if not condition:
            raise Exception('condition not parsed')
    effects, text = parse_effect.ParseEffects(text, condition)
    if not effects:
        raise Exception('effects not parsed')
    auto_ability = '{"keywords":'+str(keywords)+','\
        '"effects":['
    count = 0
    for effect in effects:
        if count > 0:
            auto_ability += ','
        auto_ability += effect
    auto_ability += ']}'
    json+=auto_ability+'}'
    return json