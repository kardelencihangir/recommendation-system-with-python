# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:16:47 2020

@author: Bengi
"""

import pandas as pandas
import numpy as np
import matplotlib.pyplot as plt
import sqlite3


#def recsystem(completion):
con = sqlite3.connect("db.sqlite")

song_df_1 = pandas.read_sql_query("SELECT * from triplets_file ;" ,con)
song_df_2 = pandas.read_sql_query("SELECT * from songs_metadata_file ;" ,con)
con.close()


song_df = pandas.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")

song_df['song'] = song_df['title'].map(str) + " - " + song_df['artist_name']
song_grouped = song_df.groupby(['song']).agg({'listen_count': 'count'}).reset_index()
grouped_sum = song_grouped['listen_count'].sum()

song_grouped['percentage']  = song_grouped['listen_count'].div(grouped_sum)*100

song_grouped.sort_values(['listen_count', 'song'], ascending = [0,1])

users = song_df['user_id'].unique()
len(users) ## return unique users 
songs = song_df['song'].unique()
len(songs) ## return  unique songs

from sklearn.model_selection import train_test_split

train_data, test_data = train_test_split(song_df, test_size = 0.20, random_state=0)

import Recommenders as Recommenders

pm = Recommenders.popularity_recommender_py()
pm.create(train_data, 'user_id', 'song')
#user the popularity model to make some prediction
user_id = users[6]
pm.recommend(user_id)



is_model = Recommenders.item_similarity_recommender_py()
is_model.create(train_data, 'user_id', 'song')



user_id = users[6]
user_items = is_model.get_user_items(user_id)

print(user_items)

#○gelenlerden bir dataset oluşturabilrsin  bunu birleştirip sonra knnn fit yapabilrisin

import pickle
with open('model.pkl','wb') as file:
    pickle.dump(user_items, file)

with open('model_columns.pkl','wb') as file:
    pickle.dump(user_id,file)    
 


