
import argparse
import time
import datetime
import sys
import requests
from multiprocessing import Pool

def request_process(i, time_long, url):
    result = {'Process':i, '2XX':0 ,'3XX':0, '4XX':0, '5XX':0}

    start_time = time.time()
    while time.time() < start_time + float(time_long) * 60 + 1:
        response = requests.get(url)
        status_code = response.status_code
        code = "{0}XX".format(str(status_code)[0])
        result[code] = result[code] + 1
    end_time = time.time()

    result['start time']=datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    result['end time']=datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
    result['duriation']=datetime.datetime.fromtimestamp(end_time-start_time).strftime('%M:%S')
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 0.0.1')
    parser.add_argument("-t", "--time", help="count downtime duriation in minutes")
    parser.add_argument("-u", "--url", help="url to test")
    parser.add_argument("-p", "--process_num", help="number of request process")
    args = parser.parse_args()
    pool = Pool(processes=int(args.process_num))
    results = []
    for i in range(int(args.process_num)):
        result = pool.apply_async(request_process, args=(i, args.time, args.url))
        results.append(result)
    pool.close()
    pool.join()
    for i in range(int(args.process_num)):
        print(results[i].get())

if __name__ == '__main__':
    main()