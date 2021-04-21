### To Do ###
### 2. Add origin marker to centre with (0,0) label or similar.
### 3. Add grid/graph lines for easy viewing.

import csv
import os

def svgPolygon(coordsString):
    return '<polygon points="' + coordsString + '" stroke="red" stroke-width="1" fill="antiquewhite" />'
    
def svgText(x,y,text):
    return '<text x="' + str(x) + '" y="' + str(y) + '">' + text + '</text>'

def svgOrigin(x,y):
    out = ['<!-- ORIGIN MARKER -->']
    out.append('<line x1="-10" y1="0" x2="10" y2="0" style="fill:none;stroke:#000;stroke-miterlimit:10"/>')
    out.append('<line x1="0" y1="-10" x2="0" y2="10" style="fill:none;stroke:#000;stroke-miterlimit:10"/>')
    out.append('<circle cx="0" cy="0" r="5"/>')
    out.append('<text x="5" y="-5">(0,0)</text>')


    
    return '\n'.join(out)

def writeFile(outputList,xMin,yMin,xMax,yMax):
    if os.path.exists("output.svg"):
        os.remove("output.svg")
    
    #Min Sizes (minus -150 adds extra padding)
    xMin = xMin - 150
    yMin = yMin - 150
    #Max Sizes (ABS Double Min sizes for ease)
    xMax = xMin * -2
    yMax = yMin * -2
    
    with open("output.svg", "a") as out:
        out.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n')
        out.write('<svg width="' + str(xMax) + '" height="' + str(yMax) + '" viewBox="' + str(xMin) + " " + str(yMin) + " " + str(xMax) + " " + str(yMax) + '" xmlns="http://www.w3.org/2000/svg">' + '\n')
        for x in outputList:
            out.write(x + '\n')
        out.write('</svg>')
    os.system("start output.svg")


def parseCSV(file):
    outputList = [] #empty array to hold output to be passed to writeFile func.
    coords = [] #empty array to hold coord value
    coordsText = [] #empty array to hold coord text value
    xMin = 0
    yMin = 0
    xMax = 0
    yMax = 0

    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        coordList = list(reader)
        for i in range(len(coordList)):
            if i >= 1: #Skip Header Row
                coordX = float(coordList[i][1])      #x value
                coordY = float(coordList[i][2]) * -1 #y value ***NOTE*** has to be flipped because of SVG coordinate system)
                
                #Creates coordinate pairing string and adds to coords list.
                coords.append(str(coordX) + "," + str(coordY))

                #adds coordinate pairing label to CoordsText list.
                coordsText.append(svgText(coordX,coordY-5,"#" + (str(coordList[i][0])) + " ( " +str(coordX) + "," + str(coordY*-1) + ")")) 

                #Calculates xMin, yMin, xMax, yMax values for viewport/sizing
                if abs(coordX) > abs(xMin):
                    xMin = abs(coordX) * -1
                if abs(coordY) > abs(yMin):
                    yMin = abs(coordY) * -1
                if coordX > xMax:
                    xMax = coordX
                if coordY > yMax:
                    yMax = coordY

        # creates single string from "coords" list.
        coordsString = ' '.join(coords) 
        # passes coordString to svgPolygon and adds return outputList
        outputList.append(svgPolygon(coordsString)) 
        
        #Loops through coordsText and adds each text as new line to outputList (has to be last so they are on highest layer)
        for i in coordsText: 
            outputList.append(i)
        
        outputList.append(svgOrigin('coordX','coordy'))
        #calls main write function passing outputList
        writeFile(outputList,xMin,yMin,xMax,yMax)

if __name__ == '__main__':
    if not os.path.exists('input.csv'):
        print('No input.csv file found!')
        input()
    else:
        parseCSV('input.csv')