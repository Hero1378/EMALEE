class Config():
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
        self.FILE = open(self.fileName, "r")

        lengthOfFile = len(self.FILE.readlines())

        self.FILE.close()
        self.FILE = open(self.fileName, "r")

        return lengthOfFile
    #}

    def getFileContents(self):
    #{
        fileContents = []
        currLine     = ""
        pos          = 0

        while(pos <= self.getLengthOfFile()):
        #{
            currLine = self.FILE.readline()

            fileContents.append(currLine)

            pos += 1
        #}

        return "".join(fileContents).split() # removes newlines
    #}

    def getValueNames(self):
    #{
        fileContents = self.getFileContentsNoNewLines()
        names        = [] # All of values
        currLine     = ""
        currName     = "" # Semi- complete value being parsed
        currChar     = "" # Char being parsed
        lineNumber   = 0

        while(lineNumber <= self.getLengthOfFile()):
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

        self.FILE.close()

        self.FILE = open(self.fileName, "r")

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
        tempFile     = open(self.fileName, "r")
        fileContents = []
        currLine     = ""
        currChar     = ""
        lineNumber   = 0

        while(lineNumber <= self.getLengthOfFile()):
        #{
            currLine = "".join(tempFile.readline().split()) # Remove '\n'

            fileContents.append(currLine)

            lineNumber += 1
        #}

        tempFile.close()

        return fileContents
    #}

    def getAmounts(self):
    #{
        fileContents = self.getFileContentsNoNewLines()
        amounts      = []
        currLine     = ""
        currChar     = ""
        currAmount   = "" # Semi- complete amount being parsed
        lineNumber   = 0

        while(lineNumber <= self.getLengthOfFile()):
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

    def getValues(self):  #T ODO
    #{
        valueNames   = self.getValueNames()
        valueAmounts = self.getAmounts()
        currValue    = ""
        currAmount   = ""

        if(len(valueNames) != len(valueAmounts)):
        #{
            print("LengthMismachError: The length of valueNames and valueAmounts"
                  " does not match.")

            return # Break
        #}

        for i in range(len(valueNames)):
        #{
            currValue  = valueNames[i]
            currAmount = valueAmounts[i]

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

        self.FILE.close()

        self.FILE = open(self.fileName, "r")
    #}

    def editValue(self, value, newValueAmount):
    #{
        pass
    #}

    def removeValue(self, valueToRemove):
    #{
        fileContents = self.getFileContents()

        pass
    #}
#}

c = Config("Text")
print(c.getValues())
