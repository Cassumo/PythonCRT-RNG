print("\n---Loading---\n")
#%%
import requests
import hashlib
import random
import matplotlib.pyplot as plt
import base64 
import time
import collections
import numpy as np
import cv2
import os
from datetime import datetime
from PIL import Image
from itertools import product
from scipy.stats import norm

#%%
def _mainS():
    global maxC, minN, maxN, baseN, new_set, filename, prng, newF, startTimeClock, endTimeClock, startTime, endTime, fTimes, dTime
    #keeps the loop running for error checking
    optionI = False
    while optionI == False:
        menu = str(input("---Menu---\n1. Load config\n2. Create a new file\n3. Load existing file\nEnter a valid number: "))
        if '0' in menu:
            #255 = white | 0 = black

            dirspl = r'C:\Users\Luc\Desktop\Python\Dissertation\splits'   #the tile function splits the images to size
            dircrt = r'C:\Users\Luc\Desktop\Python\Dissertation\crt_pics' #Original pic
            dircrp = r'C:\Users\Luc\Desktop\Python\Dissertation\crt_crop' #manualy cropped to size removing border
            dircrpg = r'C:\Users\Luc\Desktop\Python\Dissertation\crt_gray' #the cropped post processed images, used to make gray
            dirdata = r'C:\Users\Luc\Desktop\Python\Dissertation\Data'    #the dir where the data is saved
            dircrtint = r'C:\Users\Luc\Desktop\Python\Dissertation\internet_crt' #a spair directory if imgs are to be tested from another source
            for file in os.listdir(dircrp):#dir must match image.open
                img = Image.open('%s\%s' % (dircrp,file),mode='r') #mode r allows the dir to be read in binary else the permisions are denied
                imgGray = img.convert('L') #converts img to grayscale
                imgGray.save('%s\gray_%s' % (dircrpg,file),mode='r') #dir and the tile 1st dir must match
                file = ('gray_%s' % (file))
                print("Splitting: %s\%s" % (dircrpg,file))
                tile(file,dircrpg,dirspl,100) #the number at the end represents the dimensions of the splits so if 100 all splits will be 100x100
            directory = os.fsencode(dirspl)

            imgListStr = []
            data = []

            print("Colour detection:\n")
            for file in os.listdir(directory):
                print("-"*10)
                x = file.decode() #turns to a str
                print (x)
                srcImg = cv2.imread((os.path.join(dirspl,x)))#reading the image setting to a variable. os.path.join used because the file is located outside the .py location
                AColourRow = np.average(srcImg, axis=0)
                AColour = np.average(AColourRow, axis=0)
                print("Average: ", AColour[0])
                data.append(round(AColour[0])) #adding only the first element because the colour is in gray
                imgListStr.append(x)

            
            #print(imgListStr)
            datamean = round(sum(data)/len(data))
            lin = ("-"*10)
            print("%s\nAverage Colour Of All Splits:\n%s\n%s\nTotal Colour Average: %s\n%s\nSmallest Average in splits: %s\nLargest Average in splits: %s\n%s" % (lin,data,lin,datamean,lin,min(data),max(data),lin))
            _graphP(2,data,0)
            #_graphP(1,imgListStr,data)
            randli = []
            
            num0 = 0
            num1 = 0
            for x in data:
                if datamean >= x:
                    randli.append(0) # black
                    num0 += 1
                if datamean < x:
                    randli.append(1) # white
                    num1 += 1
            print(randli)
            print("Number of 0's: %s\nNumber of 1's: %s" % (num0,num1))
            _graphP(0,len(randli),randli)
            uinput = input("Save as txt? (y/n): ")
            
            if 'y' in uinput:
                defaultN = input("Save as default name? (y/n): ")
                dateTi = datetime.now()
                if 'y' in defaultN:
                    fname = ('crt-generator-data-%s' % (dateTi))
                else:
                    fname = input("Enter valid file name: ")
                fname = fname.replace(" ", "-")
                fname = fname.replace(":", ".")
                fdata = ('1.)File Time Stamp: %s\n\n2.)Crt rng bin data:\n%s\n\n3.)Average Colours from splits:\n%s\n\n4.)Split file names:\n%s' % (dateTi,randli,data,imgListStr))
                _saveF(dirdata,fname,fdata)

        if '#' in menu:
            
            srcImg = cv2.imread("Colour-Red.png")
            AColourRow = np.average(srcImg, axis=0)
            AColour = np.average(AColourRow, axis=0)
            print("Red")
            print(AColour)
           
        if '1' in menu:
            # Set Config used for loading quickly
            maxC = 869
            minN = 0
            maxN = 1
            baseN = 10
            disp = 'n'
            shaS = 'n'
            graphD = 'y'
            prng = True
            newF = 'n'
            filename = ("test.txt") # remove the comment if newF is 'y'
            _prng()
            optionI = True
        elif '2'in menu:
            prng = None
            #filename = (str(input("Enter new file name: ")) + ".txt")
            while prng == None:
                x = input("Pseudo random?\n(True/False): ").lower()
                if 't' in x:
                    prng = True
                if 'f' in x:
                    prng = False
                    baseN = int(input("What base? (2,8,10,16): "))
            maxC = int(input("Enter the max amount of numbers: "))
            minN = int(input("Enter Minimum Number: "))
            maxN = int(input("Enter Max number: "))
            loopCheck = input("Loop?\n(y/n): ")
            if 'y' in loopCheck:
                timeList = []
                prng = True
                loopCount = input("Enter loop amount: ")
                loopIter = input("Step by amount?\n(y/n): ")
                looperList = [maxC,loopCount]

                if 'y' in loopIter:
                    loopStep = int(input("Enter amount to step (int): "))#this increases the maxC by an amount each loop
                if 'n' in loopIter:
                    loopStep = 0
                #This is a manual method incase you dont want to step the same amount
                #cont = None
                #while cont != 'n':
                    #looperBits = input("Enter how many bits to generate: ")
                    #looperLoop = input("Enter how many times to loop: ")
                    #looperList.append(looperBits)
                    #looperList.append(looperLoop)
                    #cont = input("Continue?\n(y/n): ")
                while len(looperList) != 0:
                    maxC = looperList[0]
                    maxC = int(maxC)
                    del looperList[0]
                    loopAmount = looperList[0]
                    loopAmount = int(loopAmount)
                    del looperList[0]
                    while loopAmount != 0:
                        loopAmount -= 1
                        _prng()
                        dTime = endTime - startTime
                        timeList.append(dTime)
                        timeList.append(maxC)
                        #print ("Time List: \n%s\n" % (timeList))
                        print("%s| Bits Generated: %s\t| Time Taken: %s    \t|" % (loopAmount, timeList[-1] , timeList[-2])) #loopAmount is the position in the loop (0 being the final), timeList[-1] and [-2] are bits generated and time taken
                        maxC += loopStep
                timeListMaxC = timeList[::2]
                timeListG = timeList[1::2]
                _graphP(1,timeListG,timeListMaxC)
            elif 'n' in loopCheck:
                _prng()
            disp = input("Display?\n(y/n): ").lower()#might not need this or shaS or graphD if the menu above is formatted and sorted out correctly 
            #shaS = input("SHA256?\n(y/n): ").lower()
            graphD = input("Graph?\n(y/n): ").lower()
            optionI = True
        elif '3' in menu:
            filename = (str(input("Enter file name to load: ")))
            #_img()
            _load(filename)
        elif '4' in menu:
            return
    if 'y' in disp:
        print (new_set)
    #if 'y' in shaS:
        #_sha()
    if 'y' in graphD:
        gi = int(input("Which graph (0-2): "))
        if gi == 2:
            _graphP(gi,new_set,0)
            print("test")
        else:
            _graphP(gi,maxC,new_set)

    fTimes = ("Start time: %s \nEnd time: %s" % (startTimeClock, endTimeClock))
    dTime = endTime - startTime
    print(fTimes)
    fTimes = (startTimeClock, endTimeClock)
    rdTime = round(dTime,6)
    print (rdTime)

