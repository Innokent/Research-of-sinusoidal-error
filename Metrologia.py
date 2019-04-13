import pylab
import math
import random

N = 100 # Кол-во измерений
Fmax = 1 # Максимальное значение функции
Fmin = 0 # Минимальное значение функции
quality = 4 # Кол-во знаков после запятой
tav = 1  # Константа
maxVariance = 0.025 # Максимальное допустимое отклонение критериев
generationCount = 100 # Кол-во раз, которое выполняется основной цикл программы
maxIterationCount = 20 # Кол-во изменений каждого коэфицента синусоиды
referenceT1 = 0 # Эталонное значение
referenceT2 = 0 # Эталонное значение
referenceT3 = 0 # Эталонное значение
referenceT4 = 0 # Эталонное значение

valueF = []
valueT1 = []
valueT2 = []
valueT3 = []
valueT4 = []

for i in range(N):
	valueF += [0.0]
	valueT1 += [0.0]
	valueT2 += [0.0]
	valueT3 += [0.0]
	valueT4 += [0.0]

def Average(n, fList): # Среднее значение первых 'n' значений функции
	amount = 0.0
	result = 0.0
	for i in range(n):
		amount = amount + fList[i]
	result = amount / n
	return result


def S(n, fList): # Среднеквадратическое отклонение
	result = 0.0;
	for i in range(n):
		result += (fList[i] - Average(n, fList)) ** 2
	result /= 1 - n
	result = math.fabs(result)	
	result = math.sqrt(result)
	return result

def D(n, fList): # Дисперсия
	return tav * S(n, fList) / math.sqrt(n)

def T1(n, fList): # Критерий колебаний среднего
	return (Average(n, fList) - Average(n + 1, fList)) / Average (n, fList)

def T2(n, fList): # Критерий приращения колебаний среднего 	
	return T1(n, fList) - T1(n + 1, fList)

def T3(n, fList): # Критерий колебания среднеквадратического
	return (S(n, fList) - S(n + 1, fList)) / S(n, fList)

def T4(n, fList): # Критерий приращения колебаний среднего квадратического
	return (D(n, fList) - D(n + 1, fList)) / D(n, fList)

def clearAllArray(): # Выделение места и очистка памяти 
	global valueF
	global valueT1
	global valueT2
	global valueT3
	global valueT4

	for i in range(N):
		valueF[i] = [0.0]
		valueT1[i] = [0.0]
		valueT2[i] = [0.0]
		valueT3[i] = [0.0]
		valueT4[i] = [0.0]

def initF(): # Заполнение массива значений функции нецелыми значениями
	for i in range(N):
		valueF[i] = random.uniform(Fmin, Fmax)

def initSinusoid():
	k1 = random.uniform(0, (Fmax - Fmin) / 2)
	k2 = random.uniform(0, math.sqrt(maxIterationCount))
	sinusoid = []
	for j in range(N):
		sinusoid += [k1 * math.sin(k2 * i)]
	print("Current sinusoid: K1=", k1, " K2=", k2)
	return sinusoid

def initCriteria(fList): # Заполнение значений критериев
	vT1 = []
	vT2 = []
	vT3 = []
	vT4 = []

	for i in range (N-2):
		vT1 += [0.0]
		vT2 += [0.0]
		vT3 += [0.0]
		vT4 += [0.0]
	for i in range(N - 4):
		vT1[i + 2] = T1(i + 2, fList)
		vT2[i + 2] = T2(i + 2, fList)
		vT3[i + 2] = T3(i + 2, fList)
		vT4[i + 2] = T4(i + 2, fList)
	return [vT1, vT2, vT3, vT4]

