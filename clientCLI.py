# Idea is to raed .hex file then calculate checksum on the tool then we POST CHECKSUM
# when we POST CHECKSUM we will get running checksum, if running checksum==the checksum
# we calculated in this tool then firmware is uploaded safely.
from argparse import ArgumentParser
import csv
import json
from pprint import pprint
import requests
import sys
import base64
import builtins


def read(hexC, url='http://localhost:3000'):
    print("In URL method")
    for i in hexC:
        lenDecoded = len(base64.b64decode(i[1:-1]+"==="))
        print(lenDecoded)
        if lenDecoded < 20:

            response = requests.post(url, data='CHUNK: '+i[1:])
            print(response.status_code)
            print(response.text)
        else:
            print("out")


def readHex(filePath):
    with open(filePath, 'r') as f:
        hexCodes = f.readlines()

        for row in hexCodes:
            print(row)
    return hexCodes


if __name__ == '__main__':
    parser = ArgumentParser(
        description='A command line tool to interact with the API', prog='parsePlotSens')
    parser.add_argument('-s', '--send', action='store_true',
                        help='Sends a POST request to the API (data to firmware).')
    parser.add_argument('-c', '--check', action='store_true',
                        help='checks the CheckSUm')
    parser.add_argument('filename')
    args = parser.parse_args()
    print(args)
    if args.check:
        read(hexC=readHex(args.filename))
    if args.check:
        print("checksum to be implemented")
    else:
        print('Use the -h or --help flags for help')
