# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 15:14:54 2020

@author: Shayekh
"""

url = 'http://stats.espncricinfo.com/ci/engine/player/56194.html'
      '?class=3;template=results;type=allround;view=match'
      
from requests import get
response = get(url)
print(response.text[:500])

from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)


tables = html_soup.find_all('table')
caption = 'Match by match list'

data = tables[3].find('tbody').find_all('tr')
relevant_cols = [0, 6, 7, 8]
col_lables = ['runs', 'opposition', 'ground', 'date']
runs = []
opposition = []
ground = []
date = []

for rows in data:
    row = rows.find_all('td')
    runs.append(row[0].text.replace('*', ''))
    opposition.append(row[6].text[2:])
    ground.append(row[7].text)
    date.append(row[8].text)

date = [pd.to_datetime(a, format='%d-%m-%Y', infer_datetime_format=True) for a in date]
#from datetime import datetime
date = [a.strftime('%d-%m-%Y') for a in date]

import pandas as pd
df = pd.DataFrame({'date': date, 'runs': runs,\
                   'opposition': opposition, 'ground': ground})


df.to_csv('tamim_t20_jan_2020_stat_cricinfo.csv', \
          index=False, date_format='%d-%m-%Y')

