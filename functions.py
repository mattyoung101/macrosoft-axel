# Year 10 Term 4 IT Assignment (CSV editing application)
# This module contains all commands that can be executed. It is called by main.py.
# By Matt Young
import csv
import data
import main
import os
import time

# Utility functions
def __is_in_csv(value):
    """Returns True if specified value exists anywhere within the CSV, else False"""
    for x in data.opened_file_data:
        for y in x:
            if y == value:
                return True
    return False

def __get_column(heading):
    """Returns a list containing the entries down the column named heading"""
    # column iterate from https://stackoverflow.com/a/34386518/5007892
    cols = [x for x in zip(*data.opened_file_data)]
    index = data.opened_file_data[0].index(heading)
    return cols[index]

def __get_col_max_width(index):
    """Returns the max width of the Nth column"""
    # column iterate from https://stackoverflow.com/a/34386518/5007892
    cols = [x for x in zip(*data.opened_file_data)]
    column = cols[index]
    return len(sorted(column, key=len, reverse=True)[0])

def __is_float(value):
    """Returns True if this value can be cast to a float, else False"""
    try:
        float(value)
        return True
    except ValueError:
        return False

# this has to be called fopen because open() is already a function and we need to use it
def fopen(filename):
    """Open a CSV of the specified filename."""

    def __internal_open():
        # usually you'd do this in a with statement, but in our case we want the file instance to persist the whole time you're editing it
        f = open(filename, "r+", newline="")
        reader = csv.reader(f, delimiter=",")

        # we have to use a new module here "data" due to python import shenanigans - not ideal, but it works
        data.opened_file = filename
        data.opened_file_data = [x for x in reader]
        data.opened_file_handle = f

        print("Opened file", filename)

    if data.opened_file is not None:
        if main.ask("A file is currently open. Are you sure you want to continue?"):
            save()
            close()
            __internal_open()
        else:
            print("Operation aborted.")
    else:
        __internal_open()
    return True # operation always succeeds unless a write error occurs

def new(filename):
    """Makes a blank CSV with the filename specified, and opens it"""
    f = open(filename, "w")
    f.write("") # TODO is this necessary? I think open() will make a new file anyway
    f.close()
    fopen(filename)

def display():
    """Pretty-prints the current edited CSV document to the console"""
    if data.opened_file is None:
        print("Error: no file opened.")
        return False

    for row in data.opened_file_data:
        for i, col in enumerate(row):
            # we add an extra 2 spaces for padding
            max_len = __get_col_max_width(i) + 4
            print(col.ljust(max_len), end="")
        print()

def save():
    """Saves the current edited CSV file to disk."""
    if data.opened_file is None:
        print("Error: no file opened.")
        return False

    # first truncate the file (else r+ mode will append the extra data which we don't want)
    data.opened_file_handle.seek(0)
    data.opened_file_handle.truncate(0)

    writer = csv.writer(data.opened_file_handle, delimiter=",")
    for row in data.opened_file_data:
        writer.writerow(row)
    
    print("Saved file", data.opened_file, "to disk.")
    return True

def close():
    """Closes the currently open CSV file without saving."""
    if data.opened_file is None:
        print("Error: no file opened.")
        return False
    print("Closed file", data.opened_file)
    data.opened_file = None
    data.opened_file_data.clear()
    data.opened_file_handle.close()
    return True

def writebusinessdata():
    """Writes the internal business data string to disk."""
    with open("business_data.csv", "w") as f:
         f.write(main.csv_mutliline)
         print("Wrote multi-line string data to ./business_data.csv")
    return True

def delete(month):
    """Deletes the given month of data."""
    if data.opened_file is None:
        print("Error: no file opened.")
        return False
    elif not __is_in_csv(month):
        print("Error: there is no month", month, "in the CSV.")
        return False

    if main.ask("Are you sure you want to delete ALL DATA in the month {}?".format(month)):
        # find what the column index of the deleted month is
        index = data.opened_file_data[0].index(month)
        # for each row, delete that column
        for row in data.opened_file_data:
            del row[index]
        print("Data deleted.")
    else:
        print("Operation aborted.")
    return True

def insert(month):
    """Inserts an additional month of data."""
    if data.opened_file is None:
        print("Error: no file opened.")
        return False
    else:
        # add the extra month to the heading row
        data.opened_file_data[0].append(month.upper())
        # for each row, add the extra month
        for row in data.opened_file_data[1::]:
            row.append("")
        print("Inserted month", month.upper(), "successfully.")
        return True

def change(month, key, value):
    """Sets the key entry at the given month to the specified value."""
    if data.opened_file is None:
        print("Error: no file opened.")
        return False

    if not __is_in_csv(month):
        print("Error: there is no month", month, "in the CSV file. This function is case sensitive.")
        return False
    elif not __is_in_csv(key):
        print("Error: there is no key", key, "in the CSV file. This function is case sensitive.")
        return False
    else:
        # which column the month is in
        col_index = data.opened_file_data[0].index(month) 
        # find which row the key we're trying to insert is in
        row_index = __get_column("Expense").index(key)
        data.opened_file_data[row_index][col_index] = value
        print("Added data successfully.")

def clear():
    """Clears the screen"""
    os.system("cls")

def msum(month):
    """Calculates the sum of a given month's data"""
    if data.opened_file is None:
        print("Error: no filed opened.")
        return False
    elif not __is_in_csv(month):
        print("Error: there is no month", month, "in the CSV file. This function is case sensitive.")
        return False
    else:
        column = __get_column(month)
        # collect all entries in the column that are numbers (can be cast to a float)
        calculated_sum = sum([float(x) for x in column if __is_float(x)])
        print("Sum of", month, "is:", calculated_sum)

def about():
    """Prints some cool ASCII art and info about the program."""
    print("""
    __  ___                                 ______ 
   /  |/  /___ _______________  _________  / __/ /_
  / /|_/ / __ `/ ___/ ___/ __ \/ ___/ __ \/ /_/ __/
 / /  / / /_/ / /__/ /  / /_/ (__  ) /_/ / __/ /_  
/_/  /_/\__,_/\___/_/   \____/____/\____/_/  \__/  
    ___   _  __ ________ 
   /   | | |/ // ____/ / 
  / /| | |   // __/ / /  
 / ___ |/   |/ /___/ /___
/_/  |_/_/|_/_____/_____/   Python Edition

"Intuitive. Professional. Secure."

Copyright (c) 2018 Macrosoft Corp. No rights reserved.
Version: 0.0.1
Developed by Matt Young.""")