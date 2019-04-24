from tkinter import filedialog
from tkinter import simpledialog
import tkinter as tk
from pathlib import *
import os
import csv
import datetime

def main():

    application_window = tk.Tk()

    products = ["cx", "pm", "g2"]
    state = simpledialog.askstring("State", "What state are you updating?", parent=application_window)
    path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    for product in products:
      makeUpdateFile(product, path, state)

"""creates the update files, takes a string indicating the product and a string representing the path to the update csv"""
def makeUpdateFile(product, path, state):
    file = Path("~\Desktop\{0}_license_updates_{1}.txt".format(product, getDate()))
    destinationPath = file.expanduser()

    if destinationPath.exists():
        destinationPath.unlink()
        destinationPath.touch()
        procedureWriter(destinationPath)
        procedureCalls(destinationPath, path, state)
    else:
        destinationPath.touch()
        procedureWriter(destinationPath)
        procedureCalls(destinationPath, path, state)

"""copies the procedure definition for the given product from the included txt files. takes a Path() object"""
def procedureWriter(file):
    product = file.stem[:2]
    procFile = Path("{0}.txt".format(product))
    file.write_text(procFile.read_text())

"""writes the procedure calls using the supplied csv's. takes a Path() object(file) and a string representing the path to the update csv"""
def procedureCalls(file, path, state):
    product = file.stem[:2]

    if product == "pm":
        procedure = "UPDATE_RC_ST("
    elif product == "cx":
        procedure = "UPDATE_ORG_ST("
    elif product == "g2":
        procedure = "UPDATE_INSR_ST("

    lics = open(path, "rt")
    rows = csv.reader(lics)
    updates = open(file, "a")
    for row in rows:
        updates.write("{5}{0}'{1}','{2}','{3}','{4}');".format(procedure, row[0].strip(), row[1].strip(), row[2].strip(), state, os.linesep))

    if product == "pm":
        updates.writelines("{0}{0}end loop;".format(os.linesep))

    updates.write("{0}commit;{0}end;{0}/".format(os.linesep))

"""gets current date and formats it to mm_dd_yy"""
def getDate():
    date = datetime.datetime.now()
    cleanDate = date.strftime('%m_%d_%Y')
    return cleanDate

if __name__ == "__main__":
    main()