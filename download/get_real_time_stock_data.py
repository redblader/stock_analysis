import urllib2
import numpy as np
import matplotlib.pyplot as plt
import xlrd
#fh = urllib2.urlopen("http://hq.sinajs.cn/list=sh601006")
fh = urllib2.urlopen("http://www.baidu.com")
print fh.read()

class record:
    def __init__(self):
        pass


class stock:
    def __init__(self):
        self.data_storage = dict()
        pass

    def _load_data(self, s_name):
        pass

    def _load_all(self):
        pass

    def get_url_file(self, url_address):
        try:
            data = urllib2.urlopen(url_address)
        except:
            return None
            return data.read()
