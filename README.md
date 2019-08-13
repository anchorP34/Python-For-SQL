# Python-For-SQL
Python scripts to make database management easier

# DynamicTableCreations

Ever have a bunch of small CSV or Excel files that you need to upload into the database? This process will look at all of the CSV files in the working directory (easily can be changed to look for .xlsx files), reads in the table, and prints out a full SQL script that creates the tables and the insert statements. 

The sample CSV files are from the 2019 NCAA Basketball Tournament dataset from Kaggle: https://www.kaggle.com/c/mens-machine-learning-competition-2019

The python script to run is DataTableCreations. It takes in no parameters. It only needs to be in the working directory of the files of interest, and you can make small tweaks to make sure it will only pull in the correct files. All columns are made as NVARCHAR(255), so those columns can be configured to whatever correct data type before the script should be run in the databse.

# Interval Case Statement Function.py

If you have a need to know whether a value is between 0-10, 50-100, or whatever the interval space is, this function creates case statements for a lower and upper bound of equal intervals.
