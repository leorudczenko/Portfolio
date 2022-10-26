import sqlite3,os


# Function to print a number of empty lines to create spacing
def Spacing(Lines):
    for x in range(Lines):
        print()


# Function to convert a list of tuples with length 1 to a standard array
def ConvertTupleList(List):
    NewList = []
    for Tuple in List:
        NewList.append(Tuple[0])
    return NewList


# Function to create the a table to store command translations
def CreateTranslationsTable(cr, db):
    cr.execute("""CREATE TABLE CommandTranslations(
    Language_ID integer primary key AUTOINCREMENT,
    LanguageName varchar,
    SALTFalseSALT varchar,
    SALTNoneSALT varchar,
    SALTTrueSALT varchar,
    SALTandSALT varchar,
    SALTasSALT varchar,
    SALTassertSALT varchar,
    SALTasyncSALT varchar,
    SALTawaitSALT varchar,
    SALTbreakSALT varchar,
    SALTclassSALT varchar,
    SALTcontinueSALT varchar,
    SALTdefSALT varchar,
    SALTdelSALT varchar,
    SALTelifSALT varchar,
    SALTelseSALT varchar,
    SALTexceptSALT varchar,
    SALTfinallySALT varchar,
    SALTforSALT varchar,
    SALTfromSALT varchar,
    SALTglobalSALT varchar,
    SALTifSALT varchar,
    SALTimportSALT varchar,
    SALTinSALT varchar,
    SALTisSALT varchar,
    SALTnonlocalSALT varchar,
    SALTnotSALT varchar,
    SALTorSALT varchar,
    SALTpassSALT varchar,
    SALTraiseSALT varchar,
    SALTreturnSALT varchar,
    SALTtrySALT varchar,
    SALTwhileSALT varchar,
    SALTwithSALT varchar,
    SALTyieldSALT varchar,
    SALTabsSALT varchar,
    SALTallSALT varchar,
    SALTanySALT varchar,
    SALTbinSALT varchar,
    SALTboolSALT varchar,
    SALTbytearraySALT varchar,
    SALTbytesSALT varchar,
    SALTcallableSALT varchar,
    SALTchrSALT varchar,
    SALTclassmethodSALT varchar,
    SALTcompileSALT varchar,
    SALTcomplexSALT varchar,
    SALTdelattrSALT varchar,
    SALTdictSALT varchar,
    SALTdirSALT varchar,
    SALTdivmodSALT varchar,
    SALTenumerateSALT varchar,
    SALTevalSALT varchar,
    SALTexecSALT varchar,
    SALTfilterSALT varchar,
    SALTfloatSALT varchar,
    SALTformatSALT varchar,
    SALTfrozensetSALT varchar,
    SALTgetattrSALT varchar,
    SALTglobalsSALT varchar,
    SALThasattrSALT varchar,
    SALThashSALT varchar,
    SALThelpSALT varchar,
    SALThexSALT varchar,
    SALTidSALT varchar,
    SALTinputSALT varchar,
    SALTintSALT varchar,
    SALTisinstanceSALT varchar,
    SALTissubclassSALT varchar,
    SALTiterSALT varchar,
    SALTlenSALT varchar,
    SALTlistSALT varchar,
    SALTlocalsSALT varchar,
    SALTmapSALT varchar,
    SALTmaxSALT varchar,
    SALTmemoryviewSALT varchar,
    SALTminSALT varchar,
    SALTnextSALT varchar,
    SALTobjectSALT varchar,
    SALToctSALT varchar,
    SALTopenSALT varchar,
    SALTordSALT varchar,
    SALTpowSALT varchar,
    SALTprintSALT varchar,
    SALTpropertySALT varchar,
    SALTrangeSALT varchar,
    SALTreprSALT varchar,
    SALTreversedSALT varchar,
    SALTroundSALT varchar,
    SALTsetSALT varchar,
    SALTsetattrSALT varchar,
    SALTsliceSALT varchar,
    SALTsortedSALT varchar,
    SALTstaticmethodSALT varchar,
    SALTstrSALT varchar,
    SALTsumSALT varchar,
    SALTsuperSALT varchar,
    SALTtupleSALT varchar,
    SALTtypeSALT varchar,
    SALTvarsSALT varchar,
    SALTzipSALT varchar
    );""")
    db.commit()


