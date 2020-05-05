import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
data = pd.read_csv('wine-reviews/winemag-data-130k-v2.csv', encoding='utf-8',
                   usecols=['country', 'designation', 'province', 'taster_name', 'taster_twitter_handle', 'region_1',
                            'region_2', 'variety', 'winery', 'price', 'points'])
path = 'fig_130k/dropnan/'
if not os.path.exists(path):
    os.makedirs(path)
index_list = []
for index, row in data.iterrows():
    if type(row['country']) == float and math.isnan(row['country']) \
            or type(row['province']) == float and math.isnan(row['province']) \
            or type(row['designation']) == float and math.isnan(row['designation']) \
            or type(row['taster_name']) == float and math.isnan(row['taster_name']) \
            or type(row['taster_twitter_handle']) == float and math.isnan(row['taster_twitter_handle']) \
            or type(row['region_1']) == float and math.isnan(row['region_1']) \
            or type(row['variety']) == float and math.isnan(row['variety']) \
            or type(row['winery']) == float and math.isnan(row['winery']) \
            or math.isnan(row['price']) or math.isnan(row['points']):
        index_list.append(index)
data = data.drop(index_list)
data.to_csv(path + "wine_130k_v2.csv", index=True, sep=',')


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

    plt.savefig(path + 'Bar_for_' + title + '_in_wine_reviews_130k.jpg')



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
