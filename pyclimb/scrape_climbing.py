import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import time

# These are helper functions and do not need to be accessed
def findviews(soup):
    list = [thing.get_text().strip() for thing in soup.findAll('tr')]
    for i in list:
        if re.match('Page Views', i):
            return re.sub('\s+', ' ', i)
    
def findyear(soup):
    list = [thing.get_text().strip() for thing in soup.findAll('tr')]
    for i in list:
        if re.match('Shared By', i):
            return re.sub('\s+', ' ', i)


def scrape_mp(df, crawl_delay = 60, inplace = False):
    '''Function to scrape data from mountainproject.com
    
    Parameters
    ==========
    df : pandas dataframe
        This should be a dataframe with a column that includes URLs to specific
        climbs from mountainproject.com. This can be obtained by going to "route finder" on
        mountain project and exporting a csv file of the climbs you select

    crawl_delay : int
        This is the amount of delay between each time the scraper makes a request
        the default is 60 seconds because that that is what robots.txt on mountainproject.com 
        requires

    inplace : boolean
        Default is False, if set to True, the dataframe that is passed in will 
        be modified

    Notes
    =====
    This Function scrapes data from mountainproject.com, specifically, it creates 8
    different columns namely 'numVotes', 'numViews', 'Year', 'ViewsPerMonth', 
    'Shared_by', 'Month', 'Day', 'Date'

    Example
    =======

    >>> from pyclimb.clean_climbing import dataConcat
    >>> from pyclimb.scrape_climbing import scrape_mp

    >>> climbs = dataConcat(["route-finder_1.csv", "route-finder_2.csv"])
    >>> example = scrape_mp(climbs.iloc[:2], crawl_delay = 60)
    >>> example.info()

    '''

    if inplace == False:
        climbs = df.copy()
    else:
       climbs = df
    
    newcols = {
    "numVotes" : [],
    "numViews" : [],
    "Shared_by" : []
    }

    for i in range(climbs.shape[0]):
        time.sleep(crawl_delay)
        url = climbs.iloc[i]['URL']
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features = 'lxml')
        newcols["numVotes"].append(soup.find('span', {'id' : re.compile('starsWithAvgText')}).get_text().strip())
        newcols["numViews"].append(findviews(soup))
        newcols["Shared_by"].append(findyear(soup))

    newData = pd.DataFrame.from_dict(newcols)

    # cleaning the newData from the scraping
    newData["numVotes"] = newData.numVotes.str.extract("(\d+)\n")
    newData[["numViews", "ViewsPerMonth"]] = newData.numViews.str.replace(',', '').str.extract('(\d+) total.{3}(\d+)/month')
    newData[['Shared_by', 'Month', 'Day', 'Year']] = newData.Shared_by.str.extract('Shared By: (.+)on ([JFMASOND][a-z]{2}) (\d{1,2}), (\d{4})')
    newData[['numVotes', 'numViews', 'ViewsPerMonth', 'Day', 'Year']] = newData[['numVotes', 'numViews', 'ViewsPerMonth', 'Day', 'Year']].astype(int)

    # Fixing Shared_by to not include a space at the end
    newData.Shared_by = newData.Shared_by.str.strip()

    # Changing the months from 3 letters into numbers so that I can make a datetime variable
    month_dict = {
        'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'Jun' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9,
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
    }
    newData.Month.replace(month_dict, inplace = True)

    # Create a datetime variable called "Date" from Year, Month, and Day.
    newData['Date'] = pd.to_datetime(newData[['Year', 'Month', 'Day']])

    # Add all of the newData that we scraped to the original Data Frame.
    climbs[['numVotes', 'numViews', 'Year', 'ViewsPerMonth', 'Shared_by', 'Month', 'Day', 'Date']] = newData

    if inplace == False:
        return climbs
