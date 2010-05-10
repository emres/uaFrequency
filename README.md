# uaFrequency: Word Frequencies for the UA web pages

This is a small collection of utlities that I have written to extract word
frequency data from the Universiteit Antwerpen web pages. These data will
be used for further analysis and language usage quality reporting.

## wget documentation

Since I use the wget with lots of parameters, I wanted to provide a
brief documentation:

wget 

Set number of retries to 5 for each page:

-t 5  

Set the network timeout to 10 seconds:

-T 10 

Turn on recursive retrieving.:

-r   

Enable spanning across hosts when doing recursive retrieving:

-H 

Set domains to be followed. domain-list is a comma-separated list of domains. 
Note that it does not turn on '-H':

-Dwww.ua.ac.be  

Specify comma-separated lists of file name suffixes or patterns to
accept or reject:

-R gif,GIF,jpg,jpeg,png,mp3,wav,mpg,mpeg,doc,pdf,PDF,ppt,xls,docx,js,css,bmp,JPG,swf,ico,Download.aspx,download.aspx

Specify download quota for automatic retrievals. The value can be
specified in bytes (default), kilobytes (with 'k' suffix), or
megabytes (with 'm' suffix). 10 GB in this case:

-Q 1048576m

http://www.ua.ac.be/main.aspx?c=*UA  

