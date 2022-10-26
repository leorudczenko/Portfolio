   ---   Python Code Translator README   ---  
This is a program designed to translate the keywords and built-in functions of a Python script to a human language.
Keywords and built-in Python functions are referred to as commands for the purposes of this README file.

When translating a script, all text within strings, docstrings and comments is ignored.
Translations are stored within an SQL database. Therefore, a salt is used for all commands to prevent issues.

----------------------------------------------------------------------------------------------------------------------------

There are some exceptions for specific keyword translations:

	True, False, None
		These must start with a capitalized letter in ALL languages
	
	ascii, lambda
		These are not translated as they are a noun or technical term.

	ord
		When translated to a human language, the word will be "unicode".


----------------------------------------------------------------------------------------------------------------------------

Currently, the program supports the following:
- Python standard formatting
- English
- German

Scripts which are exported in Python standard formatting will be saved as a .py file, whilst all other langugaes will be saved as a .txt file.

----------------------------------------------------------------------------------------------------------------------------

Included in the directory is a test file, "Test File Python.py". This file features some basic Python formatting to demonstrate the functionality of the translator.
