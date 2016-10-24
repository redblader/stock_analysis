import os
import pandas as pd


class CSVFile:

    def __init__(self):
        self._MIN_ROWS_IN_FILE = 50
        self._data_storage = dict()

    def _load_file(self, file_name):
        name = os.path.basename(file_name).split('.')[0]
        try:
            csv_data = pd.read_csv(file_name, sep='\t', skiprows=2, header=None,
                                   names=['date', 'open', 'high', 'low', 'close', 'volume', 'turnover'])[:-1]
        except IOError, err_info:
            print 'open file %s failed, skipped it' % file_name, err_info
            return False

        if not csv_data.empty and len(csv_data) >= self._MIN_ROWS_IN_FILE:
            self._data_storage[name] = csv_data
            return True
        return False

    def _load_folder(self, folder_path):
        file_list = os.listdir(folder_path)
        total = len(file_list)
        success = 0
        for count, file_name in enumerate(file_list):
            file_name_with_full_path = folder_path + file_name
            success += self._load_file(file_name_with_full_path)
            out_string = '%4d/%4d' % (count, total)
            print '\b'*(len(out_string) + 2), out_string,
        print
        print 'total:', total, 'success:', success

    def load_all_history_stocks(self, storage_path):
        self._load_folder(storage_path)
        return self._data_storage

    @staticmethod
    def get_avg(stock_storage, stock_name, days_num, col_name='close'):
        if stock_name in stock_storage:
            hist_data = pd.DataFrame(stock_storage[stock_name][col_name])
            for i in range(days_num-1):
                shift = hist_data['close'].shift(periods=i+1, axis=0)
                hist_data.insert(i+1, 's'+str(i+1), shift)
            return list(hist_data.mean(axis=1))

    def get_multi_avg_lines(self, stock_name, col_name='close', *days_num_list):
        avg_lines_dict = dict()
        for days_num in days_num_list:
            avg_line = self.get_avg(stock_name, days_num, col_name)
            avg_lines_dict[str(days_num)+'d'] = avg_line
        return pd.DataFrame(avg_lines_dict)

if __name__ == "__main__":
    csv = CSVFile()
    stocks_data = csv.load_all_history_stocks('./storage/')
    asd = csv.get_avg(stocks_data, 'SH600519', 3)
    print pd.Series(asd).iloc[-10:]


