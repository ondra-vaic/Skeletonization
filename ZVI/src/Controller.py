import numpy as np
from Operations import *
from validators import *

import cv2




class Controller:

    def __init__(self, view):
        self.view = view
        self.states = []
        self.forwardStates = []
        self.stateNumber = 0

    def selectImage(self):
        fileName = self.view.selectOpenImage()
        if fileName == "":
            return

        newImage = cv2.imread(fileName)
        self.states = [newImage]
        self.show()

    def back(self):
        if not self.states:
            return

        self.stateNumber += 1
        self.forwardStates.append(self.states.pop())
        self.show()

    def forward(self):
        if not self.forwardStates:
            return

        self.stateNumber += 1
        self.states.append(self.forwardStates.pop())
        self.show()

    def processAndShowImg(self, algorithm, prompt, params=None):
        if len(self.states) == 0:
            self.view.promptSelectImage()
            return

        try:
            img = self.states[-1]
            newImg = algorithm(img, params)
            self.states.append(newImg)
            self.show()
            self.stateNumber += 1
        except Exception as e:
            prompt()

    def show(self):
        if len(self.states) > 0:
            self.view.setImage(cv2.cvtColor(self.states[-1], cv2.COLOR_BGR2RGB))

        if len(self.states) > 1:
            cv2.imshow(str(len(self.states)), self.states[-2])

    def exportImage(self):
        fileName = self.view.selectSaveImage()

        if fileName == "":
            return

        if not self.states:
            return

        try:
            cv2.imwrite(fileName, self.states[-1])
        except:
            self.view.promptSaveFormat()

    def closeImages(self):
        cv2.destroyAllWindows()

    # <-- OPERATIONS -->
    def convertToGray(self):
        self.processAndShowImg(toGray, self.view.operationFailed)

    def erode(self):
        try:
            width = getInput(self.view.erodeText, strElementValidator, int, self.view.promptGaussValue)
            self.processAndShowImg(erode, self.view.operationFailed, width)
        except:
            pass

    def mOpen(self):
        try:
            width = getInput(self.view.openText, strElementValidator, int, self.view.promptGaussValue)
            self.processAndShowImg(mOpen, self.view.operationFailed, width)
        except:
            pass

    def mClose(self):
        try:
            width = getInput(self.view.closeText, strElementValidator, int, self.view.promptGaussValue)
            self.processAndShowImg(mClose, self.view.operationFailed, width)
        except:
            pass

    def dilate(self):
        try:
            width = getInput(self.view.dilateText, strElementValidator, int, self.view.promptGaussValue)
            self.processAndShowImg(dilate, self.view.operationFailed, width)
        except:
            pass

    def skeletonize(self):
        try:
            neighbourHood = getInput(self.view.skeletonizationText, neighbourhoodValidator, Utils.arrayIntParser, self.view.promptNeighbourhood)
            self.processAndShowImg(skeletonize, self.view.operationFailedSkeletonize, neighbourHood)
        except:
            pass

    def threshHoldOtsu(self):
        self.processAndShowImg(thresholdOtsu, self.view.operationFailedOtsu)

    def threshHold(self):
        try:
            threshold = getInput(self.view.thresholdText, thresholdValidator, int, self.view.promptThresholdValue)
            self.processAndShowImg(thresholdManual, self.view.operationFailed, threshold)
        except:
            pass

    def resize(self):

        width = getInput(self.view.resizeText, resizeValidator, int, self.view.promptResizeValue)
        self.processAndShowImg(resize, self.view.operationFailed, width)

    def invert(self):
        self.processAndShowImg(invert, self.view.operationFailed)

    def gauss(self):
        try:
            width = getInput(self.view.gaussText, strElementValidator, int, self.view.promptGaussValue)
            self.processAndShowImg(gauss, self.view.operationFailed, width)
        except:
            pass


def getInput(textElement, validator, caster, prompt):
    text = textElement.get()
    if validator(text, caster):
        return caster(text)
    else:
        prompt()
        raise Exception()
