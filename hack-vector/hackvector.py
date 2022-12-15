import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data", help="The string that has to be encoded")

args = parser.parse_args()



data = args.data
dec_data = ""
hex_data = ""

def dec_entities(data):
    for i in data:
        global dec_data
        dec_data += f"&#{ord(i)};"

def hex_entities(data):
    for i in data:
        global hex_data
        hex_data += f"&#x{hex(ord(i)).lstrip('0x').rstrip('L')};"


dec_entities(data=data)
hex_entities(data=data)

print(f"Decimal : {dec_data}")
print("\n")
print(f"Hex : {hex_data}")