#coding=utf8
import pandas as pd
import numpy as np



df_datein = pd.read_pickle("date_in.pickle")
df_dateout = pd.read_pickle("date_out.pickle")
df_hourin = pd.read_pickle("hour_in.pickle")
df_hourout = pd.read_pickle("hour_out.pickle")


df = pd.DataFrame(index=df_datein.columns)


""" Hour """

# in_morning
df_hourin['hour'] = df_hourin['hour'].apply(lambda x: x.hour)
g = df_hourin[(df_hourin['hour'] < 12) & (df_hourin['hour'] > 6)].sum()
count = df_hourin[(df_hourin['hour'] < 12) & (df_hourin['hour'] > 6)].count()
df['in_morning_ave'] = g/count

# out_morning
df_hourout['hour'] = df_hourout['hour'].apply(lambda x: x.hour)
g = df_hourout[(df_hourin['hour'] < 12) & (df_hourout['hour'] > 6)].sum()
count = df_hourout[(df_hourout['hour'] < 12) & (df_hourout['hour'] > 6)].count()
df['out_morning_ave'] = g/count


# in_evening
g = df_hourin[(df_hourin['hour'] <= 23) & (df_hourin['hour'] > 16)].sum()
count = df_hourin[(df_hourin['hour'] <= 23) & (df_hourin['hour'] > 16)].count()
df['in_evening_ave'] = g/count

# out_evening
g = df_hourout[(df_hourin['hour'] <= 23) & (df_hourout['hour'] > 16)].sum()
count = df_hourout[(df_hourout['hour'] <= 23) & (df_hourout['hour'] > 16)].count()
df['out_evening_ave'] = g/count


df['morning_ior'] = (df['in_morning_ave'] - df['out_morning_ave'] ) / (df['in_morning_ave'] + df['out_morning_ave'] )
df['evening_ior'] = (df['in_evening_ave'] - df['out_evening_ave'] ) / (df['in_evening_ave'] + df['out_evening_ave'] )


""" Weekday ＆ weekend """


df_datein['weekday'] = df_datein['date'].apply(lambda x: x.isoweekday())
df_dateout['weekday'] = df_dateout['date'].apply(lambda x: x.isoweekday())

# in_weekday
g = df_datein[(df_datein['weekday'] < 6) & (df_datein['weekday'] >= 1)].sum()
count = df_datein[(df_datein['weekday'] < 6) & (df_datein['weekday'] >= 1)].count()
df['in_weekday_ave'] = g/count


# out_weekday
g = df_dateout[(df_dateout['weekday'] < 6) & (df_dateout['weekday'] >= 1)].sum()
count = df_dateout[(df_dateout['weekday'] < 6) & (df_dateout['weekday'] >= 1)].count()
df['out_weekday_ave'] = g/count

# in_weekends
g = df_datein[(df_datein['weekday'] <= 7) & (df_datein['weekday'] >= 6)].sum()
count = df_datein[(df_datein['weekday'] <= 7) & (df_datein['weekday'] >= 6)].count()
df['in_weekend_ave'] = g/count


# out_weekends
g = df_dateout[(df_dateout['weekday'] <= 7) & (df_dateout['weekday'] >= 6)].sum()
count = df_dateout[(df_dateout['weekday'] <= 7) & (df_dateout['weekday'] >= 6)].count()
df['out_weekend_ave'] = g/count


df['weekday_ior'] = (df['in_weekday_ave'] - df['out_weekday_ave'] ) / (df['in_weekday_ave'] + df['out_weekday_ave'] )
df['weekend_ior'] = (df['in_weekend_ave'] - df['out_weekend_ave'] ) / (df['in_weekend_ave'] + df['out_weekend_ave'] )


""" weekday weekend ratio """
# weekday
g = df_datein[(df_datein['weekday'] < 6) & (df_datein['weekday'] >= 1)].sum() + \
    df_dateout[(df_dateout['weekday'] < 6) & (df_dateout['weekday'] >= 1)].sum()
count = df_datein[(df_datein['weekday'] < 6) & (df_datein['weekday'] >= 1)].count() + \
        df_dateout[(df_dateout['weekday'] < 6) & (df_dateout['weekday'] >= 1)].count()
df['weekday_ave'] = g/count

# weekend
g = df_datein[(df_datein['weekday'] <= 7) & (df_datein['weekday'] >= 6)].sum() + \
    df_dateout[(df_dateout['weekday'] <= 7) & (df_dateout['weekday'] >= 6)].sum()
count = df_datein[(df_datein['weekday'] <= 7) & (df_datein['weekday'] >= 6)].count() + \
        df_dateout[(df_dateout['weekday'] <= 7) & (df_dateout['weekday'] >= 6)].count()
df['weekend_ave'] = g/count

df['weekdayend_r'] =  (df['weekday_ave'] - df['weekend_ave'] ) / (df['weekday_ave'] + df['weekend_ave'] ) * 3


""" total """
df['total_io'] = df_datein.sum() + df_dateout.sum()


df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
print df

df.to_pickle('processed_feature.pickle')
df.to_csv('processed_feature.csv', encoding="utf-8")



# --------
## write into metro_total.js

import json, io

d = {}
for index, row in df.iterrows():
    print index
    d[index] = int(row['total_io'])


s = json.dumps(d, encoding='utf-8', ensure_ascii=False)
s = s.replace('"','')
print s

f = io.open("web/metrototal.js", mode="w", encoding='utf8')
f.write("var metrototal = " + s + ";")

# ==========
## write hour/weekday data to metro_stat.js

d = {}

for i in range(1, 8):
    g = df_datein[df_datein['weekday'] == i].sum()
    count = df_datein[df_datein['weekday'] == i].count()
    for index, val in g.iteritems():
        if index not in d:
            d[index] = {"d_i":[], "d_o":[], "h_i":[], "h_o":[]}
        d[index]["d_i"].append(g[index]/count[index])

    g = df_dateout[df_dateout['weekday'] == i].sum()
    count = df_dateout[df_dateout['weekday'] == i].count()
    for index, val in g.iteritems():
        d[index]["d_o"].append(g[index] / count[index])

for i in range(6, 24):
    g = df_hourin[df_hourin['hour'] == i].sum()
    count = df_hourin[df_hourin['hour'] == i].count()
    for index, val in g.iteritems():
        if index == 'hour':
            continue
        d[index]["h_i"].append(g[index]/count[index])

    g = df_hourout[df_hourout['hour'] == i].sum()
    count = df_hourout[df_hourout['hour'] == i].count()
    for index, val in g.iteritems():
        if index == 'hour':
            continue
        d[index]["h_o"].append(g[index] / count[index])


s = json.dumps(d, encoding='utf-8', ensure_ascii=False)
s = s.replace('"','')
print s

f = io.open("web/metroflow.js", mode="w", encoding='utf8')
f.write("var metroflow = " + s + ";")