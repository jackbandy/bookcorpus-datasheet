#%%
import pandas as pd
import numpy as np

#%%
# Load the File
df21 = pd.read_csv('data/Smashwords21/smashwords_april_2021.csv')
# %%
# check total rows vs. total UNIQUE links (expect some duplicates)
len(df21), len(df21.Link.unique())

#%%
# drop duplicates
df21 = df21.drop_duplicates('Link')
#%%
# Glance at high and low prices
df21.Price.value_counts()

#%%
# parser function to turn the "Words" column into an integer
def my_parse(x):
    try:
        return int(x.replace(',', ''))
    except:
        try:
            return int(x)
        except ValueError:
            return 0
#%%
df21['cleaned_words'] = df21.Words.fillna(0).apply(my_parse)

#%% 
# we only want free books
filt = df21[df21.Price == "$0.00 USD"]
filt

#%%
# get the number of words per author
words = filt.groupby('Author').cleaned_words.sum()

#%%
# get the number of books per author
c = filt.Author.value_counts()
c

#%%
words

#%%
words.sum()

#%%
authors = sorted(list(set(words.index)))

#%%
# how many authors and how many books?
len(authors), len(filt)

#%%
# based on a consistent author:book ratio, how many should we
# expect based on 7815 books in original BookCorpus
print('books ratio, est')
authors_to_books =  len(authors) / len(filt)
authors_to_books, authors_to_books * 7815

#%%
print('words ratio')
authors_to_words =  len(authors) / words.sum()
authors_to_words
#%%
# uncomment in a notebook to look use systematic sampling
# to look at some examples
# authors[0:100]
# authors[1000:1100]
# authors[10000:10100]
#%%
words.describe()
# %%
c.describe()
#%%
np.isinf(words).sum()

#%%
# "share" of the top 10 authors by book count
c[c > c.quantile(0.90)].sum() / c.sum()


#%%
# # "share" of the top 10 authors by word count
words[words > words.quantile(0.90)].sum() / words.sum()
# %%
# Uncomment below for power law explorations
#import powerlaw

# #%%
# powerlaw.plot_pdf(c, color='b')
# # %%
# results = powerlaw.Fit(words)
# # %%
# print(results.power_law.alpha)
# print(results.power_law.xmin)
# # %%
# results.distribution_compare('power_law', 'exponential')

# # %%
# results.distribution_compare('power_law', 'lognormal')

# %%
