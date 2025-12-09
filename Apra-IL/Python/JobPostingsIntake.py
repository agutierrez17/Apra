import pandas as pd
import pyodbc
import warnings
import requests

warnings.filterwarnings("ignore")

# Connect to database and open SQL cursor
print('Connecting to database...')
print('')
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Truncate JobPostings table
cursor.execute("""TRUNCATE TABLE [dbo].[JobPostings]""")
cursor.commit()

# Read JobListings excel data into dataframe
print('Refreshing database table...')
print('')
data = pd.read_excel(path, index_col=None)
data = data.fillna("")

# Checking links to see if jobs are still active
print('Checking job URLs...')
print('')
for job in data.values.tolist():
    url = job[6]
    jobtitle = job[1]
    active = ''
    
    try:
        r = requests.get(url)
        if r.history:
           active = 'N'
           #print(jobtitle)
        elif r.text.find(jobtitle) < 0 and r.text.find(jobtitle.replace('&','&amp;')) < 0:
            active = 'N'
            #print(r.text)
            #print(jobtitle)
        else:
            active = 'Y'
    except Exception as e:
        active = 'Y'

    active = job[7] if job[7] == 'Y' or job[7] == 'N' else active
    data.loc[data['Link'] == url, 'Active'] = active

# Insert data into JobPostings table
cursor.executemany("""INSERT INTO [dbo].[JobPostings] ([Organization],[Job Title],[Location],[Salary Range],[Category],[Date Posted],[Link],[Active]) VALUES (?,?,?,?,?,?,?,?)""", data.values.tolist())
cursor.commit()

print('All jobs inserted.')
print('')

cursor.close()
