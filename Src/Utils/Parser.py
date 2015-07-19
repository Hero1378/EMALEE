class Parser:
#{
    def __init__(self, newFileName):
    #{
        global MAX_FILE_CACHE # how many lines can be read, before loops terminate
        MAX_FILE_CACHE = 500   # avoids massivly-long loops

        self.FILE = None
        self.fileName = str(newFileName)
                    #NOT DONE CORRECTLY
        try: # Check that file exists, before opening in a+ mode
        #{
            self.FILE = open(str(self.fileName), "r") # Open in read mode
        #}
        except(IOError) as error:
        #{
            print("== Can't open file: " + str(self.fileName) +
                  " ==\n\t" + str(error))

        #}
        else:
        #{
            self.FILE = open(str(self.fileName), "r+") # Open in read and WRITE mode
        #}
    #}

    def getNumbOfLines(self):
    #{
        numbOfLines = 0
        currLine = ""

        for currLine in self.FILE: # Read until EOF
        #{
            currLine = self.FILE.readline()

            if(numbOfLines == MAX_FILE_CACHE): # Avoid huge loops
            #{
                break
            #}

            numbOfLines += 1
        #}

        numbOfLines -= 1 # remove unwanted blank final line

        self.FILE.close() # re-open file at first line QWFX SMELL
        self.FILE = open(self.fileName, "r+")

        return numbOfLines
    #}

    def getFileContents(self):
    #{
        lengthOfFile = self.getNumbOfLines()
        fileContents = []
        currLine = "<Undefined>"

        pos = 0 # Loop Counter

        while(pos < lengthOfFile): # Until EOF
        #{
            currLine = self.FILE.readline()

            fileContents.append(currLine)

            pos += 1
        #}

        del pos # Temp var

        fileContents.pop(len(fileContents) - 1) # remove the last defunct instance

        self.FILE.close() # re-open file at first line QWFX SMELL
        self.FILE = open(self.fileName, "r+")

        return fileContents
    #}

    def getLineLengths(self):
    #{
        fileContents = self.getFileContents()
        lengthOfFile = self.getNumbOfLines()
        lineLengths = [] # Contains the length of each line read
        currLine = "" # line being read

        for pos in range(lengthOfFile):
        #{
            currLine = fileContents[pos]

            lineLengths.append(int(len(currLine)))
        #}

        return lineLengths # No defunct line, as relies on method that strips blank line (getNumbOfLines)
    #}

    def markNewLines(self, listToMark): # makes carrage returns visable to the program(post splitting)
    #{
        formattedList = listToMark # Same list as passed in, but with carrage returns marked
        tempElement = "" # Holds the nth element being parsed

        for i in range(len(formattedList)):
        #{
            if(i == (len(formattedList) - 1)): # don't add "|" to end of doc
            #{
                continue
            #}
            else:
            #{
                formattedList[i] = formattedList[i] + str("|") # Mark end of line
            #}
        #}

        return formattedList
    #}

    def getTotalNumbOfChars(self): # Adds up number of chars
    #{
        rawLength = self.getNumbOfLines()
        rawLength.pop(0) # ignore first element
        totalLength = 0 # Numb of chars in file

        for i in range(len(rawLength)):
        #{
            totalLength += rawLength[i]
        #}

        return totalLength
    #}

    def getTotalNumberOfStrings(self):
    #{
        separatedFile = "".join(self.getFileContents()).split() # Seperate file into strings
        totalLength = len(separatedFile)

        return totalLength
    #}

    def findCapitalLetters(self): # Returns the position of captials
    #{
        fileContents = "".join(self.markNewLines(self.getFileContents())) # Convert to string for parsing
        capitalLocations = [] # line, chars across
        lineNumber = 0 # number of line currently being read
        totalLengthOfFile = self.getTotalNumbOfChars() # total number of chars in the file
        currChar = "" # Current char being read
        charsAcross = 0 # Number of chars that have been read(column)
        positionInCurrentLine = 0 # like chars across ,but resets each line

        for charsAcross in range(totalLengthOfFile):
        #{
            currChar = fileContents[charsAcross]

            if(currChar == "|"): # SMELL means '|' can't be used
            #{
                lineNumber += 1

                positionInCurrentLine = 0 # set back to default as upper has been found
            #}

            if(currChar.isupper()):
            #{
                capitalLocations.append(lineNumber)
                capitalLocations.append(positionInCurrentLine)
            #}

            charsAcross += 1
            positionInCurrentLine += 1
        #}

        return capitalLocations
    #}

    def findString(self, toFind, startPoint):
    #{
        toFind = toFind
        toFindPosition = [None, None] # Contains where toFind is found
        startPoint = startPoint
        lengthOfFile = self.getNumbOfLines() # Gets all of the length (lines, length of lines)
        numbOfLines = self.getNumbOfLines()
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
            elif(startPoint[0] > self.getNumbOfLines()):
            #{
                raise NameError # line given doesn't exist
            #}
            elif(startPoint[1] > self.getLineLengths()[0]):
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

print(p.getFileContents())
