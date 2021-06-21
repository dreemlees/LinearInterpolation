### Данная программа является маленькой утилитой, написанной Яном Малявко(a.k.a. congerian), 
### студентом первого курса факультета физики ввиду отсутствия какой-либо готовой подобной утилиты.

### Пользуйтесь на здоровье!

### TODO: Прогонять файлы в один заход
### TODO: Добавить рассчёт ошибки округления




import sys, getopt, os, ctypes, re, math

#Цветооооочки:

#Врубаем поддержку цветооооочков для винды:
if(os.name == 'nt'):
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def makeColored(str, clr):
    return clr + str + bcolors.ENDC

#Немного переменных по кайфу:

inputFileName1 = ''
inputFileName2 = ''
outputFileName = ''

inputFile1 = None
inputFile2 = None
outputFile = None

#Парсим вход:

def main(argv):
    global inputFileName1, inputFileName2, outputFileName

    _IFN1_defined = False
    _IFN2_defined = False
    _OFN_defined = False

    try:
        opts, args = getopt.getopt(argv, "", ["ifile1=", "ifile2=", "ofile="])
    
    except getopt.GetoptError:
        print (makeColored( 'Неправильное использование команды. Используйте: \n'
                            'test.py -ifile1=<inputFile1> -ifile2=<inputFile2> -ofile=<outputFile>', bcolors.FAIL))
    
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("--ifile1"):
            inputFileName1 = arg
            _IFN1_defined = True
        elif opt in ("--ifile2"):
            inputFileName2 = arg
            _IFN2_defined = True
        elif opt in ("--ofile"):
            outputFileName = arg
            _OFN_defined = True

    if( 
        not _IFN1_defined or 
        not _IFN2_defined or
        not _OFN_defined
    ):
        print (makeColored( 'Неправильное использование команды. Используйте: \n'
                            'test.py -ifile1=<inputFile1> -ifile2=<inputFile2> -ofile=<outputFile>', bcolors.FAIL))
    
        sys.exit(2)    

    print (makeColored('Запарсили названия файлов, продолжаем...', bcolors.OKGREEN))

if __name__ == "__main__":
    main(sys.argv[1:])

#Пробуем открыть и создать файлы:
def openFiles():
    global inputFile1, inputFile2, outputFile

    try:
        inputFile1 = open(inputFileName1, 'r')
    except IOError:
        print(makeColored('Не удалось открыть первый входной файл!', bcolors.FAIL))
        sys.exit(2)

    try:
        inputFile2 = open(inputFileName2, 'r')
    except IOError:
        print(makeColored('Не удалось открыть второй входной файл!', bcolors.FAIL))
        sys.exit(2)

    try:
        outputFile = open(outputFileName, 'w')
    except IOError:
        print(makeColored('Не удалось создать/открыть выходной файл!', bcolors.FAIL))
        sys.exit(2)

    print (makeColored('Открыли файлы, продолжаем...', bcolors.OKGREEN))

openFiles()

xMin1 = None
xMax1 = None
xMin2 = None
xMax2 = None

#Проверяем, что они не пустые и присваиваем заодно min/max по иксу, также проверяем, что число столбцов совпадает:

def checkFiles():
    global xMin1, xMax1, xMin2, xMax2

    cols1 = 0
    cols2 = 0

    _empty1 = True
    _empty2 = True

    for line in inputFile1:
        if (line[0] == '#'):
            continue
        _empty1 = False
        xMin1 = float(re.split(' |\t', line)[0])
        xMax1 = float(re.split(' |\t', line)[0])
        cols1 = len(re.split(' |\t', line))
        break

    for line in inputFile2:
        if (line[0] == '#'): 
            continue
        _empty2 = False
        xMin2 = float(re.split(' |\t', line)[0])
        xMax2 = float(re.split(' |\t', line)[0])
        cols2 = len(re.split(' |\t', line))
        break 

    if(_empty1):
        print(makeColored('Первый файл не содержит точек!', bcolors.FAIL))
        sys.exit(2)

    if(_empty2):
        print(makeColored('Второй файл не содержит точек!', bcolors.FAIL))
        sys.exit(2)

    if(cols1 != cols2):
        print(makeColored('Число столбцов в файлах не совпадает!', bcolors.FAIL))
        sys.exit(2)

    print (makeColored('Оба файла содержат точки, продолжаем...', bcolors.OKGREEN))

    inputFile1.seek(0)
    inputFile2.seek(0)

checkFiles()

#Находим границы интервалов по иксу:

xMin = None
xMax = None

