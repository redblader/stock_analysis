import os
import pandas as pd
import matplotlib.pyplot as plt


class CSVFile:

    def __init__(self):
        self._min_rows = 5
        self._data_storage = dict()

    def get_storage(self):
        return self._data_storage

    def load_file(self, file_name):
        name = os.path.basename(file_name).split('.')[0]
        try:
            csv_data = pd.read_csv(file_name, sep='\t', skiprows=2, header=None,
                                   names=['date', 'open', 'high', 'low', 'close', 'volume', 'turnover'])[:-1]
        except IOError, err_info:
            print 'open file %s failed, skipped it' % file_name, err_info
            return False

        if not csv_data.empty and len(csv_data) >= self._min_rows:
            self._data_storage[name] = csv_data
        else:
            return False
        return True

    def load_folder(self, folder_path):
        file_list = os.listdir(folder_path)
        total = len(file_list)
        success = 0
        for count, file_name in enumerate(file_list):
            file_name_with_full_path = folder_path + file_name
            success += self.load_file(file_name_with_full_path)
            out_string = '%4d/%4d' % (count, total)
            print '\b'*(len(out_string) + 2), out_string,
        print
        print 'total:', total, 'success:', success

    def get_avg(self, stock_name, days_num):
        if stock_name in self._data_storage:
            hist_data = pd.DataFrame(self._data_storage[stock_name]['close'])
            for i in range(days_num):
                shift = hist_data['close'].shift(periods=i+1, axis=0)
                hist_data.insert(i+1, 's'+str(i+1), shift)
            return list(hist_data.mean(axis=1))

    def get_avg_lines(self, stock_name, *days_num_list):
        avg_lines_dict = dict()
        for days_num in days_num_list:
            avg_line = self.get_avg(stock_name, days_num)
            avg_lines_dict['s' + str(days_num)] = avg_line
        return pd.DataFrame(avg_lines_dict)

if __name__ == "__main__":
    csv = CSVFile()
    csv.load_folder('./storage/')
    stocks_data = csv.get_storage()
    #print list(stocks_data['SH600057']['close'][-20:])
    avg5_points = csv.get_avg('SH600057', 5)
    #print avg5_points[-20:]
    ds = pd.DataFrame({'basic':list(stocks_data['SH600057']['close'][-50:]), 'f_days':avg5_points[-50:]})
    ds.plot()
    plt.legend(loc='best')
    plt.show()
    #reference = [0, 0, 0, 0, 0, 0, 0, 0.03, 0.06, 0.1]
    #res = {'AB000000': reference}
    #for each in all_data:
    #    data = all_data[each]
    #    res[each] = (data[-10:].reset_index()['close'] - data[-10:].reset_index()['open']) / data[-10:].reset_index()['open']
    #ab = pd.DataFrame(res)
    #compute_res = ab.corr(method='pearson', min_periods=8).sort(columns='AB000000',
    #                                                            ascending=False).head(10)['AB000000']
    #print compute_res
    #data_res = compute_res.reset_index()
    #
    #show_data = {'AB000000': reference}
    #for i in range(4):
    #    stock_name = data_res.iat[i+1, 0]
    #    show_data[stock_name] = res[stock_name]
    #
    #show_plot = pd.DataFrame(show_data)
    #print show_plot
    #show_plot = show_plot.cumsum()
    #show_plot.plot()
    #plt.legend(loc='best')
    #plt.show()

