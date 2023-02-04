import streamlit as st
import pandas as pd
import datetime
import snscrape.modules.twitter as sntweet
import pymongo
from pymongo import MongoClient
key_word=st.text_input("enter the text to search",input(''))
st.write("your search is: ",key_word)
num_tweets=st.number_input("How many tweets do you wish to see?",int(input()))
start_date=st.date_input("enter start date",datetime.date(2010,1,1))  #for some reason streamlit date_input was not woring in my system, hence has explicitly typed data
end_date=st.date_input("enter end date",datetime.date(2023,1,26))

tweet_list=[]
for tweet in sntweet.TwitterSearchScraper(key_word).get_items():
    if(len(tweet_list)>num_tweets):
        break
    else:
        if(tweet.date.date()<end_date and tweet.date.date()>start_date):
            tweet_list.append([tweet.date,tweet.id,tweet.url,tweet.content,tweet.user.username,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount])  

tdf=pd.DataFrame(tweet_list, columns=['date','ID','URL','Content','Username','Replies','Retweet','Language','Source','Likes'])


client=MongoClient()
db=client['d5556']
mycollection =db['twitter_data']
x=mycollection.insert_one(tdf.to_dict())

def convert_df_csv(df):
    return df.to_csv()
csv=convert_df_csv(tdf)
def convert_df_json(df):
    return df.to_json()
json=convert_df_json(tdf)

st.download_button(label="Download data as csv",data=csv,file_name='scraper.csv')
st.download_button(label="Download data as Json",data=json,file_name='scraper.json')

if __name__ == '__main__':
    main()
