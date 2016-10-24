import sys
sys.path.append("..\download")
import get_stock_data_from_storage as sd
sys.path.append("..\\analysis")
import u_filter as uf
import pandas as pd


def get_n_days_ago_stock_storage(stock_storage, n):
    ret = {}
    for each_stock in stock_storage:
        if len(stock_storage[each_stock]) > n:
            ret[each_stock] = pd.DataFrame(stock_storage[each_stock].iloc[:-n, :])
    return ret


def estimate():
    stock_storage = sd.CSVFile().load_all_history_stocks('../download/storage/')
    his_storage = stock_storage
    for i in range(100):
        his_storage = get_n_days_ago_stock_storage(his_storage, 3)
        filtered_stocks = uf.search_all_stocks_with_u_shape(his_storage, 65, 15, False)
        print i, ':', filtered_stocks


if __name__ == "__main__":
    estimate()
