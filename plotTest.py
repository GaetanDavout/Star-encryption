# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 09:29:29 2020

@author: Gaetan Davout
"""

import numpy as np
import matplotlib.pyplot as plt
import random

""" Next Improvements :
        - variable size of the dot          [##########] 99%
        - comment clearly                   [#########-] 90%
        - variable position from init       [#####-----] 50% redo that
        - add background                    [#########-] 90%
        - make a central hole               [#---------] 10%
        - add random points in the center   [#---------] 10%
        - make a command of this            [#---------] 10%
        - add maj match                     [#---------] 10%
"""

################################ Settings ####################################

# text that will be convert. 
# the shorter parts are the better the result is.
# don't let any empty lines.
# don't write after or before the ''''.
text = ''''
je cueille des fleurs 
d'orchis au printemps
et les jette dans les nuages
mal de dents evidemment 
les poireaux sont verts
dans le champ
        '''


# size of the "stars" 
# mediocre mean the most of them will have this size
size_brightest = 8
size_big = 4
size_mediocre = 1
# percentage of brighter star
lim_brightest = 10
lim_big = 70


# variability of star from there readable position
# the closer to zero the more variable it is.
# 100 is the most you can set to be sure to be able to read it
pos_variability = 10


##############################################################################
#////////////////////////////////////////////////////////////////////////////#
##############################################################################

if lim_brightest < 100: lim_brightest = 100 - lim_brightest
else : lim_brightest = 90

if lim_big < 100: lim_big = 100 - lim_big
else : lim_big = 70

################################# DATABASE ###################################

# the following characters are stocked in this order :
# abcdefghijklmnopqrstuvwxyz0.,?!'- + " "
# N.B. : digits match the first letters
# braille characters are splited like this:
# 1 2
# 3 4
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
               [0, 0, 0, 0, 0, 0],  # " "
               ])

# match characters with there line in dt
switcher = {"a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7,
            "i": 8,
            "j": 9,
            "k": 10,
            "l": 11,
            "m": 12,
            "n": 13,
            "o": 14,
            "p": 15,
            "q": 16,
            "r": 17,
            "s": 18,
            "t": 19,
            "u": 20,
            "v": 21,
            "w": 22,
            "x": 23,
            "y": 24,
            "z": 25,
            "0": 26,
            ".": 27,
            ",": 28,
            "?": 29,
            "!": 30,
            "'": 31,
            "-": 32,
            " ": 33,
            "1": 0,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "7": 6,
            "8": 7,
            "9": 8,
            }

##############################################################################

################################ processing ##################################

# split text into lines and delete the first and last that are supposed to be
# empty
lines = text.split("\n")
del lines[0]
del lines[-1]


# Process line after line
nLines = len(lines)
for i in range(nLines): #decommante apres tests
    currentLine = (lines[i])
    nCarac = len(lines[i])
    
# create lines of coordinates for each potential "stars"
# braille are cut in three lines so there is three lines of coordinates per
# parts.
    """                          to modify                                 """
    y3 = np.linspace(-1,1,nCarac*2)
    x1 = -y3*np.cos((np.pi/2)+(i*3*np.pi/(nLines*3)))
    y1 = -y3*np.sin((np.pi/2)+(i*3*np.pi/(nLines*3)))
    x2 = -y3*np.cos((np.pi/2)+((i*3+1)*np.pi/(nLines*3)))
    y2 = -y3*np.sin((np.pi/2)+((i*3+1)*np.pi/(nLines*3)))
    x3 = -y3*np.cos((np.pi/2)+((i*3+2)*np.pi/(nLines*3)))
    y3 = -y3*np.sin((np.pi/2)+((i*3+2)*np.pi/(nLines*3)))

# for each characters print matching stars
    for j in range(nCarac):
        
        # permit to check the correct association and reading
        print([
        dt[switcher[currentLine[j]],0],
        dt[switcher[currentLine[j]],1],
        dt[switcher[currentLine[j]],2],
        dt[switcher[currentLine[j]],3],
        dt[switcher[currentLine[j]],4],
        dt[switcher[currentLine[j]],5],
        ],currentLine[j])
        
# make a better variability of position to be readable and more beautiful
        """                        to modify                               """
        # first braille line 
        if dt[switcher[currentLine[j]],0] == 1:
            r = random.randrange(100)
            if r > lim_brightest:
                plt.scatter(x1[j*2]+(x1[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y1[j*2]+(y1[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_brightest, c = 'white', marker = '.')
            elif r > lim_big:
                plt.scatter(x1[j*2]+(x1[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y1[j*2]+(y1[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_big, c = 'white', marker = '.')
            else:
                plt.scatter(x1[j*2]+(x1[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y1[j*2]+(y1[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_mediocre, c = 'white', marker = '.')
                    
        if dt[switcher[currentLine[j]],1] == 1:
            r = random.randrange(100)
            if r > lim_brightest:
                plt.scatter(x1[j*2+1]+(x1[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y1[j*2+1]+(y1[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_brightest, c = 'white', marker = '.')
            elif r > lim_big:
                plt.scatter(x1[j*2+1]+(x1[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y1[j*2+1]+(y1[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_big, c = 'white', marker = '.')
            else:
                plt.scatter(x1[j*2+1]+(x1[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y1[j*2+1]+(y1[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_mediocre, c = 'white', marker = '.')
                
                
        # second braille line
        if dt[switcher[currentLine[j]],2] == 1:
            r = random.randrange(100)
            if r > lim_brightest:
                plt.scatter(x2[j*2]+(x2[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y2[j*2]+(y2[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_brightest, c = 'white', marker = '.')
            elif r > lim_big:
                plt.scatter(x2[j*2]+(x2[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y2[j*2]+(y2[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_big, c = 'white', marker = '.')
            else:
                plt.scatter(x2[j*2]+(x2[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y2[j*2]+(y2[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_mediocre, c = 'white', marker = '.')
                    
        if dt[switcher[currentLine[j]],3] == 1:
            r = random.randrange(100)
            if r > lim_brightest:
                plt.scatter(x2[j*2+1]+(x2[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y2[j*2+1]+(y2[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_brightest, c = 'white', marker = '.')
            elif r > lim_big:
                plt.scatter(x2[j*2+1]+(x2[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y2[j*2+1]+(y2[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_big, c = 'white', marker = '.')
            else:
                plt.scatter(x2[j*2+1]+(x2[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y2[j*2+1]+(y2[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_mediocre, c = 'white', marker = '.')
           
            
        # thrid braille line
        if dt[switcher[currentLine[j]],0] == 1:
            r = random.randrange(100)
            if r > lim_brightest:
                plt.scatter(x3[j*2]+(x3[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y3[j*2]+(y3[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_brightest, c = 'white', marker = '.')
            elif r > lim_big:
                plt.scatter(x3[j*2]+(x3[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y3[j*2]+(y3[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_big, c = 'white', marker = '.')
            else:
                plt.scatter(x3[j*2]+(x3[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y3[j*2]+(y3[j*2]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_mediocre, c = 'white', marker = '.')
                    
        if dt[switcher[currentLine[j]],1] == 1:
            r = random.randrange(100)
            if r > lim_brightest:
                plt.scatter(x3[j*2+1]+(x3[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y3[j*2+1]+(y3[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_brightest, c = 'white', marker = '.')
            elif r > lim_big:
                plt.scatter(x3[j*2+1]+(x3[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y3[j*2+1]+(y3[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_big, c = 'white', marker = '.')
            else:
                plt.scatter(x3[j*2+1]+(x3[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), y3[j*2+1]+(y3[j*2+1]*(((random.randrange(100)-50)/pos_variability)/nCarac)), s = size_mediocre, c = 'white', marker = '.')
                
                

##############################################################################
                
################################### Print ####################################


# print the background
img = plt.imread("skymap14cleaned.jpg")
plt.imshow(img, extent=[-1.23,1.23,-1.23,1.23])


# add ornament
"""                                to make                                 """


# equalize and remove axis
plt.axis("equal")
plt.axis("off")



#plt.savefig("test.png")