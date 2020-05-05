import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import regex as re

data = pd.read_csv('visit-patterns-by-census-block-group/cbg_patterns.csv', encoding='utf-8')
name_list = {'census_block_group': 0, 'date_range_start': 1, 'date_range_end': 2, 'raw_visit_count': 3,
             'raw_visitor_count': 4, 'visitor_home_cbgs': 5, 'visitor_work_cbgs': 6, 'distance_from_home': 7,
             'related_same_day_brand': 8, 'related_same_month_brand': 9, 'top_brands': 10, 'popularity_by_hour': 11,
             'popularity_by_day': 12}
mx_raw_vis = np.max(data['raw_visit_count'])
mn_raw_vis = np.min(data['raw_visit_count'])
max_raw_visitor = np.max(data['raw_visitor_count'])
mn_raw_visitor = np.min(data['raw_visitor_count'])
mx_dis = np.max(data['distance_from_home'])
mn_dis = np.min(data['distance_from_home'])


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


def cos_similarity1(vec1, vec2):
    vec1 = vec1[1:-1].split(',')
    vec1 = np.asarray(list(map(float, vec1)))

    vec2 = vec2[1:-1].split(',')
    vec2 = np.asarray(list(map(float, vec2)))
    return np.sum(vec1 * vec2) / (np.linalg.norm(vec1, ord=2) * np.linalg.norm(vec2, ord=2))


def cos_similarity2(vec1, vec2):
    vec1 = vec1[1:-1].split(',')
    vec1 = [re.findall("\d+", v)[0] for v in vec1]
    vec1 = np.asarray(list(map(float, vec1)))

    vec2 = vec2[1:-1].split(',')
    vec2 = [re.findall("\d+", v)[0] for v in vec2]
    vec2 = np.asarray(list(map(float, vec2)))

    return np.sum(vec1 * vec2) / (np.linalg.norm(vec1, ord=2) * np.linalg.norm(vec2, ord=2))


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


def brand_similarity(vec1, vec2):
    vec1 = vec1[1:-1].split(',')
    vec1 = [b.strip("\"") for b in vec1]

    vec2 = vec2[1:-1].split(',')
    vec2 = [b.strip("\"") for b in vec2]
    cnt = 0
    for b1 in vec1:
        for b2 in vec2:
            if b1 == b2:
                cnt += 1.0
    cnt /= max(len(vec1), len(vec2))
    return cnt


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

    plt.savefig('fig_visit/similarity/Bar_for_' + title + '_in_visit.jpg')


def get_dis(idx_i, idx_j):
    delta = np.zeros(8)
    dis_sim = np.zeros(8)
    if isnan(data.iat[idx_i, name_list['raw_visit_count']]) or isnan(data.iat[idx_j, name_list['raw_visit_count']]):
        delta[0] = 0
    else:
        delta[0] = 1
        dis_sim[0] = num_similarity(data.iat[idx_i, name_list['raw_visit_count']],
                                    data.iat[idx_j, name_list['raw_visit_count']], mx_raw_vis, mn_raw_vis)
    if isnan(data.iat[idx_i, name_list['raw_visitor_count']]) or isnan(data.iat[idx_j, name_list['raw_visitor_count']]):
        delta[1] = 0
    else:
        delta[1] = 1
        dis_sim[1] = num_similarity(data.iat[idx_i, name_list['raw_visitor_count']],
                                    data.iat[idx_j, name_list['raw_visitor_count']], max_raw_visitor, mn_raw_visitor)
    if isnan(data.iat[idx_i, name_list['distance_from_home']]) or isnan(
            data.iat[idx_j, name_list['distance_from_home']]):
        delta[2] = 0
    else:
        delta[2] = 1
        dis_sim[2] = num_similarity(data.iat[idx_i, name_list['distance_from_home']],
                                    data.iat[idx_j, name_list['distance_from_home']], mx_dis, mn_dis)
    if isnan(data.iat[idx_i, name_list['related_same_day_brand']]) or isnan(
            data.iat[idx_j, name_list['related_same_day_brand']]):
        delta[3] = 0
    else:
        delta[3] = 1
        dis_sim[3] = brand_similarity(data.iat[idx_i, name_list['related_same_day_brand']],
                                      data.iat[idx_j, name_list['related_same_day_brand']])
    if isnan(data.iat[idx_i, name_list['related_same_month_brand']]) or isnan(
            data.iat[idx_j, name_list['related_same_month_brand']]):
        delta[4] = 0
    else:
        delta[4] = 1
        dis_sim[4] = brand_similarity(data.iat[idx_i, name_list['related_same_month_brand']],
                                      data.iat[idx_j, name_list['related_same_month_brand']])
    if isnan(data.iat[idx_i, name_list['top_brands']]) or isnan(data.iat[idx_j, name_list['top_brands']]):
        delta[5] = 0
    else:
        delta[5] = 1
        dis_sim[5] = brand_similarity(data.iat[idx_i, name_list['top_brands']],
                                      data.iat[idx_j, name_list['top_brands']])
    if isnan(data.iat[idx_i, name_list['popularity_by_hour']]) or isnan(
            data.iat[idx_j, name_list['popularity_by_hour']]):
        delta[6] = 0
    else:
        delta[6] = 1
        dis_sim[6] = cos_similarity1(data.iat[idx_i, name_list['popularity_by_hour']],
                                     data.iat[idx_j, name_list['popularity_by_hour']])
    if isnan(data.iat[idx_i, name_list['popularity_by_day']]) or isnan(data.iat[idx_j, name_list['popularity_by_day']]):
        delta[7] = 0
    else:
        delta[7] = 1
        dis_sim[7] = cos_similarity2(data.iat[idx_i, name_list['popularity_by_day']],
                                   data.iat[idx_j, name_list['popularity_by_day']])
    result = np.sum(delta * dis_sim) / np.sum(delta)
    return result