# Function to insert a given language record to the database
def InsertLanguageRecord(cr, db, Record):
    for Position in range(1,len(Record)):
        Record[Position] = "SALT" + str(Record[Position]) + "SALT"
    Record = tuple(Record)
    cr.execute("""INSERT INTO CommandTranslations(
    LanguageName,
    SALTFalseSALT,
    SALTNoneSALT,
    SALTTrueSALT,
    SALTandSALT,
    SALTasSALT,
    SALTassertSALT,
    SALTasyncSALT,
    SALTawaitSALT,
    SALTbreakSALT,
    SALTclassSALT,
    SALTcontinueSALT,
    SALTdefSALT,
    SALTdelSALT,
    SALTelifSALT,
    SALTelseSALT,
    SALTexceptSALT,
    SALTfinallySALT,
    SALTforSALT,
    SALTfromSALT,
    SALTglobalSALT,
    SALTifSALT,
    SALTimportSALT,
    SALTinSALT,
    SALTisSALT,
    SALTnonlocalSALT,
    SALTnotSALT,
    SALTorSALT,
    SALTpassSALT,
    SALTraiseSALT,
    SALTreturnSALT,
    SALTtrySALT,
    SALTwhileSALT,
    SALTwithSALT,
    SALTyieldSALT,
    SALTabsSALT,
    SALTallSALT,
    SALTanySALT,
    SALTbinSALT,
    SALTboolSALT,
    SALTbytearraySALT,
    SALTbytesSALT,
    SALTcallableSALT,
    SALTchrSALT,
    SALTclassmethodSALT,
    SALTcompileSALT,
    SALTcomplexSALT,
    SALTdelattrSALT,
    SALTdictSALT,
    SALTdirSALT,
    SALTdivmodSALT,
    SALTenumerateSALT,
    SALTevalSALT,
    SALTexecSALT,
    SALTfilterSALT,
    SALTfloatSALT,
    SALTformatSALT,
    SALTfrozensetSALT,
    SALTgetattrSALT,
    SALTglobalsSALT,
    SALThasattrSALT,
    SALThashSALT,
    SALThelpSALT,
    SALThexSALT,
    SALTidSALT,
    SALTinputSALT,
    SALTintSALT,
    SALTisinstanceSALT,
    SALTissubclassSALT,
    SALTiterSALT,
    SALTlenSALT,
    SALTlistSALT,
    SALTlocalsSALT,
    SALTmapSALT,
    SALTmaxSALT,
    SALTmemoryviewSALT,
    SALTminSALT,
    SALTnextSALT,
    SALTobjectSALT,
    SALToctSALT,
    SALTopenSALT,
    SALTordSALT,
    SALTpowSALT,
    SALTprintSALT,
    SALTpropertySALT,
    SALTrangeSALT,
    SALTreprSALT,
    SALTreversedSALT,
    SALTroundSALT,
    SALTsetSALT,
    SALTsetattrSALT,
    SALTsliceSALT,
    SALTsortedSALT,
    SALTstaticmethodSALT,
    SALTstrSALT,
    SALTsumSALT,
    SALTsuperSALT,
    SALTtupleSALT,
    SALTtypeSALT,
    SALTvarsSALT,
    SALTzipSALT)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", Record)
    db.commit()


# Function to get a given language record from the database using it's ID value
def SelectLanguageRecord(cr, db, RecordID):
    # Select all records from the table that match the given language
    cr.execute("""SELECT * FROM CommandTranslations WHERE Language_ID = ?""",(RecordID,))
    Record = cr.fetchall()[0]
    # Create an empty list to store the unsalted translations
    NewRecord = []
    # For each translation word, remove the salt and save it to the new list
    for Position in range(2, len(Record)):
        NewRecord.append(str(Record[Position])[4:-4])
    return NewRecord


# Function to get all language records from the database
def SelectAllLanguageRecords(cr, db):
    cr.execute("""SELECT * FROM CommandTranslations""")
    return cr.fetchall()


# Function to delete a given language record from the database using it's ID value
def DeleteLanguageRecord(cr, db, RecordID):
    cr.execute("""DELETE FROM CommandTranslations WHERE Language_ID = ?""",(RecordID,))
    db.commit()


# Function to save given data to a given filename
def SaveFile(Filename, FileData, NewLanguageID):
    # If the language is Python standard formatting, then a .py file is required
    if NewLanguageID == 1:
        Filename += ".py"
    # Else, a .txt file is required
    else:
        Filename += ".txt"
    # Create the file
    File = open(Filename, "a")
    # Save the data
    File.writelines(FileData)
    File.close()
    # Output a message to confirm file creation
    print("Translated file created: {0}".format(Filename))


# Function to read the data from a given file
def ReadFile(Filename):
    # Open the file
    File = open(Filename, "r")
    # Read the data and split the file contents into a list of lines
    Data = File.read().splitlines()
    File.close()
    # Output a message to confirm file read
    print("Loaded file: {0}".format(Filename))
    Spacing(1)
    return Data


# Function to get the name of the existing file from the user via input
def GetExistingFilename():
    # Retrieval is equal to False once a valid input has been provided
    Retrieval = True
    while Retrieval is True:
        # Get the existing file name as input
        ExistingFilename = str(input("Input file name including the file extension: "))
        # If the given file exists, stop the loop and return the file name
        if os.path.isfile(ExistingFilename) is True:
            Retrieval = False
            Spacing(1)
            return ExistingFilename
        # Else, output a message informing the error
        else:
            print("Please input an existing filename.")
        

# Function to get the ID of a language via user input
def GetLanguageID(cr, db, Type):
    # Get all language records from the database
    LanguagesData = SelectAllLanguageRecords(cr, db)
    # Create an empty list to store the ID value of each language
    LanguageIDs = []
    # For each language record, save the ID value to the list
    for LanguageData in LanguagesData:
        LanguageIDs.append(LanguageData[0])

    # If getting the current language of the script
    if Type == "current":
        # Output a list of available languages
        print("Available Languages:")
        for LanguageData in LanguagesData:
            print("{0} (ID: {1})".format(LanguageData[1], LanguageData[0]))
        Spacing(1)

    # Retrieval is equal to False once a valid input has been provided
    Retrieval = True
    while Retrieval is True:
        # Get a language ID as user input
        LanguageID = input("Please input the ID number of the {0} language for script: ".format(Type))
        # Try, except incase conversion of input to an integer causes an error
        try:
            # Convert input to an integer
            LanguageID = int(LanguageID)
            # If the given ID matches an existing language, stop the loop and return the language ID
            if LanguageID in LanguageIDs:
                Retrieval = False
                return LanguageID
            # Else, output a message informing the error
            else:
                print("Please input the ID number of an existing language.")
        except:
            print("Please input the ID number of an existing language.")
    Spacing(1)


# Function to get the name of the new file from the user via input
def GetNewFilename():
    # Retrieval is equal to False once a valid input has been provided
    Retrieval = True
    while Retrieval is True:
        # Get the new file name as input
        NewFilename = str(input("Input the new filename excluding the file extension: "))
        # If the file name is has characters in it
        if len(NewFilename) > 0:
            # Create a boolean value to indicate if an invalid special character is in the new file name
            SpecialCharacterBool = False
            # For each invalid special character
            for SpecialCharacter in ["\\", "/", ":", "@", "?", '"', "<", ">", "|"]:
                # If the character is in the new file name, change the boolean value to True
                if SpecialCharacter in NewFilename:
                    SpecialCharacterBool = True
            # If there is an invalid special character in the file name
            if SpecialCharacterBool is True:
                # Output a message informing the error
                print("Please input a valid filename.")
            # Else, stop the loop and return the new file name
            else:
                Retrieval = False
                Spacing(1)
                return NewFilename
        # Else, output a message informing the error
        else:
            print("Please input a valid filename.")


# Function to calculate which words must be translated in the given script
# The function will iterate through each character within the script
# As it does this, it will run checks to ensure Strings, DocStrings and Comments are ignored during translation
# It will then decipher which words within the script require translating
def GetWordsToReplace(FileData, OriginalLanguageRecord):
    # Numerical and special characters which do not form part of a word, meaning they cannot be part of a python command word
    NumericalCharacters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    SpecialCharacters = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/', ' ']
    # Python indicators for Strings and DocStrings
    SpecialChecks = {"docstring" : ["'''", '"""'],
                     "string" : ["'", '"']}

    # String and DocString track if the current character is within a DocString or a String as these do not need translating
    String = False
    DocString = False
    StringType = False
    DocStringType = False
    # IteratingDocString checks if the loop is currently iterating through the set of 3 quotes, representing a DocString
    IteratingDocString = False
    # Store the list of words that are found to be translated
    WordsToReplace = []
    
    # Iterate through each line within the existing file
    for CurrentLinePosition in range(len(FileData)):
        CurrentLine = FileData[CurrentLinePosition]
        CurrentLineLength = len(CurrentLine)
        # Save data about the current word
        CurrentWord = ""
        CurrentWordStart = False
        # Iterate through each character within the current line
        for CurrentCharacterPosition in range(CurrentLineLength):
            CurrentCharacter = CurrentLine[CurrentCharacterPosition]

            # If the program is not currrently iterating through a DocString indicator
            if IteratingDocString == False:

                # If a hashtag is found to be indicating a comment, then the current line is finished
                if CurrentCharacter == "#" and DocString == False and String == False:
                    break

                # If the program finds a quote character which indicates a String or DocString
                elif CurrentCharacter in SpecialChecks["string"]:

                    # If the program is not currently iterating through a string and the current character position is the start of a DocString indicator
                    # Checks if the second quote is at the end of the line because could be defining an empty string
                    if String == False and CurrentCharacter == CurrentLine[CurrentCharacterPosition + 1] and CurrentCharacterPosition + 2 != CurrentLineLength and CurrentCharacter == CurrentLine[CurrentCharacterPosition + 2]:
                        # The program must skip 2 iterations of characters as they are the remaining quotes to indicate the DocString
                        IteratingDocString = 2

                        # If the program is currently iterating through a DocString and the current character matches the quotes used to start the current DocString
                        if DocString == True and CurrentCharacter == DocStringType:
                            # Reset variables to show the DocString has ended
                            DocString = False
                            DocStringType = False
                        elif DocString == False:
                            # Set variables to show the DocString has started
                            DocString = True
                            DocStringType = CurrentCharacter

                    # Else if the program is not currenly iterating through a DocString
                    elif DocString == False:
                        if String == True and CurrentCharacter == StringType:
                            # Reset variables to show the String has ended
                            String = False
                            StringType = False
                        elif String == False:
                            # Set variables to show the String has started
                            String = True
                            StringType = CurrentCharacter

                # Else if the current character is alphabetical and the program is not currently iterating through a String or a DocString
                elif CurrentCharacter not in NumericalCharacters and CurrentCharacter not in SpecialCharacters and String == False and DocString == False:
                    # If the program is not currently iterating through a word
                    if CurrentWord == "":
                        # Save the line and character position of the start of the word
                        CurrentWordStart = [CurrentLinePosition, CurrentCharacterPosition]
                    # Add the current character to the current word string
                    CurrentWord += CurrentCharacter

                # If the program is not currently iterating through a String or a DocString and the currrent word is not empty and (the current character is the end of the line or the next character is not alphabetical)
                # Then a word has been found
                if String == False and DocString == False and CurrentWord != "" and (CurrentCharacterPosition == CurrentLineLength - 1 or (CurrentLine[CurrentCharacterPosition + 1] in NumericalCharacters or CurrentLine[CurrentCharacterPosition + 1] in SpecialCharacters)):
                    # If the found word is in the original language record
                    if CurrentWord in OriginalLanguageRecord:
                        # Store the word, the start position, the end position and the index of the word in the language record
                        WordsToReplace.append([CurrentWord, CurrentWordStart, [CurrentLinePosition, CurrentCharacterPosition], OriginalLanguageRecord.index(CurrentWord)])
                    # Reset the current word variables as the found word has been checked
                    CurrentWord = ""
                    CurrentWordStart = False

            # Else when the program is iterating through a DocString indicator
            else:
                # Subtract 1 from the docstring iterator value
                IteratingDocString -= 1
                # If the docstring iterator value is at the end of the docstring
                if IteratingDocString == 0:
                    # Change the iterator value to False to indicate the docstring has ended
                    IteratingDocString = False
                    
    return WordsToReplace


