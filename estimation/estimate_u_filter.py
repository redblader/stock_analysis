import sys
sys.path.append("..\download")
import get_stock_data_from_storage as sd
sys.path.append("..\\analysis")
import u_filter as uf


def estimate():
    uf.search_all_stocks_with_u_shape(sd.CSVFile().load_all_history_stocks('../download/storage/'), 65, 15, True)


estimate()