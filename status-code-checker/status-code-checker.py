import time
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="The file of subdomains")
parser.add_argument("--output", help="The file to write the info")
parser.add_argument("--status_code", help="The status code to look for")

args = parser.parse_args()


def checkStatus(url):
    try:
        time.sleep(1)
        print(f"[*] Checking {url}")
        response = requests.get(url=url, timeout=3)
        return response.status_code

    except Exception as e:
        return e


def validateUrl(url):
    if ("https" or "http") not in url:
        url = "http://" + url
    return url


with open(args.file, "r") as f:
    data = f.readlines()

for i in data:
    validatedUrl = validateUrl(i)
    statusCode = checkStatus(validatedUrl.strip())
    if statusCode == int(args.status_code):
        with open(args.output, "a+") as f:
            f.writelines(f"URL : {validatedUrl} / Status Code : {statusCode}\n")
            f.close()
