import pandas as pd
import warnings
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

# Read list of Events Page URLs
print('Reading list of APRA Chapters Events Page URLs...')
print('')
data = pd.read_excel(path, index_col=None)
data = data.fillna("")

# Loop through events
blob = ''
for index, row in data.iterrows():
    chapter_name = row['APRA Chapter']
    url = row['Events URL']
    
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
    except HTTPError as e:
        continue

    # Find Upcoming Events section of html
    upcoming = soup.find(id="idUpcomingEventsContainer")
    
    if upcoming:
        soup = upcoming

        # get all href links
        for a in soup.find_all('a', href=True):
            line_no = a.sourceline
            linktext = a.get('href')
            a.insert(line_no, ' ' + linktext)
                  
        # get text from events section
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Skip to next chapter if no upcoming events
        try:
            no_events = text.lower().index("no events available")
        except:
            no_events = None
        if no_events:
            continue

        # Remove past events 
        try:
            past_events = text.lower().index("past events")
        except:
            past_events = None
        if past_events:
            text = text[:past_events]

        # Append to text blob
        blob += chapter_name + '\n' + text + '\n\n'

# Print final text
print(blob)
print('')
print('Can you please try and parse out information on upcoming events from the text blob that will follow this prompt, so that I can insert the data into a SQL table? The columns I need will be "APRA Chapter", "Event Name", "Date", "Time", "Location", "Description" (if present), and "Link".')
