from twarc import Twarc

consumer_key = "Please enter your own twitter developer information"
consumer_secret = "Please enter your own twitter developer information"
access_key = "Please enter your own twitter developer information"
access_secret = "Please enter your own twitter developer information"

t = Twarc(consumer_key, consumer_secret, access_key, access_secret)

from zipfile import ZipFile
import os
import pandas as pd

import csv

count = 0

filenames = input("Enter filenames in format 'file:file:file' to process multiple files, or just 'file' to process one:")
is_folder = input("Is this in a zip file or folder?")
filenames = filenames.split(":")

if is_folder:
  # Processes a folder of zip files
  for folder in filenames:
    for file in os.listdir(folder):
      print(f"Reading filename {file}")
      if file.endswith(".zip"):
        with ZipFile(os.path.join(folder, file)) as zf:
          for zip_file in zf.namelist():
            print(f"Processing {zip_file}")
            temp_name = os.path.join("temp", f"{os.path.basename(zip_file)[:-4]}.csv")

            if "__MACOSX" not in zip_file and zip_file.endswith(".csv"):
              print(f"At {temp_name}")
              count += 1
              if not os.path.exists(temp_name):
                with zf.open(zip_file) as z:
                  data = pd.read_csv(z, encoding="utf-8",sep=",", names=['id', 'score'])
                  data = data['id'].sample(n=13800, random_state=1)              
                  data.to_csv(temp_name,index=False, header=False)  

                name = os.path.join("hydrated",f"{os.path.basename(folder)[:-4]}_{count//20}_sampled.csv")
                print(f"Writing to {name}")
                with open(name, 'a+', encoding="utf-8", newline="") as f:  
                  for tweet in t.hydrate(open(temp_name)):
                    fields = [tweet['created_at'], tweet['full_text'], tweet['user']['followers_count'], tweet['user']['location'], tweet['retweet_count'], tweet['favorite_count'], tweet['entities']['hashtags']]
                    writer = csv.writer(f)
                    writer.writerow(fields)

                print("Done hydrating!")
            else:
              print(f"{zip_file} already done...")

else:
  # Processes a zip file of either csvs or zip files
  for filename in filenames:
    count = 0
    print(f"Reading filename {filename}")
    if filename.endswith(".zip"):
      with ZipFile(filename) as zf:
        for zip_file in zf.namelist():
          print(f"Processing {zip_file}")
          temp_name = os.path.join("temp", f"{os.path.basename(zip_file)[:-4]}.csv")
          if "__MACOSX" not in zip_file:
            print(f"At {temp_name}")
            count += 1
            if not os.path.exists(temp_name):
                with zf.open(zip_file) as z:
                  if zip_file.endswith(".zip"):
                    try:
                      data = pd.read_csv(z, compression="zip",sep=",", names=['id', 'score'])
                      data = data['id'].sample(n=13800, random_state=1)              
                      data.to_csv(temp_name,index=False, header=False)  
                    except ValueError: 
                      print(f"{zip_file} has multiple files in it, not read...")
                    else:
                      data = pd.read_csv(z, encoding="utf-8",sep=",", names=['id', 'score'])
                      data = data['id'].sample(n=13800, random_state=1)              
                      data.to_csv(temp_name,index=False, header=False)  

                  name = os.path.join("hydrated",f"{os.path.basename(filename)[:-4]}_{count//20}_sampled.csv")
                  print(f"Writing to {name}")
                  with open(name, 'a+', encoding="utf-8", newline="") as f:  
                    for tweet in t.hydrate(open(temp_name)):
                      fields = [tweet['created_at'], tweet['full_text'], tweet['user']['followers_count'], tweet['user']['location'], tweet['retweet_count'], tweet['favorite_count'], tweet['entities']['hashtags']]
                      writer = csv.writer(f)
                      writer.writerow(fields)

                  print("Done hydrating!")
            else:
              print(f"{zip_file} already hydrated...")


