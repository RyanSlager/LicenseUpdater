from tkinter import filedialog
from tkinter import *
from pathlib import *
import os
import csv
import datetime

def main():
      root = Tk()
      paths = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                  filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
      for path in paths:
          writeUpdates(path)

"""handles paths supplied by filedialog and calls makeUpdateFile for each csv supplied"""
def writeUpdates(path):
    if "pm" in path.lower():
        file = makeUpdateFile("pm", path)
    elif "cx" in path.lower():
        file = makeUpdateFile("cx", path)
    elif "g2" in path.lower():
        file = makeUpdateFile("g2", path)

"""creates the update files, takes a string indicating the product and a string representing the path to the update csv"""
def makeUpdateFile(product, path):
    file = Path("~\Desktop\{0}_license_updates_{1}.txt".format(product, getDate()))
    fullPath = file.expanduser()

    if fullPath.exists():
        fullPath.unlink()
        fullPath.touch()
        procedureWriter(fullPath)
        procedureCalls(fullPath, path)
    else:
        fullPath.touch()
        procedureWriter(fullPath)
        procedureCalls(fullPath, path)

"""copies the procedure definition for the given product from the included txt files. takes a Path() object"""
def procedureWriter(file):
    product = file.stem[:2]
    procFile = Path("{0}.txt".format(product))
    file.write_text(procFile.read_text())

"""writes the procedure calls using the supplied csv's. takes a Path() object(file) and a string representing the path to the update csv"""
def procedureCalls(file, path):
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
        updates.write("{4}{0}'{1}','{2}','{3}');".format(procedure, row[0], row[1], row[2], os.linesep))

    updates.write("{0}commit;{0}end;{0}/".format(os.linesep))

"""gets current date and formats it to mm_dd_yy"""
def getDate():
    date = datetime.datetime.now()
    cleanDate = date.strftime('%m_%d_%Y')
    return cleanDate

if __name__ == "__main__":
    main()