# Function to replace the required words in the script with their translations
def ReplaceWords(FileData, OriginalLanguageRecord, NewLanguageRecord, WordsToReplace):
    # Create a list to store the new lines of the file
    NewLines = []
    # Iterate through each of the lines in the existing file
    for CurrentLinePosition in range(len(FileData)):
        CurrentLine = FileData[CurrentLinePosition]
        NewLine = []
        CurrentWordsToReplace = []
        NumberOfCurrentWordsToReplace = False

        # Get all words for current line
        for WordToReplacePosition in range(len(WordsToReplace)):
            WordToReplace = WordsToReplace[WordToReplacePosition]
            # If the first character in the current word is in the current line
            if WordToReplace[1][0] == CurrentLinePosition:
                # Add the current word data to the list of current words to replace for the current line
                CurrentWordsToReplace.append(WordsToReplace[WordToReplacePosition])
        # Iterate through the current list of words to replace, remove each of them from the list of all words to replace
        for CurrentWordToReplace in CurrentWordsToReplace:
            WordsToReplace.remove(CurrentWordToReplace)
        # Save the number of words to replace in the current line
        NumberOfCurrentWordsToReplace = len(CurrentWordsToReplace)

        # If there are no words to translate in the current line
        if NumberOfCurrentWordsToReplace == False:
            # Append the unedited line to the list of new lines
            NewLines.append(CurrentLine)
        # Else, calculate the translations
        else:
            
            # If only 1 word, it is treated as a special case
            if len(CurrentWordsToReplace) == 1:
                # Get the current word which needs to be translated from the line
                CurrentWord = str(CurrentLine[CurrentWordsToReplace[0][1][1]:CurrentWordsToReplace[0][2][1] + 1])
                # Get the translation of the word
                NewWord = NewLanguageRecord[OriginalLanguageRecord.index(CurrentWord)]
                # Create the new line with the newly translated word
                NewLine.extend([str(CurrentLine[:CurrentWordsToReplace[0][1][1]]), NewWord, str(CurrentLine[CurrentWordsToReplace[0][2][1] + 1:])])

            else:
                # If the first word to replace is not at the start, then the text before that word needs to be added to the list first
                if CurrentWordsToReplace[0][1][1] != 0:
                    NewLine.append(str(CurrentLine[:CurrentWordsToReplace[0][1][1]]))

                # New sections of each line are put together with a combination of the word to replace and the text following it up to the next word to replace
                for CurrentWordToReplacePosition in range(NumberOfCurrentWordsToReplace):
                    # Get the current word which needs to be translated from the line
                    CurrentWord = str(CurrentLine[CurrentWordsToReplace[CurrentWordToReplacePosition][1][1]:CurrentWordsToReplace[CurrentWordToReplacePosition][2][1] + 1])
                    # Get the translation of the word
                    NewWord = NewLanguageRecord[OriginalLanguageRecord.index(CurrentWord)]
                    # If the current word to replace is the last word to replace, the end of the text to add after it should be the end of the line rather than to the start of the next word to replace
                    if CurrentWordToReplacePosition == NumberOfCurrentWordsToReplace - 1:
                        # Get the text which follows after the word, this text should go to the end of the current line
                        FollowingText = str(CurrentLine[CurrentWordsToReplace[CurrentWordToReplacePosition][2][1] + 1:])
                    else:
                        # Get the text which follows after the word, this text should go up to the start of the next word which requires translation
                        FollowingText = str(CurrentLine[CurrentWordsToReplace[CurrentWordToReplacePosition][2][1] + 1:CurrentWordsToReplace[CurrentWordToReplacePosition + 1][1][1]])
                        
                    # Add the new word and its following text to the new line
                    NewLine.extend([NewWord, FollowingText])
                
            # Append the new line to the list of new lines and join the strings within the line together
            NewLines.append("".join(NewLine))     
            
    # Join the newly created lines together with a new line character
    NewFileData = "\n".join(NewLines)
    
    return NewFileData


