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
reNum = re.compile('\d+')
rePunct = re.compile('[-/\.%:]+')

files = glob.glob('www.ua.ac.be/*')

numFiles = len(files)
dummyCounter = 0

print "The total number of files = %i" % numFiles

conn = sqlite3.connect('frequency.db', isolation_level = "DEFERRED")
conn.text_factory = str
c = conn.cursor()

for file in files:
    fileContents = open(file).read()
    fileContents = htmlJS.sub('', fileContents)
    fileContents = htmlComment.sub('', fileContents)
    fileContents = htmlTag.sub(' ', fileContents)
    fileContents = htmlEntity.sub(' ', fileContents)

    tmpWords = fileContents.split()
    words = []

    for i in range(len(tmpWords)):
        word = tmpWords[i].strip()
        word = word.rstrip('!?,.;\'')
        word = word.strip('/:"\(\)')
        word = word.lower()
        if len(word) >= 2 and len(word) <= 27:            
            if word.find('@') < 0 and word.find('http') < 0:
                if len(rePunct.sub("", reNum.sub("", word))) > 1:
                    words.append(word)

    wordFrequencies = {}
    for word in words:
        wordFrequencies[word] = words.count(word)

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

    lastRowId = 0
    c.execute("""INSERT INTO urlTable(url) VALUES (?)""", (url,))
    lastRowId = c.lastrowid

    for word in wordSet:
        wordFrequency = 0

        #match = unicodeNonAlphanumeric.search(word)
        #if match is None:
        wordFrequency = wordFrequencies[word]         

        c.execute("""SELECT 1 FROM mainFrequency WHERE word = ? LIMIT 1""" , (word,))
        if c.fetchone() is None:
            c.execute("""INSERT INTO mainFrequency VALUES (?, 1)""", (word,))            
        else:
            c.execute("""UPDATE mainFrequency SET frequency = frequency + ? WHERE word = ?""", (wordFrequency, word,))         

        c.execute("""INSERT INTO wordReverseIndex(word, url, context) VALUES (?, ?, ?)""", (word, lastRowId, urlContext,))

    
    dummyCounter = dummyCounter + 1     

    if dummyCounter % 300 == 0:
        percentFileProcessed = str((100.0 * dummyCounter) / numFiles)[0:4]
        print '%i out of %i files processed - %%%s' % (dummyCounter, numFiles, percentFileProcessed)
        conn.commit()
    
    if dummyCounter >= maxNumFiles:
        break

conn.commit()
conn.close()
