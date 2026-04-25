import requests
from bs4 import BeautifulSoup
import yaml
import os

def check_links(file_path):
    with open(file_path, 'r') as f:
        content = yaml.safe_load(f)
    sources = content['chapter']['sources']
    report = []
    for source in sources:
        url = source.get('url')
        if url:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    report.append(f"✅ OK: {url}")
                else:
                    report.append(f"❌ FEHLER: {url} (HTTP {response.status_code})")
            except:
                report.append(f"⚠️ TIMEOUT: {url}")
    return "\n".join(report)

# Beispielaufruf für band1_kapitel1.yml
if __name__ == "__main__":
    print(check_links("docs/specs/band1_kapitel1.yml"))
