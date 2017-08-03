import nltk
nltk.data.path.append('./nltk_data/')
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models
import gensim
from collections import Counter
from operator import itemgetter

import os
from bs4 import BeautifulSoup
import re

tokenizer = RegexpTokenizer(r'\w+')

# print("\n")
inputfile = input("AutoTag(pdf): ")
path_var = "python pdf2txt.py -o autoTag.html " + inputfile
os.system(path_var)
print(".pdf to .html conversion complete...")

htmlStrip = open('./autoTag.html', 'r', encoding="utf-8")
all_soup = BeautifulSoup(htmlStrip, "html.parser")
all_data = all_soup.findAll(text=True)
htmlStrip.close()
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True
 
result = list(filter(visible, all_data))
print(".html to .txt conversion complete...")
print("\n")
# print (result)


htmlData = open('./autoTag.html', 'r', encoding="utf-8")
soup = BeautifulSoup(htmlData, "html.parser")
htmlData.close()

font_spans = [ data for data in soup.select('span') if 'font-size' in str(data) ]
output = []
for i in font_spans:
    tup = ()
    fonts_size = re.search(r'(?is)(font-size:)(.*?)(px)',str(i.get('style'))).group(2)
    tup = (str(i.text).strip(),int(fonts_size.strip()))
    output.append(tup)
output.sort(key=itemgetter(1), reverse=True)
filtered_output = []
for text, f_size in output:
    t_text = re.sub('[^A-Za-z0-9]+', ' ', text)
    item = (t_text.lower(), f_size)
    filtered_output.append(item)
output_redux = [x for x in filtered_output if x[0] != '']
output_redux = [x for x in output_redux if len(re.sub('[^A-Za-z]+', '', x[0])) > 2 ]

font_size_list = []
for n in output_redux:
    font_size_list.append(n[1])
font_size_count = Counter(font_size_list)
most_common_font = font_size_count.most_common(2)
most_common_font_val = int((most_common_font[0][0] + most_common_font[1][0]) / 2) + ((most_common_font[0][0] + most_common_font[1][0]) % 2 > 0)
# print(most_common_font[0][0])
# print(most_common_font[1][0])
# print(most_common_font_val)

big_font_tags = []
for fs in output_redux:
    if fs[1] > most_common_font[0][0]:
        apnd = fs[0].replace('\n', '')
        big_font_tags.append(apnd)
del big_font_tags[5:]


tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    
wnl = WordNetLemmatizer()
# print("\n")
# inputfile = input("AutoTag: ")
# create sample documents
doc_a = ""
for entry in result:
    doc_a += entry.replace('\n', ' ')
# with open(inputfile, 'r', encoding="utf-8") as myfile:
#     doc_a = myfile.read().replace('\n', ' ')
# doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
# doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
# doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
# doc_e = "Health professionals say that brocolli is good for your health." 

# compile sample documents into a list
doc_set = [doc_a]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    
    # clean and tokenize document string
    
    raw = i
    raw_lower = i.lower()
    tokens = tokenizer.tokenize(raw)
    tokens_lower = tokenizer.tokenize(raw_lower)
    # test_token = nltk.word_tokenize()
    tag = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tag)
