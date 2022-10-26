import os,webbrowser,tkinter,random


# Function to get the file path of the predefined directory, a folder called "Happy-Files" on the user's desktop
# This is the intended use of the program
def GetPath(FileName):
    return os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop", "Happy-Files", FileName)


# Function to get the file path of the programs own directory with the additional directory of the programs files and the given filename
# This is used for testing purposes
def GetOwnPath(FileName):
    return os.path.join(os.path.dirname(__file__), "Happy-Files", FileName)


# Function to open a file from a given file path
# This will use the default program for the file
def OpenFile(FilePath):
    os.startfile(FilePath)


# Function to open a link with the default browser
def OpenLink(URL):    
    webbrowser.open(URL, new = 1, autoraise = True)


# Function to get a list of the links from a given text file
def GetTextFileLines(FileName,GetFilePathFunction):
    # Get the file path of the text file using the given function
    FilePath = GetFilePathFunction(FileName)
    # Open the text file with the given path
    TextFile = open(FilePath)
    # For each line within the text file, append it to a list and remove any trailing characters
    LinesList = []
    for Line in TextFile:
        LinesList.append(Line.rstrip())
    # Close the text file
    TextFile.close()
    return LinesList


# Function to get a list of files in the predefined directory
def GetFileList(GetFilePathFunction):
    # FileList stores a list of the found files
    FileList = []
    # Get the required file path using the given function
    FilePath = GetFilePathFunction("Media")
    # For each file within the given directory
    for File in os.listdir(FilePath):
        # If a file is found with the given name and path
        if os.path.isfile(os.path.join(FilePath, File)):
            # Append the file path to the file list
            FileList.append(os.path.join(FilePath, File))
    return FileList


# Function to format text for a tkinter GUI window
def FormatText(Text,LineLength):
    # If the length of the given text is longer than the predefined length of each line within the GUI
    if len(Text) > LineLength:
        
        # Convert the text string into a list of characters
        Text = [Character for Character in Text]
        # LastSpace stores the index of the space character which was last found in the list of characters during iteration
        LastSpace = 0
        # CharactersInLine stores the number of characters in the current line of text, lines are split using a new line character
        CharactersInLine = 0

        # Iterate through each character within the list of characters
        for Position in range(len(Text)):

            # If the current character is a space, then assign its index to the LastSpace variable
            if Text[Position] == " ":
                LastSpace = Position
                
            # If the number of characters within the current line equals the given length of a line
            if CharactersInLine == LineLength:
                # Change the last space within the character list to a new line character
                Text[LastSpace] = "\n"
                # Update the number number of characters in the current line, this will be the current index within the character list - the index of the last space
                CharactersInLine = Position - LastSpace

            # Else runs when a new line is not required
            else:
                # Increment the number of characters in the current line by 1
                CharactersInLine += 1


        # Join the list of characters in the character string
        Text = "".join(Text)
    return Text


# Function to open a tkinter GUI window with text
def DisplayText(Text,Title):

    # If the given text is for an error
    if "ERROR" in Title.upper():
        # Set the font to be smaller and increase the line length to ensure the full message is displayed
        Font = "Helvetica 11"
        LineLength = 55
        # Format the text for the GUI
        Text = Text[0] + FormatText(Text[1], LineLength)

    # For all other given text
    else:
        # Set the font to be larger and decrease the line length to make it more readable
        Font = "Helvetica 16"
        LineLength = 32
        # Format the text for the GUI
        Text = FormatText(Text,LineLength)

    # Initialise the GUI window
    Root = tkinter.Tk()
    # Give the window a title
    Root.title(Title)
    # Set the size of the window
    Root.geometry("400x300")
    # Create the text box within the window
    TextBox = tkinter.Label(Root, text = Text, font = Font, justify = "center")
    TextBox.pack()
    # Set the positioning of the text box within the window
    TextBox.place(x = 200, y = 150, anchor = "center")
    Root.mainloop()
    

# Function to get all lists
def PerformRandomAction():
    GetFilePathFunction = GetOwnPath
    FilesList = GetFileList(GetFilePathFunction)
    LinksList = GetTextFileLines("Links.txt", GetFilePathFunction)
    QuotesList = GetTextFileLines("Quotes.txt", GetFilePathFunction)

    # Calculate the total numbe of all items within the Files, Links and Quotes
    TotalItems = len(FilesList) + len(LinksList) + len(QuotesList)
    # Randomly select an index within the range of all items
    ActionID = random.randint(0, TotalItems - 1)

##    print("Files: " + str(len(FilesList)))
##    print("Links: " + str(len(LinksList)))
##    print("Quotes: " + str(len(QuotesList)))
##    print("ActionID: " + str(ActionID))

    # If the chosen index is above the file indexes
    if ActionID > len(FilesList) - 1:
        # If the chosen index is above the files indexes + the links indexes
        if ActionID > len(FilesList) + len(LinksList) - 1:
            # The chosen index represents a quote, therefore convert the index back to the range within the list of quotes
            # Then run functions to display the quote within a window
            DisplayText(QuotesList[ActionID - len(FilesList) - len(LinksList) - 1], "Le Quotes")
        else:
            # The chosen index represents a link, therefore convert the index back to the range within the list of links
            # Then run functions to open the link within the default browser
            OpenLink(LinksList[ActionID - len(FilesList) - 1])
    else:
        # The chosen index represents a file, therefore open the file
        OpenFile(FilesList[ActionID])


# Function to perform a test which will return True if the required Happy-Files directory is present with the directory of the program
def SetupTest():
    return os.path.isdir(GetOwnPath(""))


# Function to perform a first time setup, creating the required files and directories for the program
def FirstTimeSetup():
    # Create the required directories
    os.mkdir(os.path.join(os.path.dirname(__file__), "Happy-Files"))
    os.mkdir(os.path.join(os.path.dirname(__file__), "Happy-Files", "Media"))
    # Create the required text files
    for Name in ["Links", "Quotes"]:
        CurrentFile = open(GetOwnPath(Name + ".txt"), "w")
        CurrentFile.close()
    # Display a window to inform the user a first time setup was performed successfully
    DisplayText("Performed first time setup successfully!", "Setup")
    


def Main():
    # Try to run the program
    try:
        # If the required files and directories are already setup, then run the program as normal
        if SetupTest():
            PerformRandomAction()
        # Else, perform a first time setup to initialise the required files and directories
        else:
            FirstTimeSetup()
    # If an error occurs, display the error message within a new window
    except Exception as ErrorMessage:
        DisplayText(["Something went wrong!\n\nError Message:\n\n", str(ErrorMessage)],"Error")


if __name__ == "__main__":
    Main()
