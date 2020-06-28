def fourNeighbourhood(img, x, y):
    return [img[x + 1][y], img[x - 1][y], img[x][y + 1], img[x][y - 1]]


def eightNeighbourhood(img, x, y):
    return [img[x + 1][y], img[x - 1][y], img[x][y + 1], img[x][y - 1],
            img[x + 1][y + 1], img[x - 1][y + 1], img[x + 1][y - 1], img[x - 1][y - 1]]


def arrayIntParser(strValues):
    vals = []

    for val in strValues.split(","):
        vals.append(int(val))

    return vals