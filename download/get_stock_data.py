import os 
import re

class stock_data():
    __elem_define = {'date':0,'open':1,'high':2,'low':3,'close':4,'volume':5,'total':6}
    __extra_elem = ['high_percent','low_percent','close_percent']
    __stock_stored_path = './stock_his/'
    __stocks_history_database = {}
    __separator = '\t'
    __sh_index = 'SH999999.txt'


    def __init__(self, stock_path = './stock_his/'):
        stocks_list = os.listdir(stock_path)
        self.__stock_stored_path = stock_path

        if self.__sh_index not in stocks_list:
            print 'Can not find %s file' %(self.__sh_index)
            return None

        file_name = self.__stock_stored_path + self.__sh_index
        stock_hist_data = self.__get_raw_data_from_file(file_name)
        stock_hist_data = stock_hist_data[::-1]
        if stock_hist_data:
            self.__stocks_history_database[self.__sh_index] = stock_hist_data
            print 'read %s' %(file_name)
            date_seq = self.get_one_elem_seq(self.__sh_index, 'date')
            print 'current date %s' %(date_seq[0])
        else:
            print 'There are not records in %s' %(self.__sh_index)
            return None

        stocks_list = [each_stock for each_stock in stocks_list if each_stock != self.__sh_index]

        for each_stock in stocks_list:
            file_name = self.__stock_stored_path + each_stock
            if os.path.isfile(file_name):
                stock_hist_data = self.__get_raw_data_from_file(file_name)
                if stock_hist_data:
                    stock_hist_data = stock_hist_data[::-1]
                    store_flg = True
                    for i in range(40):
                        if len(stock_hist_data) < 40 or stock_hist_data[i][0] != date_seq[i]:
                            print '%s the first records\' date is not invalid' %(each_stock)
                            store_flg = False
                            break
                    if store_flg:
                        self.__stocks_history_database[each_stock] = stock_hist_data
                        print 'read %s' %(file_name)

    def __get_raw_data_from_file(self, stock_file):
        try:
            fh = open(stock_file, 'rb')
        except:
            print 'open stock %s failed' %(stock_file)
            return None

        record_list = []
        for each_line in fh:
            record = each_line.split(self.__separator)

            if len(self.__elem_define.keys()) != len(record):
                continue

            #if not re.findall('\d{4}[\-\/]{1}\d{2}[\-\/]{1}\d{2}', record[0]):
            if not re.findall('\d{2}[\-\/]{1}\d{2}[\-\/]{1}\d{4}', record[0]):
                continue

            try:
                record[1:] = [float(record[i]) for i in range(1,len(record))]
            except:
                continue

            if 0 in record[1:]:
                continue

            record_list.append(record)
        fh.close()

        if record_list:
            return record_list
        else:
            print '%s not found invalid records' %(stock_file)
            return None

    def __calc_average(self, seq, days, avg):
        avg_seq = seq
        if days > 1 and seq:
            adj_seq = []
            if avg:
                adj_seq = [sum(seq[i:i+days])/days for i in range(0,len(seq),days)]
            else:
                adj_seq = [seq[i] for i in range(0,len(seq),days)]
            avg_seq = adj_seq    
        return avg_seq

    def __get_high_percent(self, stock_name, days = 1, avg = False):
        open_seq = self.get_one_elem_seq(stock_name, 'open', days, avg)
        high_seq = self.get_one_elem_seq(stock_name, 'high', days, avg)
        high_percent_seq = None
        if open_seq and high_seq:
            try:
                high_percent_seq = [float(high_seq[i] - open_seq[i])/float(open_seq[i]) for i in range(len(open_seq))]
            except:
                print '%s open is 0' %(stock_name)
                return None
            if days != 1:
                high_percent_seq = self.__calc_average(high_percent_seq, days, avg)
        return high_percent_seq

    def __get_low_percent(self, stock_name, days = 1, avg = False):
        open_seq = self.get_one_elem_seq(stock_name, 'open', days, avg)
        low_seq = self.get_one_elem_seq(stock_name, 'low', days, avg)
        low_percent_seq = None
        if open_seq and low_seq:
            try:
                low_percent_seq = [float(low_seq[i] - open_seq[i])/float(open_seq[i]) for i in range(len(open_seq))]
            except:
                print '%s open is 0' %(stock_name)
                return None
            if days != 1:
                low_percent_seq = self.__calc_average(low_percent_seq, days, avg)
        return low_percent_seq

    def __get_close_percent(self, stock_name, days = 1, avg = False):
        open_seq = self.get_one_elem_seq(stock_name, 'open', days, avg)
        close_seq = self.get_one_elem_seq(stock_name, 'close', days, avg)
        close_percent_seq = None
        if open_seq and close_seq:
            try:
                close_percent_seq = [float(close_seq[i] - close_seq[i+1])/float(open_seq[i]) for i in range(len(open_seq)-1)]
            except:
                print '%s open is 0' %(stock_name)
                return None
            if days != 1:
                close_percent_seq = self.__calc_average(close_percent_seq, days, avg)
        return close_percent_seq

    def get_one_elem_seq(self, stock_name, elem_name, days = 1, avg = False):
        if stock_name not in self.get_stocks_list():
            print '%s stock not in database' %(stock_name)
            return None

        elem_seq = None
        if elem_name in self.__elem_define.keys():
            stock_data = self.__stocks_history_database[stock_name]
            idx = self.__elem_define[elem_name]
            elem_seq = [stock_data[i][idx] for i in range(len(stock_data))]
            elem_seq = self.__calc_average(elem_seq, days, avg)
        elif elem_name == 'high_percent':
            elem_seq = self.__get_high_percent(stock_name, days, avg)
        elif elem_name == 'low_percent':
            elem_seq = self.__get_low_percent(stock_name, days, avg)
        elif elem_name == 'close_percent':
            elem_seq = self.__get_close_percent(stock_name, days, avg)
        else:
            print '%s not in element define table' %(elem_name)
        return elem_seq
    
    def get_all_stock_elem_seq(self, elem_name, days = 1, avg = False):
        ret = []
        for each_stock in self.get_stocks_list():
            seq = self.get_one_elem_seq(each_stock, elem_name, days, avg)
            if seq:
                ret.append(seq)
        return ret

    def get_vs_ss_res(self, stock_name, elem_name, days = 1, avg = False):
        if stock_name not in self.get_stocks_list() or self.__sh_index not in self.get_stocks_list():
            print '%s not exist in database' %(stock_name)
            return None

        res_seq = None
        if elem_name in self.__extra_elem:
            ss = self.get_one_elem_seq(self.__sh_index, elem_name, days, avg)
            stock = self.get_one_elem_seq(stock_name, elem_name, days, avg)
            if ss and stock:
                res_seq = [float(stock[i] - ss[i]) for i in range(min(len(ss), len(stock)))]
        else:
            print '%s is not in extra elements list' %(elem_name)

        return res_seq

    def get_all_stocks_avg_percent(self, elem_name, days = 30):
        s_list = self.__stocks_history_database.keys()
        if elem_name in self.__extra_elem:
            all_s_list = []
            for each_stock in s_list:
                ret = self.get_one_elem_seq(each_stock, elem_name)
                if ret and len(ret) > days:
                    all_s_list.append(ret)

            result = []
            for i in range(days):
                percent = 0.0
                for j in range(len(all_s_list)):
                    percent = percent + all_s_list[j][i]
                result.append(float(percent)/float(len(all_s_list)))
        else:
            print 'This element %s is not support' %(elem_name)
            return None
        return result

    def get_stock_elem_avg_line(self, stock_name, elem_name, days):
        if stock_name not in self.get_stocks_list() or elem_name not in self.__elem_define.keys():
            print '%s or %s can not be found' %(stock_name, elem_name)
            return None

        seq = self.get_one_elem_seq(stock_name, elem_name)

        if len(seq) < days:
            print '%s has not enough records' %(stock_name)
            return None

        return [sum(seq[i:i+days])/days for i in range(len(seq) - days)]

    def get_stocks_list(self):
        return self.__stocks_history_database.keys()

    def get_avg_compare_result(self, stock_name, elem_name, section, days):
        avg_seq = self.get_stock_elem_avg_line(stock_name, elem_name, days)
        if not avg_seq:
            print 'can not get %s avg line' %(stock_name)
            return None
        stock_seq = self.get_one_elem_seq(stock_name, elem_name)

        if not stock_seq:
            print 'can not get %s seq' %(stock_name)
            return None

        high_cnt = 0.0
        percent = 0.0
        for idx in section:
            if idx >= min(len(avg_seq), len(stock_seq)):
                print 'The idx is out of seq length for %s' %(stock_name)
                return None

            if stock_seq[idx] > avg_seq[idx]:
                high_cnt = high_cnt + 1.0

            percent = percent + float(stock_seq[idx] - avg_seq[idx])/float(stock_seq[idx])

        return [high_cnt, percent/float(len(section))]

    def get_seq_trend_statistic(self, seq):
        if len(seq) == 0:
            print 'seq legth is zero'
            return None

        up_trend_cnt = 0.0
        up_trend_per = 0.0
        idx = 0
        num = len(seq)
        while idx + 1 < num:
            if seq[idx + 1] < seq[idx]:
                up_trend_cnt = up_trend_cnt + 1.0
                try:
                    up_trend_per = up_trend_per + float(seq[idx] - seq[idx+1])/float(seq[idx+1])
                except:
                    up_trend_per = up_trend_per + 0.0
            else:
                break
            idx = idx + 1

        if up_trend_cnt == 0.0:
            return None
        else:
            return [up_trend_cnt, float(up_trend_per/up_trend_cnt)]

    def get_seq_latest_trend_statistic(self, seq):
        if len(seq) == 0:
            print 'seq legth is 0'
            return None

        trend_cnt = 0.0
        trend_per = 0.0
        trend_direction = True
        idx = 0
        num = len(seq)
        while idx + 1 < num:
            if idx == 0:
                if seq[idx + 1] < seq[idx]:
                    trend_direction = True
                else:
                    trend_direction = False
                trend_per = float(seq[idx] - seq[idx+1])/float(seq[idx+1])
                idx = idx + 1
                continue

            if seq[idx + 1] < seq[idx]:
                current_direction = True
            else:
                current_direction = False

            if trend_direction == current_direction:
                trend_cnt = trend_cnt + 1.0
                try:
                    trend_per = trend_per + float(seq[idx] - seq[idx+1])/float(seq[idx+1])
                except:
                    trend_per = trend_per + 0.0
            else:
                break
            idx = idx + 1

        if trend_cnt == 0.0:
            return None
        else:
            return [trend_direction, trend_cnt, float(trend_per/trend_cnt)]

    def get_stock_up_trend(self, stock_name, elem_name, days, select_idx_seq = []):
        if stock_name not in self.get_stocks_list() or elem_name not in self.__elem_define.keys():
            print '%s or %s can not be found in list' %(stock_name, elem_name)
            return None

        seq = self.get_stock_elem_avg_line(each, 'close', days)

        max_idx = max(select_idx_seq)
        if len(seq) > max_idx:
            print 'seq number %d is lower than max select idx %d' %(len(seq), max_idx)
            return None
        
        select_seq = [seq[i] for i in select_idx_seq]

        res = self.get_seq_trend_statistic(select_seq)
        if res:
            ret.append([each, res[0], res[1]])
        return ret

    def get_all_stock_up_trend(self, days):
        s_list = self.get_stocks_list()

        ret = []
        for each in s_list:
            sret = self.get_stock_elem_avg_line(each, 'close', days)
            if sret and len(sret) > 10:
                seq = sret[0:10]
                res = self.get_seq_trend_statistic(seq)
                if res:
                    ret.append([each, res[0], res[1]])
        return ret

    def get_lines_diff(self, line1, line2):
        legth = min(len(line1), len(line2))
        return [line1[i] - line2[i] for i in range(legth)]



