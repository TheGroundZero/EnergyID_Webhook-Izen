#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Project name: EnergieID Webhook - Izen: Automatically post IZEN solar info via WebHook
# Project URL: https://github.com/TheGroundZero/xxxxxxxxxxxxx

__author__ = 'TheGroundZero (https://github.com/TheGroundZero)'
__package__ = str("EnergieID Webhook - Izen")

import argparse
import json
import logging
from datetime import datetime

import requests
from requests import HTTPError


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
    parser.add_argument('-d', '--debug', dest='debug', required=False,
                        action='store_true', help='Enable debugging')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

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
    total = 0

    try:
        req = requests.Request("GET", url, headers=request_headers)
        prep = req.prepare()
        logging.debug(pretty_print_request(prep))

        s = requests.Session()
        resp = s.send(prep)
        logging.debug(pretty_print_response(resp))

        resp.raise_for_status()

        jsondata = resp.json()

        for item in jsondata:
            total += item['value']

        logging.info("Total production: {} kWh".format(total))
    except HTTPError as err:
        logging.exception("HTTP error occurred: {}".format(err))
    except Exception as err:
        logging.exception("Other error occurred: {}".format(err))

    return total


def create_json_object(meterid, value):
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    data = [timestamp, value]

    result = {
        "meterId": meterid,
        "data": [
            data
        ]
    }

    logging.debug(result)

    return result


def post_to_webhook(url, data):
    request_headers = {
        "Content-Type": "application/json",
    }

    try:
        req = requests.Request("POST", url, headers=request_headers, data=json.dumps(data))
        prep = req.prepare()
        logging.debug(pretty_print_request(prep))

        s = requests.Session()
        resp = s.send(prep)
        logging.debug(pretty_print_response(resp))

        resp.raise_for_status()
    except HTTPError as err:
        logging.exception("HTTP error occurred: {}".format(err))
    except Exception as err:
        logging.exception("Other error occurred: {}".format(err))
    else:
        logging.info("{} - {}".format(resp.status_code, resp.reason))


def pretty_print_request(prep):
    return "{}\n{} {}\n{}\n\n{}".format(
        "----------- REQUEST -----------",
        prep.method, prep.url,
        "\n".join("{}: {}".format(k, v) for k, v in prep.headers.items()),
        prep.body
    )


def pretty_print_response(resp):
    return "{}\n{} {}\n{}\n\n{}".format(
        "----------- RESPONSE -----------",
        resp.status_code, resp.url,
        "\n".join("{}: {}".format(k, v) for k, v in resp.headers.items()),
        resp.content
    )


if __name__ == '__main__':
    main()
