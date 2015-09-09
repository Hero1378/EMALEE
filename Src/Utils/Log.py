"""
Copyright 2015 Felix Woodhead

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0
"""

import os
import time

class Log:
#{
    def __init__(self, fileName, path):
    #{
        self.path          = path
        self.fileName      = fileName

        fileCreationFailed = False # Flag if any of the statements below are triggered

        try:
        #{
            if(self.path is None):
            #{
                print("Path not valid. Opening file in current working directory")

                self.path = os.getcwd() + "/" # Make log in current dir
            #}

            if(not os.path.exists(self.path)): # Check if self.path exists
            #{
                fileCreationFailed = True

                print("Path not valid. Making file in current working directory")

                self.path = os.getcwd() + "/" # Make log in current dir
            #}

            if(self.fileName[0].islower()):
            #{
                self.fileName = list(self.fileName)
                self.fileName[0] = self.fileName[0].upper()
                self.fileName = "".join(self.fileName) # Make first char upperCase
            #}

            if(((self.fileName + ".log") in os.listdir(self.path)) and
               (fileCreationFailed)):
            #{
                existingFiles = os.listdir() # Get existing files
                oldFileName   = self.fileName
                pos           = 0 # Loop counter
                madeFileName  = False # True if valid name has been made

                while(not madeFileName):
                #{
                    self.fileName = oldFileName + "_" + str(pos) + ".log"

                    if(self.fileName not in existingFiles):
                    #{
                        madeFileName = True

                        continue
                    #}

                    pos += 1
                #}

                print("FileName already exists, renaming fileName to: " +
                       self.fileName)
            #}

            if(".log" not in self.fileName):
            #{
                self.file = open(str(str(self.path) + "/" + str(self.fileName) +
                                 ".log"), "w")
            #}
            else:
            #{
                self.file = open(str(str(self.path) + "/" + str(self.fileName)),
                                 "w")
            #}

            if((self.fileName is None) or (self.fileName == "")):
            #{
                existingFiles = os.listdir() # Get existing files
                oldFileName   = "Log"
                pos           = 0 # Loop counter
                madeFileName  = False # True if valid name has been made

                while(not madeFileName):
                #{
                    self.fileName = oldFileName + "_" + str(pos) + ".log"

                    if(self.fileName not in existingFiles):
                    #{
                        madeFileName = True

                        continue
                    #}

                    pos += 1
                #}
            #}

            self.file = open(str(self.path + "/" + self.fileName + ".log"), "r+")
        #}
        except(IOError) as error:
        #{
            print("Got error: " + str(error))
            print("Making new file in" + str(self.path) + " named: " +
                   self.fileName)

            if(".log" not in self.fileName):
            #{
                self.file = open(str(str(self.path) + "/" + str(self.fileName) +
                                 ".log"), "w")
            #}
            else:
            #{
                self.file = open(str(str(self.path) + "/" + str(self.fileName)),
                                 "w")
            #}
        #}
    #}

    def __getDateTime(self):
    #{
        dateTime = (time.strftime("%Y") + "-" + time.strftime("%m") + "-" +
                    time.strftime("%e") + " " + time.strftime("%H") + ":" +
                    time.strftime("%M") + ":" + time.strftime("%S"))

        return dateTime # DATE-MONTH-DAY HOUR-MIN-SECOND
    #}

    def outInfo(self, message): # Display to STD out
    #{
        print(str(self.__getDateTime()) + " [INFO] " + message) # Description of Events
    #}

    def outWarn(self, message):
    #{
        print(str(self.__getDateTime()) + " [WARN] " + message) # Things are slightly different to normal
    #}

    def outError(self, message):
    #{
        print(str(self.__getDateTime()) + " [ERROR] " + message) # Something's unresponsive, all unhandled xceptions
    #}

    def outSevere(self, message):
    #{
        print(str(self.__getDateTime()) + " [SEVERE] " + message) # Something really bad, probably going to cause program to crash
    #}

    def outFatal(self, message):
    #{
        print(str(self.__getDateTime()) + " [FATAL] " + message) # Somtheing that has broken the program
    #}

    def logInfo(self, message): # Add to log file (standard)
    #{
        self.file.write(self.__getDateTime() + " [INFO] " + message + "\n")
    #}

    def logWarn(self, message):
    #{
        self.file.write(self.__getDateTime() + " [WARN] " + message + "\n")
    #}

    def logError(self, message):
    #{
        self.file.write(self.__getDateTime() + " [INFO] " + message + "\n")
    #}

    def logSevere(self, message):
    #{
        self.file.write(self.__getDateTime() + " [SEVERE] " + message + "\n")
    #}

    def logFatal(self, message):
    #{
        self.file.write(self.__getDateTime() + " [FATAL] " + message + "\n")
    #}
#}
