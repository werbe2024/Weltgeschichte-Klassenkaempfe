import requests
import yaml
import os
import glob

def check_links(file_path):
    try:
        with open(file_path, 'r') as f:
            content = yaml.safe_load(f)
        sources = content.get('chapter', {}).get('sources', [])
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
                except requests.exceptions.RequestException as e:
                    report.append(f"⚠️ TIMEOUT: {url} (Fehler: {str(e)})")
        return "\n".join(report) if report else "Keine URLs zum Prüfen gefunden."
    except Exception as e:
        return f"❌ FEHLER beim Lesen von {file_path}: {str(e)}"

if __name__ == "__main__":
    # Erstelle den Output-Ordner, falls er nicht existiert
    os.makedirs("docs/output", exist_ok=True)

    # Suche alle YAML-Dateien im specs-Ordner
    spec_files = glob.glob("docs/specs/*.yml")
    if not spec_files:
        with open("docs/output/sources_report_ERROR.md", "w") as f:
            f.write("❌ FEHLER: Keine YAML-Dateien in `docs/specs/` gefunden!")
        raise FileNotFoundError("Keine YAML-Dateien in `docs/specs/` gefunden!")

    for spec_file in spec_files:
        print(f"Prüfe {spec_file}...")
        report = check_links(spec_file)
        output_file = f"docs/output/sources_report_{os.path.basename(spec_file)}.md"
        with open(output_file, "w") as f:
            f.write(f"# Quellenprüfung: {spec_file}\n\n{report}")
