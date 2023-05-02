import time
import emoji
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import matplotlib.pyplot as plt
import pandas as pd
from joblib import Parallel,delayed 
from nltk.corpus import stopwords 
import joblib
import snscrape.modules.twitter as sntwitter
import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
def is_neutral(sentence):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(sentence)
    return sentiment_scores['compound']==0


def total_posts():
    return df.shape[0]
def ret_pos():
    return "{:.2f}".format(pos)+"%"


def ret_neu():
    return "{:.2f}".format(neu)+"%"


def ret_neg():
    return "{:.2f}".format(neg)+"%"


def create_bar(pos, neg, neu):
    plt.figure()
    plt.bar(['POSITIVE'], [pos / 10], label='POSITIVE', color='g', width=0.5)
    plt.bar(['NEGATIVE'], [neg / 10], label='NEGATIVE', color='r', width=0.5)
    plt.bar(['NEUTRAL'], [neu / 10], label='NEUTRAL', color='c', width=0.5)
    plt.text('POSITIVE', pos / 10, "{:.1f}".format(pos)+"%", ha='center', va='bottom')
    plt.text('NEGATIVE', neg / 10, "{:.1f}".format(neg)+"%", ha='center', va='bottom')
    plt.text('NEUTRAL', neu / 10, "{:.1f}".format(neu)+"%", ha='center', va='bottom')
    plt.title("Bar Graph of Sentiment Analysis "+s1)
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")
    plt.legend()
    plt.savefig(r"D:\News Sentiment\UserInterface\static\results\bar.jpg")


def create_pie(pos, neg, neu):
    sizes = [pos, neg, neu]
    mylabels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    cols = ['g', 'r', 'c']
    plt.figure()
    plt.pie(sizes, labels=mylabels, colors=cols, startangle=90, autopct="%0.1f%%", shadow=False, explode=(0.05, 0.1, 0.1),
            labeldistance=1.1,
            textprops={'fontsize': 12})
    plt.pie([1], colors="w", radius=0.5)
    plt.title('Pie Plot of Sentiment Analysis ' + s1)
    plt.axis("equal")
    plt.legend(mylabels, loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=10, frameon=True, shadow=True, framealpha=0.8)
    plt.savefig(r"D:\News Sentiment\UserInterface\static\results\pie.jpg")
    create_bar(pos, neg, neu) 




#finding out positivity,negativty and neutrality amount 
# of the posts from datafrme df
def create_chart():
    #defining variables
    global pos
    global neg
    global neu
    #using boolean masking to create sub dataframes where
    # the inner condition matches to True
    positive = df[df["Sentiment"] == "Positive"]
    #finding positivity amount
    pos = positive.shape[0] / df.shape[0] * 100
    print("Positivity: ","{:.2f}".format(pos))
    negative = df[df["Sentiment"] == "Negative"]
    #finding negativity amount
    neg = negative.shape[0] / df.shape[0] * 100
    print("Negativity: ","{:.2f}".format(neg))
    neutral = df[df["Sentiment"] == "Neutral"]
    #finding neutrality amount
    neu = neutral.shape[0] / df.shape[0] * 100
    print("Neutrality: ","{:.2f}".format(neu))
    create_pie(pos, neg, neu)


#saving the dataframe obtained as a csv file in the specified path
def save_analysis():
   
    df.to_csv(path_or_buf=r"D:\News Sentiment\UserInterface\static\results\save.csv")
    #print("Analysis report saved as save.csv")


def preProcessing(s, listOfStopWords):
    # Removing hyperlinks
    flag = 0
    for i in range(0, len(s)):
        if s[i] == 'h':
            s1 = s[i:i + 4]
            if s1 == "http":
                for j in range(i + 4, len(s)):
                    if s[j] == ' ':
                        flag = 1
                        break
            if flag == 1:
                break
    if flag == 1:
        s = s[0:i] + s[j + 1:len(s)]
        
        
    # Removing Punctuation marks
    s1 = ""
    for i in range(0, len(s)):
        if s[i].isalpha() or s[i].isnumeric() or s[i] == ' ':
            s1 = s1 + s[i]
    s = s1
    # Removing the Stop words
    s1 = s.split(" ")
    s2 = ""
    for i in s1:
        i = i.lower()
        if i not in listOfStopWords:
            s2 = s2 + i + " "
    # removing emojis if any
    s2 = emoji.demojize(s2)
    s2 = s2.replace(":", "").replace("_", "")
    return s2


