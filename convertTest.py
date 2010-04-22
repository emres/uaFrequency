import os
import glob
import re
import sqlite3

htmlJS = re.compile('<script .*?>.*?</script>', re.I | re.M | re.DOTALL)
htmlComment = re.compile('<!--.*?-->', re.I | re.M | re.DOTALL)
htmlTag = re.compile('<.*?>', re.I | re.M | re.DOTALL) 
htmlSpace     = re.compile('&nbsp;', re.I | re.M | re.DOTALL) 

# files = glob.glob('www.ua.ac.be/gecici.html')
# files = glob.glob('www.ua.ac.be/main.aspx@c=%2AAFSTUD')
files = glob.glob('www.ua.ac.be/*')
# files = glob.glob('www.ua.ac.be/geciciSonuc.html')

dummyCounter = 0

conn = sqlite3.connect('frequency.db')
c = conn.cursor()

for file in files:
    # print "Current file: " + file
    fileContents = open(file).read()
    fileContents = htmlJS.sub('', fileContents)
    fileContents = htmlComment.sub('', fileContents)
    fileContents = htmlTag.sub('', fileContents)
    fileContents = htmlSpace.sub('', fileContents)

    words = fileContents.split()

    for word in words:
        if len(word) > 1:
            
            t = (word,)

            c.execute("""SELECT * FROM mainFrequency WHERE word = ?""" , t)

            if c.fetchone() is None:
                c.execute("""INSERT INTO mainFrequency VALUES (?, 1)""", t)
            else:
                c.execute("""UPDATE mainFrequency SET frequency = frequency + 1 WHERE word = ?""", t)
                
            conn.commit()

    # print fileContents
    print dummyCounter
    dummyCounter = dummyCounter + 1
    
    if dummyCounter > 40:
        break

conn.close()



