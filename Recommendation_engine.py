# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:03:47 2019

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 13:42:51 2019

@author: Administrator
"""
from flask import Flask, jsonify,request,render_template,redirect, url_for
import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('revised_measurements.csv')#, sep='\t', names=['user_id','item_id','rating','titmestamp'])

app=Flask(__name__)

@app.route('/body_shape/<string:height>/<float:waist>/<string:bust>',methods=['POST','GET'])
def body_shape(height,waist,bust):
    #df = pd.read_csv('new.csv')#, sep='\t', names=['user_id','item_id','rating','titmestamp'])
    df = pd.read_csv('revised_measurements.csv')#, sep='\t', names=['user_id','item_id','rating','titmestamp'])
#    height='5\' 5"'
#    waist=29.0
#    bust='34b'
    
    height=height
    waist=waist
    bust=bust
    
    h=list(df[df['height']==height]['height'].unique())
    if(len(h)!=0):
        h=h[0]
        w=list(df[df['waist']==waist]['waist'].unique())
        if(len(w)!=0):
            w=w[0]
            b=list(df[df['bust size']==bust]['bust size'].unique())
            if(len(b)!=0):
                b=b[0]
                pass
            else:
                b='34b'        
        else:
            w=32.0
            b=list(df[df['bust size']==bust]['bust size'].unique())
            if(len(b)!=0):
                b=b[0]
                pass
            else:
                b='34b'
    else:
        h='5\' 6"'
        w=list(df[df['waist']==waist]['waist'].unique())
        if(len(w)!=0):
            w=w[0]
            b=list(df[df['bust size']==bust]['bust size'].unique())
            if(len(b)!=0):
                pass
            else:
                b='34b'
                
        else:
            #print(h)
            w=32.0
            b=list(df[df['bust size']==bust]['bust size'].unique())
            if(len(b)!=0):
                b=b[0]
                pass
            else:
                b='34b'
    try:
        body_shape=df[ (df['height']==h) & (df['bust size']==b) & (df['waist']==w) ]['body type'].unique()[0]
    except IndexError:
        body_shape="hourglass"    
    
    
    a=df['waist']==w
    a.any()
    
    a=df[df['bust size']==bust]['bust size'].nunique()
    #return body_shape
    return jsonify({'body_shape':body_shape})

@app.route('/dress_sugg/<string:body_shape>',methods=['POST','GET'])
def dress_suggestion(body_shape):
    dress=df[df['body type']==body_shape]['category'].unique()
    #dress=pd.DataFrame(dress)
    a=df.groupby('category')['rating'].describe()
    #Gives the threshold for the number of reviewers
    a=a[a['count']>5]
    a=(a.index.values)
    #a=pd.DataFrame(a)
    shortlisted_dress=set(a)-(set(a)-set(dress))
    #return list(shortlisted_dress)
    return jsonify({'recommendation':list(shortlisted_dress)})
    
#@app.route('/dress_sugg/<string:body_shape>',methods=['POST'])
def dress_suggestions(body_shape):
    dress=df[df['body type']==body_shape]['category'].unique()
    #dress=pd.DataFrame(dress)
    a=df.groupby('category')['rating'].describe()
    #Gives the threshold for the number of reviewers
    a=a[a['count']>5]
    a=(a.index.values)
    #a=pd.DataFrame(a)
    shortlisted_dress=set(a)-(set(a)-set(dress))
    return list(shortlisted_dress)
    #return jsonify({'recommendation':list(shortlisted_dress)})

@app.route('/cust_sugg/<string:colour>/<string:occasion>/<string:body_shape>',methods=['POST','GET'])
def custom_suggestion(colour,occasion,body_shape):
    body_shape=body_shape
    occasion=occasion
    occasion_dress=list(df[(df['body type']==body_shape) & (df['rented for']==occasion)]['category'].unique())
    j=dress_suggestions(body_shape)
    custom_dress=set(occasion_dress)-(set(occasion_dress)-set(j))
    #return list(custom_dress)
    f=list(custom_dress)
    return jsonify({'custom_recommendation':f})
    

@app.route('/rel_sugg/<string:dress>',methods=['POST','GET'])
def relative_suggestion(dress):
    shape_dress_ratings = df.pivot_table(index='body type', columns='category', values='rating')
    shape_dress_ratings.head()
    dress=dress
    dress_rating= shape_dress_ratings[dress]
    similar_to_dress=shape_dress_ratings.corrwith(dress_rating)
    similar_to_dress.head()
    corr_dress = pd.DataFrame(similar_to_dress, columns=['Correlation'])
    corr_dress.dropna(inplace=True)
    corr_dress.head()
    ratings = pd.DataFrame(df.groupby('category')['rating'].mean())
    ratings['number_of_ratings'] = df.groupby('category')['rating'].count()
    measurement_matrix = df.pivot_table(index='user_id', columns='category', values='rating')
    measurement_matrix.head()
    ratings.sort_values('number_of_ratings', ascending=False).head(10)
    corr_dress = corr_dress.join(ratings['number_of_ratings'])
    #corr_dress[corr_dress['number_of_ratings'] > 100].sort_values(by='Correlation', ascending=False).head(10)
    c=corr_dress[corr_dress['number_of_ratings'] > 100].sort_values(by='Correlation', ascending=False).head(5)
    d=list(c.index)
    return jsonify({'relative_recommendation':d})

#d=list(c.index)
app.run(debug=False,port=5000)

#a=body_shape('5\' 5"',29.0,'34b')
#b=dress_suggestions('hourglass')
#c=custom_suggestion('red','wedding','hourglass')
#d=relative_suggestion('maxi')