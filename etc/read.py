from collections import Counter
import re
import string
import os
import csv
import copy
import functools
import operator
import nltk
import numpy as np
import pandas as pd
# nltk.download('stopwords')
from nltk.corpus import stopwords

########################
# 1. IMPORT DATA
########################
# set directory
# directory = '/afs/crc.nd.edu/user/c/cdaviso1/educ_innovation/data/processed/comp_schooling/tls202/'
directory = 'C:\\Users\\Owner\\OneDrive - nd.edu\\educ_innovation\\data\\raw\\comp_schooling\\tls202'
os.chdir(directory)

# open the file in universal line ending mode
data = pd.read_csv('appln_title.csv')

# extract the variables we want
appln_id = list(data['appln_id'])
year_application = list(data['year_application'])
appln_title = list(data['appln_title'])

########################
# 2. CLEAN APPLN TITLES
########################
# print(appln_title[0:10])
#split titles into words and make lowercase
appln_title = [title.lower().split() for title in appln_title]

#use regular expressions to clean up titles
appln_title = [[re.sub('[.-]+$', '', word) for word in title] for title in appln_title]
appln_title = [[re.sub('^[.-]+', '', word) for word in title] for title in appln_title]
appln_title = [[re.sub('\.+', '', word) for word in title] for title in appln_title]
appln_title = [[re.sub('\'s$', '', word) for word in title] for title in appln_title]
appln_title = [[re.sub('s$', '', word) for word in title] for title in appln_title]
appln_title = [[re.sub('\'+', '', word) for word in title] for title in appln_title]
appln_title = [[re.sub('"+', '', word) for word in title] for title in appln_title]

#remove stopwords and numbers
appln_title = [[word.strip() for word in title if word not in set(stopwords.words("english")) and re.search('^[\d-]*$', word) == None] for title in appln_title]

#join words in title back together
appln_title = [[' '.join(title) for title in appln_title]]

#flatten list
appln_title = functools.reduce(operator.iconcat, appln_title, [])
# print(appln_title[0:10])

########################
# 3. CREATE LISTS TO SEARCH OVER.  INDEXED BY [YEAR/CUMULATIVE UP TO YEAR X]
########################
data = list(zip(appln_id, year_application, appln_title))
data = pd.DataFrame(data, columns = ['applnid', 'year_application', 'applntitle'])
data['year_application'] = pd.to_numeric(data['year_application'])

year_list = list(range(1899, 1995))

#create application title lists
appln_title_year = [data.drop(data[data.year_application != year].index)['applntitle'].values.tolist() for year in year_list]
appln_title_year_total = [' '.join(data.drop(data[data.year_application != year].index)['applntitle'].values.tolist()).strip().split() for year in year_list]
appln_id_year = [data.drop(data[data.year_application != year].index)['applnid'].values.tolist() for year in year_list]

# print(appln_title_year[2][:10])
# print(appln_title_year_total[2][:10])
# print(appln_id_year[2][:10])

########################
# 4. CREATE LISTS OF WORDS TO SEARCH WITH WHERE INDEX IS [YEAR][APPLN_TITLE][WORD] ALONG WITH NUMBER OF N-GRAMS
########################
one_word = [[title.split() for title in year] for year in appln_title_year]
two_word = [[[' '.join(w) for w in zip(title.split(), title.split()[1:])] for title in year] for year in appln_title_year]
three_word = [[[' '.join(w) for w in zip(title.split(), title.split()[1:], title.split()[2:])] for title in year] for year in appln_title_year]

one_word_length = [[len(title) for title in year] for year in one_word]
two_word_length = [[len(title) for title in year] for year in two_word]
three_word_length = [[len(title) for title in year] for year in three_word]

# print(one_word[2][:10][:])
# print(two_word[2][:10][:])
# print(three_word[2][:10][:])

########################
# 5. SEARCH OVER LISTS TO FIND UNIQUE N-GRAMS
########################

#create parallel lists for one_word to hold unique indicator
one_word_unique = copy.deepcopy(one_word)

for year_indx, year_element in enumerate(one_word_unique):
    for app_indx, app_element in enumerate(year_element):
        for patent_year in list(range(0, year_indx+1)):
            for word_indx, word_element in enumerate(app_element):
                if year_indx == 0 and appln_title_year_total[year_indx].count(str(word_element)) > 1:
                    one_word_unique[year_indx][app_indx][word_indx] = 0
                elif patent_year == year_indx and appln_title_year_total[year_indx].count(str(word_element)) > 1:
                    one_word_unique[year_indx][app_indx][word_indx] = 0
                elif year_indx > 0 and patent_year != year_indx and appln_title_year_total[patent_year].count(str(word_element)) > 0:
                    one_word_unique[year_indx][app_indx][word_indx] = 0


for year_indx, year_element in enumerate(one_word_unique):
    for app_indx, app_element in enumerate(year_element):
            for word_indx, word_element in enumerate(app_element):
                if one_word_unique[year_indx][app_indx][word_indx] != 0:
                    one_word_unique[year_indx][app_indx][word_indx] = 1

print(one_word_unique[2][:10][:])


