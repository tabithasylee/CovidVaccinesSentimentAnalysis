# Description
For CS 4260: Artificial Intelligence at Vanderbilt University.

This GitHub repository contains code on performing sentiment analysis on tweets concerning the COVID-19 Vaccine. The original dataset can be accessed as a CSV of tweet IDs if you have an IEEE Member account [here](https://ieee-dataport.org/open-access/coronavirus-covid-19-tweets-dataset) containing a large set of tweets related to the pandemic overall, which we filter out for vaccine related keywords. Using this dataset, we hydrate the tweets using the Twitter API.

# Hydrating Tweets
To hydrate tweets, run ```python hydratetweets.py``` in the same folder as the CSVs or zip file. You can either process a folder of zip files containing CSV files or a zip file of CSV files, which are the possible formats provided by the dataset. 

Please note that to accommodate for the Twitter API rate limits, it will read up to 13.8k lines of the CSV. If the CSV is larger, it will take a random sample of tweet IDs to hydrate. The hydrating tweets function also splits files up due to the size of the dataset. For your convenience, you can combine those files by running ```python combinetweets.py``` so that they can use utilized in the next steps.

# Sentiment Analysis
In order to run the sentiment analysis, ensure you have the properly hydrated tweets and that the files are named accordingly as they are in the notebook. Then simply run through the cells in ```sentiment_analysis.ipynb```.

To train the neural network, run the ```sentiment_analysis_nn.ipynb``` notebook. We've provided our dataset of filtered COVID-19 vaccine tweets and their according sentiments in ```covidvaccinesentiments.csv```, which we obtained by following the steps above for tweet hydration and sentiment analysis. 

# Demo
To run the demo, we have provided you with a pretrained model of our sentiment analysis in ```model/sentiments_model.hdf5```. Simply run ```python demo.py``` after having installed the necessary prerequisites (keras, twarc, nltk, and PySimpleGUI).