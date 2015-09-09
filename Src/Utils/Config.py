"""
Copyright 2015 Felix Woodhead

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0
"""

class Config():
#{
    def __init__(self, fileName):
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

    def __getLengthOfFile(self):
    #{
        lengthOfFile = len(self.FILE.readlines())

        self.__resetFile()

        return lengthOfFile
    #}

    def __resetFile(self): # Used to go back to first line and get changes
    #{
        self.FILE = open(self.fileName, "r")
    #}

    def __getFileContents(self):
    #{
        fileContents = []
        lengthOfFile = self.__getLengthOfFile()
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

        self.__resetFile()

        return "".join(fileContents).split() # removes newlines
    #}

    def __getBundledFileContents(self): # Gets file contents in nth-D array
    #{
        names               = self.__getValueNames() # Used for getting names
        amounts             = self.__getFieldValues() # Used for getting amounts
        bundledFileContents = [] # BFE
        tempBundle          = [None, None] # used to 'bundle' array

        if(len(names) != len(amounts)):
        #{
            print("Got error: lengthMismatchError")

            return
        #}

        for i in range(len(amounts)):
        #{
            tempBundle[0] = names[i]
            tempBundle[1] = amounts[i]

            bundledFileContents.append(tempBundle)

            tempBundle = [None, None] # Set to default to enable re-use
        #}

        return bundledFileContents
    #}

    def __getValueNames(self):
    #{
        fileContents = self.__getFileContentsNoNewLines()
        lengthOfFile = self.__getLengthOfFile()
        names        = [] # All of values
        currLine     = ""
        currName     = "" # Semi- complete value being parsed
        currChar     = "" # Char being parsed
        lineNumber   = 0

        while(lineNumber <= lengthOfFile):
        #{
            currLine = fileContents[lineNumber]

            if(len(currLine) > 0): # Ignore newlines
            #{
                if("".join(currLine)[0] == "#"): # Ignore comments
                #{
                    currName   = "" # Set to default
                    lineNumber += 1

                    continue
                #}
            #}

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

    def __getFileContentsNoNewLines(self):
    #{
        fileContents = []
        lengthOfFile = self.__getLengthOfFile()
        currLine     = ""
        currChar     = ""
        lineNumber   = 0

        while(lineNumber <= lengthOfFile):
        #{
            currLine = " ".join(self.FILE.readline().split()) # Remove '\n'

            fileContents.append(currLine)

            lineNumber += 1
        #}

        self.__resetFile()

        return fileContents
    #}

    def __getFieldValues(self):
    #{
        fileContents = self.__getFileContentsNoNewLines()
        lengthOfFile = self.__getLengthOfFile()
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

    def __getValueLineNumbers(self): # Returns line numbers in 'Machine Numbers'
    #{
        lineNumbers      = {}
        lengthOfFile     = self.__getLengthOfFile()
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

        self.__resetFile()

        return lineNumbers
    #}

    def getValues(self):  #T ODO
    #{
        valueNames   = self.__getValueNames()
        valueAmounts = self.__getFieldValues()
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

    def addField(self, newValueName, newValueAmount):
    #{
        values       = self.__getValueNames()
        self.FILE    = open(self.fileName, "a") # open after values
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

        self.__resetFile()
    #}

    def addComment(self, comment):
    #{
        self.FILE    = open(self.fileName, "a") # open after values

        self.FILE.write("# " + str(comment) + "\n") # E.G. xValue: 12

        self.__resetFile()
    #}

    def editFieldValue(self, value, newValueAmount):
    #{
        fileContents                   = self.__getBundledFileContents()
        valueLine                      = self.__getValueLineNumbers()[value]
        self.FILE                      = open(self.fileName, "w")
        fileContents[valueLine + 1][1] = newValueAmount # +1 to skip machine code
        currName                       = ""
        currValue                      = ""

        for i in range (len(fileContents)):
        #{
            currName = fileContents[i][0]

            pos = 1
            while(pos < len(fileContents[i])): # Start from 1 to avoid first element
            #{
                currValue += "" + str(fileContents[i][pos]) # Add spaces and concatente

                pos += 1
            #}

            currValue = " ".join(currValue.split()) # Remove 'ghost' space at start of string

            self.FILE.write(str(currName) + ": " + str(currValue) + "\n")


            currValue = ""
        #}

        self.__resetFile()
    #}

    def editFieldName(self, value, newValueName):
    #{
        fileContents                   = self.__getBundledFileContents()
        valueLine                      = self.__getValueLineNumbers()[value]
        self.FILE                      = open(self.fileName, "w")
        fileContents[valueLine + 1][0] = newValueName # +1 to skip machine code
        currName                       = ""
        currValue                      = ""

        for i in range (len(fileContents)):
        #{
            currName  = fileContents[i][0]
            currValue = fileContents[i][1]
            currValue = " ".join(currValue.split()) # Remove 'ghost' space at start of string

            if(":" not in currName):
            #{
                self.FILE.write(str(currName) + ": " + str(currValue) + "\n")
            #}
            else:
            #{
                self.FILE.write(str(currName) + " " + str(currValue) + "\n")
            #}
        #}

        self.__resetFile()
    #}

    def removeField(self, valueToRemove):
    #{
        fileContents                   = self.__getBundledFileContents()
        valueLine                      = self.__getValueLineNumbers()[valueToRemove]
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
                    self.FILE.write(str(currName) + "" + str(currValue) + "\n")
                #}
            #}
        #}

        self.__resetFile()
    #}
#}