indexes = []


def get_index(name):
    dis = 100
    tmp_index = 0

    index_j = 0
    while index_j < 100:
        rand_index = np.random.randint(0, tnt_data, 1)[0]
        if isnan(data.iat[rand_index, name_list[name]]):
            continue
        result = get_dis(index_i, rand_index)
        if result < dis:
            dis = result
            tmp_index = rand_index
        index_j += 1
    indexes.append(tmp_index)


path = 'fig_visit/similarity/'
if not os.path.exists(path):
    os.makedirs(path)

index_i = 0
tnt_data = len(data)
while index_i < tnt_data:
    if index_i % 200 == 0:
        print(index_i)
    if isnan(data.iat[index_i, name_list['raw_visit_count']]):
        continue
    if isnan(data.iat[index_i, name_list['visitor_home_cbgs']]):
        get_index('visitor_home_cbgs')
    if isnan(data.iat[index_i, name_list['visitor_work_cbgs']]):
        get_index('visitor_work_cbgs')
    if isnan(data.iat[index_i, name_list['distance_from_home']]):
        get_index('distance_from_home')
    if isnan(data.iat[index_i, name_list['related_same_day_brand']]):
        get_index('related_same_day_brand')
    if isnan(data.iat[index_i, name_list['related_same_month_brand']]):
        get_index('related_same_month_brand')
    if isnan(data.iat[index_i, name_list['top_brands']]):
        get_index('top_brands')
    if isnan(data.iat[index_i, name_list['popularity_by_hour']]):
        get_index('popularity_by_hour')
    if isnan(data.iat[index_i, name_list['popularity_by_day']]):
        get_index('popularity_by_day')
    index_i += 1

index_i = 0
cnt = 0
while index_i < tnt_data:
    if index_i % 200 == 0:
        print(index_i)
    if isnan(data.iat[index_i, name_list['raw_visit_count']]):
        continue
    if isnan(data.iat[index_i, name_list['visitor_home_cbgs']]):
        data.loc[index_i, 'visitor_home_cbgs'] = data['visitor_home_cbgs'][indexes[cnt]]
        cnt += 1
    if isnan(data.iat[index_i, name_list['visitor_work_cbgs']]):
        data.loc[index_i, 'visitor_home_cbgs'] = data['visitor_home_cbgs'][indexes[cnt]]
        cnt += 1
    if isnan(data.iat[index_i, name_list['distance_from_home']]):
        data.loc[index_i, 'distance_from_home'] = data['distance_from_home'][indexes[cnt]]
        cnt += 1
    if isnan(data.iat[index_i, name_list['related_same_day_brand']]):
        data.loc[index_i, 'related_same_day_brand'] = data['related_same_day_brand'][indexes[cnt]]
        cnt += 1
    if isnan(data.iat[index_i, name_list['related_same_month_brand']]):
        data.loc[index_i, 'related_same_month_brand'] = data['related_same_month_brand'][indexes[cnt]]
        cnt += 1
    if isnan(data.iat[index_i, name_list['top_brands']]):
        data.loc[index_i, 'top_brands'] = data['top_brands'][indexes[cnt]]
        cnt += 1
    if isnan(data.iat[index_i, name_list['popularity_by_hour']]):
        data.loc[index_i, 'popularity_by_hour'] = data['popularity_by_hour'][indexes[cnt]]
        cnt += 1
    if isnan(data.iat[index_i, name_list['popularity_by_day']]):
        data.loc[index_i, 'popularity_by_day'] = data['popularity_by_day'][indexes[cnt]]
        cnt += 1
    index_i += 1

data = data.dropna()
data.to_csv("fig_visit/similarity/visit-v2.csv", index=True, sep=',')
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
