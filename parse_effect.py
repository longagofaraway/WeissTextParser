import utils


JSON_THIS_CARD='{"type":1}'


def GetAttribute(text):
    if text.startswith('Power'):
        attr = 1
        text = text[len('Power'):]
    elif text.startswith('Soul'):
        attr = 2
        text = text[len('Soul'):]
    elif text.startswith('Level'):
        attr = 3
        text = text[len('Level'):]
    else:
        raise Exception('unknown attr')
    return attr, text


def GetDuration(text):
    if text.startswith('for the turn'):
        text = text[len('for the turn'):]
        return 1, text
    if text.startswith('until end of turn'):
        text = text[len('until end of turn'):]
        return 1, text
    return 0, text  


def EarlyPlayEffect(text, condition):
    text = text[len('while in your hand'):]
    text = utils.SkipSpacesAndCommas(text)
    effect = '{"type":14'
    if condition:
        effect += ',"cond":'+condition
    effect += '}'
    return effect, text

def ParseAttributeGain(text, condition):
    text = utils.SkipSpacesAndCommas(text)
    if text[0] != '-' and text[0] != '+':
        raise Exception("no sign in attr gain")
    sign = text[0]
    text = text[1:]
    value, text = utils.GetNumber(text)
    text = utils.SkipSpacesAndCommas(text)
    attribute, text = GetAttribute(text)
    text = utils.SkipSpacesAndCommas(text)
    if text.startswith('while in your hand'):
        return EarlyPlayEffect(text, condition)
    duration, text = GetDuration(text)
    text = utils.SkipSpacesAndCommas(text)
    effect = '{"type":1,'
    if condition:
        effect += '"cond":'+condition+','
    effect += '"effect":{"target":'+JSON_THIS_CARD+','\
        '"type":'+str(attribute)+','\
        '"gainType":1,'\
        '"value":'
    if sign == '-':
        effect += '-'
    effect += value+','\
        '"duration":'+str(duration)+'}}'
    return effect, text


def ParseCannotPlayBackup(text, condition):
    if text.startswith('your Opponent cannot play BACKUP from hand'):
        text = text[len('your Opponent cannot play BACKUP from hand'):]
    else:
        raise Exception('cannot play Backup not parsed')
    text = utils.SkipSpacesAndCommas(text)
    effect = '{"type": 19,'
    if condition:
        effect += '"cond":'+condition+','
    effect += '"effect":{"what":1,"player":2,"duration":0}}'
    return effect, text
    

def ParseEffects(text, condition):
    text = utils.SkipSpacesAndCommas(text)
    effects = []
    while True:
        if text.startswith('this gains') or text.startswith('this gets'):
            if (text.startswith('this gains')):
                text = text[len('this gains'):]
            else:
                text = text[len('this gets'):]
            effect, text = ParseAttributeGain(text, condition)
            effects.append(effect)
        elif text.startswith('your Opponent cannot play BACKUP'):
            effect, text = ParseCannotPlayBackup(text, condition)
            effects.append(effect)
        else:
            print('effect not recognised ', text)
            break
        if len(text) < 1:
            break
    
    return effects, text