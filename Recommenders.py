# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:54:31 2020

@author: Bengi
"""
import numpy as np
import pandas
 

class popularity_recommender_py():
    def __init__(self):        
     self.train_data = None        
     self.user_id = None        
     self.item_id = None        
     self.popularity_recommendations = None            
    
    def create(self, train_data, user_id, item_id): #item_id  = song(title+artist)
        self.train_data = train_data
        self.user_id = user_id        
        self.item_id = item_id         
        
        
       
        train_data_grouped = train_data.groupby([self.item_id]).agg({self.user_id: 'count'}).reset_index()        
        train_data_grouped.rename(columns = {'user_id': 'score'},inplace=True)            
        #Sort the songs based upon recommendation score
        train_data_sort = train_data_grouped.sort_values(['score', self.item_id], ascending = [0,1])            
        #Generate a recommendation rank based upon score
        train_data_sort['Rank'] = train_data_sort['score'].rank(ascending=0, method='first')
        #Get the top 10 recommendations
        self.popularity_recommendations = train_data_sort.head(10)     
        #Use the popularity based recommender system model to    
        #make recommendations    
    def recommend(self, user_id):            
        user_recommendations = self.popularity_recommendations                 
        #Add user_id column for which the recommendations are being generated        
        user_recommendations['user_id'] = user_id           
        #Bring user_id column to the front        
        cols = user_recommendations.columns.tolist()        
        cols = cols[-1:] + cols[:-1]        
        user_recommendations = user_recommendations[cols]
        return user_recommendations
  
class item_similarity_recommender_py():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.cooccurence_matrix = None
        self.songs_dict = None
        self.rev_songs_dict = None
        self.item_similarity_recommendations = None
        
    #Get unique items (songs) corresponding to a given user
    def get_user_items(self, user):
        user_data = self.train_data[self.train_data[self.user_id] == user]
        user_items = list(user_data[self.item_id].unique())
        
        return user_items
        
    #Get unique users for a given item (song)
    def get_item_users(self, item):
        item_data = self.train_data[self.train_data[self.item_id] == item]
        item_users = set(item_data[self.user_id].unique())
            
        return item_users
        
    #Get unique items (songs) in the training data
    def get_all_items_train_data(self):
        all_items = list(self.train_data[self.item_id].unique())
            
        return all_items
        
   

    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

