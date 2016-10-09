import os
import pandas as pd
import urllib2



class URLData:
    '''http://hq.sinajs.cn/list=sh601006'''
    def __init__(self, proxy_flag=False):
        self._RETRY_TIMES = 3
        stock_files = os.listdir('./storage')
        self._stock_names = [each.split('.')[0].lower() for each in stock_files if each != 'SH999999']
        self._elem_list = [
                           'name',
                           'open',
                           'pre_close',
                           'curr_price',
                           'high',
                           'low',
                           'buy_1',
                           'sell_1',
                           'volume',
                           'amount', 
                           'buy_v1',
                           'buy_p1',
                           'buy_v2',
                           'buy_p2',
                           'buy_v3',
                           'buy_p3',
                           'buy_v4',
                           'buy_p4',
                           'buy_v5',
                           'buy_p5',
                           'sell_v1',
                           'sell_p1',
                           'sell_v2',
                           'sell_p2',
                           'sell_v3',
                           'sell_p3',
                           'sell_v4',
                           'sell_p4',
                           'sell_v5',
                           'sell_p5',
                           'curr_date',
                           'curr_time'
                           ]
        self._storage = dict()
        for each in self._stock_names:
            self._storage[each] = pd.DataFrame(columns=self._elem_list)

        if proxy_flag:
            self._set_proxy()

    def _set_proxy(self):
        proxy_handler = urllib2.ProxyHandler({"http" : 'http://10.144.1.10:8080'})
        opener = urllib2.build_opener(proxy_handler) 
        urllib2.install_opener(opener)

    def get_data(self, stock_name):
        if stock_name in self._storage:
            for i in range(self._RETRY_TIMES):
                try:
                    resp = urllib2.urlopen('http://hq.sinajs.cn/list=' + stock_name, timeout=1)
                    break
                except:
                    if i == self._RETRY_TIMES - 1:
                        print ' failed'
                        return
                    continue
            res_string = resp.read()
            rel_data = res_string.split('=')[1].replace('"', '').replace(';', '').split(',')
            if len(rel_data) >= len(self._elem_list):
                self._storage[stock_name] = self._storage[stock_name].append(pd.DataFrame([rel_data[:len(self._elem_list)]], columns=self._elem_list))
            print

    def get_all_stocks_data(self):
        for i, each in enumerate(self._storage):
            print i, each,
            self.get_data(each)

    
    def refresh_plot(self):
        pass
    
if __name__ == "__main__":
    test = URLData(True)
    #test.get_data('sh600875')
    print 'start'
    test.get_all_stocks_data()
    print 'finished'