def main():
    print 'This calculate stock_data test'

    stock = stock_data('./stock_his/')

    s_list = stock.get_stocks_list()


    ret = stock.get_all_stock_up_trend(10)
    for each in ret:
        print each
        print '%s\t%.1f\t%.4f' %tuple(each)


    if 0:
        #ret = stock.get_stock_elem_avg_line('SH#600988.txt','close', 10)
        ret = stock.get_all_stocks_avg_percent('close_percent')
        for e in ret:
            print e

    if 0:
        for each in s_list:
            ret = stock.get_stock_elem_avg_line(each, 'close', 10)
            if ret and len(ret) > 10:
                seq = ret[0:10]
                res = stock.get_seq_trend_statistic(seq)
                if res:
                    print each + '\t%.1f\t%.6f' %tuple(res)



    if 0:
        for each in s_list:
            out = []
            ret = stock.get_avg_compare_result(each, 'close', range(5), 5)
            if ret is None:
                continue
            out = out + ret
            ret = stock.get_avg_compare_result(each, 'close', range(5), 10)
            if ret is None:
                continue
            out = out + ret
            ret = stock.get_avg_compare_result(each, 'close', range(5), 30)
            if ret is None:
                continue
            out = out + ret
            print len(out)
            print each +'\t%.1f\t%.6f'*3 %tuple(out)


    if 0:
        for each in s_list:
            print each
        print 'total %d' %(len(s_list))


        print s_list[2]
        seq = stock.get_stock_elem_avg_line(s_list[2], 'close', 3)
        for e in seq:
            print e


    if 0:
        stock_list = os.listdir('.\stock_his')
        obj = stock_data(stock_list)

        print 'test case 1'
        elem_define = {'date':0,'open':1,'high':2,'low':3,'close':4,'volume':5,'total':6}

        ret = obj.get_one_elem_seq('SH#999999.txt', 'date', 1, False)

        print ret[0:10]
    
    if 0:
        count = 0
        for each in stock_list:
                for each_elem in ['close_percent']:
                    for days in [1]:
                        for avg_fg in [True]:
                            ret = obj.get_one_elem_seq(each, each_elem, days, avg_fg)
                            out_file = 'vsss_ref_%s_%s_%d_%d.txt' %(each, each_elem, days, avg_fg)
                            out_file = str(count) + out_file
                            out_fh = open(out_file, 'wb')
                            if ret:
                                print 'ret seq len = %d' %(len(ret))
                                #print [ret[i] for i in range(len(ret)) if ret[i] < 0]
                                out_string = '\r\n'.join([str(ret[i]) for i in range(len(ret))])
                                out_fh.write(out_string)
                            else:
                                print 'ret seq len = 0'
                                out_fh.write('ret seq len = 0')
                            out_fh.close()

                            ret = obj.get_one_elem_seq('SH#999999.txt', each_elem, days, avg_fg)
                            out_file = 'vsss_ss_%s_%s_%d_%d.txt' %(each, each_elem, days, avg_fg)
                            out_file = str(count) + out_file
                            out_fh = open(out_file, 'wb')
                            if ret:
                                print 'ret seq len = %d' %(len(ret))
                                #print [ret[i] for i in range(len(ret)) if ret[i] < 0]
                                out_string = '\r\n'.join([str(ret[i]) for i in range(len(ret))])
                                out_fh.write(out_string)
                            else:
                                print 'ret seq len = 0'
                                out_fh.write('ret seq len = 0')
                            out_fh.close()
                            
                            ret = obj.get_vs_ss_res(each, each_elem, days, avg_fg)
                            print 'input: stock_name %s, elem_name %s, days %d, avg %d' %(each, each_elem, days, avg_fg)
                            out_file = 'vsss_out_%s_%s_%d_%d.txt' %(each, each_elem, days, avg_fg)
                            out_file = str(count) + out_file
                            out_fh = open(out_file, 'wb')
                            if ret:
                                print 'ret seq len = %d' %(len(ret))
                                #print [ret[i] for i in range(len(ret)) if ret[i] < 0]
                                out_string = '\r\n'.join([str(ret[i]) for i in range(len(ret))])
                                out_fh.write(out_string)
                            else:
                                print 'ret seq len = 0'
                                out_fh.write('ret seq len = 0')
                            out_fh.close()
                            
                            count = count + 1
    
    
    if 0:
        for each in stock_list:
            for each_elem in elem_define.keys():
                for days in [1,3,5,10,20]:
                    for avg_fg in [True, False]:
                        ret = obj.get_one_elem_seq(each, each_elem, days, avg_fg)
                        print 'input: stock_name %s, elem_name %s, days %d, avg %d' %(each, each_elem, days, avg_fg)
                        out_file = '%s_%s_%d_%d.txt' %(each, each_elem, days, avg_fg)
                        out_fh = open(out_file, 'wb')
                        if ret:
                            print 'ret seq len = %d' %(len(ret))
                            out_string = '\r\n'.join([str(ret[i]) for i in range(len(ret))])
                            out_fh.write(out_string)
                        else:
                            print 'ret seq len = 0'
                            out_fh.write('ret seq len = 0')
                        out_fh.close()



#main()

