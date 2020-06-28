from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from Controller import Controller
from PIL import Image, ImageTk
import numpy as np


class View(Tk):

    def __init__(self):
        super(View, self).__init__()

        self.controller = Controller(self)
        self.originalImg = None
        self.states = []

        self.title("Skeletonization")
        self.configure(background="white")
        self.minsize(900, 600)

        self.frame = Frame(self, bg="grey")
        self.frame.pack(expand=True, fill="both")

        # top edit
        topFrame = LabelFrame(self.frame, text="Edit")
        topFrame.pack(padx=10, pady=10, fill="x")

        browseFileFrame = LabelFrame(topFrame, text="Open image", labelanchor="n")
        browseFileFrame.pack(padx=10, pady=10, side=LEFT)

        browseFileBtn = Button(browseFileFrame, text="Browse a File", command=self.controller.selectImage)
        browseFileBtn.pack(fill="x")

        undoRedoFrame = LabelFrame(topFrame, text="Undo/Redo", labelanchor="n")
        undoRedoFrame.pack(padx=10, pady=10, side=LEFT)

        backwardBtn = Button(undoRedoFrame, text="<", command=self.controller.back)
        backwardBtn.pack(padx=10, pady=10, side=LEFT)

        forwardBtn = Button(undoRedoFrame, text=">", command=self.controller.forward)
        forwardBtn.pack(padx=10, pady=10, side=RIGHT)

        closeImagesFrame = LabelFrame(topFrame, text="Close all windows", labelanchor="n")
        closeImagesFrame.pack(padx=10, pady=10, side=LEFT)

        closeImagesBtn = Button(closeImagesFrame, text="X", command=self.controller.closeImages)
        closeImagesBtn.pack(padx=10, pady=10, expand=True, fill="x", side=LEFT)

        exportImagesFrame = LabelFrame(topFrame, text="Export current image", labelanchor="n")
        exportImagesFrame.pack(padx=10, pady=10, side=LEFT)

        exportImageButton = Button(exportImagesFrame, text="Export", command=self.controller.exportImage)
        exportImageButton.pack(padx=10, pady=10, expand=True, fill="x", side=LEFT)



        # operations
        self.operationsPanel = LabelFrame(self.frame, text="Operations")
        self.operationsPanel.pack(padx=10, pady=10, side=LEFT, anchor=N)

        firstColumnOperations = Frame(self.operationsPanel)
        firstColumnOperations.pack(side=LEFT)

        secondColumnOperations = Frame(self.operationsPanel)
        secondColumnOperations.pack(side=TOP)

        self.resizeText = self.initOperation(firstColumnOperations, "Resize", True, self.controller.resize, "400")
        self.initOperation(firstColumnOperations, "Convert to grayscale", False, self.controller.convertToGray)
        self.initOperation(firstColumnOperations, "Invert", False, self.controller.invert)
        self.initOperation(firstColumnOperations, "Otsu threshold", False, self.controller.threshHoldOtsu)
        self.thresholdText = self.initOperation(firstColumnOperations, "Threshold", True, self.controller.threshHold, "127")
        self.dilateText = self.initOperation(firstColumnOperations, "Dilate", True, self.controller.dilate, "3")

        self.erodeText = self.initOperation(secondColumnOperations, "Erode", True, self.controller.erode, "3")
        self.openText = self.initOperation(secondColumnOperations, "Open", True, self.controller.mOpen, "3")
        self.closeText = self.initOperation(secondColumnOperations, "Close", True, self.controller.mClose, "3")
        self.gaussText = self.initOperation(secondColumnOperations, "Gaussian blur", True, self.controller.gauss, "5")
        self.skeletonizationText = self.initOperation(secondColumnOperations, "Skeletonize", True, self.controller.skeletonize, "4, 8")

        # canvas
        self.currentImage = ImageTk.PhotoImage(Image.fromarray(np.ones((250, 350))*255))
        currentImageParent = LabelFrame(self.frame, text="Current Image")
        currentImageParent.pack(padx=10, pady=10, side=TOP)
        self.canvas = Canvas(currentImageParent, width=350, height=250)
        self.canvas.pack()
        self.imageArea = self.canvas.create_image(0, 0, anchor=NW, image=self.currentImage)


        #self.controller.selectImage()
        #self.controller.resize()
        #self.controller.convertToGray()
        #self.controller.invert()
        #self.controller.threshHoldOtsu()
        #self.controller.closeImages()
        #self.controller.skeletonize()


        mainloop()

    def initTextInput(self, parent, placeholder):
        textEntry = ttk.Entry(parent)
        textEntry.pack(fill="x")
        textEntry.insert(0, placeholder)
        return textEntry

    def initOperation(self, parent, labelText, hasInput, operation, placeholder=""):
        labelFrame = LabelFrame(parent, text=labelText)
        labelFrame.pack(padx=10, pady=10, fill="x")

        button = Button(labelFrame, text="Apply", command=operation)
        button.pack(fill="x")

        inputField = self.initTextInput(labelFrame, placeholder)
        if not hasInput:
            inputField.config(state='disabled')

        return inputField

    def selectOpenImage(self):
        fileName = filedialog.askopenfilename(initialdir="/", title="Select A File")

        if fileName != "":
            self.title("Skeletonization - " + "<" + fileName + ">")
        else:
            self.title("Skeletonization - " + "<path not selected>")

        return fileName

    def selectSaveImage(self):
        fileName = filedialog.asksaveasfilename(initialdir="/", title="Select A File")
        return fileName

    def setImage(self, img):
        self.currentImage = ImageTk.PhotoImage(Image.fromarray(img))
        self.canvas.config(width=img.shape[1], height=img.shape[0])
        self.canvas.itemconfigure(self.imageArea, image=self.currentImage)

    def promptSelectImage(self):
        mb.showwarning("No image", "No image selected, please select one.")

    def promptThresholdValue(self):
        mb.showwarning("Wrong number format", "Threshold can only be an integer number in range <0, 255>.")

    def promptResizeValue(self):
        mb.showwarning("Wrong number format", "Width must be a positive integer.")

    def promptGaussValue(self):
        mb.showwarning("Wrong number format", "Width must be an odd positive integer.")

    def promptSaveFormat(self):
        mb.showwarning("Save failure", "Make sure that the saved image ends with a specified format.")

    def promptNeighbourhood(self):
        mb.showwarning("Wrong number format", "Neighbourhood can only be 4 or 8.")

    def operationFailed(self):
        mb.showwarning("Operation failed", "This operation failed.")

    def operationFailedOtsu(self):
        mb.showwarning("Operation fail", "This operation failed. Make sure that the image is converted to grayscale.")

    def operationFailedSkeletonize(self):
        mb.showwarning("Operation fail", "This operation failed. Make sure that the image is binarized with thresholding.")