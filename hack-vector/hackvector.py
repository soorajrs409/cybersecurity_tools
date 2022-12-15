import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data", help="The string that has to be encoded")

args = parser.parse_args()



data = args.data
dec_data = ""
hex_data = ""
unicode_data = ""
hex_escaped = ""
oct_escaped = ""

def dec_entities(data):
    for i in data:
        global dec_data
        dec_data += f"&#{ord(i)};"

def hex_entities(data):
    for i in data:
        global hex_data
        hex_data += f"&#x{hex(ord(i)).lstrip('0x').rstrip('L')};"

def unicode_encode(data):
    for i in data:
        global unicode_data
        unicode_data += r"\u00{}".format(hex(ord(i)).lstrip("0x").rstrip("L"))

def hex_escape(data):
    for i in data:
        global hex_escaped
        hex_escaped += f"\\x{hex(ord(i)).lstrip('0x').rstrip('L')}"

def oct_escape(data):
    for i in data:
        global oct_escaped
        oct_escaped += f"\\{oct(ord(i)).lstrip('0o')}"

dec_entities(data=data)
hex_entities(data=data)
unicode_encode(data=data)
hex_escape(data=data)
oct_escape(data=data)

print("\n")
print(f"Decimal : {dec_data}")
print("\n")
print(f"Hex : {hex_data}")
print("\n")
print(f"Unicode : {unicode_data}")
print("\n")
print(f"Hex Escaped : {hex_escaped}")
print("\n")
print(f"Oct Escaped : {oct_escaped}")
print("\n")
