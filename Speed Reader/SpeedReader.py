import tkinter as tk

# Define the program as an object
class SpeedReader:
    # Define the initialisation processes of the object
    def __init__(self):
        # Define the user interface window
        Root = tk.Tk()
        Root.title("Speed Reader")
        Root.geometry("300x150")

        # Define text label of the user interface window
        self.Title = tk.Label(Root, text = "Text:", font = "Helvetica 16", justify = "center")
        self.Title.pack()
        self.Title.place(x = 150, y = 20, anchor = "center")

        # Define text input box of the user interface window
        self.Text = tk.Entry(Root)
        self.Text.pack()
        self.Text.place(x = 150, y = 45, anchor = "center")

        # Define the words per minute label of the user interface window
        self.Subtitle = tk.Label(Root, text = "Words per minute:", font = "Helvetica 16", justify = "center")
        self.Subtitle.pack()
        self.Subtitle.place(x = 150, y = 65, anchor = "center")

        # Define the words per minute input box of the user interface window
        self.WPM = tk.Entry(Root)
        self.WPM.pack()
        self.WPM.place(x = 150, y = 90, anchor = "center")
        self.WPM.insert(tk.END, 300)

        # Define the button of the user interface window
        self.ActionButton = tk.Button(Root, text = "Start", command = lambda: self.SwitchMode(Root))
        self.ActionButton.pack()
        self.ActionButton.place(x = 150, y = 120, anchor = "center")

        # Define the text and durations which will be used for the countdown
        self.Countdown = ["Starting in: 3", "Starting in: 2", "Starting in: 1", ""]
        self.CountdownDuration = [500, 500, 500, 200]

        # Duration defines the number of miliseconds between each word being displayed
        self.Duration = 0
        # Data defines the list of words to display
        self.Data = []

        Root.mainloop()


    # Function to switch the mode of the program from the menu to the countdown
    def SwitchMode(self,Root):
        # Move the menu labels and entry boxes out of view of the window
        self.Text.place(x = 1000, y = 1000)
        self.Subtitle.place(x = 1000, y = 1000)
        self.WPM.place(x = 1000, y = 1000)

        # Move the text display to the center of the window and change the font
        self.Title.place(x = 150, y = 55)
        self.Title.config(font = "Helvetica 30")
        # Update the button to end the program when clicked
        self.ActionButton.config(text = "Done", command = Root.destroy)

        # Format the text string into a list of words
        self.Data = str(self.Text.get()).split()
        # Convert the inputted number of words per minute to the number of miliseconds between each word
        self.Duration = int((60 / float(self.WPM.get())) * 1000)

        # Start the countdown before the speed reader begins
        self.RunCountdown()

    # Function to run the countdown
    def RunCountdown(self):
        # This if statement serves as a base case of the recursive call when true
        # If there are no more elements left to the countdown, then run the speed reader
        if len(self.Countdown) == 0:
            self.RunReader()
        # Otherwise, run the recursive call
        else:
            # Update the text display to the display the current countdown element
            self.Title.config(text = self.Countdown[0])
            # Get the amount of time between the current countdown element and the next
            Time = self.CountdownDuration[0]
            # Remove the current countdown element from the list of countdown elements
            self.Countdown = self.Countdown[1:]
            # Remove the current duration from the list of duration elements
            self.CountdownDuration = self.CountdownDuration[1:]
            # Schedule a recursive call to occur after the current duration has passed
            self.Title.after(Time, self.RunCountdown)

    # Function to run the speed reader
    def RunReader(self):
        # This if statement serves as a base case of the recursive call when true
        # If there are no more words left in the list of words from the text, then return nothing to exit the recursive loop
        if len(self.Data) == 0: # Break the recursive loop if the array is empty
            return
        # Otherwise, run the recursive call
        else:
            # Get the current word to display from the list of words
            String = self.Data[0]
            # Update the text display to show the current word
            self.Title.config(text = self.Data[0])
            # Update the list of words to remove the first value
            self.Data = self.Data[1:]

            # If the last character in the current word string is in the list, it is displayed for 3x as long because it is the end of a sentence
            if String[len(String) - 1] in ["?", "!", "."]:
                # Schedule a recursive call to occur after the specified duration has passed
                self.Title.after(self.Duration * 3, self.RunReader)
            # If the last character in the current word string is a comma, it is displayed 2x as long because it is a break in the sentence
            elif String[len(String) - 1] == ",":
                # Schedule a recursive call to occur after the specified duration has passed
                self.Title.after(int(self.Duration * 1.5), self.RunReader)
            # Otherwise, schedule a recursive call to occur after the specified duration has passed
            else:
                self.Title.after(self.Duration, self.RunReader)
            

    
if __name__ == "__main__":
    SpeedReader()
