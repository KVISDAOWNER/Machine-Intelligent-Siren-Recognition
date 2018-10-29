from sklearn.linear_model import LogisticRegression
from scipy.io import wavfile
import numpy as np
CONST_CLIPSIZE = 288193 #shortest clip contains this number of samples

def SetSize():


	#Række af for loops til at sørge for alle input listerne har samme size
	for x in range(CONST_CLIPSIZE):
		arSirene1.append(fssir1[x])

	for x in range(CONST_CLIPSIZE):
		arSirene2.append(fssir2[x])

	for x in range(CONST_CLIPSIZE):
		arSirene3.append(fssir3[x])

	for x in range(CONST_CLIPSIZE):
		arSirene4.append(fssir4[x])

	for x in range(CONST_CLIPSIZE):
		arSirene5.append(fssir5[x])

	for x in range(CONST_CLIPSIZE):
		arBirds.append(fsBirds[x])

	for x in range(CONST_CLIPSIZE):
		arRandAndThunder.append(fsRainAndThunder[x])

	for x in range(CONST_CLIPSIZE):
		arConstruction.append(fsConstruction[x])
		



#Opens filestreams
datasir1, fssir1 = wavfile.read("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\Sirene41.wav")
datasir2, fssir2 = wavfile.read("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\Sirene42.wav")
datasir3, fssir3 = wavfile.read("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\Sirene43.wav")
datasir4, fssir4 = wavfile.read("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\Sirene44.wav")
datasir5, fssir5 = wavfile.read("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\Sirene45.wav")
dataBirds, fsBirds = wavfile.read("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\Birds.wav")
dataRaindAndThunder, fsRainAndThunder = wavfile.read("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\RainAndThunder.wav")
dataConstruction, fsConstruction = wavfile.read("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\Construction.wav")

#list for holding all the filestreams, currently not in use
ArrList = [fssir1,fssir2,fssir3,fssir4,fssir5,fsBirds,fsRainAndThunder,fsConstruction] 

#Lists for all the different filestreams with their datapoints
arSirene1 = []
arSirene2 = []
arSirene3 = []
arSirene4 = []
arSirene5 = []
arBirds = []
arRandAndThunder = []
arConstruction = []

SetSize()

X = [arSirene1, arSirene2, arSirene3, arBirds, arRandAndThunder] #training
Y = [[True], [True], [True], [False], [False]] #Training answers
Z = [arSirene4, arSirene5, arConstruction] #Test

LR = LogisticRegression(solver='liblinear')
LR.fit(X,Y)

prediction = LR.predict(Z)
print(prediction)