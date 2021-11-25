# Arvato Bertelsmann Customer Analysis
A UDACITY Data Science nano degree project


## Contents

- [Project Overview](#projectoverview)
- [Technical Overview](#technicaloverview)
- [Dependencies](#dependencies)
- [Instructions to run Web App](#InstructionstorunWebApp)



***

<a id='projectoverview'></a>

## 1. Project Overview

The aim of the project is to analyze demographics data for customers of a mail-order sales company in Germany, comparing it against demographics information for the general population.

The data for this project includes general population dataset, customer segment data set, dataset of mailout campaign with response and test dataset that needs to make predictions. The data is not publically available. It was provided by Udacity partners at Bertelsmann Arvato Analytics only to those participating in the Udacity nano degree program.

The solution approach includes the following 3 phases:
* Data pre-processing: clean and re-encode data.
* Segmentation: use unsupervised learning techniques to create clusterings of customer and general population, and then identify the difference.
* Prediction: use the demographic features to predict whether or not a person became a customer after a mailout campaign.

At the end a web app was developed to enable realtime prediction of possible customers based on the model generated.

## 2. Technical overview:

The following workflow was used to implement this project and covered in detail in the notebook: 

* Data Exploration & Cleansing
* Dimensionality Reduction
* Clustering
* Feature Importance
* Supervised Learning
* Model Evaluation and Selection



## 3. Dependencies

All the libraries used in this prject are included in the Anaconda distribution for Python versions 3.*


## 4. Data Files

This project is builds on real-life data captured by Arvato. There are 4 datasets and 2 CSV files describing some of the features:

Azdias.csv — Demographics data for the general population of Germany (891211 x 366).
Customers.csv — Demographics data for customers of the German mail-order company (191652 x 369).
Mailout_train.csv — Demographics data for individuals who were targets of a marketing campaign (42982 x 367).
Mailout_test.csv — Demographics data for individuals who were targets of a marketing campaign (42833 x 366).

## 5. Instructions to run Web App

The instructions on how to run the web app are captured in How_to_run_website.txt. 





