# Bring in your imports
import pandas as pd
import os

# Get the list of Excel files in the directory
files = [f for f in os.listdir() if f.endswith('.csv')]

# Load in each file
for f in files:
    
    df = pd.read_csv(f)

    # Get the columns of the table and clean up the naming of the table
    table_columns = df.columns
    table_name = f.replace('.csv','')

    # Create the SQL to create the table
    print('DROP TABLE IF EXISTS dbo.{}'.format(table_name))
    print('GO\n')
    print('CREATE TABLE dbo.{}'.format(table_name))
    print('(')
    for col_idx, col in enumerate(table_columns):
        if col_idx == 0:
            print('\t[{}] NVARCHAR(255)'.format(col))
        else:
            print('\t, [{}] NVARCHAR(255)'.format(col))
    print(')')


    # Create the insert statements 

    # get all of the values of each record in NVARCHAR format

    for i in range(len(df)):
        vals = df.iloc[i, :].values

        val_inserts = "'" + "', '".join(str(val) for val in vals) + "'"

        insert_statement = 'INSERT INTO dbo.{} VALUES ({})'.format(table_name, val_inserts)

        print(insert_statement)

    print('\n\n')
    


