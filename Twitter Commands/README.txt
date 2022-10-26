   ---   Twitter Commands README   ---
This is a program that allows a user to tweet commands which can then be executed on their windows computer.
The program will check the given twitter account every 1.5 seconds for a new tweet, with a command being indicated by a ! at the start of the tweet.
When a new command is found on the given twitter account, the program will retrieve the tweet data before automatically deleting it.
All executed commands and found errors are saved to the log file with relevant information.

The program comes with an interface which will display the latest tweet from the account, as well as the last run command during the active session.
The interface allows a user to pause the program, which will temporarily stop the program from checking the twitter account and therefore prevent command execution.

Functions from the HiddenFunctions file are not included for security reasons, as they contain private API keys and file paths.

----------------------------------------------------------------------------------------------------------------------------

Commands which can be run are presented below. Commands parameters are put in place of symbols <> whilst detailed command information is shown in brackets () below the command:

	open <program name>
		(If the filepath is known, it will run the executable file, otherwise it will use the windows search function to find the program.)

	link <link to open>
		(A space must be inserted before the top-level domain [.com, .org, etc.] to prevent twitter from shortenting the link.)

	youtube <search/play> <query>
		(When using YouTube query functionality, results can be displayed when using the "search" parameter or the first video from the results can be played using the "play" parameter.)

	twitch <twitch channel name>
		(The channel name must be included with no spaces.)

	press <key>
		(Any keyboard key can be used as a parameter here.)

	refresh
		(Refresh the current window.)

	close
		(Close the current program.)

	mute
		(Mute windows sound.)

	unmute
		(Unmute windows sound.)

	volume <up/down>
		(The volume can be raised up or down by specifying the relevant parameter. Volume levels are changed in increments of 20.)
	skip
		(Skip media which is currently playing.)

	pause
		(Pause the current media.)

	play
		(Play the current media.)

	pausebot
		(Pause the program's process. This will stop the program from checking the given twitter account. Reactivation must be done from the windows computer.)

	end
		(End the program on the windows computer.)

	type <text to type>
		(Given text will be typed on the windows computer.)

	print <text to print>
		(Given text will be printed to the terminal on the windows computer.)

----------------------------------------------------------------------------------------------------------------------------

An example log file is included in the directory. All logs within the file are from personal usage.