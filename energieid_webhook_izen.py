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
        allow_abbrev=True
    )
    parser.add_argument('-c', '--config', dest='config', required=False,
                        help='config.json file containing url, meter and guid')
    parser.add_argument('-u', '--url', dest='url', required=False,
                        help='EnergieID Webhook url')
    parser.add_argument('-m', '--meter', dest='meterid', required=False,
                        help='EnergieID MeterID')
    parser.add_argument('-g', '--guid', dest='guid', required=False,
                        help='Izen GUID')
    parser.add_argument('-d', '--debug', dest='debug', required=False,
                        action='store_true', help='Enable debugging')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.WARNING)

    if args.config:
        logging.debug("Reading config")
        config = read_config(args.config)
        monitor_izen(*config)
    else:
        logging.debug("Reading params")
        monitor_izen(args.guid, args.url, args.meterid)


def read_config(filename):
    logging.debug("Opening {}".format(filename))
    with open(filename, 'r') as config:
        data=config.read()

    obj = json.loads(data)
    logging.debug(obj)
    return (obj['guid'],obj['url'],obj['meter'])


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
        logging.exception(error_codes(resp.status_code))
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
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
        logging.exception(error_codes(resp.status_code))
        logging.exception("HTTP error occurred: {}".format(err))
    except Exception as err:
        logging.exception("Other error occurred: {}".format(err))
    else:
        logging.info("{} - {}".format(resp.status_code, resp.reason))


def error_codes(status):
    error = {
        400: "400 Bad Request - The payload sent in your request cannot be understood.",
        403: "403 Forbidden - The webhook associated with your request has been disabled.",
        404: "404 Not found - The webhook URL does not exsist or is no longer available.",
        429: "429 Too Many Requests - Rate-limit hit. Maximum rate is 20 requests per 15 minutes."
    }
    return error.get(status, "Unknown error code ({})".format(status))


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
