import os
import glob
import pandas as pd

name = input("Enter file to combine:")
csv_files = glob.glob(f"*{name}*")
print(csv_files)

df_append = pd.DataFrame()#append all files together
for file in csv_files:
    print(f"File processing: {file}")
    df_temp = pd.read_csv(file, names=["created_at", "full_text", "user_followers", "user_location", "retweets", "favorites", "hashtags"])
    print(df_append.shape)
    print(df_temp.shape)
    df_append = pd.concat([df_append, df_temp], ignore_index=True)
              
df_append.to_csv(f"{name}.csv",index=False, header=False) 