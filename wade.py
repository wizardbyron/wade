
import argparse
import time
import datetime
import sys
import requests



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 0.0.1')
    parser.add_argument("-t", "--time", help="count downtime duriation in minutes")
    parser.add_argument("-u", "--url", help="full path of .csv file")
    args = parser.parse_args()

    start_time = time.time()

    while time.time() < start_time + float(args.time) * 60 + 1:
        response = requests.get(args.url)
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print('[{0}]status:{1}'.format(st,response.status_code))

if __name__ == '__main__':
    main()