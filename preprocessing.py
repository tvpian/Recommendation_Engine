# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 00:44:27 2019

@author: IMGADMIN
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

dataset=pd.read_csv("revised_measurements_new.csv")
dataset.drop_duplicates()


dataset_final=dataset.copy()



sns.heatmap(dataset.isnull(),yticklabels=False,cbar=False,cmap='viridis')


def impute_age(cols):
    Age = cols[0]
    Pclass = cols[1]
    
    if pd.isnull(Age):

        if Pclass == a[0][0]:
            return a[0][1]

        elif Pclass == a[1][0]:
            return a[1][1]
        
        elif Pclass == a[2][0]:
            return a[2][1]
        
        elif Pclass == a[3][0]:
            return a[3][1]
        
        elif Pclass == a[4][0]:
            return a[4][1]
        
        elif Pclass == a[5][0]:
            return a[5][1]
        
        else:
            return a[6][1]

    else:
        return Age
    
    
dataset['weight']=dataset['weight'].apply(lambda x: str(x).split("l")[0])

a=dataset.groupby('body type').median()['bra size'].reset_index()
a=np.array(a)  
    
#train['Age']
b = dataset[['bra size','body type']].apply(impute_age,axis=1)
dataset['bra size']=b


#pd.isnull(dataset['weight'][3])


dataset.dropna(inplace=True)

dataset.to_csv("preprocessed_dataset.csv")


data= dataset.drop_duplicates(subset='user_id', keep="first")

data.drop(['user_id','item_id','rating','review_text','review_summary','review_date','user_name'],axis=1,inplace=True)
data.drop(['bust','cup size'],axis=1,inplace=True)



bust_size = pd.get_dummies(data['bust size'],drop_first=True)
rented_for = pd.get_dummies(data['rented for'],drop_first=True)
category = pd.get_dummies(data['category'],drop_first=True)
length = pd.get_dummies(data['length'],drop_first=True)
fit = pd.get_dummies(data['fit'],drop_first=True)


data.drop(['bust size','rented for','category','length','fit'],axis=1,inplace=True)
data = pd.concat([data,bust_size,rented_for,category,length,fit],axis=1)


data.to_csv("preprocessed_dataset.csv")
