# ml_AutoTag

README:

AutoTagv2 is a python3 program that generates important tags based on a pdf document as input.
(AutoTagv4 was a step towards hitting an image recognition API but is unfinished.)

program written by Robert Malito (malito2@illinois.edu) with the help of Jack Mazenec: Interns Summer 2017


Program Flow:

1) PDF document is converted to HTML using seperate script pdf2txt.py
2) HTML is parsed for FULL TEXT and FONT SIZE tags with their TEXT
3) FONT SIZE + TEXT is sorted then counted
4) All strings with fonts larger than the most common font size are added to a TAGS list
5) FULL TEXT is fed into STANFORD NER
6) STANFORD NER outputs are parsed, reduced using an arbirary threshold, then counted
7) Outputs from each entity category are added to TAGS list then sorted by frequency
8) FULL TEXT is converted to special "bag of words" form then fed into gensim LDA and LSI models
9) Model output is reduced to unique entries then added to a TAGS list
10) all 3 TAGS lists are merged to form OUTPUT TAGS list


| SETUP |
(PYTHON LIBRARIES NEEDED) (Anaconda Comes with a few of these already)

------------------

nltk		http://www.nltk.org/install.html

stop_words	https://pypi.python.org/pypi/stop-words

gensim		https://radimrehurek.com/gensim/install.html

collections	(python core library) 

operator	(python core library)

os		(python core library)

bs4		https://www.crummy.com/software/BeautifulSoup/bs4/doc/

re		(python core library)

------------------

1) Unpack "pdfminer.six-master.zip" 
2) pdf2txt.py is located in subdirectory "pdfminer.six-master\tools" move it to same directory as AutoTagv2.py
3) install libraries as needed (see links above for help)




example command from git bash on Windows, or other linux like terminal:	
------------------

$ python AutoTagv2.py

enter pdf location:
------------------

AutoTag(pdf): ./test_docs/janitorial_request.pdf


output:
------------------

.pdf to .html conversion complete...
.html to .txt conversion complete...




===== OUTPUT TAGS =====


[ LDA/LSI model topics: ]

city

contractor

shall

service

[ Named Entity Extraction: ]

City

Contractor

Burien

2011

RFP

Community

14700

98166

Services

Washington

Center

Per

Exhibit

RCW

Facilities

Parks

Month

SECTION

Intent

Request

Myron

[ Font Size Extraction: ]

city of burien washington

request for proposals rfp

for

janitorial services

service locations

-------------------