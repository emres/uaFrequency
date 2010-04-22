import os
import glob
import re

htmlJS        = re.compile('<script .*?>.*?</script>', re.I | re.M | re.DOTALL)
htmlComment   = re.compile('<!--.*?-->', re.I | re.M | re.DOTALL)
htmlTag       = re.compile('<.*?>', re.I | re.M | re.DOTALL) 
htmlEmptyLine = re.compile('^$', re.I | re.M | re.DOTALL) 
htmlSpace     = re.compile('&nbsp;', re.I | re.M | re.DOTALL) 

# files = glob.glob('www.ua.ac.be/gecici.html')
# files = glob.glob('www.ua.ac.be/main.aspx@c=%2AAFSTUD')
files = glob.glob('www.ua.ac.be/*')


for file in files:
    # print "Current file: " + file
    fileContents = open(file).read()
    fileContents = htmlJS.sub('', fileContents)
    fileContents = htmlComment.sub('', fileContents)
    fileContents = htmlTag.sub('', fileContents)
    fileContents = htmlEmptyLine.sub('', fileContents)
    fileContents = htmlSpace.sub('', fileContents)

    print fileContents



####################

    # for word in wordSet:
    #     if len(word) > 1:            
    #         if word in mainFrequency:
    #             mainFrequency[word] = mainFrequency[word] + 1
    #         else:
    #             mainFrequency[word] = 1

    #         if word not in wordReverseIndex:
    #             wordReverseIndex[word] = file


#    if dummyCounter > 500:
        # for (word, frequency) in mainFrequency.items():
        #     wordTuple = (word,frequency,)
        #     c.execute("""INSERT INTO mainFrequency VALUES (?, ?)""", wordTuple)
        #     #print "%s %i" % (word, frequency)

        # for (word, file) in wordReverseIndex.items():
        #     wordUrlTuple = (word, file,)
        #     c.execute("""INSERT INTO wordReverseIndex(word, url) VALUES (?, ?)""", wordUrlTuple) 

#        break
