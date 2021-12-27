import json
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from movie_metadata import get_metadata

METADATA = get_metadata(key='title')

class recommender():
    # Initialize Recommender
    def __init__(self, machine_powerful, info):
        sns.set_style("darkgrid")

        # set the amount of movies loaded depending on input variable, determining machine capabilities
        if machine_powerful:
            df1 = pd.read_csv('data/combined_data_1.txt', header=None, names=['Cust_Id', 'Rating'], usecols=[0, 1])
            df2 = pd.read_csv('data/combined_data_2.txt', header=None, names=['Cust_Id', 'Rating'], usecols=[0, 1])
            df3 = pd.read_csv('data/combined_data_3.txt', header=None, names=['Cust_Id', 'Rating'], usecols=[0, 1])
            df4 = pd.read_csv('data/combined_data_4.txt', header=None, names=['Cust_Id', 'Rating'], usecols=[0, 1])
            df = df1
            df = df.append(df2)
            df = df.append(df3)
            df = df.append(df4)
        else:
            df1 = pd.read_csv('data/combined_data_1.txt', header=None, names=['Cust_Id', 'Rating'], usecols=[0, 1],
                              nrows=50000)
            df = df1

        # Data Preprocessing
        df['Rating'] = df['Rating'].astype(float)
        df.index = np.arange(0, len(df))

        df_nan = pd.DataFrame(pd.isnull(df.Rating))
        df_nan = df_nan[df_nan['Rating'] == True]
        df_nan = df_nan.reset_index()

        movie_np = []
        movie_id = 1

        for i, j in zip(df_nan['index'][1:], df_nan['index'][:-1]):
            # numpy approach
            temp = np.full((1, i - j - 1), movie_id)
            movie_np = np.append(movie_np, temp)
            movie_id += 1

        last_record = np.full((1, len(df) - df_nan.iloc[-1, 0] - 1), movie_id)
        movie_np = np.append(movie_np, last_record)

        # remove those Movie ID rows
        df = df[pd.notnull(df['Rating'])]

        df['Movie_Id'] = movie_np.astype(int)
        df['Cust_Id'] = df['Cust_Id'].astype(int)

        f = ['count', 'mean']

        self.df_movie_summary = df.groupby('Movie_Id')['Rating'].agg(f)
        self.df_movie_summary.index = self.df_movie_summary.index.map(int)
        movie_benchmark = round(self.df_movie_summary['count'].quantile(0.7), 0)
        drop_movie_list = self.df_movie_summary[self.df_movie_summary['count'] < movie_benchmark].index

        df_cust_summary = df.groupby('Cust_Id')['Rating'].agg(f)
        df_cust_summary.index = df_cust_summary.index.map(int)
        cust_benchmark = round(df_cust_summary['count'].quantile(0.7), 0)
        drop_cust_list = df_cust_summary[df_cust_summary['count'] < cust_benchmark].index

        df = df[~df['Movie_Id'].isin(drop_movie_list)]
        df = df[~df['Cust_Id'].isin(drop_cust_list)]

        # Let's pivot the data set and put it into a giant matrix - we need it for our recommendation system:
        self.df_p = pd.pivot_table(df, values='Rating', index='Cust_Id', columns='Movie_Id')
        self.df_title = pd.read_csv('data/movie_titles.csv', encoding="ISO-8859-1", header=None, names=['Movie_Id', 'Year', 'Name'])
        self.df_title.set_index('Movie_Id', inplace=True)

    def explore_dataset(self, df):
        print('Full dataset shape: {}'.format(df.shape))
        print('-Dataset examples-')
        print(df.iloc[::5000000, :])

        p = df.groupby('Rating')['Rating'].agg(['count'])

        # get movie count
        movie_count = df.isnull().sum()[1]

        # get customer count
        cust_count = df['Cust_Id'].nunique() - movie_count

        rating_count = df['Cust_Id'].count() - movie_count
        ax = p.plot(kind='barh', legend=False, figsize=(15, 10))
        plt.title(
            'Total pool: {:,} Movies, {:,} customers, {:,} ratings given'.format(movie_count, cust_count, rating_count),
            fontsize=20)
        plt.axis('off')
        for i in range(1, 6):
            ax.text(p.iloc[i - 1][0] / 4, i - 1, 'Rating {}: {:.0f}%'.format(i, p.iloc[i - 1][0] * 100 / p.sum()[0]),
                    color='white', weight='bold')
        plt.show()

        # print('Movie minimum times of review: {}'.format(movie_benchmark))

        # print('Customer minimum times of review: {}'.format(cust_benchmark))
        print('Original Shape: {}'.format(df.shape))
        print('After Trim Shape: {}'.format(df.shape))
        print('-Data Examples-')
        print(df.iloc[::5000000, :])


    def recommend(self, movie_title, min_count=0, limit=10):
        print(movie_title)
        # Recommend with Pearsons' R correlations
        # The way it works is we use Pearsons' R correlation to measure the linear correlation between review scores of all pairs of movies, then we provide the top 10 movies with highest correlations:
        i = int(self.df_title.index[self.df_title['Name'] == movie_title][0])
        target = self.df_p[i]
        similar_to_target = self.df_p.corrwith(target)
        corr_target = pd.DataFrame(similar_to_target, columns=['PearsonR'])
        corr_target.dropna(inplace=True)
        corr_target = corr_target.sort_values('PearsonR', ascending=False)
        corr_target.index = corr_target.index.map(int)
        corr_target = corr_target.join(self.df_title).join(self.df_movie_summary)[['PearsonR', 'Name', 'count', 'mean']]
        corr_target.index = np.arange(1, len(corr_target) + 1)
        corr_target = corr_target.iloc[1:]

        # filter to only
        corr_target = corr_target[corr_target['count'] > min_count][:limit]

        result_dict = corr_target.to_dict(orient='records')

        for r in result_dict:
            r['metadata'] = METADATA[r['Name']]

        # extra delay
        time.sleep(0.5)

        return result_dict
