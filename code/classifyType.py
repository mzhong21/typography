import LoadTrainingData as ltd
import tesseract
import cv2.cv as cv
import ast
import itertools
import math

def loadTrainingData():
    training = open("training.txt", "r")
    trainingDict = ast.literal_eval(training.readline().strip())
    return trainingDict
def getPixelDistribution(pixelPaths):
    pixelPathBlack = pixelPaths[0.0]
    horDistr = {}
    pixelHorPos = sorted(pixelPathBlack, key=lambda tup:tup[1])
    minHor = pixelHorPos[0][1]
    maxHor = pixelHorPos[-1][1]
    for i in range(maxHor-minHor+1):
        horDistr[i] = 0
    for pos in pixelHorPos:
        horDistr[pos[1]-minHor] += 1
    return horDistr
def compareDistributions(testPixelDistr, trainPixelDistr):
    minTest = min(testPixelDistr)
    maxTest = max(testPixelDistr)
    minTrain = min(trainPixelDistr)
    maxTrain = max(trainPixelDistr)
    slope = float(maxTrain-minTrain)/(maxTest-minTest)
    testData = []
    trainData = []
    for i in range(maxTest):
        if i % 2 == 0:
            endPoint = math.floor(slope*(i+2))
            begPoint = math.floor(slope*(i))
            if endPoint > maxTrain or i+2 > maxTest:
                break
            if testPixelDistr[i+2] == 0 or testPixelDistr[i] == 0:
                continue
            if trainPixelDistr[endPoint] == 0 or trainPixelDistr[begPoint] == 0:
                continue
            testData.append(float(testPixelDistr[i+2])/testPixelDistr[i])
            trainData.append(float(trainPixelDistr[endPoint])/trainPixelDistr[begPoint])
    counter = 0
    sum = 0
    for test, train in itertools.izip(testData,trainData):
        sum += math.fabs(train-test)
        counter += 1
    return sum/counter
                    

trainingData = loadTrainingData()

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)

images = ["arial48", "baskervilleoldface48", "georgia48", "idealsansbook48", "minionpro48",
          "timesnewroman48", "verdana48", "timestest", "verdana1", "arial1", "idealsansbook1", 
          "baskerville1", "verdana2", "georgia1", "timesnewroman1"]
for item in images:
    address = "./test/" + item + ".png"
    image = ltd.loadGrayImage(address)
    tesseract.SetCvImage(image,api)
    
    text=api.GetUTF8Text()
    letterAndCoords=api.GetBoxText(1)
    letterAndCoords = letterAndCoords.split("\n")
    letterAndCoords = [info.split() for info in letterAndCoords]
    height = image.height
    testData = []
    
    for info in letterAndCoords:
        if len(info) > 1:
            left = int(info[1])-1
            top = height - int(info[4]) - 1
            subHeight = int(info[4]) - int(info[2])+2
            subWidth = int(info[3])-int(info[1])+2
            testData.append((info[0],cv.GetSubRect(image, (left, top,subWidth, subHeight))))
    #test data contains [(character,image),...] of character
    #training data contains {character: [(type, horDistr, vertDistr), ...], ...}
    typeOccurances = {}
    for charAndImage in testData:
        char = charAndImage[0]
        image = charAndImage[1]
        pixelPaths = ltd.getPixelPaths(image)
        testPixelDistr = getPixelDistribution(pixelPaths)
        bestType = 0
        lowestAverage = 1000000000000000
        if char.isalnum() == True:
            for types in trainingData[char]:
                avg = compareDistributions(testPixelDistr, types[1])
                if avg < lowestAverage:
                    bestType = types[0]
                    lowestAverage = avg
        if lowestAverage > 0.4:
            continue
        if bestType not in typeOccurances:
            typeOccurances[bestType] = 1
        else:
            typeOccurances[bestType] += 1
    bestType = 0
    highestCount = 0
    for type in typeOccurances:
        if typeOccurances[type] > highestCount:
            highestCount = typeOccurances[type]
            bestType = type
    print bestType