def showGraphics(sourceFuncList, sourceCriteria, currentFuncList, currentCriteria, k1, k2): # Рисуем графики для критериев
	n_list = [i + 2 for i in range(N - 4)]
	x_list = [i for i in range(N)]
	sin_x_list = [i * (N - 0) / (N * N) for i in range(N * N)]
	sin_y_list = [k1 * math.sin(k2 * x) + (Fmax + Fmin) / 2 for x in sin_x_list]
	T1_list = [sourceCriteria[0][i] for i in n_list]
	T2_list = [sourceCriteria[1][i] for i in n_list]
	T3_list = [sourceCriteria[2][i] for i in n_list]
	T4_list = [sourceCriteria[3][i] for i in n_list]

	newT1_list = [currentCriteria[0][i] for i in n_list]
	newT2_list = [currentCriteria[1][i] for i in n_list]
	newT3_list = [currentCriteria[2][i] for i in n_list]
	newT4_list = [currentCriteria[3][i] for i in n_list]

	varianceTopListX = [0, N]
	varianceTopListY = [maxVariance, maxVariance]
	varianceDownListX = [0, N]
	varianceDownListY = [-maxVariance, -maxVariance]

	pylab.figure(1)
	pylab.subplot(3, 2, 3)
	pylab.plot(n_list, T1_list)
	pylab.plot(varianceTopListX, varianceTopListY, '--r')
	pylab.plot(varianceDownListX, varianceDownListY, '--r')
	pylab.title("Criterion T1")

	pylab.figure(1)
	pylab.subplot(3, 2, 4)
	pylab.plot(n_list, T2_list)
	pylab.plot(varianceTopListX, varianceTopListY, '--r')
	pylab.plot(varianceDownListX, varianceDownListY, '--r')
	pylab.title("Criterion T2")

	pylab.figure(1)
	pylab.subplot(3, 2, 5)
	pylab.plot(n_list, T3_list)
	pylab.plot(varianceTopListX, varianceTopListY, '--r')
	pylab.plot(varianceDownListX, varianceDownListY, '--r')
	pylab.title("Criterion T3")

	pylab.figure(1)
	pylab.subplot(3, 2, 6)
	pylab.plot(n_list, T4_list)
	pylab.plot(varianceTopListX, varianceTopListY, '--r')
	pylab.plot(varianceDownListX, varianceDownListY, '--r')
	pylab.title("Criterion T4")

	pylab.figure(1)
	pylab.subplot(3, 1, 1)
	pylab.plot(x_list, sourceFuncList)
	pylab.title("Function")

	pylab.figure(2)
	pylab.subplot(3, 2, 3)
	pylab.plot(n_list, newT1_list)
	pylab.plot(varianceTopListX, varianceTopListY, '--r')
	pylab.plot(varianceDownListX, varianceDownListY, '--r')
	pylab.title("Criterion T1")

	pylab.figure(2)
	pylab.subplot(3, 2, 4)
	pylab.plot(n_list, newT2_list)
	pylab.plot(varianceTopListX, varianceTopListY, '--r')
	pylab.plot(varianceDownListX, varianceDownListY, '--r')
	pylab.title("Criterion T2")

	pylab.figure(2)
	pylab.subplot(3, 2, 5)
	pylab.plot(n_list, newT3_list)
	pylab.plot(varianceTopListX, varianceTopListY, '--r')
	pylab.plot(varianceDownListX, varianceDownListY, '--r')
	pylab.title("Criterion T3")

	pylab.figure(2)
	pylab.subplot(3, 2, 6)
	pylab.plot(n_list, newT4_list)
	pylab.plot(varianceTopListX, varianceTopListY, '--r')
	pylab.plot(varianceDownListX, varianceDownListY, '--r')
	pylab.title("Criterion T4")

	pylab.figure(2)
	pylab.subplot(3, 1, 1)
	pylab.plot(x_list, currentFuncList)
	pylab.title("New function")
	
	pylab.figure(3)
	pylab.plot(sin_x_list, sin_y_list, 'r')
	pylab.plot(x_list, sourceFuncList)
	pylab.title("Sinusoid")

	pylab.show()

def searchVariance(criteriaList):
	isFirstT1 = True
	isFirstT2 = True
	isFirstT3 = True
	isFirstT4 = True
	indexT1 = 0
	indexT2 = 0
	indexT3 = 0
	indexT4 = 0

	for i in range(N - 4):
		if((math.fabs(criteriaList[0][N - i - 3]) > maxVariance) and (isFirstT1)):
			indexT1 = N - i - 3
			isFirstT1 = False
		if((math.fabs(criteriaList[1][N - i - 3]) > maxVariance) and (isFirstT2)):
			indexT2 = N - i - 3
			isFirstT2 = False
		if((math.fabs(criteriaList[2][N - i - 3]) > maxVariance) and (isFirstT3)):
			indexT3 = N - i - 3
			isFirstT3 = False
		if((math.fabs(criteriaList[3][N - i - 3]) > maxVariance) and (isFirstT4)):
			indexT4 = N - i - 3
			isFirstT4 = False

	#print("T1 ", indexT1)
	#print("T2 ", indexT2)
	#print("T3 ", indexT3)
	#print("T4 ", indexT4)

	return [indexT1, indexT2, indexT3, indexT4]

