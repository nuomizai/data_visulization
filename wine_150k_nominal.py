import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('wine-reviews/winemag-data_first150k.csv', encoding='utf-8',
                   usecols=['country', 'designation', 'province', 'region_1', 'region_2', 'variety', 'winery'])


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

    plt.savefig('fig_150k_nominal/origin/Bar_for_' + title + '_in_wine_reviews_150k.jpg')


path = 'fig_150k_nominal/origin/'
if not os.path.exists(path):
    os.makedirs(path)
plot_bar(data['country'].value_counts(sort=True), 'country')
plot_bar(data['designation'].value_counts(sort=True), 'designation')
plot_bar(data['province'].value_counts(sort=True), 'province')
plot_bar(data['region_1'].value_counts(sort=True), 'region_1')
plot_bar(data['region_2'].value_counts(sort=True), 'region_2')
plot_bar(data['variety'].value_counts(sort=True), 'variety')
plot_bar(data['winery'].value_counts(sort=True), 'winery')