def tile(filename, dir_in, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size
    
    grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)

def _time():
    dt = time.time()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S:%I", t)
    return (dt, current_time)
#%%
def _apiGrab():
    global maxC, minN, maxN, baseN, new_set, prng

    dirdata = r'C:\Users\Luc\Desktop\Python\Dissertation\Data'
    response = requests.get('https://www.random.org/integers/?num=%s&min=%s&max=%s&col=1&base=%s&format=plain&rnd=new' % (maxC, minN, maxN, baseN)) # Https api request with custom variables inserted into the link using %s
    if '503' in str(response.status_code): # Verifying connectivity/ avalability of API
        print("Status code %s was returned \n--Changing to prng--" % response.status_code)
        prng = True
        _prng() # If TRNG isn't avalible then switches over to PRNG automatically
    if '200' in str(response.status_code):
        print("Status code %s was returned \n--Succseful connection--" % response.status_code)
        if maxC >= 10000:
            warn = input("Warning! You are requesting more than 10000 bits,\n Continue? (y/n): ").lower()
            if 'y' in warn:
                warn = True
            if 'n' in warn:
                warn = False
        if maxC < 10000:
            warn = True
        if warn == True:
            #print(response.content)
            content = response.content.decode("ascii")
            new_set = [x.replace('\n', '') for x in content] 
            x = 1 # the reason x != 0 is because by setting it to 1 it shifts what bit is popped bellow
            while x < (maxC+1):
                if '' in new_set[x]:
                    new_set.pop(x)
                x+=1
            print("CONTENT\n" + ("-" * 30) + "\n" + content + "\n" + ("-" * 30))
            dateTi = datetime.now()
            fname = ('trng-data-%s' % (dateTi))
            fname = fname.replace(" ", "-")
            fname = fname.replace(":", ".")
            print(new_set)
            _saveF(dirdata,fname,str(new_set))
    else: 
        print("Status code %s was returned" % response.status_code)
