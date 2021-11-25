# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 22:48:28 2021

@author: Peter.Evah
"""

import numpy as np
from flask import Flask, request, render_template, send_file
import pickle
from werkzeug.utils import secure_filename


import pandas as pd
from sklearn.impute import SimpleImputer
Imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
from scipy import stats
from sklearn.preprocessing import  StandardScaler #,OneHotEncoder


app = Flask(__name__)

vocab_model = pickle.load(open('vocab-uauc_model.pkl', 'rb'))
url = 'http://localhost:5001/'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    output= None; csv_output= None; f= None; download_text=None; disp=None;
    
    if request.method == 'POST':
        
        # Process csv
        
        if request.files['file'] :
            f = request.files['file']
            f.save(secure_filename(f.filename))
            csv_output, output = classify_csv(f.filename)
            download_text = "Click here to download"
            disp = 'Find below the first 5 rows of predicted result:'
        

    return render_template('index.html', prediction_text=output, shape=csv_output, download=download_text, disp=disp)
    


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    return render_template('index.html', shape='File not yet processed')

def clean_data(df, cluster, dataset=None):
    
    if cluster:
        if dataset == 'azdias':
            df = df[df.isnull().sum(axis=1) <= 16].reset_index(drop=True)
        
        
    
    cols_drop = ['ALTER_KIND1', 'ALTER_KIND2', 'ALTER_KIND3', 'ALTER_KIND4', 'EXTSEL992', 'KK_KUNDENTYP']
    
    df = df.drop(cols_drop,axis=1)
    df = df.drop(['EINGEFUEGT_AM'],axis=1)
    df = df.drop(['D19_LETZTER_KAUF_BRANCHE'],axis=1)


       
    cor_mat = df.corr().abs()
    upper_lim = cor_mat.where(np.triu(np.ones(cor_mat.shape), k=1).astype(np.bool))
    
    drop_cols = [column for column in upper_lim.columns if any(upper_lim[column] > .7)]
    
    df = df.drop(drop_cols, axis=1)
    print('after correlation', df.shape)


    
    df[['CAMEO_DEUG_2015','CAMEO_INTL_2015']] = df[['CAMEO_DEUG_2015','CAMEO_INTL_2015']].replace(['X','XX'],-1)
    df[['CAMEO_DEUG_2015','CAMEO_INTL_2015']] = df[['CAMEO_DEUG_2015','CAMEO_INTL_2015']].fillna(-1)
    df[['CAMEO_DEUG_2015','CAMEO_INTL_2015']] = df[['CAMEO_DEUG_2015','CAMEO_INTL_2015']].astype(int)
    df[['CAMEO_DEU_2015','OST_WEST_KZ']]=df[['CAMEO_DEU_2015','OST_WEST_KZ']].fillna(-1)



    # fillna with 9 for fields that has 9 marked as unknown
    df[df.columns[(df==9).any()]] = df[df.columns[(df==9).any()]].fillna(9)

    # fillna with 0 for fields that has 0 marked as unknown
    df[df.columns[(df==0).any()]] = df[df.columns[(df==0).any()]].fillna(0)

    # fillna with -1 for fields that has 0 marked as unknown
    df[df.columns[(df==-1).any()]] = df[df.columns[(df==-1).any()]].fillna(-1)


    
    df = pd.get_dummies(df)
    print('after encoding', df.shape)
    
    df_columns = list(df.columns.values)

    gen_imputer = Imputer
    df = gen_imputer.fit_transform(df)
    df = pd.DataFrame(df)
    print('after impute', df.shape)
    
    df = df.astype(int)


    if cluster:
        df = df[(np.abs(stats.zscore(df)) < 6).all(axis=1)] 
        print('before scaling', df.shape)
    
    scaler = StandardScaler(copy=False)
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled,columns= df_columns)
    print('after scaling', df.shape)
    
    df = df.set_index('LNR')
    return df

def pred_result(model, test, lnr):
    predictions = model.predict_proba(test)
    res = pd.DataFrame({'LNR':lnr, 'RESPONSE':predictions[:,0]})
    return res

def classify_csv(file_name):
    
    model = pickle.load(open('ada_model.pkl', 'rb')) 
    mailout_test = pd.read_csv(file_name, sep=';')
    lnr = mailout_test.LNR
    
    
    mailout_test_processed  = clean_data(mailout_test, False)
    
    res = pred_result(model, mailout_test_processed, lnr)
    res.to_csv('output_data.csv', index=False)
    
    
           
    return file_name + ' file processed successfully! ', [res.head().to_html(classes='data', header="true")]
    

@app.route('/download')
def download_file():
	
	path = 'output_data.csv'
	
	return send_file(path, as_attachment=True)


    

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="localhost", port=5001, debug=True)