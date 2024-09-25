import pandas as pd
import time
import argparse
from sqlalchemy import create_engine
import os


def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table
    url = params.url
    
    output = 'yellow_tripdata_2021-01.csv.gz'

    os.system(f"wget {url} -O {output} ")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()


    df_iter = pd.read_csv(output,iterator=True,chunksize=100000)
    df = next(df_iter)
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df.head(0).to_sql(table,con=engine,if_exists="replace")
    df.to_sql(table,con=engine,if_exists="append")
    while True:
        start = time.time()
        df = next(df_iter)
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
        df.to_sql(table,con=engine,if_exists='append')
        time_taken = time.time()-start
        print(f"added chunk in {time_taken}")


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--host')
    parser.add_argument('--port')
    parser.add_argument('--db')
    parser.add_argument('--table')
    parser.add_argument('--url')
    args = parser.parse_args()
    main(args)