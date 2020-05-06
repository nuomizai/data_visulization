import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_origin = pd.read_csv('visit-patterns-by-census-block-group/cbg_patterns.csv', encoding='utf-8')
data_dropnan = pd.read_csv('fig_visit/dropnan/visit-v2.csv', encoding='utf-8')
data_high_frequency = pd.read_csv('fig_visit/high_frequency/visit-v2.csv', encoding='utf-8')
data_similarity = pd.read_csv('fig_visit/similarity/visit-v2.csv', encoding='utf-8')

path = 'fig_visit/contrast/'
if not os.path.exists(path):
    os.makedirs(path)


def plot_bar(series_origin, series_dropnan, series_high_frequency, series_similarity, title):
    plt.clf()
    tnt = 0
    number = []
    bar_width = 0.15
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
    plt.bar(x - 2 * bar_width, number, width=bar_width, label='origin')
    plt.xticks(x, work_type, rotation=90)

    number = []
    for name in work_type:
        if name in series_dropnan.index:
            number.append(series_dropnan[name])
        else:
            number.append(0)
    plt.bar(x - bar_width, number, width=bar_width, label='drop nan')

    number = []
    for name in work_type:
        if name in series_high_frequency.index:
            number.append(series_high_frequency[name])
        else:
            number.append(0)
    plt.bar(x, number, width=bar_width, label='high frequency')

    number = []
    for name in work_type:
        if name in series_similarity.index:
            number.append(series_similarity[name])
        else:
            number.append(0)
    plt.bar(x + bar_width, number, width=bar_width, label='similarity')

    plt.legend(loc='upper right')
    plt.grid(axis='y', linestyle='--')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path + '/Bar_for_' + title + '_in_visit.jpg')


plot_bar(data_origin['related_same_day_brand'].value_counts(sort=True), data_dropnan['related_same_day_brand'].value_counts(sort=True),
         data_high_frequency['related_same_day_brand'].value_counts(sort=True),
         data_similarity['related_same_day_brand'].value_counts(sort=True), 'related_same_day_brand')

plot_bar(data_origin['related_same_month_brand'].value_counts(sort=True), data_dropnan['related_same_month_brand'].value_counts(sort=True),
         data_high_frequency['related_same_month_brand'].value_counts(sort=True),
         data_similarity['related_same_month_brand'].value_counts(sort=True), 'related_same_month_brand')

plot_bar(data_origin['top_brands'].value_counts(sort=True), data_dropnan['top_brands'].value_counts(sort=True),
         data_high_frequency['top_brands'].value_counts(sort=True),
         data_similarity['top_brands'].value_counts(sort=True), 'top_brands')


def plot_box(series_origin, series_dropnan, series_high_frequency, series_similarity, title):
    plt.clf()
    plt.subplot(141)
    series_origin.plot.box(title='origin')
    plt.grid(axis='y', linestyle='--')
    plt.subplot(142)
    series_dropnan.plot.box(title='drop nan')
    plt.grid(axis='y', linestyle='--')
    plt.subplot(143)
    series_high_frequency.plot.box(title='high frequency')
    plt.grid(axis='y', linestyle='--')
    plt.subplot(144)
    series_similarity.plot.box(title='similarity')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.savefig(path + 'Box_for_' + title + '_in_visit.jpg')


plot_box(data_origin['raw_visit_count'], data_dropnan['raw_visit_count'], data_high_frequency['raw_visit_count'],
         data_similarity['raw_visit_count'], 'raw_visit_count')

plot_box(data_origin['raw_visitor_count'], data_dropnan['raw_visitor_count'], data_high_frequency['raw_visitor_count'],
         data_similarity['raw_visitor_count'], 'raw_visitor_count')


