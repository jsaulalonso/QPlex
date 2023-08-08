#!/usr/bin/env python3

import requests, json
from jinja2 import Environment, FileSystemLoader

PLEX_VERSIONS_URL = "https://plex.tv/api/downloads/5.json"

try:
    plex_info = requests.get(PLEX_VERSIONS_URL)
    if plex_info.status_code == 200:
        plex_qnap_info = plex_info.json()['nas']['QNAP']
        plex_version = '.'.join(plex_qnap_info['version'].split('.')[:3])
        for release in plex_qnap_info['releases']:
            if release['build'] == 'linux-aarch64':
                aarch64_url = release['url']
            elif release['build'] == 'linux-x86_64':
                x86_64_url = release['url']
        j2_template = Environment(loader=FileSystemLoader(".")).get_template("repo.xml.j2")
        with open('repo.xml', mode="w", encoding="utf-8") as repo_file:
            repo_file.write(j2_template.render(plex_version=plex_version, aarch64_url=aarch64_url, x86_64_url=x86_64_url))
except:
    print('ERROR')
#qnap_plex_info = requests.get(PLEX_VERSIONS_URL).json()

#print(qnap_plex_info['nas']['QNAP'])