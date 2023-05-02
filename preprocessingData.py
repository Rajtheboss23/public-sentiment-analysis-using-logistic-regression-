import csv
from nltk.corpus import stopwords 

def preProcessing(s,listOfStopWords):
    #Removing hyperlinks 
    s1=""
    flag=0

    for i in range(0,len(s)):
        if s[i]=='h':
            s1=s[i:i+4]
            if s1=="http":
                for j in range(i+4,len(s)):
                    if s[j]==' ':
                        flag=1
                        break
                
            if flag==1:
                break

    if flag==1:
        s=s[0:i]+s[j+1:len(s)]

    #Removing Punctuation marks 
    s1=""
    for i in range(0,len(s)):
        if s[i].isalpha() or s[i].isnumeric() or s[i]==' ':
            s1=s1+s[i]
    s=s1

    #Removing the Stop words
    s1=s.split(" ")
    s2=""
    for i in s1: 
        i=i.lower()
        if i not in listOfStopWords:
            s2=s2+i+" "
    return s2


file1=open("F:/St. Xaviers/Project/sentimentAnalysisDatasetTwitter.csv", "r")
file2=open("F:/St. Xaviers/Project/sentimentAnalysisDatasetTwitter3.csv", "a")
listOfStopWords=stopwords.words("english")
s=csv.reader(file1)
c=0
for rows in s:
    print(c)
    c=c+1
    file2.write(preProcessing(rows[0],listOfStopWords)+",")
    if rows[1]=="neutral":
        file2.write("2"+"\n")
    elif rows[1]=="positive":
        file2.write("4"+"\n")
    elif rows[1]=="negative":
        file2.write("0"+"\n")
    else:
        file2.write(rows[1]+"\n")

file1.close()
file2.close()