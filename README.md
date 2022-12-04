# Description
For CS 4260: Artificial Intelligence at Vanderbilt University.

This GitHub repository contains code on performing sentiment analysis on tweets concerning the COVID-19 Vaccine. The original dataset can be accessed as a CSV of tweet IDs if you have an IEEE Member account [here](https://ieee-dataport.org/open-access/coronavirus-covid-19-tweets-dataset) containing a large set of tweets related to the pandemic overall, which we filter out for vaccine related keywords. Using this dataset, we hydrate the tweets using the Twitter API.

# Hydrating Tweets
To hydrate tweets, run ```python hydratetweets.py``` in the same folder as the CSVs or zip file. You can either process a folder of zip files containing CSV files or a zip file of CSV files, which are the possible formats provided by the dataset. 

Please note that to accommodate for the Twitter API rate limits, it will read up to 13.8k lines of the CSV. If the CSV is larger, it will take a random sample of tweet IDs to hydrate. 

# Sentiment Analysis