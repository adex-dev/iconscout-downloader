import os
import requests
from urllib.parse import urlparse
import json


OUTPUT_DIR = "path_lottie"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_url(link):
    path = urlparse(link).path
    last_part = path.split("/")[-1]
    name, id_ = last_part.rsplit("_", 1)
    return name, id_,path

def build_final_url(path_):
    try:
        url = "https://node.api.freeanimationdownloader.com/scrape"
        payload = {
            "url": "https://iconscout.com" +path_
        }
        headers = {
            "Content-Type": "application/json",
            "Origin": "https://freeanimationdownloader.com",
            "Referer": "https://freeanimationdownloader.com/",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        data = response.json()
        return data["links"]["original"]

    except Exception as e:
      print(f"Failed: {path_} => {e}")

def download_image(url, filename):
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()

        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    except Exception as e:
        print(f"Failed: {url} => {e}")

def process_txt(file_path):
      with open(file_path, "r") as f:
        for line in f:
            original_url = line.strip()
            if not original_url:
                continue

            name, id_,_path = parse_url(original_url)

            final_url = build_final_url(_path)
            filename = f"{name}.json"

            download_image(final_url, filename)

            
def main():
    process_txt("lottie.txt")
    
if __name__ == "__main__":
    main()