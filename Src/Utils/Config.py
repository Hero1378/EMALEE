class Config(): # TODO remove any 'temp file ghuff'
#{
    def __init__(self, fileName): # TODO add somthing to remove spaces in valueNames (like with colons)
    #{
        self.fileName = (str(fileName) + ".conf")

        try: # Does file exist
        #{
            self.FILE = open(self.fileName, "r")
        #}
        except(IOError) as error: # If no existing file, make one
        #{
            print("Got error: " + str(error))

            self.FILE = open(self.fileName, "w")

            self.FILE.close()

            self.FILE = open(self.fileName, "r")
        #}

        self.values = {}

    def getLengthOfFile(self):
    #{
        lengthOfFile = len(self.FILE.readlines())

        self.resetFile()

        return lengthOfFile
    #}

    def resetFile(self): # Used to go back to first line
    #{
        self.FILE = open(self.fileName, "r")
    #}

    def getFileContents(self):
    #{
        fileContents = []
        lengthOfFile = self.getLengthOfFile()
        currLine     = ""
        pos          = 0

        while(pos <= lengthOfFile):
        #{
            currLine = self.FILE.readline()

            if(currLine != ""):
            #{
                fileContents.append(currLine)
            #}

            pos += 1
        #}

        self.resetFile()

        return "".join(fileContents).split() # removes newlines
    #}

    def getBundledFileContents(self): # Gets file contents in nth-D array
    #{
        fileContents        = self.getFileContents()
        bundledFileContents = [] # BFE
        tempBundle          = [None, None] # used to 'bundle' array
        isComplete          = False # Fires every 2 loops, to allow BFC to be appended to

        for i in range(len(fileContents)):
        #{
            if((i % 2) == 0): # Test if even to alternate [0/1]
            #{
                tempBundle[0] = fileContents[i]
                isComplete    = False
            #}
            else:
            #{
                tempBundle[1] = fileContents[i]
                isComplete    = True
            #}

            if(isComplete):
            #{
                bundledFileContents.append(tempBundle)

                tempBundle = [None, None]
            #}
        #}

        return bundledFileContents
    #}

    def getValueNames(self):
    #{
        fileContents = self.getFileContentsNoNewLines()
        lengthOfFile = self.getLengthOfFile()
        names        = [] # All of values
        currLine     = ""
        currName     = "" # Semi- complete value being parsed
        currChar     = "" # Char being parsed
        lineNumber   = 0

        while(lineNumber <= lengthOfFile):
        #{
            currLine = fileContents[lineNumber]

            for i in range(len(currLine)):
            #{
                currChar = currLine[i]

                if(currChar == ":"):
                #{
                    break
                #}
                else:
                #{
                    currName += currChar
                #}
            #}

            names.append(currName)

            currName   = "" # Set to default
            lineNumber += 1
        #}

        if("" in names):
        #{
            while("" in names):
            #{
                names.remove("")
            #}
        #}

        return names
    #}

    def getFileContentsNoNewLines(self):
    #{
        fileContents = []
        lengthOfFile = self.getLengthOfFile()
        currLine     = ""
        currChar     = ""
        lineNumber   = 0

        while(lineNumber <= lengthOfFile):
        #{
            currLine = " ".join(self.FILE.readline().split()) # Remove '\n'

            fileContents.append(currLine)

            lineNumber += 1
        #}

        self.resetFile()

        return fileContents
    #}

    def getAmounts(self):
    #{
        fileContents = self.getFileContentsNoNewLines()
        lengthOfFile = self.getLengthOfFile()
        amounts      = []
        currLine     = ""
        currChar     = ""
        currAmount   = "" # Semi- complete amount being parsed
        lineNumber   = 0

        while(lineNumber <= lengthOfFile):
        #{
            currLine = fileContents[lineNumber]

            for i in range(len(currLine)):
            #{
                currChar = currLine[i]

                if(currChar == ":"):
                #{
                    currAmount = currLine[(i + 1) : len(currLine)] # Everything AFTER the colon

                    amounts.append(currAmount)

                    break
                #}
            #}

            lineNumber += 1
        #}

        return amounts
    #}

    def getValueLineNumbers(self): # Returns line numbers in 'Machine Numbers'
    #{
        lineNumbers      = {}
        lengthOfFile     = self.getLengthOfFile()
        currLineNumber   = 0
        currLine         = ""
        currValue        = ""
        currChar         = ""
        pos              = 0 # Position in current line being parsed

        while(currLineNumber < lengthOfFile):
        #{
            currLine = "".join(self.FILE.readline().split())

            while((currChar != ":") and (pos < len(currLine))):
            #{
                currChar = currLine[pos]

                pos += 1
            #}

            currValue = currLine[0 : (pos - 1)] # '-1' as UP TO colon

            lineNumbers[currValue] = currValue
            lineNumbers[currValue] = currLineNumber - 1 # To counteract previous nam

            currChar        = ""
            pos             = 0 # Reset
            currLineNumber += 1
        #}

        self.resetFile()

        return lineNumbers
    #}

    def getValues(self):  #T ODO
    #{
        valueNames   = self.getValueNames()
        valueAmounts = self.getAmounts()
        currValue    = ""
        currAmount   = ""

        if(len(valueNames) != len(valueAmounts)):
        #{
            print("LengthMismatchError: The length of valueNames and valueAmounts"
                  " does not match.")

            return # Break
        #}

        for i in range(len(valueNames)):
        #{
            currValue  = valueNames[i]
            currAmount = valueAmounts[i]

            if(currAmount[0] == " "): # Removes space at start of string
            #{
                currAmount = " ".join(currAmount.split())
            #}

            self.values[currValue] = currValue # Add new key
            self.values[currValue] = currAmount
        #}

        return self.values
    #}

    def addValue(self, newValueName, newValueAmount):
    #{
        values       = self.getValueNames()
        self.FILE    = open(self.fileName, "a") # open after values TODO file mode conflict
        valueName    = newValueName
        valueAmount  = newValueAmount

        if(":" in valueName): # remove : to stop mix-up
        #{
            valueName = valueName.replace(":", "")
        #}

        if(" " in valueName): # remove ' ' to stop mix-up
        #{
            valueName = valueName.replace(" ", "")
        #}

        if(valueName not in values): # prevent doubles
        #{
            self.FILE.write(str(valueName) + ": " + str(valueAmount) + "\n") # E.G. xValue: 12
        #}
        else:
        #{
            print("The valueName: '" + str(valueName) + "' given already existes") # TRY?
        #}

        self.resetFile()
    #}

    def editValueAmount(self, value, newValueAmount): # TODO
    #{
        fileContents                   = self.getBundledFileContents()
        valueLine                      = self.getValueLineNumbers()[value]
        self.FILE                      = open(self.fileName, "w")
        fileContents[valueLine + 1][1] = newValueAmount # +1 to skip machine code
        currName                       = ""
        currValue                      = ""

        for i in range (len(fileContents)):
        #{
            currName = fileContents[i][0]

            for pos in range(len(fileContents[i])): # Add spaces between elements
            #{
                currValue += " " + str(fileContents[i][pos])
            #}

            self.FILE.write(str(currName) + " " + str(currValue) + "\n")
        #}

        self.resetFile()
    #}

    def editValueName(self, value, newValueName):
    #{
        fileContents                   = self.getBundledFileContents()
        valueLine                      = self.getValueLineNumbers()[value]
        self.FILE                      = open(self.fileName, "w")
        fileContents[valueLine + 1][0] = newValueName # +1 to skip machine code
        currName                       = ""
        currValue                      = ""

        for i in range (len(fileContents)):
        #{
            currName = fileContents[i][0]
            currValue = fileContents[i][1]

            if(":" not in currName):
            #{
                self.FILE.write(str(currName) + ": " + str(currValue) + "\n")
            #}
            else:
            #{
                self.FILE.write(str(currName) + " " + str(currValue) + "\n")
            #}
        #}

        self.resetFile()
    #}

    def removeValue(self, valueToRemove):
    #{
        fileContents                   = self.getBundledFileContents()
        valueLine                      = self.getValueLineNumbers()[valueToRemove]
        self.FILE                      = open(self.fileName, "w")
        fileContents[valueLine + 1][0] = "" # +1 to skip machine code
        fileContents[valueLine + 1][1] = "" # +1 to skip machine code
        currName                       = ""
        currValue                      = ""

        for i in range (len(fileContents)):
        #{
            currName = fileContents[i][0]
            currValue = fileContents[i][1]

            if((":" not in currName) and (currName != "")):
            #{
                self.FILE.write(str(currName) + ": " + str(currValue) + "\n")
            #}
            else:
            #{
                if(currName != ""):
                #{
                    self.FILE.write(str(currName) + " " + str(currValue) + "\n")
                #}
            #}
        #}

        self.resetFile()
    #}
#}