#%%
def _load(filename):

    with open(filename, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(' ', '')
    maxC = len(filedata)
    new_set = []
    for x in filedata:
        new_set.append(x)
    for x in range(0, len(new_set)): # converts to int
        new_set[x] = int(new_set[x])
    print('File loaded')
    print(new_set)
#%%
def _img():
    global maxC, new_set, filename

    image = open((filename), 'rb') # rb = read binary
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read)
    #print (image_64_encode)
    image_64_decode = base64.decodestring(image_64_encode)
   
    image_result = open((filename + '_decoded' + '.png'), 'wb') # create a writable image and write the decoding result
    image_result.write(image_64_decode)
    print(image_64_decode)
#%%
def _saveF(fDir,fName,fData):
    try:
        with open('%s\%s.txt' % (fDir,fName),'w') as f:
            f.write(fData)
    except Exception as e:
        print("An error occured!")
        print(e)
    finally:
        print("%s saved as txt under %s" % (fName,fDir))
        return

def _fileG():
    global new_set, filename

    # FileG used to format the data given from api into something usable
    with open(filename,"w") as file:
        file.write(str(new_set))

    # Read in the file
    with open(filename, 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(',', '')
    filedata = filedata.replace('[', '')
    filedata = filedata.replace(']', '')
    filedata = filedata.replace("'", '')
    #filedata = filedata.replace(' ', '')
    # Write the file out again
    with open(filename, 'w') as file:
      file.write(filedata)
    for x in range(0, len(new_set)): # converts str in list to int | this could also be done as the while loop above
        new_set[x] = int(new_set[x])
#%%
def _prng():
    global maxC, minN, maxN, new_set, prng, startTimeClock, endTimeClock, startTime, endTime

    # PRNG used for offline or if no bits avalible on random.org
    startTime, _ = _time() #Setting the start time to calc the amount of seconds
    _, startTimeClock = _time() #start time digital clock
    fdir = r'C:\Users\Luc\Desktop\Python\Dissertation\Data\PRNG' 
    fname = ('PRNG - %s bits - between %s & %s - %s' %(maxC,minN,maxN,round(startTime,8)))
    fname = fname.replace(":", ".")
    if prng == True:
        x = 0
        new_set = []
        while x < maxC:
            n = random.randrange(int(minN),int(maxN+1))
            new_set.append(n)
            x += 1
    elif prng == False:
        _apiGrab()
    _, endTimeClock = _time()
    endTime, _ = _time()
    ftime = endTime-startTime
    fdata = ('PRNG FILE\n\nTime stamps:\nTime taken: %s\nStart Time: %s\nEnd Time: %s\n-----\nConfig:\nAmount generated: %s\nMin number: %s\nMax number: %s\n-----\nBits generated:\n%s' % (ftime,startTimeClock,endTimeClock,maxC,minN,maxN,new_set))
    _saveF(fdir,fname,fdata)
#%%
def _graphP(x,a,b):
    try:
        if x == 0:
            maxC = a
            new_set = b
            oc = collections.Counter(new_set)
            ocV = oc.values()
            ocK = oc.keys()
        
            y_pos = np.arange(len(ocK))
            plt.bar(y_pos, ocV, align='center', alpha=0.5)
            plt.xticks(y_pos)
            plt.ylabel('Amount Generated')
            plt.xlabel('Different Numbers')
            plt.title('%s Bits Generated' % maxC)

            plt.show()
        if x == 1:
            maxC = a
            new_set = b
            plt.scatter(maxC, new_set, s=10, c="blue", alpha=0.5)
            plt.show()

        if x == 2:
            data = a

            mu = sum(data)/len(data)
            std = np.std(data)
        
            domain = np.linspace(min(data)-(min(data)/0.95),(max(data)+(max(data)/0.95)), 1000) # dividing the distance between min and max into 1000 points on the x axis
            plt.figure(figsize=(16, 9))
            #for mu, std in zip(means, std_values):
                # pdf stands for Probability Density Function, which is the plot the probabilities of each range of values
            probabilities = norm.pdf(domain, mu, std)
            plt.plot(domain, probabilities, label=f"$\mu={mu}$\n$\sigma={std}$\n")

            plt.legend()
            plt.xlabel("Value")
            plt.ylabel("Probability")
            plt.show()

        print("graph end")
    except Exception as e:
        print(e)
    finally:
        return
#%%
def _sha(filename):
    # Turns the binary of a file into a Sha256 hash
    with open(filename,"rb") as f:
        bytess = f.read() 
        hashs = hashlib.sha256(bytess).hexdigest()
        print(hashs)
    return(hashs)
        
#%%

mains = None

while mains == None:
    _mainS()
    rep = None
    while rep == None:
        x = input("Repeat?\n(y/n): ")
        if 'y' or '' in x:
           # timeList.append(dTime)# These appends need adding to a def, so that it can be used to loop the program a set amount of times and be called on when needed each loop
            #timeList.append(maxC)
            #print ("Time List: \n%s\n" % (timeList))
            rep = False
        if 'n' in x:
            print("--Goodbye--")
            #timeListMaxC = timeList[::2]
            #timeListG = timeList[1::2]
            #_graphP(1,timeListG,timeListMaxC)
            rep = False
            mains = False