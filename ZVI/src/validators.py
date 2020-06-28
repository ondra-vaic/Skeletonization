
def inRange(val, caster, minimum, maximum):
    try:
        castedVal = caster(val)
        if minimum < castedVal < maximum:
            return True
    except:
        return False


def neighbourhoodValidator(val, caster):
    try:
        neighbourhoods = caster(val)

        if neighbourhoods[0] == 4 or neighbourhoods[0] == 8:
            if neighbourhoods[1] == 4 or neighbourhoods[1] == 8:
                return True
    except:
        return False


def thresholdValidator(val, caster):
    return inRange(val, caster, 0, 255)


def resizeValidator(val, caster):
    return inRange(val, caster, 0, float('inf'))


def strElementValidator(val, caster):
    try:
        width = caster(val)
        if width > 0 and width % 2 == 1:
            return True
    except:
        return False