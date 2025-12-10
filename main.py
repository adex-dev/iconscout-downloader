import os
import requests
from urllib.parse import urlparse

OUTPUT_DIR = "path_downloaders"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_url(link):
    path = urlparse(link).path
    last_part = path.split("/")[-1]
    name, id_ = last_part.rsplit("_", 1)
    return name, id_

def build_final_url(name, id_):
    return f"https://cdn3d.iconscout.com/3d/premium/thumb/{name}-png-download-{id_}.png"
def download_image(url, filename):
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()

        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        print(f"Downloaded: {filepath}")
    except Exception as e:
        print(f"Failed: {url} => {e}")

def process_txt(file_path):
    with open(file_path, "r") as f:
        for line in f:
            original_url = line.strip()
            if not original_url:
                continue

            name, id_ = parse_url(original_url)

            final_url = build_final_url(name, id_)
            filename = f"{name}_{id_}.png"

            download_image(final_url, filename)
            
def main():
    process_txt("urls.txt")
    
if __name__ == "__main__":
    main()