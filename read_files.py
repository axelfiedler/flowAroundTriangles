# -*- coding: utf-8 -*-

from os import listdir
import pandas as pd
import numpy as np
import re

# Get all file names from results folder
file_list = listdir("simple_laminar/C_D/")

# Initialize lists to store data
all_data = []
mean_cd_200 = []
mean_cd_400 = []
mean_cd_600 = []
x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []
Re = []

# Loop through list of files and get parameter values from file name
for i,file in enumerate(file_list):
    # Load drag coefficient data
    file_data = pd.read_csv("simple_laminar/C_D/"+file,skiprows=8,sep="\t")
    file_data.columns = file_data.columns.str.strip()
    all_data.append(file_data)
    # Append x,y and drag coefficient data to lists
    Re = int(re.search(r'Re-(\d+)',file).group(1))
    if Re == 200:
        x1.append(int(re.search(r'x1-(\d+)',file).group(1)))
        y1.append(int(re.search(r'y1-(\d+)',file).group(1)))
        x2.append(int(re.search(r'x2-(\d+)',file).group(1)))
        y2.append(int(re.search(r'y2-(\d+)',file).group(1)))
        x3.append(int(re.search(r'x3-(\d+)',file).group(1)))
        y3.append(int(re.search(r'y3-(\d+)',file).group(1)))
        mean_cd_200.append(np.mean(file_data["Cd"]))
    if Re == 400:
        mean_cd_400.append(np.mean(file_data["Cd"]))
    if Re == 600:
        mean_cd_600.append(np.mean(file_data["Cd"]))
# Create a DataFrame with all x1,y1,x2,y2,x3,y3,mean_cd_200,mean_cd_400 and mean_cd_600 as columns
# that can be used to train the NN model
df = pd.DataFrame(data={"x1":x1,"y1":y1,"x2":x2,"y2":y2,"x3":x3,"y3":y3,"mean Cd 200":mean_cd_200,"mean Cd 400":mean_cd_400,"mean Cd 600":mean_cd_600})
df.to_csv("tmp/df.csv")

# Not used right now
# df["x1Re"] = (df["x1"]-np.mean(df["x1"]))*(df["Re"]-np.mean(df["Re"]))
# df["y1Re"] = (df["y1"]-np.mean(df["y1"]))*(df["Re"]-np.mean(df["Re"]))
# df["x2Re"] = (df["x2"]-np.mean(df["x2"]))*(df["Re"]-np.mean(df["Re"]))
# df["y2Re"] = (df["y2"]-np.mean(df["y2"]))*(df["Re"]-np.mean(df["Re"]))
# df["x3Re"] = (df["x3"]-np.mean(df["x3"]))*(df["Re"]-np.mean(df["Re"]))
# df["y3Re"] = (df["y3"]-np.mean(df["y3"]))*(df["Re"]-np.mean(df["Re"]))
