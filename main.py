# -*- coding: utf-8 -*-

import argparse
import html
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from math import ceil, log10

from curl_cffi import requests
from rich import print

REGEX_URL = '^https://sushiscan.net/catalogue/[a-z0-9-]+/$'
ROOT_FOLDER = "DL SushiScan"

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

def make_request(url, cookie_cf_clearance, user_agent):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'Cookie': f'cf_clearance={cookie_cf_clearance}',
        'User-Agent': user_agent
    }
        
    response = requests.get(url, headers=headers, impersonate="chrome")
    return response

def download_image(url, folder_path, cookie_cf_clearance, user_agent, i, number_len, max_retries=3):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'Cookie': f'cf_clearance={cookie_cf_clearance}',
        'User-Agent': user_agent
    }

    retries = 0
    while retries <= max_retries:
        response = requests.get(url, headers=headers, impersonate="chrome")
        
        if response.status_code == 200:
            with open(os.path.join(folder_path, str(i).zfill(number_len)) + "." + url.split('/')[-1].split(".")[-1], 'wb') as file:
                file.write(response.content)
                print(f"[bold green]Image téléchargée : {url}[/bold green]")
            return
        else:
            retries += 1
            print(f"[bold yellow]Échec du téléchargement de l'image : {url}. Tentative {retries}/{max_retries}...[/bold yellow]")

    print(f"[bold red]Impossible de télécharger l'image après {max_retries} tentatives : {url}[/bold red]")


def main():
    parser = argparse.ArgumentParser(description="Téléchargement d'un catalogue SushiScan.")
    parser.add_argument("-u", "--url", required=True, help="URL du catalogue SushiScan à télécharger.")
    parser.add_argument("-c", "--cookie", required=True, help="Valeur du cookie 'cf_clearance'.")
    parser.add_argument("-ua", "--user-agent", required=True, help="L'User-Agent pour les requêtes.")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Nombre de threads à utiliser (par défaut : 10).")

    args = parser.parse_args()

    if not re.match(REGEX_URL, args.url):
        print("[bold red]Format d'URL invalide.[/bold red]")
        exit()

    cookie_cf_clearance_value = args.cookie
    user_agent = args.user_agent
    threads = args.threads if isinstance(args.threads, int) and args.threads > 0 else 10

    response = make_request(args.url, cookie_cf_clearance_value, user_agent)

    if response.status_code == 403:
        print("[bold red]Accès refusé.[/bold red]\n[bold yellow]Vérifiez vos cookies ou l'User-Agent.[/bold yellow]")
        exit()

    elif response.status_code == 200:
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
                    print(f"[bold red]Erreur de parsing JSON pour le lien {link} : {e}[/bold red]")
                    links_of_all_volumes.append([])
            else:
                print(f"[bold red]Erreur de requête pour le lien {link} : {response.status_code}[/bold red]")
                links_of_all_volumes.append([])

        links_of_all_volumes = [[url.replace("http://", "https://") for url in sublist] for sublist in links_of_all_volumes]

        pairs = list(zip(volumes, links_of_all_volumes))

        user_input = input(f"Entrez la plage de volumes à télécharger (par exemple, pour tout télécharger : 1-{len(pairs)}) : ").strip()

        try:
            start, end = map(int, user_input.split('-'))
            if start < 1 or end > len(pairs) or start > end:
                raise ValueError("Plage invalide.")
        except ValueError:
            print(f"[bold red]Erreur : Veuillez entrer une plage valide au format DEBUT-FIN, et dans les limites disponibles, ici {len(pairs)}.[/bold red]")
            exit()

        selected_pairs = pairs[start-1:end]

        print(f"[bold green]Nombre de volumes à télécharger : {len(selected_pairs)}[/bold green]")
        print(f"[bold yellow]Téléchargement des volumes de {start} à {end}...[/bold yellow]")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for volume, images in selected_pairs:
                volume_folder = os.path.join(ROOT_FOLDER, title, volume)
                os.makedirs(volume_folder, exist_ok=True)
                number_len = ceil(log10(len(images)))
                for i, image_url in enumerate(images):
                    executor.submit(download_image, image_url, volume_folder, cookie_cf_clearance_value, user_agent, i, number_len)

        print("[bold green]Téléchargement terminé.[/bold green]")

    else:
        print(f"[bold red]La requête a échoué avec le code de statut : {response.status_code}[/bold red]")

if __name__ == "__main__":
    main()
