import time

'''
This function checks if 5 is equal to or within the given variable
'''
def FunctionName(VariableName):
    # If 5 is the variable or it is in the variable, then True, otherwise False
    if VariableName == 5 or 5 in VariableName:
        NewVariable = True
    else:
        NewVariable = False
    return NewVariable

def Main():
    VariableName = ["This is a string", 5, "this is a str"]
    ResultVariable = FunctionName(VariableName)
    print(ResultVariable)

Main()
