# Year 10 Term 4 IT Assignment (CSV editing application)
# This is the main file, it handles parsing commands and is the entry point of the program.
# By Matt Young
import csv
import functions
import data
from inspect import getmembers, isfunction, getdoc

# multi line CSV string as defined in the task
csv_mutliline = """Expense,JAN,FEB,MAR
Wages,4000,4000,4000
Rent,1750,1750,1750
Telephone,459,553,659
Electricity,250,225,233
BankCharges,39,473,55
StateGovernmentTax,55,51,49
Advertising,2500,2390,2000
Postage,300,340,320
CarExpenses,670,650,598
LifeInsurance,300,300,300"""

def prompt():
    """Prints a REPL prompt and returns the user's input"""
    while True:
        user_input = input("\n({}) axel> ".format("no file opened" if data.opened_file is None else data.opened_file))
        if user_input.strip() != "":
            return user_input

def ask(question):
    """Gets the answer to a yes or no question"""
    while True:
        user_input = input(question + " (y/n) ").lower()
        if user_input.lower().startswith("y") or user_input.lower().startswith("n"):
            # code to handle the Australian vernacular
            if "yeah nah" in user_input.lower():
                return ask("Do you mean \"Yeah nah yeah sure\" or \"Yeah nahh nahhh\" mate?")
            else:
                return user_input.lower().startswith("y")
        else:
            print("Error: invalid input, try again.\n")

def parse_cmd(cmd):
    """Checks if a command is a builtin like help or quit and handles it, otherwise passes it to eval_cmd()"""
    # TODO make these functions in functions.py instead of here?
    # will fix misleading error message, e.g. "command exit not found" (since it goes to the final else and technically it isn't a function in functions.py)
    if cmd.strip() == "exit" or cmd.strip() == "quit":
        if data.opened_file is not None:
            if ask("Save unsaved changes to {}?".format(data.opened_file)):
                functions.save()
        print("Thank you for using Macrosoft Axel '88. Your license expires in 2 minutes.")
        exit()
    elif cmd.strip() == "help":
        do_help()
    else:
        eval_cmd(cmd)

def do_help():
    """Returns a help string consisting of "{function name}: {function docstring}"""
    # this complex list comprehension essentially grabs all functions in the module "functions" if they are not private (doesn't start with _) 
    # and assembles a string with the name and docstring attached
    function_names = [x[1].__name__ + ": " + x[1].__doc__ for x in getmembers(functions) if isfunction(x[1]) and not x[0].startswith("_")]
    # TODO pretty print the help (use ljust on the columns)
    print("List of functions in Macrosoft Axel:\n" + "\n".join(function_names))

def eval_cmd(cmd):
    """Dynamically finds and evaluates a function defined in functions.py using Python reflection and exec()"""
    function_names = [x[1].__name__ for x in getmembers(functions) if isfunction(x[1]) and not x[0].startswith("_")]
    target_function = cmd.split()[0].strip()

    for name in function_names:
        if name.lower() == target_function.lower():
            # get the args to the function (ignore the first token because it's the function's name)
            args = ["\"" + x + "\"" for x in cmd.split()[1::]]
            # assemble the python code to pass to exec()
            call = "functions.{}({})".format(name, ", ".join(args))
            
            try:
                # we use exec() to dynamically run the command. it's generally bad practice but in this case is the best solution.
                exec(call)
            except Exception as e:
                print("Error evaluating command \"{}\"\n{}: {}".format(cmd, e.__class__.__name__, str(e)))
            return
    print("Error: There is no function named \"{}\"".format(target_function))

if __name__ == "__main__":
    print("Welcome to the Macrosoft Axel REPL environment. Type 'help' for assistance or 'quit' to exit.")
    print("Copyright (c) 1988 Macrosoft Corp. Developed by Matt Young.")
    
    while True:
        # main loop
        cmd = prompt()
        parse_cmd(cmd)