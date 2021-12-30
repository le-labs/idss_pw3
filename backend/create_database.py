import pandas as pd
from tqdm import tqdm
import sqlite3
import numpy as np
import time


def preprocessing(df, drop_movies_with_few_ratings=False, drop_customers_with_few_ratings=False):
    # Data Preprocessing
    df['Rating'] = df['Rating'].astype(float)
    df.index = np.arange(0, len(df))

    df_nan = pd.DataFrame(pd.isnull(df.Rating))
    df_nan = df_nan[df_nan['Rating'] == True]
    df_nan = df_nan.reset_index()

    # Fixing the Movie format
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

    if drop_movies_with_few_ratings:
        df_movie_summary = df.groupby('Movie_Id')['Rating'].agg(f)
        df_movie_summary.index = df_movie_summary.index.map(int)
        movie_benchmark = round(df_movie_summary['count'].quantile(0.7), 0)
        drop_movie_list = df_movie_summary[df_movie_summary['count'] < movie_benchmark].index
        df = df[~df['Movie_Id'].isin(drop_movie_list)]

    if drop_customers_with_few_ratings:
        df_cust_summary = df.groupby('Cust_Id')['Rating'].agg(f)
        df_cust_summary.index = df_cust_summary.index.map(int)
        cust_benchmark = round(df_cust_summary['count'].quantile(0.7), 0)
        drop_cust_list = df_cust_summary[df_cust_summary['count'] < cust_benchmark].index
        df = df[~df['Cust_Id'].isin(drop_cust_list)]
    return df


def create_ratings_db():
    files = ['data/combined_data_1.txt', 'data/combined_data_2.txt', 'data/combined_data_3.txt',
             'data/combined_data_4.txt']
    for file in tqdm(files):
        print(f"\nFILE_TO_DF {file}")
        start = time.time()
        df = pd.read_csv(file, header=None, names=['Cust_Id', 'Rating'], usecols=[0, 1]) #, nrows=50000)
        end = time.time()
        print(f"FILE_TO_DF time: {end - start}")

        print("DF_PREPROCESSING")
        start = time.time()
        df = preprocessing(df)
        end = time.time()
        print(f"DF_PREPROCESSING time: {end - start}")

        print("DF_TO_SQL")
        start = time.time()
        df.to_sql(name='raw_data', con=conn, if_exists='append')
        end = time.time()
        print(f"DF_TO_SQL time: {end - start}")


def get_unique_cust_movie_id(cursor):
    cursor.execute("SELECT DISTINCT Movie_Id FROM raw_data;")
    movie_ids = cursor.fetchall()
    cursor.execute("SELECT DISTINCT Cust_Id FROM raw_data;")
    cust_ids = cursor.fetchall()
    return cust_ids, movie_ids


def create_pivot_db(cursor, cust_ids, movie_ids):
    all_movie_ids_string = ""
    for movie_id in movie_ids:
        all_movie_ids_string = f"{all_movie_ids_string}'{movie_id[0]}' INTEGER,"
    create_table_string = f"CREATE TABLE IF NOT EXISTS pivot_table ('Cust_Id' INTEGER, {all_movie_ids_string[:-1]});"
    cursor.execute(create_table_string)

    for cust_id in tqdm(cust_ids):
        cursor.execute(f"SELECT Movie_Id, Rating FROM raw_data WHERE Cust_Id ={cust_id[0]}")
        customer_ratings = cursor.fetchall()
        movie_ids_string = ""
        ratings_string = ""
        for customer_rating in customer_ratings:
            # extract the keywords and place in form
            movie_ids_string = f"{movie_ids_string}'{customer_rating[0]}',"
            ratings_string = f"{ratings_string}{customer_rating[1]},"
        insert_query = f"INSERT INTO pivot_table (Cust_Id, {movie_ids_string[:-1]}) VALUES ({cust_id[0]}, {ratings_string[:-1]});"
        cursor.execute(insert_query)


def create_title_db():
    df = pd.read_csv('data/movie_titles.csv', encoding="ISO-8859-1", header=None, names=['Movie_Id', 'Year', 'Name'])
    df.to_sql(name='movie_titles', con=conn, if_exists='append')


if __name__ == '__main__':
    conn = sqlite3.connect('movie_ratings.db')
    c = conn.cursor()
    #create_title_db()
    #create_ratings_db()

    cust_ids, movie_ids = get_unique_cust_movie_id(c)
    create_pivot_db(c, cust_ids, movie_ids)
    conn.commit()
