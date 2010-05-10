import os
import glob
import re
import sqlite3

import contextData

htmlJS = re.compile('<script .*?>.*?</script>', re.I | re.M | re.DOTALL)
htmlComment = re.compile('<!--.*?-->', re.I | re.M | re.DOTALL)
htmlTag = re.compile('<.*?>', re.I | re.M | re.DOTALL) 
htmlEntity     = re.compile('&.*?;', re.I | re.M | re.DOTALL) 

files = glob.glob('www.ua.ac.be/*')

numFiles = len(files)
dummyCounter = 0

print "The number of files = %i" % numFiles

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
    for key in contextData.context.keys():
        if file.find(key) > 1:
            urlContext = contextData.context[key]
            break

    for word in wordSet:
        word = word.strip().strip(',').strip()

        if len(word) > 1:   
         
            wordTuple = (word,)
            wordUrlTuple = (word, url,)
            wordUrlContextTuple = (word, url, urlContext,)

            c.execute("""SELECT * FROM mainFrequency WHERE word = ?""" , wordTuple)

            if c.fetchone() is None:
                c.execute("""INSERT INTO mainFrequency VALUES (?, 1)""", wordTuple)
            else:
                c.execute("""UPDATE mainFrequency SET frequency = frequency + 1 WHERE word = ?""", wordTuple)         
            c.execute("""SELECT * FROM wordReverseIndex WHERE word = ? AND url = ?""", wordUrlTuple)

            if c.fetchone() is None:
                c.execute("""INSERT INTO wordReverseIndex(word, url, context) VALUES (?, ?, ?)""", wordUrlContextTuple) 
                            

    dummyCounter = dummyCounter + 1

    if dummyCounter % 10 == 0:
        percentFileProcessed = str((100.0 * dummyCounter) / numFiles)[0:4]
        print '%i out of %i files processed - %%%s' % (dummyCounter, numFiles, percentFileProcessed)
    
    if dummyCounter > 100:
        break

conn.commit()
conn.close()