# one word
# for year_indx, year_element in enumerate(one_word):
#     for app_indx, app_element in enumerate(year_element):
#         for word_indx, word_element in enumerate(app_element):
#             if year_indx == 0 and appln_title_year_total[year_indx].count(str(word_element)) < 2:
#                 one_word[year_indx][app_indx][word_indx] = 1
#             elif appln_title_cuml[year_indx-1].count(str(word_element)) == 0 and appln_title_year_total[year_indx].count(str(word_element)) < 2:
#                 one_word[year_indx][app_indx][word_indx] = 1
#             else:
#                 one_word[year_indx][app_indx][word_indx] = 0

# print(one_word[5][:10][:])

# # two word
# two_word_unique = copy.deepcopy(two_word)

# for year_indx, year_element in enumerate(two_word_unique):
#     for app_indx, app_element in enumerate(year_element):
#         for word_indx, word_element in enumerate(app_element):
#             if year_indx == 0 and appln_title_year_total[year_indx].count(str(word_element)) < 2:
#                 two_word_unique[year_indx][app_indx][word_indx] = 1
#             elif appln_title_cuml[year_indx-1].count(str(word_element)) == 0 and appln_title_year_total[year_indx].count(str(word_element)) < 2:
#                 two_word_unique[year_indx][app_indx][word_indx] = 1
#             else:
#                 two_word_unique[year_indx][app_indx][word_indx] = 0

# print(two_word[5][:10][:])
# print(two_word_unique[5][:10][:])

# # three word
# three_word_unique = copy.deepcopy(three_word)

# for year_indx, year_element in enumerate(three_word_unique):
#     for app_indx, app_element in enumerate(year_element):
#         for word_indx, word_element in enumerate(app_element):
#             if year_indx == 0 and appln_title_year_total[year_indx].count(str(word_element)) < 2:
#                 three_word_unique[year_indx][app_indx][word_indx] = 1
#             elif appln_title_cuml[year_indx-1].count(str(word_element)) == 0 and appln_title_year_total[year_indx].count(str(word_element)) < 2:
#                 three_word_unique[year_indx][app_indx][word_indx] = 1
#             else:
#                 three_word_unique[year_indx][app_indx][word_indx] = 0

# print(three_word[5][:10][:])
# print(three_word_unique[5][:10][:])

# one_word_number_unique = [[sum(title) for title in year] for year in one_word_unique]
# two_word_number_unique = [[sum(title) for title in year] for year in two_word_unique]
# three_word_number_unique = [[sum(title) for title in year] for year in three_word_unique]

# ########################
# # 6. CREATE INDICATOR FOR WHETHER PATENT TITLE IS UNIQUE
# ########################
# #create list for indicator for whether or not the patent has a unique word in it
# appln_id_one_unique = copy.deepcopy(appln_id_year)
# appln_id_two_unique = copy.deepcopy(appln_id_year)
# appln_id_three_unique = copy.deepcopy(appln_id_year)

# #one word
# for year_indx, year_element in enumerate(appln_id_year):
#     for app_indx, app_element in enumerate(year_element):
#         if max(one_word_unique[year_indx][app_indx], default = 0) == 1:
#             appln_id_one_unique[year_indx][app_indx] = 1
#         else:
#             appln_id_one_unique[year_indx][app_indx] = 0

# #two word
# for year_indx, year_element in enumerate(appln_id_year):
#     for app_indx, app_element in enumerate(year_element):
#         if max(two_word_unique[year_indx][app_indx], default = 0) == 1:
#             appln_id_two_unique[year_indx][app_indx] = 1
#         else:
#             appln_id_two_unique[year_indx][app_indx] = 0


# #three word
# for year_indx, year_element in enumerate(appln_id_year):
#     for app_indx, app_element in enumerate(year_element):
#         if max(three_word_unique[year_indx][app_indx], default = 0) == 1:
#             appln_id_three_unique[year_indx][app_indx] = 1
#         else:
#             appln_id_three_unique[year_indx][app_indx] = 0

# print(appln_id_year[5][:10])
# print(appln_id_one_unique[5][:10])
# print(appln_id_two_unique[5][:10])
# print(appln_id_three_unique[5][:10])

# ########################
# # 7. ZIP OUTPUT UP AND EXPORT
# ########################

# #flatten lists
# appln_id_year_flat = functools.reduce(operator.iconcat, appln_id_year, [])
# appln_id_one_unique_flat = functools.reduce(operator.iconcat, appln_id_one_unique, [])
# appln_id_two_unique_flat = functools.reduce(operator.iconcat, appln_id_two_unique, [])
# appln_id_three_unique_flat = functools.reduce(operator.iconcat, appln_id_three_unique, [])
# one_word_number_unique_flat = functools.reduce(operator.iconcat, one_word_number_unique, [])
# two_word_number_unique_flat = functools.reduce(operator.iconcat, two_word_number_unique, [])
# three_word_number_unique_flat = functools.reduce(operator.iconcat, three_word_number_unique, [])
# one_word_length_flat = functools.reduce(operator.iconcat, one_word_length, [])
# two_word_length_flat = functools.reduce(operator.iconcat, two_word_length, [])
# three_word_length_flat = functools.reduce(operator.iconcat, three_word_length, [])

