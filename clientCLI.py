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
import codecs


def check(hexC, url='http://localhost:3000'):
    print("Sending data ...")
    t = 0
    for i in hexC:
        print("sending chunk: ", t)
        c = checkHelper(url, i)
        t = c+t

    checkSumPost(hexC, url)


def checkHelper(url_, i):

    lenDecoded = len(base64.b64decode(i[1:-1] + '=' * (4 - len(i[1:-1]) % 4)))
    # print(lenDecoded)
    if lenDecoded < 20:

        response = requests.post(url_, data='CHUNK: '+i[1:])
        print(response.status_code)
        print(response.text)

        return 1
    else:

        return checkHelper(url_, i[:len(i)//2])+checkHelper(url_, i[(len(i)//2)+1:])

        # print("out")


def checkSumPost(hexC_, url_='http://localhost:3000'):
    checkSumRemote = 0
    for i in hexC_:
        msg = base64.b64decode(i[1:-1] + '=' * (4 - len(i[1:-1]) % 4))
        # print(msg)
        # print("Here checksum's gonna be calculated ")
        # checkSumRemote+=msg.decode()
    # Lets say checksum we got here is stored in checkSumRemote
    if checkSumRemote == requests.post(url_, data='CHECKSUM '):
        print("Verified ! Firmware updated successfully")
    else:
        print("Checksums didn't matched ! Firmware failed")


def readHex(filePath):
    with open(filePath, 'r') as f:
        hexCodes = f.readlines()
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
    # print(args)
    if args.send:
        check(hexC=readHex(args.filename))
    if args.check:
        checkSumPost(readHex(args.filename))
    else:
        print('\nUse the -h or --help flags for help')
