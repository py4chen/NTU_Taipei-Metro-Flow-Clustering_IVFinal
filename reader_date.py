#coding=utf-8
import pandas as pd
from datetime import datetime


for prefix in ['in', 'out']:

    df = pd.read_csv("./Data/date_" +prefix+"_201604.csv", encoding="BIG5")

    # TODO: Mapping
    # for column_name in df.columns:
    #     if column_name == u'日期':
    #         continue
    #     print column_name

    new_columns = []
    for index, c in enumerate(df.columns):
        new_columns.append(c.replace("/", ""))
    df.columns = new_columns

    for column in df:
        if column == u'日期':
            continue
        df[column] = df[column].str.replace(u",", "")
        df[column] = pd.to_numeric(df[column])


    df['date'] = df[u'日期'].apply(lambda x: datetime.strptime(x, "%Y/%m/%d"))
    df.drop([u'日期'], axis = 1, inplace = True)

    print df
    # print type(df[u"松山機場"][1])
    # print type(df[u"date"][1])

    df.to_pickle('date_'+prefix+'.pickle')


