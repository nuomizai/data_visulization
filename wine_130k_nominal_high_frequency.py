import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

data = pd.read_csv('wine-reviews/winemag-data-130k-v2.csv', encoding='utf-8',
                   usecols=['country', 'designation', 'province', 'taster_name', 'taster_twitter_handle', 'region_1',
                            'region_2', 'variety', 'winery'])
path = 'fig_130k_nominal/high_frequency/'
if not os.path.exists(path):
    os.makedirs(path)
country = data['country'].value_counts(sort=True).index[0]
designation = data['designation'].value_counts(sort=True).index[0]
province = data['province'].value_counts(sort=True).index[0]
region_1 = data['region_1'].value_counts(sort=True).index[0]
region_2 = data['region_2'].value_counts(sort=True).index[0]
variety = data['variety'].value_counts(sort=True).index[0]
winery = data['winery'].value_counts(sort=True).index[0]
taster_name = data['taster_name'].value_counts(sort=True).index[0]
taster_twitter_handle = data['taster_twitter_handle'].value_counts(sort=True).index[0]

for index, row in data.iterrows():
    if type(row['country']) == float and math.isnan(row['country']):
        row['country'] = country
    if type(row['province']) == float and math.isnan(row['province']):
        row['province'] = province
    if type(row['designation']) == float and math.isnan(row['designation']):
        row['designation'] = designation
    if type(row['taster_name']) == float and math.isnan(row['taster_name']):
        row['taster_name'] = taster_name
    if type(row['taster_twitter_handle']) == float and math.isnan(row['taster_twitter_handle']):
        row['taster_twitter_handle'] = taster_twitter_handle
    if type(row['region_1']) == float and math.isnan(row['region_1']):
        row['region_1'] = region_1
    if type(row['region_2']) == float and math.isnan(row['region_2']):
        row['region_2'] = region_2
    if type(row['variety']) == float and math.isnan(row['variety']):
        row['variety'] = variety
    if type(row['winery']) == float and math.isnan(row['winery']):
        row['winery'] = winery


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

    plt.savefig('fig_130k_nominal/high_frequency/Bar_for_' + title + '_in_wine_reviews_130k.jpg')
plot_bar(data['country'].value_counts(sort=True), 'country')
plot_bar(data['designation'].value_counts(sort=True), 'designation')
plot_bar(data['province'].value_counts(sort=True), 'province')
plot_bar(data['region_1'].value_counts(sort=True), 'region_1')
plot_bar(data['region_2'].value_counts(sort=True), 'region_2')
plot_bar(data['variety'].value_counts(sort=True), 'variety')
plot_bar(data['winery'].value_counts(sort=True), 'winery')
plot_bar(data['taster_name'].value_counts(sort=True), 'taster_name')
plot_bar(data['taster_twitter_handle'].value_counts(sort=True), 'taster_twitter_handle')
