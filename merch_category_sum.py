#merchant_category_idから情報を取り出したい
#そのままone_hotにしてcard_idごとに和を取ろうとするとメモリが死ぬ
#とりあえず上位100のmerch_categoryで試してみる

import numpy as np
import pandas as pd
import gc
from tqdm import tqdm

historical_transactions = pd.read_csv('./input/historical_transactions.csv', usecols=['card_id', 'merchant_category_id'])
new_transactions = pd.read_csv('./input/new_merchant_transactions.csv', usecols=['card_id', 'merchant_category_id'])

top100_category = historical_transactions['merchant_category_id'].value_counts()[:100].keys()

historical_transactions['top100'] = historical_transactions['merchant_category_id'].apply(lambda x: 1 if x in top100_category else 0)
historical_transactions = historical_transactions[historical_transactions['top100'] == 1][['card_id', 'merchant_category_id']]
historical_transactions = pd.get_dummies(historical_transactions, columns=['merchant_category_id'])

df_sum = historical_transactions[['card_id', 'merchant_category_id_2']].groupby('card_id').sum()
cols = list(historical_transactions.columns.values)
cols = cols[2:]

for col in tqdm(cols):
    df_sum[col] = historical_transactions[['card_id', col]].groupby('card_id').sum()
    del historical_transactions[col]
    gc.collect()

df_svd.to_csv('merch_category_sum.csv')
