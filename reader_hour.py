#coding=utf-8
import pandas as pd
import numpy as np
from datetime import datetime
import cPickle


for prefix in ['in', 'out']:

    df = pd.read_csv("./Data/hour_"+prefix+"_201604.csv", encoding="BIG5")

    new_columns = []
    for index, c in enumerate(df.columns):
        new_columns.append(c.replace("/", ""))
    df.columns = new_columns

    # print df

    for column in df:
        df[column] = df[column].astype(str)
        if column == u'日期' or column == u'時段':
            continue

        df[column] = df[column].str.replace(u",", "")
        df[column] = pd.to_numeric(df[column], errors="ignore")
    df['hour_str'] = df[u'日期'].str.cat(df[u'時段'], sep='/')
    df['hour'] = df[u'hour_str'].apply(lambda x: datetime.strptime(x, "%Y/%m/%d/%H"))

    df.drop(['hour_str', u'日期', u'時段'], axis=1, inplace=True)

    print df

    df.to_pickle('hour_'+prefix+'.pickle')