indexList = []
criteria = []
averageIndexT1 = 0.0
averageIndexT2 = 0.0
averageIndexT3 = 0.0
averageIndexT4 = 0.0

for i in range(generationCount):
	clearAllArray()
	initF()
	criteria = initCriteria(valueF)
	indexList = searchVariance(criteria)
	averageIndexT1 += indexList[0]
	averageIndexT2 += indexList[1]
	averageIndexT3 += indexList[2]
	averageIndexT4 += indexList[3]

averageIndexT1 /= generationCount
averageIndexT2 /= generationCount
averageIndexT3 /= generationCount
averageIndexT4 /= generationCount

referenceT1 = round(averageIndexT1)
referenceT2 = round(averageIndexT2)
referenceT3 = round(averageIndexT3)
referenceT4 = round(averageIndexT4)

output = open("output.txt", "w")


def main():
	clearAllArray()

	initF()
	criteria = initCriteria(valueF)
	indexList = searchVariance(criteria)
	currentMinVariance = (indexList[0] - referenceT1) ** 2 + (indexList[1] - referenceT2) ** 2 + (indexList[2] - referenceT3) ** 2 + (indexList[3] - referenceT4) ** 2

	output.write(str(currentMinVariance) + " ")
	print("Reference: ", referenceT1, referenceT2, referenceT3, referenceT4)
	print("Source squareVariance", currentMinVariance)
	print("Source", indexList)
	
	#mySinusoid = initSinusoid()
	#for i in range(N):
	#	valueF[i] += mySinusoid[i]
	
	#criteria = initCriteria(valueF)
	#indexList = searchVariance(criteria)
	#currentMinVariance = (indexList[0] - referenceT1) ** 2 + (indexList[1] - referenceT2) ** 2 + (indexList[2] - referenceT3) ** 2 + (indexList[3] - referenceT4) ** 2
	
	#output.write(str(currentMinVariance) + " ")
	#print("Source squareVariance with sinusiod", currentMinVariance)
	#print("Source with sinusiod", indexList)
	
	firstCoefficent = 0
	secondCoefficent = 0
	#showGraphics(valueF, criteria, valueF, criteria, firstCoefficent, secondCoefficent)
	
	for i in range(maxIterationCount):
		k1 = i * ((Fmax - Fmin) / (2 * (maxIterationCount - 1)))
	
		for j in range(maxIterationCount):
			k2 = j * ((math.sqrt(maxIterationCount) - 1) / (maxIterationCount - 1)) + 1
			sinusoid = [k1 * math.sin(k2 * x) for x in range(N)]
			newF = [valueF[k] - sinusoid[k] for k in range(N)]
	
			newCriteria = initCriteria(newF)
			currentCriteria = searchVariance(newCriteria)
			squareVariance = (currentCriteria[0] - referenceT1) ** 2 + (currentCriteria[1] - referenceT2) ** 2 + (currentCriteria[2] - referenceT3) ** 2 + (currentCriteria[3] - referenceT4) ** 2
	
			if((squareVariance < currentMinVariance) or (currentMinVariance < 0)):
				currentMinVariance = squareVariance
				firstCoefficent = k1
				secondCoefficent = k2
	
	sinusoid = [firstCoefficent * math.sin(secondCoefficent * x) for x in range(N)]
	newF = [valueF[k] - sinusoid[k] for k in range(N)]
	
	output.write(str(currentMinVariance) + "\n")
	print("Current squareVariance", currentMinVariance)
	print("k1 = ", firstCoefficent, "; k2 = ", secondCoefficent)
	newCriteria = initCriteria(newF)
	print("Current", searchVariance(newCriteria))
	
	#showGraphics(valueF, criteria, newF, newCriteria, firstCoefficent, secondCoefficent)
	
for i in range(100):
	print("===================================================================================================")	
	print("CURRENT ITTERATION IS ", i + 1)
	main()
	print("===================================================================================================")

output.close()
	
