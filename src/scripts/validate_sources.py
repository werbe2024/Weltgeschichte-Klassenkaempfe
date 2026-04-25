import requests
import yaml
import os
import glob

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

if __name__ == "__main__":
    # Prüfe ALLE YAML-Dateien im specs-Ordner
    os.makedirs("docs/output", exist_ok=True)
    for spec_file in glob.glob("docs/specs/*.yml"):
        print(f"Prüfe {spec_file}...")
        report = check_links(spec_file)
        output_file = f"docs/output/sources_report_{os.path.basename(spec_file)}.md"
        with open(output_file, "w") as f:
            f.write(f"# Quellenprüfung: {spec_file}\n\n{report}")
