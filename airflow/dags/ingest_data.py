import pandas as pd
import time
import argparse
from sqlalchemy import create_engine
import os


def ingest_callable(user,password,host,port,db,table,csv_file):


    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    print('fghj')
    df_iter = pd.read_csv(csv_file,iterator=True,chunksize=100000)
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


