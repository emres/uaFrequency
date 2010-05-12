import os
import glob
import re
import sqlite3
import sys
import getopt
import string

import contextData

import psyco
psyco.full()
psyco.log()


def usage():
    print " "
    print "Usage: convert.py -n maximumNumberOfFilesToBeProcessed"
    print " "
    print "Example: convert.py -n 999"
    print " "

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:")
except getopt.GetoptError, err:
    usage()
    print str(err)    
    sys.exit(2)

for o, a in opts:
    if o == "-n":
        maxNumFiles = int(a)
        print "Maximum number of files to be processed = %d" % maxNumFiles
    else:
        assert False, "unhandled option"
        usage()
        sys.exit(2)

htmlJS = re.compile('<script .*?>.*?</script>', re.I | re.M | re.DOTALL)
htmlComment = re.compile('<!--.*?-->', re.I | re.M | re.DOTALL)
htmlTag = re.compile('<.*?>', re.I | re.M | re.DOTALL) 
htmlEntity     = re.compile('&.*?;', re.I | re.M | re.DOTALL) 
contextRegEx  = re.compile('main.aspx@c=((%2A)|\.)(.*?)&', re.DOTALL)
contextRegEx2 = re.compile('main.aspx@c=((%2A)|\.)(.*?)$')
unicodeNonAlphanumeric = re.compile('\W+', re.UNICODE)

files = glob.glob('www.ua.ac.be/*')

numFiles = len(files)
dummyCounter = 0

print "The total number of files = %i" % numFiles

conn = sqlite3.connect('frequency.db')
conn.text_factory = str
c = conn.cursor()

mainFrequency = dict()
wordReverseIndex = dict()

for file in files:
    fileContents = open(file).read()
    fileContents = htmlJS.sub('', fileContents)
    fileContents = htmlComment.sub('', fileContents)
    fileContents = htmlTag.sub(' ', fileContents)
    fileContents = htmlEntity.sub(' ', fileContents)

    words = fileContents.split()

    wordSet = set(words)

    url = file.replace("%2A", "*")
    url = url.replace("@", "?")
    url = url.replace("\\", "/")
    url = "http://" + url

    urlContext = "UNKNOWN"
    match = contextRegEx.search(file)
    if match is not None: 
        if match.group(3) is None or match.group(3) == '':
            match = contextRegEx2.search(file)
            if match is not None:
                urlContext = contextData.context.get(match.group(3), "UNKNOWN")
        else:
            urlContext = contextData.context.get(match.group(3), "UNKNOWN")
    else:
        match = contextRegEx2.search(file)
        if match is not None:
            urlContext = contextData.context.get(match.group(3), "UNKNOWN")

    for word in wordSet:
        word = word.strip()
        word = word.rstrip(';\'')
        word = word.strip(',/:"\(\)')
       
        wordFrequency = 0

        if len(word) >= 2 and len(word) <= 30:

            #match = unicodeNonAlphanumeric.search(word)
            #if match is None:
            if True:
                wordFrequency = string.count(fileContents, word)
         
                c.execute("""SELECT * FROM mainFrequency WHERE word = ?""" , (word,))
                if c.fetchone() is None:
                    c.execute("""INSERT INTO mainFrequency VALUES (?, 1)""", (word,))

                else:
                    c.execute("""UPDATE mainFrequency SET frequency = frequency + ? WHERE word = ?""", (wordFrequency, word,))         

                c.execute("""SELECT * FROM wordReverseIndex WHERE word = ? AND url = ?""", (word, url,))
                if c.fetchone() is None:
                    c.execute("""INSERT INTO wordReverseIndex(word, url, context) VALUES (?, ?, ?)""", (word, url, urlContext,)) 
                            

    dummyCounter = dummyCounter + 1

    if dummyCounter % 200 == 0:
        percentFileProcessed = str((100.0 * dummyCounter) / numFiles)[0:4]
        print '%i out of %i files processed - %%%s' % (dummyCounter, numFiles, percentFileProcessed)
        conn.commit()
    
    if dummyCounter >= maxNumFiles:
        break

conn.commit()
conn.close()
