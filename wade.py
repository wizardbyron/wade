
import argparse
import time
import datetime
import sys
import requests
from multiprocessing import Pool

def request_thread(i, time_long, url):
    result = {'Thread':i, '2XX':0 ,'3XX':0, '4XX':0, '5XX':0}
    print(result)
    start_time = time.time()
    while time.time() < start_time + float(time_long) * 60 + 1:
        response = requests.get(url)
        status_code = response.status_code
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print("[{0}] Thread-{1}:{2}".format(st,i,status_code))
        code = "{0}XX".format(str(status_code)[0])
        result[code] = result[code] + 1
        print(result)
    
    # return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 0.0.1')
    parser.add_argument("-t", "--time", help="count downtime duriation in minutes")
    parser.add_argument("-u", "--url", help="url to test")
    parser.add_argument("-n", "--thread_num", help="number of request thread")
    args = parser.parse_args()
    pool = Pool(processes=int(args.thread_num))
    results = []
    for i in range(int(args.thread_num)):
        result = pool.apply_async(request_thread, args=(i, args.time, args.url))
        results.append(result)    
    pool.close()
    pool.join()

    # request_thread(1, args.time, args.url)

    # for result in results:
    #     print(result)

if __name__ == '__main__':
    main()