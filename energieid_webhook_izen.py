#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Project name: EnergieID Webhook - Izen: Automatically post IZEN solar info via WebHook
# Project URL: https://github.com/TheGroundZero/xxxxxxxxxxxxx

__author__ = 'TheGroundZero (https://github.com/TheGroundZero)'
__package__ = str("EnergieID Webhook - Izen")

import argparse
from datetime import datetime

import requests


def main():
    parser = argparse.ArgumentParser(
        prog='energieid_webhook_izen.py',
        description='Automatically post IZEN solar info via WebHook',
        allow_abbrev=False
    )
    parser.add_argument('-u', '--url', dest='url', required=True,
                        help='EnergieID Webhook url')
    parser.add_argument('-m', '--meter', dest='meterid', required=True,
                        help='EnergieID MeterID')
    parser.add_argument('-g', '--guid', dest='guid', required=True,
                        help='Izen GUID')

    args = parser.parse_args()

    monitor_izen(args.guid, args.url, args.meterid)


def monitor_izen(guid, url, meterid):
    data = get_total(guid)
    json = create_json_object(meterid, data)
    post_to_webhook(url, json)


def get_total(guid):
    url = "https://izen-monitoring.be/api/customer/customer/productionTotal/{}".format(guid)

    request_headers = {
        "Accept": "application/json,application/vnd.iman.v1+json,text/plain, */*",
        "Referer": "https://izen-monitoring.be",
        "Content-Type": "application/json",
    }

    request = requests.get(url, headers=request_headers)

    json = request.json()
    total = 0

    for item in json:
        total += item['value']

    print(total)

    return total


def create_json_object(meterid, value):
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    data = [timestamp, value]

    result = {
        "meterId": meterid,
        "data": data
    }

    print(result)
    return result


def post_to_webhook(url, data):
    requests.post(url, json=data)


if __name__ == '__main__':
    main()
