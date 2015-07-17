class Parser:
#{
    def __init__(self, file):
    #{
        global MAX_FILE_CACHE # how many lines can be read, before loops terminate
        MAX_FILE_CACHE = 500   # avoids massivly-long loops

        self.FILE = None
        self.file = str(file)
                    #NOT DONE CORRECTLY
        try: # Check that file exists, before opening in a+ mode
        #{
            self.FILE = open(str(self.file), "r") # Open in read mode
        #}
        except(IOError) as error:
        #{
            print("== Can't open file: " + str(self.file) +
                  " ==\n\t" + str(error))

        #}
        else:
        #{
            self.FILE = open(str(self.file), "r+") # Open in read and WRITE mode
        #}
    #}

    def getFileContents(self):
    #{
        numbOfLines = self.getFileLen()
        fileContents = []
        currLine = "<Undefined>"

        pos = 0 # Loop Counter

        while((currLine != "") and (pos < MAX_FILE_CACHE)): # Until EOF
        #{
            currLine = self.FILE.readline()

            fileContents.append(currLine)

            pos += 1
        #}

        del pos # Temp var

        fileContents.pop(len(fileContents) - 1) # remove the last defunct instance

        self.FILE.close() # re-open file at first line QWFX SMELL
        self.FILE = open(self.file, "r+")

        return fileContents
    #}
    # Returns an array with the number of lines, and the len(chars) of the longest line
    def getFileLen(self):
    #{
        fileLen = [] # Contains numbOfLines, length of X line
        lineLengths = [] # Contains the length of the lines read TEMP
        numbOfLines = 0 # Number of lines in the file
        lenCurrLine = -1 # The length of the line being read
        currLine = "<Undefined>" # The line currently being read

        while((currLine != "") and (numbOfLines < MAX_FILE_CACHE)): # Read until EOF
        #{
            currLine = self.FILE.readline()
            lenCurrLine = len(currLine)

            lineLengths.append(str(lenCurrLine - 1)) # Remove defunct ""

            numbOfLines += 1
        #}

        numbOfLines -= 1 # Remove defunct ""

        fileLen.append(numbOfLines)

        for pos in range(len(lineLengths)):
        #{
            fileLen.append(int(lineLengths[pos])) # add to array in form of int
        #}

        fileLen.pop(len(fileLen) - 1) # Remove unwanted "-1"


        self.FILE.close() # R-open file at first line QWFX SMELL
        self.FILE = open(self.file, "r+")

        return fileLen
    #}

    def markCarrageReturns(self, listToMark): # makes carrage returns visable to the program(post splitting)
    #{
        formattedList = listToMark
        pos = 0 # Loop counter

        while(("\n" not in formattedList) and (pos < len(formattedList))):
        #{
            pass # QWFX
            pos += 1
        #}

        return formattedList
    #}

    def findCapitalLetters(self): # Returns the position of captials
    #{
        fileContents = self.getFileContents()
        fileContents = self.markCarrageReturns(fileContents)
        fileContents = "".join(fileContents).split() # cast to string to format seperate into strings
        lengthOfFile = self.getFileLen()[0] # SMELL separate into methods
        captials = [] # Contains the position(s) of all capitals found in file
        lineNumber = 0 # Line being read
        currString = "" # Current string being read

        for pos in range(lengthOfFile):
        #{
            currString = fileContents[pos]

            if(currString == "¬|¬"): # SMELL
            #{
                lineNumber += 1
            #}

            if(currString.isupper()):
            #{
                captials.append(lineNumber) # line
                captials.append(pos) # number of chars across the line
            #}
        #}

        return captials
    #}

    def findString(self, toFind, startPoint):
    #{
        toFind = toFind
        toFindPosition = [None, None] # Contains where toFind is found
        startPoint = startPoint
        lengthOfFile = self.getFileLen() # Gets all of the length (lines, length of lines)
        numbOfLines = lengthOfFile[0]
        fileContents = self.getFileContents()
        currLine = "" # Line being read
        currChar = "" # Character being read
        currLinePos = 0 # Line being read (position)
        currCharPos = 0 # Character being read (position)
        lenCurrLine = -1 # Length of the line being read
        foundItem = False # If the loop has found 'toFind'
        pos = 0 # Loop counter

        if(toFind is None): # TODO Remove this Try- like crap, pass in object instead
        #{
            raise NameError
        #}
        elif(startPoint is not None):
        #{
            if(len(startPoint) > 2): # 2 args should be passed in
            #{
                raise NameError
            #}
            elif(not (isinstance(startPoint[0], int))): # If not an integer
            #{
                raise NameError
            #}
            elif(not (isinstance(startPoint[1], int))):
            #{
                raise NameError
            #}
            elif(startPoint[0] > self.getFileLen()[0]):
            #{
                raise NameError # line given doesn't exist
            #}
            elif(startPoint[1] > self.getFileLen()[1]):
            #{
                raise NameError # line given doesn't exist
            #}
        #}
        else:
        #{
            startPoint = [0, 0] # Default start point line 0, col 0
        #}

        currLinePos = startPoint[0]
        currCharPos = startPoint[1]

        while((not foundItem) and (pos < len(fileContents))): # loops until found the item, or array end reached
        #{
            currLine = fileContents[currLinePos].split() # Converts to individual words
            lenCurrLine = len(currLine) # "+1" as the 1st elemet is how many lines in the file

            while((not foundItem) and (currCharPos < lenCurrLine)): # Until end of line
            #{
                currChar = currLine[currCharPos]

                if(currChar == toFind):
                #{
                    foundItem = True

                    toFindPosition[0] = currLinePos # Line Number
                    toFindPosition[1] = currCharPos # Column Number
                #}

                currCharPos += 1
            #}

            currCharPos = 0 # Back to default

            currLinePos += 1
            pos += 1
        #}

        if(not foundItem):
        #{
                print("String: '" + str(toFind) + "' was not found!")
                raise EOFError # May be incorrect
        #}
        else:
        #{
            return toFindPosition
        #}
    #}

    def findChar(self):
    #{
        # TODO
        pass #QWFX
    #}

    def replace(self):
    #{
        # TODO
        pass #QWFX
    #}
#}

file = "FileExample.txt"

p = Parser(file)

startPoint = [12, 12]

print(p.findCapitalLetters())
# print(p.findString("qui", startPoint)) # Example
print(p.findString("qui", None)) # Example
