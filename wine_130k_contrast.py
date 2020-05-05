import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import copy

data_origin = pd.read_csv('wine-reviews/winemag-data-130k-v2.csv', encoding='utf-8')
data_dropnan = pd.read_csv('fig_130k/dropnan/wine_130k_v2.csv', encoding='utf-8')
data_high_frequency = pd.read_csv('fig_130k/high_frequency/wine_130k_v2.csv', encoding='utf-8')
data_similarity = pd.read_csv('fig_130k/similarity/winemag-data-130k-v3.csv.csv', encoding='utf-8')
data_relationship = pd.read_csv('fig_130k/relationship/winemag-data-130k-v4.csv', encoding='utf-8')

path = 'fig_130k/contrast/'
if not os.path.exists(path):
    os.makedirs(path)


def plot_bar(series_origin, series_dropnan, series_high_frequency, series_relationship, series_similarity, title):
    plt.clf()
    tnt = 0
    number = []
    bar_width = 0.15
    scale = 1
    for values in series_origin.values:
        number.append(values)
        tnt += 1
        if tnt == 25:
            break
    tnt = 0
    work_type = []
    for keys in series_origin.index:
        work_type.append(keys)
        tnt += 1
        if tnt == 25:
            break
    x = np.arange(len(work_type))
    plt.bar(x - 2 * bar_width, number, width=scale * bar_width, label='origin')
    plt.xticks(x, work_type, rotation=90)

    number = []
    for name in work_type:
        if name in series_dropnan.index:
            number.append(series_dropnan[name])
        else:
            number.append(0)
    plt.bar(x - bar_width, number, width=scale * bar_width, label='drop nan')

    number = []
    for name in work_type:
        if name in series_high_frequency.index:
            number.append(series_high_frequency[name])
        else:
            number.append(0)
    plt.bar(x, number, width=scale * bar_width, label='high frequency')

    number = []
    for name in work_type:
        if name in series_relationship.index:
            number.append(series_relationship[name])
        else:
            number.append(0)
    plt.bar(x + bar_width, number, width=scale * bar_width, label='relationship')

    number = []
    for name in work_type:
        if name in series_similarity.index:
            number.append(series_similarity[name])
        else:
            number.append(0)
    plt.bar(x + 2 * bar_width, number, width=scale * bar_width, label='similarity')

    plt.legend(loc='upper right')
    plt.grid(axis='y', linestyle='--')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path + '/Bar_for_' + title + '_in_wine_reviews_130k.jpg')


plot_bar(data_origin['country'].value_counts(sort=True), data_dropnan['country'].value_counts(sort=True),
         data_high_frequency['country'].value_counts(sort=True), data_relationship['country'].value_counts(sort=True),
         data_similarity['country'].value_counts(sort=True), 'country')

plot_bar(data_origin['designation'].value_counts(sort=True), data_dropnan['designation'].value_counts(sort=True),
         data_high_frequency['designation'].value_counts(sort=True),
         data_relationship['designation'].value_counts(sort=True),
         data_similarity['designation'].value_counts(sort=True), 'designation')

plot_bar(data_origin['province'].value_counts(sort=True), data_dropnan['province'].value_counts(sort=True),
         data_high_frequency['province'].value_counts(sort=True),
         data_relationship['province'].value_counts(sort=True),
         data_similarity['province'].value_counts(sort=True), 'province')

plot_bar(data_origin['region_1'].value_counts(sort=True), data_dropnan['region_1'].value_counts(sort=True),
         data_high_frequency['region_1'].value_counts(sort=True),
         data_relationship['region_1'].value_counts(sort=True),
         data_similarity['region_1'].value_counts(sort=True), 'region_1')

plot_bar(data_origin['region_2'].value_counts(sort=True), data_dropnan['region_2'].value_counts(sort=True),
         data_high_frequency['region_2'].value_counts(sort=True),
         data_relationship['region_2'].value_counts(sort=True),
         data_similarity['region_2'].value_counts(sort=True), 'region_2')

plot_bar(data_origin['variety'].value_counts(sort=True), data_dropnan['variety'].value_counts(sort=True),
         data_high_frequency['variety'].value_counts(sort=True),
         data_relationship['variety'].value_counts(sort=True),
         data_similarity['variety'].value_counts(sort=True), 'variety')

plot_bar(data_origin['winery'].value_counts(sort=True), data_dropnan['winery'].value_counts(sort=True),
         data_high_frequency['winery'].value_counts(sort=True),
         data_relationship['winery'].value_counts(sort=True),
         data_similarity['winery'].value_counts(sort=True), 'winery')

plot_bar(data_origin['taster_name'].value_counts(sort=True), data_dropnan['taster_name'].value_counts(sort=True),
         data_high_frequency['taster_name'].value_counts(sort=True),
         data_relationship['taster_name'].value_counts(sort=True),
         data_similarity['taster_name'].value_counts(sort=True), 'taster_name')

plot_bar(data_origin['taster_twitter_handle'].value_counts(sort=True),
         data_dropnan['taster_twitter_handle'].value_counts(sort=True),
         data_high_frequency['taster_twitter_handle'].value_counts(sort=True),
         data_relationship['taster_twitter_handle'].value_counts(sort=True),
         data_similarity['taster_twitter_handle'].value_counts(sort=True), 'taster_twitter_handle')


def plot_box(series_origin, series_dropnan, series_high_frequency, series_relationship, series_similarity, title):
    plt.clf()
    plt.subplot(151)
    series_origin.plot.box(title='origin')
    plt.grid(axis='y', linestyle='--')
    plt.subplot(152)
    series_dropnan.plot.box(title='drop nan')
    plt.grid(axis='y', linestyle='--')
    plt.subplot(153)
    series_high_frequency.plot.box(title='high frequency')
    plt.grid(axis='y', linestyle='--')
    plt.subplot(154)
    series_relationship.plot.box(title='relationship')
    plt.grid(axis='y', linestyle='--')
    plt.subplot(155)
    series_similarity.plot.box(title='similarity')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.savefig(path + 'Box_for_' + title + '_in_wine_reviews_130k.jpg')


plot_box(data_origin['price'], data_dropnan['price'], data_high_frequency['price'], data_relationship['price'],
         data_similarity['price'], 'price')

plot_box(data_origin['points'], data_dropnan['points'], data_high_frequency['points'], data_relationship['points'],
         data_similarity['points'], 'points')
