class Parser: # excuse the terrible practice of modifying methods based upon their
#{              prams, after all this is a prototype.
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
            self.FILE.close()
            self.FILE = open(str(self.fileName), "r+") # Open in read and WRITE mode
        #}
    #}

    def getNumbOfLines(self):
    #{
        numbOfLines = len(self.FILE.readlines())

        self.FILE.close() # re-open file at first line QWFX SMELL
        self.FILE = open(self.fileName, "r+")

        return numbOfLines
    #}

    def getFileContents(self):
    #{
        lengthOfFile = self.getNumbOfLines()
        fileContents = []
        currLine     = "<Undefined>"

        pos = 0 # Loop Counter

        while(pos <= lengthOfFile): # Until EOF
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
        lineLengths  = [] # Contains the length of each line read
        currLine     = "" # line being read

        for pos in range(lengthOfFile):
        #{
            currLine = fileContents[pos - 1] # '-1' as start from '0' not '1'

            lineLengths.append(int(len(currLine)))
        #}

        return lineLengths # No defunct line, as relies on method that strips blank line (getNumbOfLines)
    #}

    def getExistingBars(self, toFindIn): # returns the 'coords' of the existing newLine markers
    #{
        if(toFindIn is None):
        #{
            fileContents = self.getFileContents() # file is default
        #}
        else:
        #{
            fileContents = toFindIn
        #}
        
        lengthOfFile    = self.getNumbOfLines()
        currChar        = "" # Current line being read (char)
        currLine        = "" # Current character being read (String)
        currLineNumber  = 0 # Current line being read (numerical)
        currCharNumber  = 0 # Current character being read (numerical)
        currBarLocation = [None, None] # temp var, used to 'bundle' arrays
        barLocations    = [] # currLine, currChar

        for pos in range(lengthOfFile):
        #{
            currLine = fileContents[pos]
            currLine = "".join(currLine)

            if("|" in currLine): # save time
            #{
                for i in range(len(currLine)):
                #{
                    currCharNumber += 1

                    if("|" in currLine[i]):
                    #{
                        currBarLocation[0] = currLineNumber
                        currBarLocation[1] = (currCharNumber - 1) # '-1' to counteract machine starting from 0
                        barLocations.append(currBarLocation)      # whereas this variable starts from 1
                        currBarLocation    = [None, None]
                    #}
                #}

                currCharNumber = 0 # reset as on new line
            #}

            currLineNumber += 1 # after loop, as machine starts from 0
        #}

        return barLocations
    #}

    def markNewLines(self, listToMark): # makes cariage returns visable to the program(post splitting) and pre joining
    #{
        formattedList = listToMark
        currString    = "" # The current string being parsed

        if(listToMark is None):
        #{
            formattedList = self.getFileContents()
        #}
        else:
        #{
            formattedList = listToMark # Same list as passed in, but with carrage returns marked
        #}

        for i in range(len(formattedList)): # SMELL can't use '|'
        #{
            if(("\n" in formattedList[i]) and (" |" not in formattedList[i])): # Chekc if not already been formatted
            #{
                formattedList[i] += " |" # space to seperat bar from existing string
            #}
        #}

        return formattedList
    #}

    def getTotalNumbOfChars(self, toFindIn): # Adds up number of chars
    #{
        if(toFindIn is None):
        #{
            fileContents = self.getFileContents()
        #}
        else:
        #{
            fileContents = toFindIn
        #}

        lengthOfFile   = self.getNumbOfLines()
        totalLength = 0 # Numb of chars in file

        for i in range(lengthOfFile):
        #{
            totalLength += len(fileContents[i])
        #}

        return totalLength
    #}

    def getTotalNumbOfStrings(self):
    #{
        separatedFile = "".join(self.getFileContents()).split() # Seperate file into strings
        totalLength   = len(separatedFile)

        return totalLength
    #}

    def findCapitalLetters(self): # Returns the position of captials
    #{
        fileContents          = "".join(self.markNewLines(self.getFileContents())) # Convert to string for parsing
        capitalLocations      = [] # line, chars across
        currCapitalLocation   = [None, None] # Temp var used to 'bundle' arrays
        lineNumber            = 0 # number of line currently being read
        totalLengthOfFile     = self.getTotalNumbOfChars(None) # total number of chars in the file
        currChar              = "" # Current char being read
        charsAcross           = 0 # Number of chars that have been read(column)
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
                currCapitalLocation[0] = lineNumber
                currCapitalLocation[1] = positionInCurrentLine

                capitalLocations.append(currCapitalLocation)

                currCapitalLocation = [None, None]
            #}

            charsAcross += 1
            positionInCurrentLine += 1
        #}

        return capitalLocations
    #}

    def findPunctuation(self, startPoint, toFindIn):
    #{
        if(toFindIn is None):
        #{
            fileContents = self.getFileContents()
        #}
        else:
        #{
            fileContents = toFindIn
        #}

        if(startPoint is None):
        #{
            currLine       = "" # Current line being read
            currChar       = "" # Current char being read
            currLineNumber = 0 # Numerical rep of line being read
            currCharNumber = 0 # Numerical rep of column being read
        #}
        else:
        #{
            currLineNumber = startPoint[0]
            currCharNumber = startPoint[1]
            currLine       = fileContents[currLineNumber]
            currCharNumber = fileContents[currCharNumber]
        #}

        lengthOfFile  = self.getNumbOfLines()
        punctuation   = [",", ".", "(", ")", "!", "", '"', "£", "$", "%", "^",
                         "&", "*", "[", "]", "{", "}", "`", "¬", "|", " \ ", ":",
                         ";", "~", "@", "-", "_"] # Which fool decided to use Python!
        puncPositions = [] # Line number, char
        currPuncPos   = [None, None] # Temp Var used to 'bundle' arrays

        for i in range(lengthOfFile):
        #{
            currLine = fileContents[i]

            for pos in range(len(currLine)):
            #{
                currChar = currLine[pos]
                currCharNumber += 1

                if(currChar in punctuation):
                #{
                    currPuncPos[0] = currLineNumber
                    currPuncPos[1] = currCharNumber - 1 # Counteract startpoint being 0

                    puncPositions.append(currPuncPos)

                    currPuncPos = [None, None]
                #}
            #}

            currCharNumber = 0 # re-set back to default
            currLineNumber += 1 # after, to make statement above valid
        #}

        return puncPositions
    #}

    def removePunctuation(self, punctuationCoords, startPoint, toFindIn):
    #{
        fileContents = self.getFileContents()
        startPoints  = self.findPunctuation(startPoint, toFindIn)
        currLine     = "" # Current Alpha-form line being read
        currChar     = "" # Current Alpha-form char being read
        currLineNumb = 0 # Current Numerical-form line being read
        currCharNumb = 0 # Current Numerical-form char being read

        for i in range(len(startPoints) - 1): # While there are still caps to change todo out of range too small, one extra value is ignored
        #{
            currLineNumb               = startPoints[i][0] # Line
            currCharNumb               = startPoints[i][1] # Char
            currLine                   = " ".join(fileContents[currLineNumb].split()) # convert to String keeping spaces
            currChar                   = currLine[currCharNumb] # Split the string up into a list of chars
            currLine                   = currLine.replace(currChar, "") # TODO world's larget's pain in the arse, see problems(>>>)
            fileContents[currLineNumb] = currLine
        #}

        return fileContents
    #}

    def findString(self, toFind, toFindIn, startPoint): # To find in is the text body to look in (optional if passed in)
    #{
        toFind         = toFind
        toFindPosition = [None, None] # Contains where toFind is found
        startPoint     = startPoint
        lengthOfFile   = self.getNumbOfLines() # Gets all of the length (lines, length of lines)
        numbOfLines    = self.getNumbOfLines()

        if(toFindIn is None): # if nothing given
        #{
            fileContents = self.getFileContents()
        #}
        else:
        #{
            fileContents = toFindIn
        #}

        currLine    = "" # Line being read
        currChar    = "" # Character being read
        currLinePos = 0 # Line being read (position)
        currCharPos = 0 # Character being read (position)
        lenCurrLine = -1 # Length of the line being read
        foundItem   = False # If the loop has found 'toFind'
        pos         = 0 # Loop counter

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

        return toFindPosition
    #}

    def findAllStrings(self, toFind, toFindIn, newStartPoint): # TODO
    #{
        pass
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

p_1 = Parser(file)

print(p_1.removePunctuation(None, None, None))