def get_sentiment(post_len):
    #creating an empty Pandas Series to store sentiment_val
    sentiment_val = pd.Series([])
    #the dumped vocubulary object which includes the vocabulary dictionary is loaded
    vocabulary = joblib.load(r"D:\News Sentiment\UserInterface\trained_dataset\vocabulary.pkl")
    #the dumped trained logistic regression model is loaded
    analysingObject = joblib.load(r"D:\News Sentiment\UserInterface\trained_dataset\sentiment.pkl")
    #imports the stopwords from the Natural Language Toolkit (nltk) library for English language
    listOfStopWords = stopwords.words("english")
    for i in range(post_len):
        #getting each_post in ith row of Posts column
        each_post = df._get_value(i, "Posts")
        #the post is then preprocessed by calling preprocessing function befor analysing each post
        each_post = preProcessing(each_post, listOfStopWords)
        #the preprocessed post is stored in datafrane
        df.at[i, "PreprocessedPosts"] = each_post
        #calling is_neutral function to check for amount of neutrality in post
        if is_neutral(each_post) == True:
            sentiment_val[i] = "Neutral"
        else:
            #using the trained logistic regression model to predict the sentiment of a given post
            #represented as a list of single element
            answer = analysingObject.predict(vocabulary.transform([each_post, ]))
            #[4] indicates positive
            #[0] indicates negative
            if answer == 4:
                sentiment_val[i] = "Positive"
            else:
                sentiment_val[i] = "Negative"
       # print((i+1),". ",each_post,"->",sentiment_val [i] ,"\n\n")
    return sentiment_val


#function to scrape tweets from Twitter
def twitter_config():
    #search query for twitter 
    query = s1 
    i = df.shape[0] - 1
    #number of posts to fetch from twitter
    limit = 2500
    c = 0
    #using the TwitterSearchScraper class of sntwitter library to scrape tweets
    #based on the specified query
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        i += 1
        c += 1
        if c < limit:
            #Posts column of ith row is updated with
            #the raw content of a tweet extracted from TwitterSearchScraper
            #print(tweet.rawContent)
            df.at[i, "Posts"] = tweet.rawContent 
            #the corresponding source in the dataframe updated to Twitter
            df.at[i, "Source"] = "Twitter"
        else:
            break
        
        
        
#function to store posts and apply analysis on the stored result in dataframe
def store_posts(posts):
    global df
     #crreating an empty dataframe
    df = pd.DataFrame()
    i = 0
    #creating an empty Pandas Series to store post_content
    post_content = pd.Series([]) 
    #creating an empty Pandas Series to store post_source
    post_source = pd.Series([])
    for post in posts:
        #getting post_content 
        post_content[i] = post.get_text()
        #storing post_source as reddit
        post_source[i] = "Reddit"
        i += 1
        
        
    #appending post_content series to dataframe
    df.insert(0, "Posts", post_content) 
    df.insert(1, "PreprocessedPosts", [None] * df.shape[0])
    #appending post_csource series to dataframe
    df.insert(2, "Source", post_source)
    #calling twitter_config to scrape twitter
    twitter_config()
    post_len = df.shape[0]
    #calling analysis function
    sentiment_val = get_sentiment(post_len)
    #appending returned sentiment_val series to the dataframe
    df.insert(3, "Sentiment", sentiment_val)
    #calling save_analysis
    save_analysis()
    

    #calling create_chart for visual representation
    create_chart()


def parse_html(soup, driver):
    #finding all the HTML tags that are "h3" and have the given class attribute 
    posts = soup.find_all("h3", class_="_eYtD2XCVieq6emjKBH3m") 
    driver.close()  # closing the automated Chrome Web driver
    store_posts(posts) 





 #search parameter passed to this function from main.py
def connect_service(search):
    global s1
    # removing whitespaces if any invloved
    search = search.replace(" ", "")  
    s1 = search
    #Using the Service class of selenium library to automate Chrome Web browser using chromedriver.exe
    s = Service(r"C:\Users\RAJDEEP\Desktop\RAJ\News Sentiment\UserInterface\chromedriver.exe")
    #the following method initializes a new Chrome browser window
    driver = webdriver.Chrome(service=s)
    #url to the required reddit search
    url = "https://www.reddit.com/search/?q=" + s1 + "&t=all"
    driver.get(url)#navigating to specified url
    delay = 0
    #providing auto-scroll for reddit page
    while delay < 250:
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        delay += 3
    #creating a soup object to extract specific elements and data from the parsed HTML code
    soup = BeautifulSoup(driver.page_source, "html.parser")
    parse_html(soup, driver)