# Function to translate the given script with the original language to the new language
def TranslateScript(cr, db, FileData, OriginalLanguageID, NewLanguageID):
    # Retrieve the required language records
    OriginalLanguageRecord = SelectLanguageRecord(cr, db, OriginalLanguageID)
    NewLanguageRecord = SelectLanguageRecord(cr, db, NewLanguageID)
    # Get the list of words to translate in the script
    WordsToReplace = GetWordsToReplace(FileData, OriginalLanguageRecord)
    # Translate the found words in the script
    NewFileData = ReplaceWords(FileData, OriginalLanguageRecord, NewLanguageRecord, WordsToReplace)
    # Output a message confirming translation success
    Spacing(1)
    print("Script translated successfully.")
    Spacing(1)
    return NewFileData, NewLanguageID


# Function to initialise the database if required
def InitialiseDatabase(cr, db):
    # Get the list of tables in the current database
    cr.execute("""SELECT name FROM sqlite_master WHERE type = 'table'""")
    Tables = ConvertTupleList(cr.fetchall())
    # If the table of translatinos is not in the database
    if "CommandTranslations" not in Tables:
        # Output a message confirming that a table has not been found and will be created
        print("Translation data not found. Initialising database.")
        Spacing(1)
        # Create the table
        CreateTranslationsTable(cr, db)
        # Create a list of the required language records
        LanguageRecords = [["Python", "False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
                            "abs", "all", "any", "bin", "bool", "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip"],
                           ["English", "False",  "None",  "True",  "and",  "as",  "assert",  "asynchronous",  "await",  "break",  "class",  "continue",  "define",  "delete",  "elseif",  "else",  "except",  "finally",  "for",  "from",  "global",  "if",  "import",  "in",  "is",  "nonlocal",  "not",  "or",  "pass",  "raise",  "return",  "try",  "while",  "with",  "yield", 
                            "absolute",  "all",  "any",  "binary",  "boolean",  "bytearray",  "bytes",  "callable",  "character",  "classmethod",  "compile",  "complex",  "deleteattribute",  "dictionary",  "directory",  "divisionmodulo",  "enumerate",  "evaluate",  "execute",  "filter",  "float",  "format",  "frozenset",  "getattribute",  "globals",  "hasattribute",  "hash",  "help",  "hexadecimal",  "identity",  "input",  "integer",  "isinstance",  "issubordinateclass",  "iterator",  "length",  "list",  "locals",  "map",  "maximum",  "memoryview",  "minimum",  "next",  "object",  "octal",  "open",  "unicode",  "power",  "print",  "property",  "range",  "readable",  "reversed",  "round",  "set",  "setattribute",  "slice",  "sorted",  "staticmethod",  "string",  "sum",  "super",  "tuple",  "type",  "variables",  "zip"],
                           ["German", "Falsch", "Keiner", "Stimmt", "und", "wie", "behaupten", "asynchron", "erwarten", "unterbrechung", "klasse", "fortsetzen", "definieren", "löschen", "anderswenn", "anders", "außer", "endlich", "zum", "aus", "global", "wenn", "importieren", "in", "ist", "nichtlokal", "nicht", "oder", "passieren", "heben", "rückkehr", "versuchen", "während", "mit", "ertrag",
                            "absolut", "alle", "irgendein", "binär", "boolesch", "bytereihe", "bytes", "abrufbar", "charakter", "klassemethode", "kompilieren", "komplex", "löschenattribut", "wörterbuch", "verzeichnis", "aufteilungmodulo", "aufzählen", "auswerten", "ausführen", "filter", "schweben", "format", "gefroreneinstellen", "erhaltenattribut", "globals", "hatattribut", "hasch", "hilfe", "hexadezimal", "identität", "eingang", "ganzezahl", "istbeispiel", "istuntergeordnetklasse", "iterator", "länge", "aufführen", "einheimische", "karte", "maximal", "erinnerungaussicht", "minimum", "nächste", "objekt", "oktal", "offen", "unicode", "energie", "drucken", "eigentum", "angebot", "lesbar", "umgedreht", "runden", "einstellen", "einstellenattribut", "scheibe", "sortiert", "statischmethode", "schnur", "summe", "super", "tupel", "typ", "variablen", "postleitzahl"]]
        # For each language record, insert the language into the database
        for Language in LanguageRecords:
            InsertLanguageRecord(cr, db, Language)


def Main():
    # Connect to the database file
    with sqlite3.connect("PythonTranslations.db") as db:
        cr = db.cursor()
    InitialiseDatabase(cr,db)
    ExistingFileData = ReadFile(GetExistingFilename())
    TranslatedScript, NewLanguageID = TranslateScript(cr, db, ExistingFileData, GetLanguageID(cr,db,"current"), GetLanguageID(cr,db,"new"))
    SaveFile(GetNewFilename(), TranslatedScript, NewLanguageID)



if __name__ == "__main__":
    Main()