#     print(entities)
    # print("\n")
    # print("\n")
    # print("<||||||||||||||||||||NER||||||||||||||||||||>")
    # print("\n")

    PERSON_list = []
    ORGANIZATION_list = []
    LOCATION_list = []
    FACILITY_list = []
    GPE_list = []
    CD_list = []

    for people in entities.subtrees(filter=lambda t: t.label() == 'PERSON'):
        #     print(people)
            entity_name = people.leaves()
            for x in entity_name:
                PERSON_list.append(x[0])
    for orgs in entities.subtrees(filter=lambda t: t.label() == 'ORGANIZATION'):
        #     print(orgs)
            entity_name = orgs.leaves()
            for x in entity_name:
                ORGANIZATION_list.append(x[0])
    for places in entities.subtrees(filter=lambda t: t.label() == 'LOCATION'):
        #     print(places)
            entity_name = places.leaves()
            for x in entity_name:
                LOCATION_list.append(x[0])
    for noteable in entities.subtrees(filter=lambda t: t.label() == 'FACILITY'):
        #     print(noteable)
            entity_name = noteable.leaves()
            for x in entity_name:
                FACILITY_list.append(x[0])
    for geo_pol_ent in entities.subtrees(filter=lambda t: t.label() == 'GPE'):
        #     print(geo_pol_ent)
            entity_name = geo_pol_ent.leaves()
            for x in entity_name:
                GPE_list.append(x[0])

    for cd in entities:
        if(type(cd) == tuple):
                if(cd[1] == 'CD'):
                        if(len(cd[0]) > 3):
                                CD_list.append(cd[0])

    tags_ner = []
    tags_ner_plain = []
    # print("----------------------PERSON----------------------")
    
    PERSON_counts = Counter(PERSON_list)
    # print(len(PERSON_counts))
    # print(PERSON_counts)
    # print("\n")

    num_relevant = int(len(PERSON_counts) / 8) + 1
    if(num_relevant > 10):
        num_relevant = 10
    for tag, count in PERSON_counts.most_common(num_relevant):
        obj = (tag, count)
        tags_ner.append(obj)

    # print("-------------------ORGANIZATION-------------------")
    ORGANIZATION_counts = Counter(ORGANIZATION_list)
    # print(len(ORGANIZATION_counts))
    # print(ORGANIZATION_counts)
    # print("\n")

    num_relevant = int(len(ORGANIZATION_counts) / 8) + 1
    if(num_relevant > 10):
        num_relevant = 10
    for tag, count in ORGANIZATION_counts.most_common(num_relevant):
        obj = (tag, count)
        tags_ner.append(obj)

    # print("---------------------LOCATION---------------------")
    LOCATION_counts = Counter(LOCATION_list)
    # print(len(LOCATION_counts))
    # print(LOCATION_counts)
    # print("\n")

    num_relevant = int(len(LOCATION_counts) / 8) + 1
    if(num_relevant > 10):
        num_relevant = 10
    for tag, count in LOCATION_counts.most_common(num_relevant):
        obj = (tag, count)
        tags_ner.append(obj)

    # print("---------------------FACILITY---------------------")
    FACILITY_counts = Counter(FACILITY_list)
    # print(len(FACILITY_counts))
    # print(FACILITY_counts)
    # print("\n")

    num_relevant = int(len(FACILITY_counts) / 8) + 1
    if(num_relevant > 10):
        num_relevant = 10
    for tag, count in FACILITY_counts.most_common(num_relevant):
        obj = (tag, count)
        tags_ner.append(obj)

    # print("-----------------------GPE------------------------")
    GPE_counts = Counter(GPE_list)
    # print(len(GPE_counts))
    # print(GPE_counts)        
    # print("\n")

    num_relevant = int(len(GPE_counts) / 8) + 1
    if(num_relevant > 10):
        num_relevant = 10
    for tag, count in GPE_counts.most_common(num_relevant):
        obj = (tag, count)
        tags_ner.append(obj)

    # print("---------------------CD(YEAR)---------------------")  
    CD_counts = Counter(CD_list)
    # print(len(CD_counts))
    # print(CD_counts)
    # print("\n")

    num_relevant = int(len(CD_counts) / 8) + 1
    if(num_relevant > 10):
        num_relevant = 10
    for tag, count in CD_counts.most_common(num_relevant):
        obj = (tag, count)
        tags_ner.append(obj)

    tags_ner.sort(key=itemgetter(1), reverse=True)
    for tag, freq in tags_ner:
            tags_ner_plain.append(tag)

    # print("\n")    
    # print("<|||||||||||||||||||||||||||||||||||||||||||>")
    # print("\n")

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens_lower if not i in en_stop]

    # stem tokens
    # stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    lemma_tokens = [wnl.lemmatize(i) for i in stopped_tokens]
    # add tokens to list
    texts.append(lemma_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
tags_ML = []
# print("===== STARTING LDA MODEL =====")
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=100)

# print(ldamodel.print_topics(num_topics=2, num_words=5))
# print("\n")

unformatted_tags = ldamodel.show_topics(num_topics=2, num_words=5, log=False, formatted=False)
for tag, rate in unformatted_tags[0][1]:
        tags_ML.append(tag)
for tag, rate in unformatted_tags[1][1]:
        tags_ML.append(tag)
# tags_ML[0][0][1])
# tags_ML[0][1][1]

# print("===== STARTING LSI MODEL =====")
lsimodel = gensim.models.lsimodel.LsiModel(corpus, id2word = dictionary, num_topics = 3)
# print(lsimodel.print_topics(num_topics=1, num_words=5))
unformatted_tags = lsimodel.show_topics(num_topics = 3, num_words = 5, log=False, formatted=False)
# type_check[0][1][x][0])
for tag, rate in unformatted_tags[0][1]:
        tags_ML.append(tag)
# for i in  lsimodel.show_topics(num_words=4):
#     print (i[0], i[1])
output_tags = tags_ML
output_tags.append("\n")
output_tags.append("[ Named Entity Extraction: ]")
output_tags.extend(tags_ner_plain)
output_tags.append("\n")
output_tags.append("[ Font Size Extraction: ]")
output_tags.extend(big_font_tags)

# print("\n")
print("\n")
print("===== OUTPUT TAGS =====")
print("\n")
print("[ LDA/LSI model topics: ]")
for T in list(dict.fromkeys(output_tags)):
    if(len(T) > 1):
        print (T)
print("\n")
# print(output_tags)
