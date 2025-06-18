from urllib.request import urlopen
from bs4 import BeautifulSoup
import pyodbc
from time import sleep

# Connect to database and open SQL cursor
print('Connecting to database...')
print('')
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Query URLs from database
print('Querying URLs...')
print('')
cursor.execute("""
SELECT DISTINCT 
CAST(LC.[URL] AS varchar(max)) 
FROM [APRA-IL].[dbo].[LinkClicks] LC WITH (NOLOCK)
LEFT OUTER JOIN dbo.URLPageTitles U WITH (NOLOCK) ON CAST(LC.[URL] AS varchar(max)) = CAST(U.[URL] AS varchar(max)) 

WHERE
U.URL IS NULL""")
URLs = cursor.fetchall()

# Loop through URLs, get page title and insert into table
print('Getting page titles, inserting into database...')
print('')
for url in URLs:
    URL = url[0]
    
    try:
        title = BeautifulSoup(urlopen(URL),features='html.parser').title.get_text()
    except Exception as e:
        print('Title not found: ' + URL)
        title = ''
        
    cursor.execute("""INSERT INTO [dbo].[URLPageTitles] ([URL],[Page Name]) VALUES (?,?)""", (URL, title))
    cursor.commit()
    sleep(1)

print('All rows inserted')
