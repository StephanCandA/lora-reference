'''
 _  __  ____    _   _
| |/ / |  _ \  | \ | |
| ' /  | |_) | |  \| |
| . \  |  __/  | |\  |
|_|\_\ |_|     |_| \_|
Key Generator and Shannon Entropy Calculator
for Python
Entropy Calculator inspired by: https://rosettacode.org/wiki/Entropy
(c) 2018 KPN
License: MIT License
Author: Mark Prins

(c) 2021 Faunabit
Export function to csv in the Thingspark import format.
Stephan Peterse - Faunabit.eu

'''




import os, sys
import math
import binascii
import csv
import argparse
import os.path
from os import path



DEFAULT_KEYLENGTH = 8
APPKEY_KEYLENGTH = 16
# APPEUI = "70B3D57ED0028D38"

keys = 1
appeui =''
profile = ''
connectid = ''
routing = ''

parser = argparse.ArgumentParser()
parser.add_argument('--keys','-k', type=int, help='Number of DevEUI Keys.', default=keys)
parser.add_argument('--appeui','-a', type=str, help='APPEUI for all keys', default='')
parser.add_argument('--profile','-p', type=str, help='Profile name for all keys', default='')
parser.add_argument('--connectid','-c', type=str, help='Connectivity Plan ID for all keys', default='')
parser.add_argument('--routing','-r', type=str, help='AS Routing Profile ID for all keys', default='')
parser.add_argument('--file','-f', type=str, help='Name of the file to write the keys to.', default='no name')
args = parser.parse_args()

keys = int(args.keys)
appeui = args.appeui
profile = args.profile
connectid = args.connectid
routing = args.routing

file =  args.file

#Defenitions
def write_csv(dataset):
    try:
     with open(file, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',quotechar=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(dataset)
    except PermissionError:
        print("CSV file is opened by an other program")
        sys.exit(1)

def generate_key(length=DEFAULT_KEYLENGTH):
    """ Returns a bytestring of <length> (proper) random bytes """
    return os.urandom(length)


def shannon_entropy(inputstring):
    """ Returns the shannon entropy in bits/symbol calculated over the <inputstring> """
    return sum(
        [-(inputstring.count(c) / float(len(inputstring)) * math.log(inputstring.count(c) / float(len(inputstring)), 2))
         for c in set(inputstring)])


def checkHex(s):
    # Iterate over string
    for ch in s:

        # Check if the character
        # is invalid
        if ((ch < '0' or ch > '9') and
                (ch < 'A' or ch > 'F')):
             return False
        else:
            return True




if file is 'no name':
    print('Please enter file name in start string: python3 keygen.py -f <FILE NAME>. See keygen -h for more help')
    sys.exit(1)

if appeui != '':
    if checkHex(appeui) is False:
        print('Appkeys is not a hexadecimal value')
        sys.exit(1)



if path.exists(file):
    print('File already exists, keys are added to the file')
else:
    write_csv(['Type','Device EUI (16)','Device Addr (8)','AppEUI (16)','NwkSKey (32)','App(S)Key (32)','Device Profile Name','Connectivity Plan ID','AS Routing Profile ID','Device name'])




if keys is 0:
    print("How many keys: ")
    keys = int(input())


for i in range(keys):
    # if __name__ == "__main__":
    #
    #     if len(sys.argv) > 1:
    #
    #         keylength = int(sys.argv[1])
    #     else:
    #         keylength = DEFAULT_KEYLENGTH

    DEVEUI = generate_key(DEFAULT_KEYLENGTH)
    APPKEY = generate_key(DEFAULT_KEYLENGTH*2)
    # print(DEVEUI)
    # print(APPKEY)
    DEVEUI_HEX="{DEVEUI}".format(DEVEUI=binascii.b2a_hex(DEVEUI).decode("utf8").upper())
    APPKEY_HEX="{APPKEY}".format(APPKEY=binascii.b2a_hex(APPKEY).decode("utf8").upper())

    # print(DEVEUI_HEX)

    write_csv(['OTAA',DEVEUI_HEX,'',appeui,'',APPKEY_HEX,profile,connectid,routing])

print('{} DEVEUI and APPKEY keys added to {}'.format(keys,file))
if appeui != '':
    print('APPKey: {} is added to these as keys'.format(appeui))