def findBorders():
    global xMin1, xMax1, xMin2, xMax2, xMin, xMax

    for line in inputFile1:
        if (line[0] == '#'):
            continue
        t = float((re.split(' |\t', line)[0]))
        if (xMin1 > t):
            xMin1 = t
        elif (xMax1 < t):
            xMax1 = t

    for line in inputFile2:
        if (line[0] == '#'):
            continue
        t = float((re.split(' |\t', line)[0]))
        if (xMin2 > t):
            xMin2 = t
        elif (xMax2 < t):
            xMax2 = t
    
    if(xMin1 <= xMin2):
        if(xMax1 < xMin2):
            print(makeColored('Интервал иксов в файлах не пересекаются!', bcolors.FAIL))
            sys.exit(2)
        else:
            xMin = xMin2
            xMax = min(xMax1, xMax2)
    else:
        if(xMax2 < xMin1):
            print(makeColored('Интервал иксов в файлах не пересекаются!', bcolors.FAIL))
            sys.exit(2)
        else:
            xMin = xMin1
            xMax = min(xMax1, xMax2)

    if(xMax == xMin):
        print(makeColored('Интервал иксов представляет из себя одну точку!', bcolors.FAIL))
        sys.exit(2)
    else:
        print(makeColored('Общий интервал иксов найден!', bcolors.OKGREEN))
        print('xMin:', xMin, 'xMax:', xMax)
        
    inputFile1.seek(0)
    inputFile2.seek(0)

findBorders()

#Находим файл, в котором точек в заданном интервале больше, и приравниваем его inputFile1:

def findBiggerFile():
    global inputFile1, inputFile2

    count1 = 0
    count2 = 0

    for line in inputFile1:
        if (line[0] == '#'):
            continue
        t = float((re.split(' |\t', line)[0]))
        if (xMin <= t):
            if(t <= xMax):
                count1 = count1 + 1
            else:
                break

    for line in inputFile2:
        if (line[0] == '#'):
            continue
        t = float((re.split(' |\t', line)[0]))
        if (xMin <= t):
            if(t <= xMax):
                count2 = count2 + 1
            else:
                break

    print('В первом файле', count1, 'точек в заданном интервале.')
    print('Во втором файле', count2, 'точек в заданном интервале.')

    if(count1 < 3 or count2 < 3):
        print(makeColored('Слишком мало точек для интерполяции!', bcolors.FAIL))

    if(count1 < count2):
        print(makeColored('Больше точек во втором входном файле!', bcolors.OKGREEN))
        inputFile1, inputFile2 = inputFile2, inputFile1
    else:
        print(makeColored('Больше точек в первом входном файле!', bcolors.OKGREEN))
    
    inputFile1.seek(0)
    inputFile2.seek(0)

findBiggerFile()

#Погнали интерполировать:

def interpolate():
    global inputFile1, inputFile2, outputFile
    
    #Находим первую и вторую точки в заданном интервале во втором файле:

    s = inputFile2.readline()

    while(  s[0] == '#' or 
            float(re.split(' |\t', s)[0]) < xMin ):
        s = inputFile2.readline()

    d22 = (float(re.split(' |\t', s)[0]), [float(u) for u in re.split(' |\t', s)[1:]])

    s = inputFile1.readline()

    while(  s[0] == '#' or 
            float(re.split(' |\t', s)[0]) < xMin ):
        s = inputFile1.readline()
    
    d11 = (float(re.split(' |\t', s)[0]), [float(u) for u in re.split(' |\t', s)[1:]])

    for line2 in inputFile2:
        d21 = d22
        d22 = (float(re.split(' |\t', line2)[0]), [float(u) for u in re.split(' |\t', line2)[1:]])

        if(d11[0] > xMax):
            print(makeColored('Интерполяция закончена!', bcolors.OKGREEN))
            break

        if(d22[0] > xMax):
            print(makeColored('Интерполяция закончена!', bcolors.OKGREEN))
            break

        if (s[-1:] != '\n'):
            print(makeColored('Интерполяция закончена!', bcolors.OKGREEN))
            break

        if(d11[0] > d22[0]):
            continue

        while(d11[0] <= d22[0]):
            if(d11[0] >= d21[0]):
                outputFile.write(str(d11[0]) + ' ')
                
                for i in range(0, len(d11[1])-1):
                    outputFile.write(str(d11[1][i]) + ' ' + str(d21[1][i] + (d11[0]-d21[0])*(d22[1][i]-d21[1][i])/(d22[0]-d21[0])) + ' ')
                
                outputFile.write('\n')
            
            s = inputFile1.readline()
            if (s[-1:] != '\n'):
                print(makeColored('Интерполяция закончена!', bcolors.OKGREEN))
                break
            
            d11 = (float(re.split(' |\t', s)[0]), [float(u) for u in re.split(' |\t', s)[1:]])

interpolate()

outputFile.close()
