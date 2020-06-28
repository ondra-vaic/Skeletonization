import cv2
import numpy as np
import Utils


def toGray(image, params):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def empty(image, params):
    return image


def mOpen(image, width):
    kernel = np.ones((width, width), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def mClose(image, width):
    kernel = np.ones((width, width), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


def erode(image, width):
    kernel = np.ones((width, width), np.uint8)
    return cv2.erode(image, kernel)


def dilate(image, width):
    kernel = np.ones((width, width), np.uint8)
    return cv2.dilate(image, kernel)


def thresholdOtsu(image, params):
    __, newImg = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return newImg


def thresholdManual(image, threshold):
    __, newImg = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return newImg


def resize(image, width):
    aspect = image.shape[0] / image.shape[1]
    return cv2.resize(image, (width, int(aspect * width)))


def gauss(image, width):
    return cv2.GaussianBlur(image, (width, width), 0)


def invert(image, params):
    return 255 - image


def skeletonize(image, neighbourhood):

    neighbourhoodDistanceTransform = Utils.fourNeighbourhood if neighbourhood[0] == 4 else Utils.eightNeighbourhood
    neighbourhoodSkeleton = Utils.fourNeighbourhood if neighbourhood[1] == 4 else Utils.eightNeighbourhood

    originalImage = image / 255
    currentImage = np.copy(image) / 255
    unchanged = set()

    while True:
        newImg = np.copy(currentImage)
        changed = False

        for y in range(1, image.shape[0] - 1):
            for x in range(1, image.shape[1] - 1):

                if (y, x) in unchanged:
                    continue

                lastVal = currentImage[y][x]
                newImg[y][x] = originalImage[y][x] + min(neighbourhoodDistanceTransform(currentImage, y, x))

                if lastVal == newImg[y][x]:
                    unchanged.add((y, x))
                else:
                    changed = True

        currentImage = newImg

        if not changed:
            showDistanceTransform(currentImage)
            return finishSkeleton(currentImage, neighbourhoodSkeleton)


def finishSkeleton(img, neighbourhoodFunction):

    newImg = np.zeros(img.shape, np.uint8)
    for y in range(1, img.shape[0] - 1):
        for x in range(1, img.shape[1] - 1):
            maximum = max(neighbourhoodFunction(img, y, x))
            if img[y][x] >= maximum:
                newImg[y][x] = 255
            else:
                newImg[y][x] = 0
    return newImg


def showDistanceTransform(img):
    maxIntensity = img.max()
    minIntensity = img.min()

    newImg = np.copy(img)
    for y in range(1, newImg.shape[0]):
        for x in range(1, newImg.shape[1]):
            newImg[y][x] = 255 * ((newImg[y][x] - minIntensity)/(maxIntensity - minIntensity))

    cv2.imshow("Distance Transform", newImg.astype(np.uint8))
