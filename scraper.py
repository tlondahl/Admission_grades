import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


url = 'https://www.studera.nu/jamfor-utbildning/?asp=Stockholms+universitet&ast=Juristprogrammet&q=&f=1%5bS384*2%5bsu*4%5bp&e=i.uoh.su.jjupg.29513.20211'
page = urllib.request.urlopen(url).read()
soup = BeautifulSoup(page, 'lxml')

dfs = pd.read_html(url)
df = dfs[0]
df.drop([0, 1, 2, 4, 6, 7, 8], axis=0, inplace=True)
df = df.transpose()
df = df[1:]
df.reset_index(inplace=True)
df.rename({'index': 'term', 3:'Alt1', 5:'Alt2'}, inplace=True, axis=1)

# Clean and create two columns with only floats
df[['term', 'Alt1', 'Alt2']].apply(str)
df['BI'] = df['Alt1'].str[-5:]
df['BII'] = df['Alt2'].str[-5:]
df[['BI', 'BII']] = df[['BI', 'BII']].apply(pd.to_numeric)

# Export to csv
school = url.split('=',2)[1].split('&')[0] #Extracting the name of the university from the URL
program = url.split('=',2)[2].split('&')[0] #Extracting the name of the program from the URL
df.to_csv(school+'_'+program+'.csv')

# Clean the "term" column and create a datetime column
df['term'] = df['term'].str[-6:]
df['termin'] = df.term.str[:2]
df['year'] = df.term.str[-4:]
df['month'] = df.term.apply(lambda x: 8 if 'HT' in x else 1)
df['day'] = df.term.apply(lambda x: 31 if 'HT' in x else 18)
df['term_start'] = pd.to_datetime(df[['year', 'month','day']])

# A plot of the lowest admission grade per semester
#plot = sns.relplot(x='term_start', y='BI', data=df, hue='termin', kind='line')
#plot.fig.autofmt_xdate()
#plt.show()