# output = list(zip(appln_id_year_flat, appln_id_one_unique_flat, appln_id_two_unique_flat, appln_id_three_unique_flat, one_word_number_unique_flat, one_word_length_flat, \
#     two_word_number_unique_flat, two_word_length_flat, three_word_number_unique_flat, three_word_length_flat))
# output = pd.DataFrame(output, columns = ['appln_id', 'unique_one', 'unique_two', 'unique_three', 'number_unique_one', 'number_one', \
#     'number_unique_two', 'number_two', 'number_unique_three', 'number_three',])

# output['frac_one_unique'] = output['number_unique_one']/output['number_one']
# output['frac_two_unique'] = output['number_unique_two']/output['number_two']
# output['frac_three_unique'] = output['number_unique_three']/output['number_three']

# print(output.head(10))

# output.to_csv('unique_patents'+'.csv')













# """

# for year_indx, year_element in enumerate(one_word_unique):
#     print(year_indx)
#     counter = 0
#     while counter <= year_indx:
#         for app_indx, app_element in enumerate(year_element):
#             for word_indx, word_element in enumerate(app_element):
#                 one_word_unique[year_indx][app_indx][word_indx] = 1
#                 if year_indx == 0 and appln_title_year_total[year_indx].count(str(word_element)) >= 2:
#                     one_word_unique[year_indx][app_indx][word_indx] = 0
#                 elif counter == 0 and appln_title_year_total[year_indx].count(str(word_element)) >= 2:
#                     one_word_unique[year_indx][app_indx][word_indx] = 0
#                 elif counter > 0 and appln_title_year_total[year_indx-counter].count(str(word_element)) > 0:
#                     one_word_unique[year_indx][app_indx][word_indx] = 0
#     counter += 1
#     print(one_word[year_indx][app_indx][word_indx])

# print(one_word_unique)

# df_list_cuml = []
# df_list_year = []
# appln_title_cuml = []
# appln_title_year = []
# appln_title_year_total = []
# appln_id_year = []
# c = -1
# for i in range(1899,1995):
#     c = c + 1
#     year_end = i

#     #create dataframe lists
#     df_list_cuml.append(data0.drop(data0[data0.year_application > i].index))
#     df_list_year.append(data0.drop(data0[data0.year_application != i].index))
#     #print(df_list_cuml[c]['applntitle'])

#     #create application title lists
#     appln_title_cuml.append(df_list_cuml[c]['applntitle'].values.tolist())
#     appln_title_cuml[c] = ' '.join(appln_title_cuml[c]).strip().split()

#     appln_title_year.append(df_list_year[c]['applntitle'].values.tolist())

#     appln_title_year_total.append(df_list_year[c]['applntitle'].values.tolist())
#     appln_title_year_total[c] = ' '.join(appln_title_year_total[c])

#     appln_id_year.append(df_list_year[c]['applnid'].values.tolist())


# #create joined list of one words for counting
# one_word_total = []
# for current_word in appln_title:
#     one_word_total += current_word.split()

# print(one_word_total)


# #create word frequency
# one_word_freq = [one_word_total.count(w) for w in one_word_total]
# print(one_word_freq)
# print(one_word_freq[0])

# #merge word frequency with list of words
# #try looping over items in list

# one_word_final = list(zip(one_word_total, one_word_freq))
# print(one_word_final)

# #create list that holds the number of words in each appln_title
# one_word_length = []
# for x in one_word:
#     one_word_length.append(len(x))

# print(one_word_length)


# # created nested list from non nested list
# one_word_total_nested = []
# c = 0
# for i in range(len(one_word_length)):
#     c_old = c
#     c = one_word_length[i] + c
#     one_word_total_nested.append(one_word_final[c_old:c])

# print(one_word_total_nested)


# #create parallel list for one_word to hold unique indicator
# one_word_unique = copy.deepcopy(appln_title_year)
# print(one_word)
# print(appln_title_cuml)
# print(len(appln_title_cuml))

# for r_indx, r_element in enumerate(one_word_unique):
#     print(r_indx)
#     print(r_element)
#     for c_indx, c_element in enumerate(r_element):
#         print(c_indx)
#         print(c_element)
#         print(one_word_unique[r_indx][c_indx])
#         print(appln_title_cuml[r_indx])
#         if r_indx == 0:
#             one_word_unique[r_indx][c_indx] = 1
#         else:
#             if c_element in appln_title_cuml[r_indx-1]:
#                 one_word_unique[r_indx][c_indx] = 0
#             else:
#                 one_word_unique[r_indx][c_indx] = 1

# print(one_word_unique)
# """
# """TEST: DELETE LATER
# appln_title_hold = appln_title[0]
# appln_title1 = []
# appln_title1.append(appln_title_hold)
# print(appln_title1)

# appln_title2 = appln_title[1:]
# print(appln_title2)

# one_word_total_test = []
# for current_word in appln_title2:
#     one_word_total_test += current_word.split()

# print(one_word_total_test)
# TEST: DELETE LATER"""
