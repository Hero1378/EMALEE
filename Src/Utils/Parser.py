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

        self.FILE.close() # re-open file at first line QWFX SMELL
        self.FILE = open(self.file, "r+")

        return fileLen
    #}

    def find(self, toFindType, toFind, startPoint):
    #{
        toFind = toFind
        toFindType = toFindType
        startPoint = startPoint
        lengthOfFile = self.getFileLen()[0]
        fileContents = self.getFileContents()
        foundItem = False # If the loop has found 'toFind'
        pos = 0 # Loop counter

        if(toFindType not in ("string", "char")): # Pre-checks
        #{
            raise NameError
        #}
        elif(len(toFind) < 1):
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
            elif(len(startPoint[0]) > self.getFileLen()[0]):
            #{
                raise NameError # line given doesn't exist
            #}
            elif(len(startPoint[1]) > self.getFileLen()[1]):
            #{
                raise NameError # line given doesn't exist
            #}
        #}

        print("len fileContents: ", len(fileContents)) # QWFX

        while((not foundItem) and (pos < len(fileContents))): # loops until found the item, or array end reached
        #{
            pass # TODO
            pos += 1
        #}
    #}
#}

file = "FileExample.txt"

p = Parser(file)
p.find("string", "qui", None)
