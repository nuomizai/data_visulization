import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import copy

data = pd.read_csv('wine-reviews/winemag-data-130k-v2.csv', encoding='utf-8',
                   usecols=['country', 'designation', 'province', 'taster_name', 'taster_twitter_handle', 'region_1',
                            'region_2', 'variety', 'winery', 'points', 'price'])
path = 'fig_130k/high_frequency/'
if not os.path.exists(path):
    os.makedirs(path)
country = copy.deepcopy(data['country'].value_counts(sort=True).index[0])
designation = copy.deepcopy(data['designation'].value_counts(sort=True).index[0])
province = copy.deepcopy(data['province'].value_counts(sort=True).index[0])
region_1 = copy.deepcopy(data['region_1'].value_counts(sort=True).index[0])
region_2 = copy.deepcopy(data['region_2'].value_counts(sort=True).index[0])
variety = copy.deepcopy(data['variety'].value_counts(sort=True).index[0])
winery = copy.deepcopy(data['winery'].value_counts(sort=True).index[0])
taster_name = copy.deepcopy(data['taster_name'].value_counts(sort=True).index[0])
taster_twitter_handle = copy.deepcopy(data['taster_twitter_handle'].value_counts(sort=True).index[0])
points = copy.deepcopy(data['points'].value_counts(sort=True).index[0])
price = copy.deepcopy(data['price'].value_counts(sort=True).index[0])

for index, row in data.iterrows():
    if type(row['country']) == float and math.isnan(row['country']):
        data.loc[index, 'country'] = country
    if type(row['province']) == float and math.isnan(row['province']):
        data.loc[index, 'province'] = province
    if type(row['designation']) == float and math.isnan(row['designation']):
        data.loc[index, 'designation'] = designation
    if type(row['taster_name']) == float and math.isnan(row['taster_name']):
        data.loc[index, 'taster_name'] = taster_name
    if type(row['taster_twitter_handle']) == float and math.isnan(row['taster_twitter_handle']):
        data.loc[index, 'taster_twitter_handle'] = taster_twitter_handle
    if type(row['region_1']) == float and math.isnan(row['region_1']):
        data.loc[index, 'region_1'] = region_1
    if type(row['region_2']) == float and math.isnan(row['region_2']):
        data.loc[index, 'region_2'] = region_2
    if type(row['variety']) == float and math.isnan(row['variety']):
        data.loc[index, 'variety'] = variety
    if type(row['winery']) == float and math.isnan(row['winery']):
        data.loc[index, 'winery'] = winery
    if math.isnan(float(row['points'])):
        data.loc[index, 'points'] = points
    if math.isnan(row['price']):
        data.loc[index, 'price'] = price


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

    plt.savefig('fig_130k/high_frequency/Bar_for_' + title + '_in_wine_reviews_130k.jpg')


plot_bar(data['country'].value_counts(sort=True), 'country')
plot_bar(data['designation'].value_counts(sort=True), 'designation')
plot_bar(data['province'].value_counts(sort=True), 'province')
plot_bar(data['region_1'].value_counts(sort=True), 'region_1')
plot_bar(data['region_2'].value_counts(sort=True), 'region_2')
plot_bar(data['variety'].value_counts(sort=True), 'variety')
plot_bar(data['winery'].value_counts(sort=True), 'winery')
plot_bar(data['taster_name'].value_counts(sort=True), 'taster_name')
plot_bar(data['taster_twitter_handle'].value_counts(sort=True), 'taster_twitter_handle')


def five_number(num):
    Minimun = np.min(num)
    Maximum = np.max(num)
    Q1 = np.percentile(num, 25)
    Median = np.median(num)
    Q3 = np.percentile(num, 75)
    return Minimun, Q1, Median, Q3, Maximum


plt.clf()
data['points'].plot.box(title="Points")
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(path + 'Box_for_points_in_wine_reviews_130k.jpg')

minimum, q1, median, q3, maximum = five_number(data['points'])
f = open(path + 'five_number_summary.csv', 'w', newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(['name', 'minimum', 'Q1', 'median', 'Q3', 'maximum'])
csv_writer.writerow(['points', minimum, q1, median, q3, maximum])

plt.clf()
data['price'].plot.box(title="Price")
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(path + 'Box_for_price_in_wine_reviews_130k.jpg')
minimum, q1, median, q3, maximum = five_number(data['price'])
csv_writer.writerow(['price', minimum, q1, median, q3, maximum])

f.close()
