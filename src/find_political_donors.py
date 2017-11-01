import os
import sys
import heapq

class Record(object):
    def __init__(self, CMTE_ID, 
                ZIP_CODE, TRANSACTION_DT, 
                TRANSACTION_AMT, OTHER_ID):
        self.CMTE_ID = CMTE_ID
        self.ZIP_CODE = ZIP_CODE
        self.TRANSACTION_DT = TRANSACTION_DT
        self.TRANSACTION_AMT = TRANSACTION_AMT
        self.OTHER_ID = OTHER_ID


class MedianFinder:
    def __init__(self, input_path, output_path_zip, output_path_date):
        self.input_path = input_path
        self.output_path_zip = output_path_zip
        self.output_path_date = output_path_date
        self.records = []
        self.zip_dict = {}
        self.date_dict = {}

    def insert_records(self):
        with open(self.input_path, 'r') as f:
            for line in f:
                fields = line.split('|')
                if len(fields) < 21:
                    continue    
                CMTE_ID = fields[0]
                ZIP_CODE = fields[10][0:5]
                TRANSACTION_DT = fields[13]
                TRANSACTION_AMT = fields[14]
                OTHER_ID = 'empty' if fields[15] == '' else fields[15] 
                DATE_KEY = CMTE_ID + '_' + TRANSACTION_DT
                ZIP_KEY = CMTE_ID + '_' + ZIP_CODE

                record = Record(CMTE_ID, 
                                ZIP_CODE, 
                                TRANSACTION_DT,
                                TRANSACTION_AMT, 
                                OTHER_ID)
                self.records.append(record)
                if OTHER_ID != 'empty' or not TRANSACTION_AMT.isdigit():
                    continue
                if not ZIP_CODE.isdigit():
                    continue
                if ZIP_KEY not in self.zip_dict:
                    self.zip_dict[ZIP_KEY] = [int(TRANSACTION_AMT)]
                else:
                    self.zip_dict[ZIP_KEY].append(int(TRANSACTION_AMT))    
                
                if len(TRANSACTION_DT) != 8 or not TRANSACTION_DT.isdigit:
                    continue    
                if len(CMTE_ID) != 9:
                    continue    
                if DATE_KEY not in self.date_dict:
                    self.date_dict[DATE_KEY] = [int(TRANSACTION_AMT)]
                else:
                    self.date_dict[DATE_KEY].append(int(TRANSACTION_AMT))
                self.output_records_zip(record, ZIP_KEY)
        self.output_records_date()

    def output_records_zip(self, record, ZIP_KEY):
        median = self.get_median(self.zip_dict[ZIP_KEY])
        zip_line = '{}|{}|{}|{}|{}\n'.format(record.CMTE_ID, 
                                      record.ZIP_CODE, 
                                      median,
                                      str(len(self.zip_dict[ZIP_KEY])),
                                      str(sum(self.zip_dict[ZIP_KEY]))
                                      )
        with open(self.output_path_zip, 'a+') as f:
            f.write(zip_line)


    def output_records_date(self):
        with open(self.output_path_date, 'w+') as f:
            for i in sorted(self.date_dict.keys()):
                median = self.get_median(self.date_dict[i])
                date_line = '{}|{}|{}|{}|{}\n'.format(i.split('_')[0],
                                        i.split('_')[1], 
                                        median,
                                        str(len(self.date_dict[i])),
                                        str(sum(self.date_dict[i]))
                                        )
                f.write(date_line)
            

    def print_records(self):
        for record in self.records:
            print "CMTE_ID: " + record.CMTE_ID
            print "ZIP_CODE: " + record.ZIP_CODE
            print "TRANSACTION_DT: " + record.TRANSACTION_DT
            print "TRANSACTION_AMT: " + record.TRANSACTION_AMT
            print "OTHER_ID: " + record.OTHER_ID
            print "\n"

    def get_median(self, nums):
        large, small = [], []
        median = 0
        for i in nums:
            heapq.heappush(small, -heapq.heappushpop(large, i))
            if len(small) > len(large):
                heapq.heappush(large, -heapq.heappop(small))
        if len(large) > len(small):
            median = large[0]
        else:
            median = int(round((large[0] - small[0]) / 2.0))
        return median

if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path_zip = sys.argv[2]
    output_path_date = sys.argv[3]
    zip = open(output_path_zip, 'w+')
    zip.close()
    m = MedianFinder(input_path, output_path_zip, output_path_date)
    m.insert_records()
    #m.print_records()
    