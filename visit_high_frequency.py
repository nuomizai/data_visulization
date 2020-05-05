import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import csv

data = pd.read_csv('visit-patterns-by-census-block-group/cbg_patterns.csv', encoding='utf-8')
name_list = {'census_block_group': 0, 'date_range_start': 1, 'date_range_end': 2, 'raw_visit_count': 3,
             'raw_visitor_count': 4, 'visitor_home_cbgs': 5, 'visitor_work_cbgs': 6, 'distance_from_home': 7,
             'related_same_day_brand': 8, 'related_same_month_brand': 9, 'top_brands': 10, 'popularity_by_hour': 11,
             'popularity_by_day': 12}

path = 'fig_visit/high_frequency/'
if not os.path.exists(path):
    os.makedirs(path)


def dropnan():
    index = 0
    index_list = []
    while index < len(data):
        if data.iat[index, name_list['related_same_day_brand']] == '[]' or \
                data.iat[index, name_list['related_same_month_brand']] == '[]' or \
                data.iat[index, name_list['top_brands']] == '[]' or \
                data.iat[index, name_list['visitor_home_cbgs']] == '{}' or \
                data.iat[index, name_list['visitor_work_cbgs']] == '{}' or \
                data.iat[index, name_list['popularity_by_day']] == '{}' or \
                data.iat[index, name_list['popularity_by_hour']] == '[]':
            index_list.append(index)
        index += 1
    return index_list


def plot_bar(series, title):
    plt.clf()
    tnt = 0
    number = []
    for values in series.values:
        number.append(values)
        tnt += 1
        if tnt == 25:
            break
    tnt = 0
    work_type = []
    for keys in series.index:
        work_type.append(keys)
        tnt += 1
        if tnt == 25:
            break

    x = np.arange(len(work_type))
    plt.bar(x, number, color='salmon')
    plt.xticks(x, work_type, rotation=90)
    plt.grid(axis='y', linestyle='--')
    plt.title(title)
    plt.tight_layout()

    plt.savefig(path + 'Bar_for_' + title + '_in_wine_reviews_150k.jpg')


related_same_day_brand = data['related_same_day_brand'].value_counts(sort=True).index[0]
if related_same_day_brand == '[]':
    related_same_day_brand = data['related_same_day_brand'].value_counts(sort=True).index[1]

related_same_month_brand = data['related_same_month_brand'].value_counts(sort=True).index[0]
if related_same_month_brand == '[]':
    related_same_month_brand = data['related_same_month_brand'].value_counts(sort=True).index[1]

top_brands = data['top_brands'].value_counts(sort=True).index[0]
if top_brands == '[]':
    top_brands = data['top_brands'].value_counts(sort=True).index[1]
census_block_group = data['census_block_group'].value_counts(sort=True).index[0]
raw_visit_count = data['raw_visit_count'].value_counts(sort=True).index[0]
raw_visitor_count = data['raw_visitor_count'].value_counts(sort=True).index[0]
distance_from_home = data['distance_from_home'].value_counts(sort=True).index[0]


def isnan(zeta):
    if type(zeta) == float or type(zeta) == np.float64:
        if math.isnan(zeta):
            return True
        else:
            return False
    else:
        if zeta == '[]' or zeta == '{}':
            return True
        else:
            return False


index = 0
while index < len(data):
    if isnan(data.iat[index, name_list['related_same_day_brand']]):
        data.loc[index, 'related_same_day_brand'] = related_same_day_brand
    if isnan(data.iat[index, name_list['related_same_month_brand']]):
        data.loc[index, 'related_same_month_brand'] = related_same_month_brand
    if isnan(data.iat[index, name_list['top_brands']]):
        data.loc[index, 'top_brands'] = top_brands
    if isnan(data.iat[index, name_list['raw_visit_count']]):
        data.loc[index, 'raw_visit_count'] = raw_visit_count
    if isnan(data.iat[index, name_list['raw_visitor_count']]):
        data.loc[index, 'raw_visitor_count'] = raw_visitor_count
    if isnan(data.iat[index, name_list['distance_from_home']]):
        data.loc[index, 'distance_from_home'] = distance_from_home
    index += 1

indexes = dropnan()
data = data.drop(indexes)
data = data.dropna()
data.to_csv(path + "visit-v2.csv", index=True, sep=',')
plot_bar(data['related_same_day_brand'].value_counts(sort=True), 'related_same_day_brand')
plot_bar(data['related_same_month_brand'].value_counts(sort=True), 'related_same_month_brand')
plot_bar(data['top_brands'].value_counts(sort=True), 'top_brands')


def five_number(num):
    Minimun = np.min(num)
    Maximum = np.max(num)
    Q1 = np.percentile(num, 25)
    Median = np.median(num)
    Q3 = np.percentile(num, 75)
    return Minimun, Q1, Median, Q3, Maximum


plt.clf()
data['census_block_group'].plot.box(title="census_block_group")
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(path + 'Box_for_census_block_group_in_visit.jpg')
minimum, q1, median, q3, maximum = five_number(data['census_block_group'])
f = open(path + 'five_number_summary.csv', 'w', newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(['name', 'minimum', 'Q1', 'median', 'Q3', 'maximum'])
csv_writer.writerow(['census_block_group', minimum, q1, median, q3, maximum])

plt.clf()
data['raw_visit_count'].plot.box(title="raw_visit_count")
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(path + 'Box_for_raw_visit_count_in_visit.jpg')
minimum, q1, median, q3, maximum = five_number(data['raw_visit_count'])
csv_writer.writerow(['raw_visit_count', minimum, q1, median, q3, maximum])
print(raw_visit_count)

plt.clf()
data['raw_visitor_count'].plot.box(title="raw_visitor_count")
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(path + 'Box_for_raw_visitor_count_in_visit.jpg')
minimum, q1, median, q3, maximum = five_number(data['raw_visitor_count'])
csv_writer.writerow(['raw_visitor_count', minimum, q1, median, q3, maximum])

plt.clf()
data['distance_from_home'].plot.box(title="distance_from_home")
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(path + 'Box_for_distance_from_home_in_visit.jpg')
minimum, q1, median, q3, maximum = five_number(data['distance_from_home'])
csv_writer.writerow(['distance_from_home', minimum, q1, median, q3, maximum])

f.close()
