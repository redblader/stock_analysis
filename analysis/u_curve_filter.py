import sys
sys.path.append("..\download")
import get_stock_data_from_storage as sd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def u_filter(x):
    col = list(x)
    minidx = col.index(min(col))
    length = len(col)
    if minidx > float(length)*0.4 and minidx < float(length)*0.7:
        la = (float(col[minidx]) - float(col[0]))/float(minidx)
        ra = (float(col[-1]) - float(col[minidx]))/float(length - minidx - 1)
        if la < 0 and ra > 0 and col[-1] < float(col[0])*0.95:
            ref = [la * float(i) + float(col[0]) for i in range(minidx)] + [ra * float(j - minidx) + float(col[minidx]) for j in range(minidx, length, 1)]
            for i in range(length):
                if col[i] > ref[i]:
                    return [0, minidx, length]
            return [1, minidx, length]
    return [0, minidx, length]

if __name__ == '__main__':
    csv_data = sd.CSVFile()
    csv_data.load_folder('../download/storage/')
    stocks = csv_data.get_storage()
    for days in range(15, 60, 1):
        print days, ' days',
        ds = pd.DataFrame()
        for stock_name in stocks:
            avg_seq = csv_data.get_avg(stock_name, 5)
            if len(stocks[stock_name]) >= (days+5):
                ds.insert(0, stock_name, avg_seq[-days:])
        res = ds.apply(u_filter)
        res_ds = pd.DataFrame(dict(res)).T
        flt_res = dict(res_ds[res_ds[0] == 1].T)
        print len(flt_res.keys()), ' stocks'
        for each in flt_res.keys():
            se = ds.loc[:, each]
            plt.clf()
            se.plot()
            param = '_'.join([str(par) for par in flt_res[each]])
            plt.savefig('./'+str(days) + 'days_' + each + '_' + param + '.jpg')
    
    