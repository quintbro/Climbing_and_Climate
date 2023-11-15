import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import time

climbs = pd.read_csv('new_utah_climbs.csv')

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

newcols = {
    "numVotes" : [],
    "numViews" : [],
    "Shared_by" : []
}

for i in range(climbs.shape[0]):
    time.sleep(60)
    url = climbs.iloc[i]['URL']
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features = 'lxml')
    newcols["numVotes"].append(soup.find('span', {'id' : re.compile('starsWithAvgText')}).get_text().strip())
    newcols["numViews"].append(findviews(soup))
    newcols["Shared_by"].append(findyear(soup))
    if i % 60 == 0:
      print('So far I have completed', i, 'number of rows! Only', climbs.shape[0] - i, "left to go")



newData = pd.DataFrame.from_dict(newcols)

climbs[['numVotes', 'numViews', 'Year']] = newData

climbs.to_csv('climbs.csv', index = False)