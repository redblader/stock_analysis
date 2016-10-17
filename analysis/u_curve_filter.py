import sys
sys.path.append("..\download")
import get_stock_data_from_storage as sd
import pandas as pd
import matplotlib.pyplot as plt


def u_filter(x):
    col = list(x)
    min_index = col.index(min(col))
    length = len(col)
    if float(length) * 0.4 < min_index < float(length) * 0.7:
        la = (float(col[min_index]) - float(col[0]))/float(min_index)
        ra = (float(col[-1]) - float(col[min_index]))/float(length - min_index - 1)
        if la < 0 < ra:
            if col[-1] < float(col[0])*0.95:
                ref = [la * float(i) + float(col[0]) for i in range(min_index)] +\
                      [ra * float(j - min_index) + float(col[min_index]) for j in range(min_index, length, 1)]
                std_diff_info = list(((pd.Series(ref) - pd.Series(col)).abs()/float(x.mean())).describe())
                if std_diff_info[1] < 0.01 and std_diff_info[-1] < 0.02:
                    return [1, min_index, length, std_diff_info[1], std_diff_info[-1]]
    return [0, min_index, length, 1, 1]

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
