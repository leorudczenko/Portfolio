import twitter,time,pyautogui,os,json,ast,datetime,tkinter,webbrowser
# Personal credential methods and filepaths not shown for security reasons
from HiddenFunctions import GetCredentials,GetFilePaths

# Defining the tkinter application as a class
class TkinterApplication():
    # Function is run to initialise an instance of the class
    def __init__(self):
        self.Root = tkinter.Tk()
        # Setting the basic attributes of the GUI window
        self.Root.title("Twitter Command Bot")
        self.Root.geometry("580x120") #500x250

        # Defining the frames to create the widgets of the interface
        self.DisplayFrame = tkinter.Frame(self.Root)
        self.DisplayFrame.columnconfigure(0, weight = 1)
        self.StatusFrame = tkinter.Frame(self.Root)
        self.StatusFrame.columnconfigure(0, weight = 1)

        # Setting initial bot statuses
        self.Status = "start"
        self.AllJobs = []
        self.CurrentRecursiveJob =  None

        # Defining the minimum size of each column within the display grid
        DisplayColumnSizes = [110, 120, 90, 260]
        for Position in range(len(DisplayColumnSizes)):
            self.DisplayFrame.grid_columnconfigure(Position, minsize = DisplayColumnSizes[Position])
        # Defining the minimum size of each row within the display grid
        for Position in range(3):
            self.DisplayFrame.grid_rowconfigure(Position, minsize = 25)
        
        # Row names
        self.CommandRowLabel = tkinter.Label(self.DisplayFrame, text = "Last Command:", font = "Helvetica 9")
        self.CommandRowLabel.grid(row = 1, column = 0)
        self.TweetRowLabel = tkinter.Label(self.DisplayFrame, text = "Last Tweet:", font = "Helvetica 9")
        self.TweetRowLabel.grid(row = 2, column = 0)

        # Column names
        self.SourceColumnLabel = tkinter.Label(self.DisplayFrame, text = "Source", font = "Helvetica 9")
        self.SourceColumnLabel.grid(row = 0, column = 1)
        self.TimeColumnLabel = tkinter.Label(self.DisplayFrame, text = "Check Time", font = "Helvetica 9")
        self.TimeColumnLabel.grid(row = 0, column = 2)
        self.TextColumnLabel = tkinter.Label(self.DisplayFrame, text = "Text", font = "Helvetica 9")
        self.TextColumnLabel.grid(row = 0, column = 3)
        
        # Last command cells
        self.LastCommandSource = tkinter.Label(self.DisplayFrame, text = "N/A")
        self.LastCommandSource.grid(row = 1, column = 1)
        self.LastCommandTime = tkinter.Label(self.DisplayFrame, text = "N/A")
        self.LastCommandTime.grid(row = 1, column = 2)
        self.LastCommandText = tkinter.Label(self.DisplayFrame, text = "N/A")
        self.LastCommandText.grid(row = 1, column = 3)
        
        # Last tweet cells
        self.LastTweetSource = tkinter.Label(self.DisplayFrame, text = "N/A")
        self.LastTweetSource.grid(row = 2, column = 1)
        self.LastTweetTime = tkinter.Label(self.DisplayFrame, text = "N/A")
        self.LastTweetTime.grid(row = 2, column = 2)
        self.LastTweetText = tkinter.Label(self.DisplayFrame, text = "N/A")
        self.LastTweetText.grid(row = 2, column = 3)
        
        # Status cells
        self.StatusLabel = tkinter.Label(self.StatusFrame, text = "Status:", font = "Helvetica 10")
        self.StatusLabel.grid(row = 3, column = 0)
        self.StatusDisplay = tkinter.Label(self.StatusFrame, text = "Ready", font = "Helvetica 10 bold")
        self.StatusDisplay.grid(row = 3, column = 1, sticky = "w")

        # Action button
        self.ActionButton = tkinter.Button(self.StatusFrame, text = "Start", font = "Helvetica 10 bold", command = self.ChangeStatus)
        self.ActionButton.grid(row = 3, column = 2)

        # Separators
        self.RowSeparator = tkinter.ttk.Separator(self.DisplayFrame, orient = "vertical").grid(row = 0, column = 1, rowspan = 3, sticky = "wns")
        self.ColumnSeparator = tkinter.ttk.Separator(self.DisplayFrame, orient = "horizontal").grid(row = 0, column = 0, columnspan = 4, sticky = "sew")
        self.StatusSeparator = tkinter.ttk.Separator(self.DisplayFrame, orient = "horizontal").grid(row = 2, column = 0, columnspan = 4, sticky = "sew")
        
        # Defining the minimum size of each column within the status grid
        StatusColumnSizes = [60, 440, 60]
        for Position in range(len(StatusColumnSizes)):
            self.StatusFrame.grid_columnconfigure(Position, minsize = StatusColumnSizes[Position])
        # Defining the minimum size of the row within the status grid
        self.StatusFrame.grid_rowconfigure(0, minsize = 10)

        # Defining the positions of each widget within the main window grid
        self.DisplayFrame.grid(row = 0, column = 0)
        self.StatusFrame.grid(row = 1, column = 0)

        # Defining a dictionary to call executeable commands via their functions
        self.MainCommands = {"open" : self.Command_Open,
                             "link" : self.Command_Link,
                             "youtube" : self.Command_Youtube,
                             "twitch" : self.Command_Twitch,
                             "press" : self.Command_Press,
                             "refresh" : self.Command_Refresh,
                             "close" : self.Command_Close,
                             "mute" : self.Command_ToggleMute,
                             "unmute" : self.Command_ToggleMute,
                             "volume" : self.Command_Volume,
                             "skip" : self.Command_Skip,
                             "pause" : self.Command_ToggleMediaPause,
                             "play" : self.Command_ToggleMediaPause,
                             "pausebot" : self.Command_BotPause,
                             "end" : self.Command_End,
                             "type" : self.TypeText,
                             "print" : print}
        
        self.Root.mainloop()


    # Function to update the last command displayed in the interface
    def UpdateLastCommand(self, CommandData):
        self.LastCommandSource.config(text = CommandData[2])
        self.LastCommandTime.config(text = CommandData[1])
        self.LastCommandText.config(text = CommandData[0])
        

    # Function to update the last tweet displayed in the interface
    def UpdateLastTweet(self, TweetData):
        self.LastTweetSource.config(text = TweetData[2])
        self.LastTweetTime.config(text = TweetData[1])
        self.LastTweetText.config(text = TweetData[0])


    # Function to change the status of the bot
    def ChangeStatus(self):
        '''When the start button is pressed'''
        # If the current status is the starting status of the bot
        if self.Status == "start":
            # Change the button text to pause
            self.ActionButton.config(text = "Pause")
            # Change the status display text to running
            self.StatusDisplay.config(text = "Running", fg = "green")
            # Change the bot status to running
            self.Status = "run"
            # Run the bot
            self.RunBot()

        '''When the pause button is pressed'''
        # Else if the current status of the bot is running
        elif self.Status == "run":
            # Change the button text to run
            self.ActionButton.config(text = "Run")
            # Change the status display text to paused
            self.StatusDisplay.config(text = "Paused", fg= "orange")
            # Change the bot status to paused
            self.Status = "pause"
            # Clear all current jobs
            self.ClearAllJobs()

        '''When the run button is pressed'''
        # Else if the current status of the bot is paused
        elif self.Status == "pause":
            # Change the button text to pause 
            self.ActionButton.config(text = "Pause")
            # Change the status display text to running
            self.StatusDisplay.config(text = "Running", fg = "green")
            # Change the bot status to running
            self.Status = "run"
            # Run the bot
            self.RunBot()


    # Function to clear all the current jobs which are queued or executing
    def ClearAllJobs(self):
        # For each job in the list of jobs
        for Job in self.AllJobs:
            # Cancel the job
            self.Root.after_cancel(Job)
        # Set the list of jobs to an empty list
        self.AllJobs = []
        # Set the current recursive job to none to indicate no current jobs are executing or queued
        self.CurrentRecursiveJob = None


    # Function to remove a given job
    def RemoveJob(self, Job):
        # Cancel the job
        self.Root.after_cancel(Job)
        # Remove the job from the list of jobs
        self.AllJobs.remove(Job)

    # Function to add a current recursive job
    # Allows the current recursion loop to be tracked and halted if necessary
    def AddRecursiveJob(self, Job):
        # Add the recursive job to the list of jobs
        self.AllJobs.append(Job)
        # Set the current recursive job to the given job
        self.CurrentRecursiveJob = Job


    # Function to run the bot in a recursive loop
    def RunBot(self):
        # All code within the function is run through a try except branch to catch errors
        try:
            # If the bot status is set to run
            if self.Status == "run":
                # Get the latest tweet from the twitter account and check if the tweet is a command
                TweetData = self.GetTweet()
                CheckResult = self.CheckTweet(TweetData)
                # If the latest tweet is a command
                if CheckResult == True:
                    # Update the latest command currently displayed within the interface
                    self.UpdateLastCommand([self.FormatTweet(TweetData[0]), self.GetCurrentTime(), self.FormatTweetSource(TweetData[2])])
                    # Delete the tweet from the twitter account
                    self.DeleteTweet(TweetData[1])
                    # Format and execute the command
                    Command = self.FormatCommand(TweetData[0][1:])
                    CommandStatus = self.ExecuteCommand(Command)
                    # If the command exists and can be executed then true is returned, otherwise false
                    # Save the command and status to the log file
                    if CommandStatus == True:
                        self.LogData("Command Executed <{0}> [{1}]:: '{2}'\n".format(self.FormatTweetSource(TweetData[2]), self.GetCurrentDateTime(), TweetData[0]))
                    elif CommandStatus == False:
                        self.LogData("Command Not Found <{0}> [{1}]:: '{2}'\n".format(self.FormatTweetSource(TweetData[2]), self.GetCurrentDateTime(), TweetData[0]))
                # If the latest tweet is not a command
                else:
                    # Update the latest tweet currently displayed within the interface
                    self.UpdateLastTweet([self.FormatTweet(TweetData[0]), self.GetCurrentTime(), self.FormatTweetSource(TweetData[2])])

                # If a recursive job call has been called
                if self.CurrentRecursiveJob != None:
                    # Remove the recursive job call to allow room for a new one
                    self.RemoveJob(self.CurrentRecursiveJob)
                # Add a new recursive job call
                self.AddRecursiveJob(self.Root.after(1300, self.RunBot))

        # Catch an error message
        except Exception as ErrorMessage:
            # Convert the error message into a string
            StringErrorMessage = str(ErrorMessage)
            # If the string is longer than 54 characters long then remove the end section so that it will fit in the interface
            if len(StringErrorMessage) > 54:
                DisplayErrorMessage = "{0}...".format(StringErrorMessage[:51])
            # Else, assign the error message string to the same variable as above
            else:
                DisplayErrorMessage = StringErrorMessage
            # Set the status of the bot to pause
            self.Status = "pause"
            # Set the action button to display the restart option
            self.ActionButton.config(text = "Restart")
            # Clear all currently scheduled jobs
            self.ClearAllJobs()
            # Display the error message within the interface and save the error message to the log file
            self.StatusDisplay.config(text = "Error: {0}".format(DisplayErrorMessage), fg= "red")
            self.LogData("Error Encountered [{0}]:: '{1}'\n".format(self.GetCurrentDateTime(),  StringErrorMessage))


    '''Below are functions to execute the bot itself, not the interface'''
    
    # Function to return the current time
    def GetCurrentTime(self):
        return str(datetime.datetime.now())[-15:-7]


    # Function to get the current date and time
    def GetCurrentDateTime(self):
        return str(datetime.datetime.now())


    # Function to get the latest Tweet from the account using the Twitter API
    def GetTweet(self):
        # Establish API token credentials
        ConsumerKey, ConsumerSecretKey, AccessToken, AccessTokenSecret, ScreenName = GetCredentials()
        TwitterAPI = twitter.Api(consumer_key = ConsumerKey, consumer_secret = ConsumerSecretKey,
                        access_token_key = AccessToken, access_token_secret = AccessTokenSecret)
        # Fetch the timeline from the account, get the text and ID of the most recent Tweet
        Timeline = TwitterAPI.GetUserTimeline(screen_name = ScreenName)
        # Save just the text, ID and source of the newest tweet in the timeline
        TweetData = [Timeline[0].text, Timeline[0].id_str, Timeline[0].source]
        return TweetData


    # Function to check if the most recent Tweet is intended to be a command, indicated by using ! as the first character
    def CheckTweet(self, TweetData):
        if TweetData[0][0] == "!":
            return True
        else:
            return False


    # Function to delete a Tweet on the account using the given Tweet ID
    def DeleteTweet(self, TweetID):
        # Establish API token credentials
        ConsumerKey, ConsumerSecretKey, AccessToken, AccessTokenSecret, ScreenName = GetCredentials()
        TwitterAPI = twitter.Api(consumer_key = ConsumerKey, consumer_secret = ConsumerSecretKey,
                        access_token_key = AccessToken, access_token_secret = AccessTokenSecret)
        # Delete the given tweet
        TwitterAPI.DestroyStatus(TweetID)


    # Function to format the tweet source to only include the basic string aspect
    def FormatTweetSource(self, TweetSource):
        # When the first < symbol is found, set below to True as the second < symbol in the string  is needed
        FirstLessThanCharFound = False
        # Save the index of the first instance of the > symbol and the index of the second instance of the < symbol
        SourceEnds = [False,False]
        # Loop through each character in the source string
        for Position in range(len(TweetSource)):
            Character = TweetSource[Position]
            # If both symbol ends have been found then end the loop
            if False not in SourceEnds:
                break
            # If the first < symbol has been found then assign True to indicate this
            elif FirstLessThanCharFound == False:
                FirstLessThanCharFound = True
            # If a < character is found, it is the second occurence and the second source end is not yet found
            elif Character == "<" and FirstLessThanCharFound == True and SourceEnds[1] == False:
                # Save the current index to the second source end
                SourceEnds[1] = Position
            # If a > character is found and the first source end is not yet found
            elif Character == ">" and SourceEnds[0] == False:
                # Save the current index to the first source end
                SourceEnds[0] = Position
        return TweetSource[SourceEnds[0] + 1 : SourceEnds[1]]


    # Function to format the text from a tweet if it is intended to be a command
    def FormatCommand(self, TweetText):
        # Return the text converted to all lowercase as a list of words
        return TweetText.lower().split()


    # Function to format the text from a tweet if it is a genuine tweet
    def FormatTweet(self, TweetText):
        # If the tweet is longer than 40 characters, reduce it down so that it will fit in the interface display
        if len(TweetText) > 40:
            TweetText = "{0}...".format(TweetText[:37])
        # Return the text with replaced newline characters to prevent interface display issues
        return TweetText.replace("\n", " ")


    # Function to log given data witin a text file, including commands executed and errors encountered
    def LogData(self, Data):
        # If the log file does not current exist
        if os.path.isfile("TwitterBot_Log.txt") == False:
            # Create the new, empty log file and close it
            LogFile = open("TwitterBot_Log.txt", "w")
            LogFile.close()
        # Open the log file
        LogFile = open("TwitterBot_Log.txt", "a")
        # Save the log data
        LogFile.write(Data)
        # Close the file
        LogFile.close()


    # Function to press the keys which create a piece of given text
    def TypeText(self, Text):
        # For character position in the text
        for Position in range(len(Text)):
            # Press the corresponding key to the character in the current position
            pyautogui.press(Text[x])


    # Function to execute the given command
    def ExecuteCommand(self, Command):
        MainCommand = Command[0]
        # If the first command word, the main command, is in the list of main commands
        if MainCommand in self.MainCommands:
            # If there is more than 1 word in the command
            if len(Command) > 1:
                # If there is only one word after the main command
                if len(Command[1:]) == 1:
                    # Execute the required function, passing only the word after the main command
                    self.MainCommands[MainCommand](Command[1])
                # Else, execute the required funtion, passing a list of all words after the main command
                else:
                    self.MainCommands[MainCommand](Command[1:])
            # Else, execute the required functions with no parameters
            else:
                self.MainCommands[MainCommand]()

            # Return True if a command is found, return False if not
            return True
        else:
            return False

    
    '''Below are the commands for the bot'''
    
    # Function to execute the command "open"
    def Command_Open(self, Program):
        # Get the known file paths of executable files
        FilePaths = GetFilePaths()
        # If the file path of the given program is known
        if Program in FilePaths:
            # Run the executable
            os.startfile(FilePaths[Program])
        else:
            # Else, use the windows search bar to find the program
            pyautogui.press('win')
            # Sleep is used to allow the device to load content
            time.sleep(1)
            self.TypeText(Program)
            pyautogui.press('enter')


    # Function to execute the command "link"
    def Command_Link(self, URL):
        # Use the default device browser to open the link in a new window
        webbrowser.open("".join(URL), new = 1, autoraise = True)


    # Function to execute the command "youtube"
    def Command_Youtube(self, Command):
        # If the first parameter of the command is search
        if Command[0] == "search":
            # Open a link of the youtube search results, with the user query being inserted into a youtube query link
            self.Command_Link("https://www.youtube.com/results?search_query={0}".format("+".join(Command[1:])))
        # Else if the first parameter of the command is play
        elif Command[0] == "play":
            # Open a link of the youtube search results, with the user query being inserted into a youtube query link and with the additional string, '&sp=EgIQAQ%253D%253D', being added at the end
            # The additional string indicates the query should only return video results
            self.Command_Link("https://www.youtube.com/results?search_query={0}&sp=EgIQAQ%253D%253D".format("+".join(Command[1:])))
            # Sleep is used to allow the device to load content
            time.sleep(5)
            # Move the selector down to the first video
            pyautogui.press('tab')
            # Open the first video
            pyautogui.press('enter')


    # Function to execute the command "twitch"
    def Command_Twitch(self, TwitchChannel):
        # Open a link of the twitch channel with the user query being added at the end of the link
        self.Command_Link("https://twitch.tv/{0}".format(TwitchChannel))


    # Function to execute the command "press"
    def Command_Press(self, Command):
        # The number of presses is set to 1 by default
        Repeat = 1
        # If there are multiple parameters to the command
        if len(Command) > 1:
            # The number of repeats is the second parameter
            Repeat = int(Command[1])
        # Press the given key the required number of times
        for x in range(Repeat):
            pyautogui.press(Command[0])


    # Function to execute the command "refresh"
    def Command_Refresh(self):
        # Use keyboard keys to refresh the current window
        pyautogui.keyDown('ctrl')
        pyautogui.press('r')
        pyautogui.keyUp('ctrl')


    # Function to execute the command "close"
    def Command_Close(self):
        # Use keyboard keys to close the current window
        pyautogui.keyDown('alt')
        pyautogui.press('f4')
        pyautogui.keyUp('alt')


    # Function to execute the command "mute"
    def Command_ToggleMute(self):
        # Use keyboard keys to press the mute button
        pyautogui.press('volumemute')


    # Function to execute the command "volume"
    def Command_Volume(self, Type):
        # Press the given volume button 10 times
        # This prevents the user from having to input the command multiple times to quickly change the volume
        for Value in range(10):
            pyautogui.press('volume' + Type)
            # Sleep is used to allow the device to load content
            time.sleep(0.01)


    # Function to execute the command "skip"
    def Command_Skip(self):
        # Use keyboard keys to press the media skip hotkey
        pyautogui.keyDown('shift')
        pyautogui.press('n')
        pyautogui.keyUp('shift')


    # Function to execute the command "play" or "pause"
    def Command_ToggleMediaPause(self):
        # Use the keyboard keys to press the play/pause button
        pyautogui.press("playpause")


    # Function to execute the command "pausebot"
    def Command_BotPause(self):
        # Change the status of the bot
        # At this stage, the status would have to be running for this command to execute
        # Therefore, it will be changed to paused
        self.ChangeStatus()


    # Function to execute the command "end"
    def Command_End(self):
        # This function uses the after method to execute a second function, Function_End, 0.5s later
        # This allows the !end command to be saved to the log file before the program ends
        self.Root.after(500, self.Function_End)


    # Function to end the bot process
    def Function_End(self):
        # Close the interface window
        self.Root.destroy()
        # Exit the program
        raise SystemExit(0)

            

if __name__ == "__main__":
    TkinterApplication()
    

