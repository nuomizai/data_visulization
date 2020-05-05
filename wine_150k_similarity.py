import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import copy

name_list = {'country': 1, 'description': 2, 'designation': 3, 'points': 4, 'price': 5, 'province': 6, 'region_1': 7,
             'region_2': 8, 'variety': 9, 'winery': 10}


def order_similarity(r1, r2, max_f):
    if math.isnan(r1) or math.isnan(r2):
        return 0
    z1 = (r1 - 1) / (max_f - 1)
    z2 = (r2 - 1) / (max_f - 1)
    return abs(z1 - z2)


def num_similarity(r1, r2, max_f, min_f):
    if math.isnan(r1) or math.isnan(r2):
        return 0
    return abs(r1 - r2) / (max_f - min_f)


def nomi_similarity(word1, word2):
    if word1.strip() == word2.strip():
        return 0.0
    else:
        return 1.0


def isnan(zeta):
    if type(zeta) == float or type(zeta) == np.float64:
        if math.isnan(zeta):
            return True
        else:
            return False
    else:
        return False


def get_dis(row_i, row_j, max_po, max_pr, min_pr):
    delta = np.zeros(9)
    dis_sim = np.zeros(9)
    if isnan(data.iat[row_i, name_list['country']]) or isnan(data.iat[row_j, name_list['country']]):
        delta[0] = 0
    else:
        delta[0] = 1
        dis_sim[0] = nomi_similarity(data.iat[row_i, name_list['country']], data.iat[row_j, name_list['country']])
    if isnan(data.iat[row_i, name_list['designation']]) or isnan(data.iat[row_j, name_list['designation']]):
        delta[1] = 0
    else:
        delta[1] = 1
        dis_sim[1] = nomi_similarity(data.iat[row_i, name_list['designation']],
                                     data.iat[row_j, name_list['designation']])
    if isnan(data.iat[row_i, name_list['points']]) or isnan(data.iat[row_j, name_list['points']]):
        delta[2] = 0
    else:
        delta[2] = 1
        dis_sim[2] = order_similarity(data.iat[row_i, name_list['points']], data.iat[row_j, name_list['points']],
                                      max_po)
    if isnan(data.iat[row_i, name_list['price']]) or isnan(data.iat[row_j, name_list['price']]):
        delta[3] = 0
    else:
        delta[3] = 1
        dis_sim[3] = num_similarity(data.iat[row_i, name_list['price']], data.iat[row_j, name_list['price']], max_pr,
                                    min_pr)
    if isnan(data.iat[row_i, name_list['province']]) or isnan(data.iat[row_j, name_list['province']]):
        delta[4] = 0
    else:
        delta[4] = 1
        dis_sim[4] = nomi_similarity(data.iat[row_i, name_list['province']], data.iat[row_j, name_list['province']])
    if isnan(data.iat[row_i, name_list['region_1']]) or isnan(data.iat[row_j, name_list['region_1']]):
        delta[5] = 0
    else:
        delta[5] = 1
        dis_sim[5] = nomi_similarity(data.iat[row_i, name_list['region_1']], data.iat[row_j, name_list['region_1']])
    if isnan(data.iat[row_i, name_list['region_2']]) or isnan(data.iat[row_j, name_list['region_2']]):
        delta[6] = 0
    else:
        delta[6] = 1
        dis_sim[6] = nomi_similarity(data.iat[row_i, name_list['region_2']], data.iat[row_j, name_list['region_2']])
    if isnan(data.iat[row_i, name_list['variety']]) or isnan(data.iat[row_j, name_list['variety']]):
        delta[7] = 0
    else:
        delta[7] = 1
        dis_sim[7] = nomi_similarity(data.iat[row_i, name_list['variety']], data.iat[row_j, name_list['variety']])
    if isnan(data.iat[row_i, name_list['winery']]) or isnan(data.iat[row_j, name_list['winery']]):
        delta[8] = 0
    else:
        delta[8] = 1
        dis_sim[8] = nomi_similarity(data.iat[row_i, name_list['winery']], data.iat[row_j, name_list['winery']])
    result = np.sum(delta * dis_sim) / np.sum(delta)
    return result


data = pd.read_csv('wine-reviews/winemag-data_first150k.csv', encoding='utf-8')
tnt_data = len(data)
path = 'fig_150k/similarity/'
if not os.path.exists(path):
    os.makedirs(path)

max_points = np.max(data['points'])
max_price = np.max(data['price'])
min_price = np.min(data['price'])
indexes = []


def get_index(name):
    dis = 100
    tmp_index = 0

    index_j = 0
    while index_j < 100:
        rand_index = np.random.randint(0, tnt_data, 1)[0]
        if isnan(data.iat[rand_index, name_list[name]]):
            continue
        result = get_dis(index_i, rand_index, max_points, max_price, min_price)
        if result < dis:
            dis = result
            tmp_index = rand_index
        index_j += 1
    indexes.append(tmp_index)


index_i = 0
while index_i < tnt_data:
    if index_i % 200 == 0:
        print(index_i)
    if isnan(data.iat[index_i, name_list['country']]):
        get_index('country')
    if isnan(data.iat[index_i, name_list['designation']]):
        get_index('designation')
    if isnan(data.iat[index_i, name_list['province']]):
        get_index('province')
    if isnan(data.iat[index_i, name_list['region_1']]):
        get_index('region_1')
    if isnan(data.iat[index_i, name_list['variety']]):
        get_index('variety')
    if isnan(data.iat[index_i, name_list['winery']]):
        get_index('winery')
    if isnan(data.iat[index_i, name_list['price']]):
        get_index('price')
    if isnan(data.iat[index_i, name_list['points']]):
        get_index('points')
    index_i += 1

cnt = 0

index_i = 0
for index_i, row_i in data.iterrows():
    if isnan(row_i['country']):
        data.loc[index_i, 'country'] = data['country'][indexes[cnt]]
        cnt += 1
    if isnan(row_i['designation']):
        data.loc[index_i, 'designation'] = data['designation'][indexes[cnt]]
        cnt += 1
    if isnan(row_i['province']):
        data.loc[index_i, 'province'] = data['province'][indexes[cnt]]
        cnt += 1
    if isnan(row_i['region_1']):
        data.loc[index_i, 'region_1'] = data['region_1'][indexes[cnt]]
        cnt += 1
    if isnan(row_i['variety']):
        data.loc[index_i, 'variety'] = data['variety'][indexes[cnt]]
        cnt += 1
    if isnan(row_i['winery']):
        data.loc[index_i, 'winery'] = data['winery'][indexes[cnt]]
        cnt += 1
    if isnan(row_i['price']):
        data.loc[index_i, 'price'] = data['price'][indexes[cnt]]
        cnt += 1
    if isnan(row_i['points']):
        data.loc[index_i, 'points'] = data['points'][indexes[cnt]]
        cnt += 1

data.to_csv(path + "wine-150k-v2.csv", index=True, sep=',')


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

    plt.savefig(path + '/Bar_for_' + title + '_in_wine_reviews_150k.jpg')


plot_bar(data['country'].value_counts(sort=True), 'country')
plot_bar(data['designation'].value_counts(sort=True), 'designation')
plot_bar(data['province'].value_counts(sort=True), 'province')
plot_bar(data['region_1'].value_counts(sort=True), 'region_1')
plot_bar(data['region_2'].value_counts(sort=True), 'region_2')
plot_bar(data['variety'].value_counts(sort=True), 'variety')
plot_bar(data['winery'].value_counts(sort=True), 'winery')


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
