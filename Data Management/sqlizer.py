# sqlizer - a simple tool to facilitate importing CSVs into an SQL database. Super minimal
# Python 3.6

# Import Block
import sqlite3 as sql
import csv
import os
import sys

def statusprint(jobsDone, sumJobs): # adapted from Tapestry, which was adapted from somewhere else.
    lengthBar = 15.0
    doneBar = int(round((jobsDone/sumJobs)*lengthBar))
    doneBarPrint = str("#"*int(doneBar)+"-"*int(round((lengthBar-doneBar))))
    percent = float((jobsDone/sumJobs)*100)
    text = ("\r{0}: [{1}] {2}%" .format("Parsing", doneBarPrint, percent))
    sys.stdout.write(text)
    sys.stdout.flush()

print("Welcome to PSavLabs SQLizer.")
print("Please specify the location of the database you want to modify/create.")
print("If you specify an incomplete path, it will be created as a subdirectory of %s" % os.getcwd())
pathDB = input("DB Path: ")
print("Please wait while I bring that up for you.")
conn = sql.connect(pathDB)
cur = conn.cursor()
print("OK.")
importing = True
while importing:
    sumLines = 0
    print("Each import is treated as a new table. Please enter a name for this table.")
    nameTable = input(">")
    print("Please specify the filename you wish to import as this table.")
    nameCSV = input("CSV filename: ")
    print("Is this an excel, excel-tab, or unix CSV?")
    typeCSV = input("Select: ").lower()
    if typeCSV not in csv.list_dialects():
        print("Invalid input, assuming sanest default.")
        typeCSV = "excel"
    fileCSV = open(nameCSV, "r")
    readerTable = csv.DictReader(fileCSV, dialect=typeCSV, restval=None)
    with open(nameCSV, "r") as f:
        for lines in f:
            sumLines += 1
    sumLines -= 1 # because we take the headers, we can ignore that row.
    print("Using row 1 as the table headers.")
    columns = ""
    rowColumns = readerTable.fieldnames
    for header in rowColumns:
        columns+=(str(header)+", ") # Super ghetto method to turn a literal list into a string list.
    # Never parse statements this way in any use case where a user input would be included, unless you are the only user.
    stmnt = ("CREATE TABLE %s (%s)" % (nameTable, columns.rstrip(", ")))  # Leave one at the end, get an error.
    cur.execute(stmnt)
    # From now on, no commiting until we're done, in case we break something along the way.
    # This script is being designed to run under the weirdest possible use case.
    Qs = ""
    for q in rowColumns: # if there are three fieldnames, we will be feeding in three values.
        Qs += "?, "
    stmntAdd = ("INSERT INTO %s (%s) VALUES (%s)" % (nameTable, columns.rstrip(", "), Qs.rstrip(", ")))
    #time to read them in
    to_db = []
    numLine = 0
    for line in readerTable:
        statusprint(numLine, sumLines)  # Stolen from Tapestry, another PSavLabs project
        tupData = []
        for i in line.items(): # a line is ORDEREDDICT for some reason.
            tupData.append(i[1])  # the order of values and the order of fieldnames is same
        to_db.append(tupData)
        numLine += 1
        statusprint(numLine, sumLines)
    cur.executemany(stmntAdd, to_db)
    conn.commit()

    print("\nTable has been imported. Add another table?")
    do_it = input("y/n? ")

    if do_it.lower() == "n":
        importing = False

conn.close()
print("Ok. Your database has been built.")