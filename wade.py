
import argparse
import datetime
import sys
import time
from multiprocessing import Pool

import requests


def request_process(i, duration, url):
    result = {'Process': i, '2XX': 0, '3XX': 0, '4XX': 0, '5XX': 0}
    logs = []
    process_start_time = time.time()
    while time.time() < process_start_time + float(duration) * 60 + 1:
        request_start_time = time.time()
        response = requests.get(url)
        request_end_time = time.time()
        status_code = response.status_code
        code = "{0}XX".format(str(status_code)[0])
        result[code] = result[code] + 1
        st = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')
        log = "[{0}] Thread-{1}:{2} in {3} seconds".format(
            st, i, status_code, round(request_end_time - request_start_time, 2))
        logs.append(log)

    process_end_time = time.time()
    result['start time'] = datetime.datetime.fromtimestamp(
        process_start_time).strftime('%Y-%m-%d %H:%M:%S')
    result['end time'] = datetime.datetime.fromtimestamp(
        process_end_time).strftime('%Y-%m-%d %H:%M:%S')
    result['duriation'] = datetime.datetime.fromtimestamp(
        process_end_time-process_start_time).strftime('%M:%S')
    result['logs'] = logs
    return result


def progress(duration):
    start_time = time.time()
    end_time = start_time + float(duration) * 60 + 1
    while time.time() < end_time:
        time_remain = datetime.datetime.fromtimestamp(
            end_time-time.time()).strftime('%M minutes %S seconds remain')
        print("{0}".format(time_remain))
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version",
                        action='version',
                        version='%(prog)s 0.0.1')
    parser.add_argument("-t", "--time",
                        help="count downtime duriation in minutes")
    parser.add_argument("-u", "--url",
                        help="url to test")
    parser.add_argument("-p", "--process_num",
                        help="number of request process")
    args = parser.parse_args()
    pool = Pool(processes=int(args.process_num))
    results = []
    # pool.apply_async(countdown, args=(args.time))
    for i in range(int(args.process_num)):
        result = pool.apply_async(
            request_process, args=(i, args.time, args.url))
        results.append(result)
    pool.close()
    pool.join()

    for i in range(int(args.process_num)):
        print(results[i].get())


if __name__ == '__main__':
    main()
