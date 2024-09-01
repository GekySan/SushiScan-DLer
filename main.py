from curl_cffi import requests
import re
import json
import os
import html
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from math import ceil, log10

regex_url = '^https://sushiscan.net/catalogue/[a-z0-9-]+/$'
root_folder = "DL SushiScan"

"""
Functions

parse_lr       : ✓
make_request   : ✖
download_image : ✖
"""

def parse_lr(text, left, right, recursive, unescape=True):
    """
    Parse the text for substrings between 'left' and 'right' markers.

    Parameters:
    text (str): The text to search within.
    left (str): The left marker.
    right (str): The right marker.
    recursive (bool): If True, returns all matches, else returns the first match.
    unescape (bool): If True, unescapes HTML entities in the found text.

    Returns:
    list or str: All matches if recursive is True, else the first match.
    """
    pattern = re.escape(left) + '(.*?)' + re.escape(right)
    matches = re.findall(pattern, text)

    if unescape:
        matches = [html.unescape(match) for match in matches]

    return matches if recursive else matches[0] if matches else None

def make_request(url, cookie_cf_clearance=None, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'User-Agent': user_agent
    }
    if cookie_cf_clearance:
        headers['Cookie'] = f'cf_clearance={cookie_cf_clearance}'
        
    response = requests.get(url, headers=headers, impersonate="chrome")
    return response

def download_image(url, folder_path, cookie_cf_clearance, user_agent, i, number_len):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'User-Agent': user_agent
    }
    if cookie_cf_clearance:
        headers['Cookie'] = f'cf_clearance={cookie_cf_clearance}'

    response = requests.get(url, headers=headers, impersonate="chrome")

    if response.status_code == 200:
        with open(os.path.join(folder_path, str(i).zfill(number_len)) + "." + url.split('/')[-1].split(".")[-1], 'wb') as file:
            file.write(response.content)
            print(Fore.GREEN + f"Image downloaded : {url}" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Image could not be downloaded (status code {response.status_code}): {url}" + Style.RESET_ALL)

"""
Main

Execution of main tasks: URL input, request handling,
image downloading, and error management.
"""

cookie_cf_clearance_value = None
user_agent = None

url = input("Please enter the URL of catalogue: ")
if not re.match(regex_url, url):
    print(Fore.RED + "Invalid URL format." + Style.RESET_ALL)
    exit()

response = make_request(url)
while response.status_code == 403:
    print(Fore.YELLOW + "Access denied with status code 403. Please enter 'cf_clearance' cookie value." + Style.RESET_ALL)
    cookie_cf_clearance_value = input("Cookie value for 'cf_clearance': ")
    user_agent = input("Please enter your User-Agent: ")
    response = make_request(url, cookie_cf_clearance_value, user_agent)


if response.status_code == 200:
    html_content = response.text
    title = html.unescape(parse_lr(html_content, '<h1 class="entry-title" itemprop="name">', '</h1>', False))
    volumes = parse_lr(html_content, '<span class="chapternum"> ', '</span>', True)
    links = parse_lr(html_content, '<a href="', '">\n<span class="chapternum">', True)
    volumes.reverse()
    links.reverse()
    links_of_all_volumes = []

    for link in links:
        response = make_request(link, cookie_cf_clearance_value, user_agent)
        if response.status_code == 200:
            json_string = parse_lr(response.text, 'ts_reader.run(', ');</script>', False)
            try:
                data = json.loads(json_string)
                images = data['sources'][0]['images']
                links_of_all_volumes.append(images)
            except json.JSONDecodeError as e:
                print(Fore.RED + f"JSON parsing error for link {link}: {e}" + Style.RESET_ALL)
                links_of_all_volumes.append([])
        else:
            print(Fore.RED + f"Request error for link {link}: {response.status_code}" + Style.RESET_ALL)
            links_of_all_volumes.append([])

    links_of_all_volumes = [[url.replace("http://", "https://") for url in sublist] for sublist in links_of_all_volumes]

    with ThreadPoolExecutor(max_workers=20) as executor:
        for volume, images in zip(volumes, links_of_all_volumes):
            volume_folder = os.path.join(root_folder, title, volume)
            os.makedirs(volume_folder, exist_ok=True)
            number_len = ceil(log10(len(images)))
            for i, image_url in enumerate(images):
                executor.submit(download_image, image_url, volume_folder, cookie_cf_clearance_value, user_agent, i, number_len)
    
    print(Fore.GREEN + "Download completed." + Style.RESET_ALL)

else:
    print(Fore.RED + f"Request failed with status code: {response.status_code}" + Style.RESET_ALL)
