import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data", help="The string that has to be encoded")
parser.add_argument("--file", help="Enter the file of payloads")
parser.add_argument("--output", help="Enter the filename for writing output")

args = parser.parse_args()



def dec_entities(data):
    dec_data = ""
    for i in data:
        dec_data += f"&#{ord(i)};"
    return dec_data

def hex_entities(data):
    hex_data = ""
    for i in data:
        hex_data += f"&#x{hex(ord(i)).lstrip('0x').rstrip('L')};"
    return hex_data

def unicode_encode(data):
    unicode_data = ""
    for i in data:
        unicode_data += r"\u00{}".format(hex(ord(i)).lstrip("0x").rstrip("L"))
    return unicode_data

def hex_escape(data):
    hex_escaped = ""
    for i in data:
        hex_escaped += f"\\x{hex(ord(i)).lstrip('0x').rstrip('L')}"
    return hex_escaped

def oct_escape(data):
    oct_escaped = ""
    for i in data:
        oct_escaped += f"\\{oct(ord(i)).lstrip('0o')}"
    return oct_escaped

if args.data:


    print("\n")
    print(f"Decimal : {dec_entities(args.data)}")
    print("\n")
    print(f"Hex : {hex_entities(args.data)}")
    print("\n")
    print(f"Unicode : {unicode_encode(args.data)}")
    print("\n")
    print(f"Hex Escaped : {hex_escape(args.data)}")
    print("\n")
    print(f"Oct Escaped : {oct_escape(args.data)}")
    print("\n")
 
if args.file and args.output:
    payloads = []
    with open(args.file, "r+") as f:
        payloads = f.read().splitlines()
    for i in payloads:
        with open(args.output + "-dec.txt", "a+") as f:
            f.write(f"{dec_entities(i)}\n")
        with open(args.output + "-hex-entity.txt", "a+") as fx:
            fx.write(f"{hex_entities(i)}\n")
        with open(args.output + "-unicode.txt", "a+") as fu:
            fu.write(f"{unicode_encode(i)}\n")
        with open(args.output + "-hex-escape.txt", "a+") as fxe:
            fxe.write(f"{hex_escape(i)}\n")
        with open(args.output + "-oct-escape.txt", "a+") as fo:
            fo.write(f"{oct_escape(i)}\n")
