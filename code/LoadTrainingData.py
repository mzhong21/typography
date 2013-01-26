import math
import cv2.cv as cv

COLOR_DIFF = 16
BLACK = 0.0
typographies = ["idealsansbook", "timesnewroman", "arial", "georgia", "minionpro", "verdana","baskerville"]
capitalLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowerLetters = "abcdefghijklmnopqrstuvwxyz"
numbers = "1234567890"

def loadGrayImage(image):
    grayImage = cv.LoadImage(image, cv.CV_LOAD_IMAGE_GRAYSCALE)
    return grayImage

def getPixelPaths(image):
    width = image.width
    height = image.height
    pixelPaths = {}
    #store all pixel paths
    for i in range(1, width):
        for j in range(1,height):
            discoveredSimPixel = False
            for key in pixelPaths:
                if math.fabs(key - image[j,i]) < COLOR_DIFF:
                    pixelPaths[key].append((j,i))
                    discoveredSimPixel = True
                    break
            if discoveredSimPixel == False:
                pixelPaths[image[j,i]] = [(j,i)]
    return pixelPaths

def getTrainingData():
    trainingData = {}
    for type in typographies:
        for capital in capitalLetters:
            location = "./fonts/" + type + "/capital/" + capital + ".png"
            image = loadGrayImage(location)
            pixelPath = getPixelPaths(image)
            if capital not in trainingData:
                trainingData[capital] = [(type,pixelPath[BLACK])]
            else:
                trainingData[capital].append((type, pixelPath[BLACK]))
        for lower in lowerLetters:
            location = "./fonts/" + type + "/lower/" + lower + ".png"
            image = loadGrayImage(location)
            pixelPath = getPixelPaths(image)
            if lower not in trainingData:
                trainingData[lower] = [(type,pixelPath[BLACK])]
            else:
                trainingData[lower].append((type, pixelPath[BLACK]))
        for num in numbers:
            location = "./fonts/" + type + "/numeric/" + num + ".png"
            image = loadGrayImage(location)
            pixelPath = getPixelPaths(image)
            if num not in trainingData:
                trainingData[num] = [(type,pixelPath[BLACK])]
            else:
                trainingData[num].append((type, pixelPath[BLACK]))
    return trainingData
def getPixelDistributions(trainingData):
    pixelDistributions = {}
    
    for character in trainingData:
        for typeData in trainingData[character]:
            horDistr = {}
            vertDistr = {}
            pixelHorPosition = sorted(typeData[1], key=lambda tup:tup[1])
            pixelVertPosition = sorted(typeData[1], key=lambda tup:tup[0])
            minHor = pixelHorPosition[0][1]
            maxHor = pixelHorPosition[-1][1]
            for i in range(maxHor-minHor+1):
                horDistr[i] = 0
            for pos in pixelHorPosition:
                horDistr[pos[1]-minHor] += 1
            minVert = pixelVertPosition[0][0]
            maxVert = pixelVertPosition[-1][0]
            for j in range(maxVert-minVert+1):
                vertDistr[j] = 0
            for pos in pixelVertPosition:
                vertDistr[pos[0]-minVert] += 1
            distribution = (typeData[0], horDistr, vertDistr)
            if character in pixelDistributions:
                pixelDistributions[character].append(distribution)
            else:
                pixelDistributions[character] = [distribution]
    return pixelDistributions
def main():           
    trainingFile = open("training.txt", "w")
    trainingData = getTrainingData()
    
    pixelDistributions = getPixelDistributions(trainingData)
    
    trainingFile.write(str(pixelDistributions))
    trainingFile.close()

if __name__ == "__main__":
    main()
        
    