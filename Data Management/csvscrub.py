# CSVSCRUB - configurably sanitize CSVed tables.
# Built in Python 3.6 // instructions in USAGE.md

import argparse  # needed to fetch the files to parse
import configparser  # needed to fetch the parsing instructions
import csv  # needed because we're dealing with csvs.
import sys  # needed so I don't have to reinvent statusprint

#Set the encoding of the input CSVs used.
enc = "cp1252"  # At present I have a need for this, but if you don't need it, set the value to none
out = "utf-8"

# Define Classes
class header(object):  # Little object we can predefine config values for elegance
    def __init__(self, name):
        self.name = str(name)
        self.scrub = False
        self.scrubbed = "0xdeadbeef"  # Could be any value, not used by default.
        self.indexed = False

    def parse(self, cfg):  # Expects a read-in configparser object
        self.counter = 0  # Per-header counter.
        self.scrub = cfg.getboolean(self.name, "scrub")
        self.indexed = cfg.getboolean(self.name, "map")
        if self.indexed:
            self.dictIndex = {}  # Used for "Mapped Scrub"
        self.scrubbed = cfg.get(self.name, "scrubbed value")
        if self.scrubbed == "%blank%":
            self.scrubbed = None

# Define Functions

def initHeaders(cfg):  # expects cfgparser, returns iterable of header objects
    listHeaders = cfg.sections()
    headers = {}
    for hname in listHeaders:
        h = header(hname)
        h.parse(cfg)
        headers.update({h.name: h})
    return headers

def scrub(header):  # expects the relevant header object
    try:
        valueNew = (header.scrubbed % str(header.counter))
    except TypeError:  # if for some reason the number is mismatched (usually no sub provided), we say fuckit
        valueNew = header.scrubbed
    header.counter += 1
    return valueNew

def indexedScrub(header, value):  # expects the babysitter function to hand it the right object
    if str(value) not in header.dictIndex:
        indexNum = str(header.counter)
        header.dictIndex.update({str(value): indexNum})
        header.counter += 1

    indexNum = header.dictIndex[str(value)]
    try:
        valueNew = (header.scrubbed % indexNum)
    except TypeError:  # For Mapped Scrub, a %s replace MUST be included in the scrubbed value or it don't work.
        print("An exception has occurred handling %s - no sub character was included in the scrubbed value." % header.name)
        exit()
    return valueNew

def statusprint(file, jobsDone, sumJobs): # adapted from Tapestry, which was adapted from somewhere else.
    lengthBar = 30.0
    doneBar = int(round((jobsDone/sumJobs)*lengthBar))
    doneBarPrint = str("#"*int(doneBar)+"-"*int(round((lengthBar-doneBar))))
    percent = int((jobsDone/sumJobs)*100)
    text = ("\r{0}: [{1}] {2}%" .format(file, doneBarPrint, percent))
    sys.stdout.write(text)
    sys.stdout.flush()

# Pre-Runtime Initialization
parser = argparse.ArgumentParser(description="Automatically sanitize a given csv according to the values in csvscrub.cfg")
parser.add_argument('files', help="Fully-Qualified path to files, space-seperated", nargs='+', type=str, action="store") #  Set nargs to + to indicate an arbitrary number >0 expected.
args = parser.parse_args()
listFiles = args.files

conf = configparser.ConfigParser(interpolation=None)
conf.read('csvscrub.cfg')

#  Predefine Runtime
rules = initHeaders(conf)
print("csvscrub will now attempt to scrub these files: "+str(listFiles))
for file in listFiles:
    print("\nNow scrubbing "+str(file))
    with open(file, "r", encoding=enc) as data:
        with open(file, "r", encoding=enc) as f:
            thisDialect = csv.Sniffer().sniff(f.readline())
        with open(file, "r", encoding=enc) as f:
            sumLines = 0
            for l in f:
                sumLines += 1
            sumLines -= 1 # because we can ignore the header.
        reader = csv.DictReader(data, dialect=thisDialect)
        linesDone = 0
        statusprint(file, linesDone, sumLines)
        headersObserved = reader.fieldnames
        scrubbedLinesFeed = []
        for line in reader:
            scrubbedLine = {}
            for i in line.items():
                useHeader = None
                try:
                    useHeader = rules[str(i[0])]
                except KeyError:  # if a given column isn't in the dictionary, default is to ignore.
                    scrubbedLine.update({i[0]: i[1]})
                if useHeader is None:
                    useHeader = header("foo")  # Headers have scrub = False by default, so we just need a throwaway.
                if useHeader.scrub:
                    if useHeader.indexed:
                        newvalue = indexedScrub(useHeader, i[1])
                    else:
                        newvalue = scrub(useHeader)
                    scrubbedLine.update({i[0]: newvalue})
                else:
                    scrubbedLine.update({i[0]: i[1]})
            scrubbedLinesFeed.append(scrubbedLine)
            linesDone += 1
            statusprint(file, linesDone, sumLines)
        with open(("scrubbed_"+file), "w", encoding=out) as output:
            print("Saving converted file to CWD.")
            writer = csv.DictWriter(output, dialect="excel", fieldnames=headersObserved)
            writer.writeheader()
            writer.writerows(scrubbedLinesFeed)
            print("Done.")