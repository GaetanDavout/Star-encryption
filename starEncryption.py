# -*- coding: utf-8 -*-
"""
    *** Star Encryption ***
Created on Tue Mar 17 09:29:29 2020
@author: Gaetan Davout

   *   '*
           *
                *
                       *
               *
                     *
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import configparser

################################## Functions #################################

# randomly return a star size
def starSize():
    r = random.randrange(100)
    if r < brightest_rate:
        return size_brightest
    elif r < (big_rate+brightest_rate):
        return size_big
    else:
        return size_mediocre
    
# plot star giving radius
def plotStar(radius,subline,color):
    xrand = radius + (random.random()-0.5)*(2/FullnCarac)
    yrand = (random.random()-0.5)*(xrand*(variability/100)/(nLines))
    xrand = xrand-xrand*(1-np.cos(yrand))
    x = -((xrand*np.cos((np.pi/2)+((i*3+subline)*np.pi/(nLines*3))))+(yrand*np.sin((np.pi/2)+((i*3+subline)*np.pi/(nLines*3)))))
    y = ((yrand*np.cos((np.pi/2)+((i*3+subline)*np.pi/(nLines*3))))-(xrand*np.sin((np.pi/2)+((i*3+subline)*np.pi/(nLines*3)))))
    plt.scatter(x,y,s=starSize(),c=color,marker='.',edgecolors = 'none')
    
##############################################################################

################################ Settings ####################################

# see config file for param explanations

config = configparser.RawConfigParser()
config.read('config.txt')

textfile = config.get('IO','textfile')
outputfile = config.get('IO','outputfile')

# retrieve the text that will be convert. 
file = open(textfile, "r")
lines = file.readlines()
file.close()

# retrieve stars parameters
#   - size
size_brightest = config.getfloat('Stars','size_brightest')
size_big = config.getfloat('Stars','size_big')
size_mediocre = config.getfloat('Stars','size_mediocre')
#   - size proportion
brightest_rate = config.getfloat('Stars','brightest_rate')
if brightest_rate > 100: brightest_rate = 100
elif brightest_rate < 0: brightest_rate = 0
big_rate = config.getfloat('Stars','big_rate')
if big_rate > (100 - brightest_rate): big_rate = (100 - brightest_rate)
elif big_rate < 0: big_rate = 0
#   - variability
variability = config.getint('Stars','variability')
if variability < 0: variability = 0
#   - central hole params
centralDensity = config.getfloat('Stars','centralDensity')
if centralDensity < 0: centralDensity = 0
elif centralDensity > 100: centralDensity = 10
#   - colors
color0 = config.get('Stars','color0')
color1 = config.get('Stars','color1')
color2 = config.get('Stars','color2')
color3 = config.get('Stars','color3')
color4 = config.get('Stars','color4')
color5 = config.get('Stars','color5')
centralcolor = config.get('Stars','centralcolor')

# retrieve msg help decoder
decodeHelp = config.getboolean('msg','decodeHelp')

# retrieve debug parameters
nPass = config.getint('Debug','nPass')
if nPass < 1: nPass = 1
debugging=config.getboolean('Debug','debugging')

# get text parameters
nLines = len(lines)
nCaracMax = 0
for i in range(nLines):
    currentLine = (lines[i])
    currentLine = currentLine.replace('\n','')
    nCarac = len(currentLine)
    if nCarac > nCaracMax:
        nCaracMax = nCarac
if nCaracMax%2 == 1:
    nCaracMax = nCaracMax+1

# set figure resolution
plt.figure(dpi=1200)

##############################################################################

################################# DATABASE ###################################

# the following characters are stocked in this order :
# abcdefghijklmnopqrstuvwxyz0.,?!'- + " "
# N.B. : digits match the first letters
# N.B.2: uppercase is set as lowercase
# braille characters are splited like this:
# 1 2
# 3 4       =>      [1 2 3 4 5 6]
# 5 6
dt = np.array([[1, 0, 0, 0, 0, 0],  # a U 1
               [1, 0, 1, 0, 0, 0],  # b U 2
               [1, 1, 0, 0, 0, 0],  # c U 3
               [1, 1, 0, 1, 0, 0],  # d U 4
               [1, 0, 0, 1, 0, 0],  # e U 5
               [1, 1, 1, 0, 0, 0],  # f U 6
               [1, 1, 1, 1, 0, 0],  # g U 7
               [1, 0, 1, 1, 0, 0],  # h U 8
               [0, 1, 1, 0, 0, 0],  # i U 9
               [0, 1, 1, 1, 0, 0],  # j
               [1, 0, 0, 0, 1, 0],  # k
               [1, 0, 1, 0, 1, 0],  # l
               [1, 1, 0, 0, 1, 0],  # m
               [1, 1, 0, 1, 1, 0],  # n
               [1, 0, 0, 1, 1, 0],  # o
               [1, 1, 1, 0, 1, 0],  # p
               [1, 1, 1, 1, 1, 0],  # q
               [1, 0, 1, 1, 1, 0],  # r
               [0, 1, 1, 0, 1, 0],  # s
               [0, 1, 1, 1, 1, 0],  # t
               [1, 0, 0, 0, 1, 1],  # u
               [1, 0, 1, 0, 1, 1],  # v
               [0, 1, 1, 1, 0, 1],  # w
               [1, 1, 0, 0, 1, 1],  # x
               [1, 1, 0, 1, 1, 1],  # y
               [1, 0, 0, 1, 1, 1],  # z
               [0, 1, 1, 1, 0, 0],  # 0
               [0, 0, 1, 1, 0, 1],  # .
               [0, 0, 1, 0, 0, 0],  # ,
               [0, 0, 1, 0, 1, 1],  # ?
               [0, 0, 1, 1, 1, 0],  # !
               [0, 0, 0, 0, 1, 0],  # '
               [0, 0, 0, 0, 1, 1],  # -
               [1, 1, 1, 1, 1, 1],  # *
               [0, 0, 0, 0, 0, 0],  # " "
               ])

# match characters with there line in dt
switcher = {"a": 0,     "A": 0,     "1": 0,     "à":0,
            "b": 1,     "B": 1,     "2": 1,
            "c": 2,     "C": 2,     "3": 2,     "ç":2,
            "d": 3,     "D": 3,     "4": 3,
            "e": 4,     "E": 4,     "5": 4,     "é":4,"è":4,"ê":4,"ë":4,
            "f": 5,     "F": 5,     "6": 5,
            "g": 6,     "G": 6,     "7": 6,
            "h": 7,     "H": 7,     "8": 7,
            "i": 8,     "I": 8,     "9": 8,
            "j": 9,     "J": 9,
            "k": 10,    "K": 10,
            "l": 11,    "L": 11,
            "m": 12,    "M": 12,
            "n": 13,    "N": 13,
            "o": 14,    "O": 14,
            "p": 15,    "P": 15,
            "q": 16,    "Q": 16,
            "r": 17,    "R": 17,
            "s": 18,    "S": 18,
            "t": 19,    "T": 19,
            "u": 20,    "U": 20,                "ù":20,
            "v": 21,    "V": 21,
            "w": 22,    "W": 22,
            "x": 23,    "X": 23,
            "y": 24,    "Y": 24,
            "z": 25,    "Z": 25,
            "0": 26,
            ".": 27,
            ",": 28,
            "?": 29,
            "!": 30,
            "'": 31,
            "-": 32,
            "*": 33,
            " ": 34,
            }

##############################################################################

############################## printing Background ###########################

# background : 
# use those param : extent=[-1.199,1.113,-1.462,1.36] -> r full circle = 1.11
img = plt.imread("src/Background.jpg")
plt.imshow(img, extent=[-1.199,1.113,-1.462,1.36])

# print background ornament
# 1. circles : the inner circle should limit the center hole where stars aren't data
rCircles = np.array([1.11,.8,.48,.25])
for i in range(len(rCircles)):
    theta = np.linspace(0, 2*np.pi, 100)
    r = np.sqrt(rCircles[i])
    xCircle = r*np.cos(theta)
    yCircle = r*np.sin(theta)
    if i == 0:
        plt.plot(xCircle, yCircle,'k',linewidth = .5)
    else:
        plt.plot(xCircle, yCircle,'k',linewidth = .1) 

# 2. lines : should follow the braille ?
plt.plot([-np.sqrt(1.11),np.sqrt(1.11)],[0,0],'k',linewidth=.1)
plt.plot([0,0],[-np.sqrt(1.11),np.sqrt(1.11)],'k',linewidth=.1)
for i in range(12):
    seg = np.linspace(-1,1,nCaracMax*2+(int(nCaracMax)))
    segX = -seg*np.cos((np.pi/2)+(i*np.pi/12))
    segY = -seg*np.sin((np.pi/2)+(i*np.pi/12))
    
    ja = 0
    jb = 0
    for j in range(nCaracMax*2 + int(nCaracMax)):
        
        if j >= int((nCaracMax) + (nCaracMax)):
            if jb == 0:
                jb = j-1
        elif j >= int(nCaracMax):
            if ja == 0:
                ja = j
                
    Xa = np.array([np.sqrt(1.11)*np.cos((np.pi/2)+(i*np.pi/12)),segX[ja]])
    Ya = np.array([np.sqrt(1.11)*np.sin((np.pi/2)+(i*np.pi/12)),segY[ja]])
    Xb = np.array([segX[jb],-np.sqrt(1.11)*np.cos((np.pi/2)+(i*np.pi/12))])
    Yb = np.array([segY[jb],-np.sqrt(1.11)*np.sin((np.pi/2)+(i*np.pi/12))])
    
    plt.plot(Xa,Ya,'k',linewidth=.1)
    plt.plot(Xb,Yb,'k',linewidth=.1)
    
    if i == 0:
        r = segY[ja]
        xCircle = r*np.cos(theta)
        yCircle = r*np.sin(theta)
        plt.plot(xCircle, yCircle,'k',linewidth = .15)

##############################################################################

################################ processing ##################################

# can process multiple time to check the readableness
for n in range(nPass):
    print(n+1,"/",nPass)
    
    # Process line after line
    for i in range(nLines):
        
        # get current line and shape it
        currentLine = (lines[i])
        currentLine = currentLine.replace('\n','')
        nCarac = len(currentLine)
        if nCarac < nCaracMax:
            for m in range(nCaracMax-nCarac):
                currentLine = currentLine + " "
            nCarac = len(currentLine)
            
        FullnCarac = nCarac*2+(int(nCarac))
        
        # create base line of stars wich will be use 3 times (for each braille
        # lines). Then plotStar() will give those stars a new angle and noise
        radius = np.linspace(-1,1,FullnCarac)
    
        # for each characters print matching stars
        for j in range(nCarac + int(nCarac/2)):
            
            # print all the meaning stars
            if j < int(nCarac/2) or j >= int((nCarac/2) + (nCarac/2)):
                k = j
                if j >= int((nCarac/2) + (nCarac/2)):
                    k = j - int(nCarac/2)
                    
                # permit to check the correct association and reading
                if debugging:
                    print([
                    dt[switcher[currentLine[k]],0],
                    dt[switcher[currentLine[k]],1],
                    dt[switcher[currentLine[k]],2],
                    dt[switcher[currentLine[k]],3],
                    dt[switcher[currentLine[k]],4],
                    dt[switcher[currentLine[k]],5],
                    ],currentLine[k])

                # first braille line 
                if dt[switcher[currentLine[k]],0] == 1:
                    plotStar(radius[j*2],0,color0)                    
                if dt[switcher[currentLine[k]],1] == 1:
                    plotStar(radius[j*2+1],0,color1)  
                # second braille line
                if dt[switcher[currentLine[k]],2] == 1:
                    plotStar(radius[j*2],1,color2) 
                if dt[switcher[currentLine[k]],3] == 1:
                    plotStar(radius[j*2+1],1,color3) 
                # third braille line
                if dt[switcher[currentLine[k]],4] == 1:
                    plotStar(radius[j*2],2,color4) 
                if dt[switcher[currentLine[k]],5] == 1:
                    plotStar(radius[j*2+1],2,color5) 

            # fill the hole with random stars
            else:
                # first braille line 
                if random.randrange(100) >= 100 - centralDensity:
                    plotStar(radius[j*2],0,centralcolor)  
                if random.randrange(100) >= 100 - centralDensity:
                    plotStar(radius[j*2+1],0,centralcolor)  
                # second braille line
                if random.randrange(100) >= 100 - centralDensity:
                    plotStar(radius[j*2],1,centralcolor) 
                if random.randrange(100) >= 100 - centralDensity:
                    plotStar(radius[j*2+1],1,centralcolor)
                # third braille line
                if random.randrange(100) >= 100 - centralDensity:
                    plotStar(radius[j*2],2,centralcolor) 
                if random.randrange(100) >= 100 - centralDensity:
                    plotStar(radius[j*2+1],2,centralcolor)

##############################################################################
                
################################### Print ####################################

# equalize and remove axis
plt.axis("equal")
plt.axis("off")

# print info to help decoding
if decodeHelp:
    plt.text(0.043,-1.186,str(nLines)+":"+str(nCaracMax)+":"+str(1.0),
         color='k',fontsize=2,ha='right',va='center')

# save and close
plt.savefig(outputfile)
plt.close()

##############################################################################
#////////////////////////////////////////////////////////////////////////////#
##############################################################################