import requests
from bs4 import BeautifulSoup
import os
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def download_mp3(word, retries=3):
    base_url = "https://dictionary.cambridge.org"
    search_url = f"{base_url}/us/dictionary/english/{word}"
    
    for attempt in range(retries):
        try:
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}: Failed to retrieve the page for {word}: {e}")
            if attempt == retries - 1:
                return
            time.sleep(2)  # Wait before retrying

    soup = BeautifulSoup(response.content, "html.parser")
    mp3_url = None
    
    for audio_tag in soup.find_all("source", {"type": "audio/mpeg"}):
        mp3_url = audio_tag["src"]
        break
    
    if not mp3_url:
        print(f"No MP3 found for {word}")
        return
    
    mp3_url = base_url + mp3_url
    
    for attempt in range(retries):
        try:
            response = requests.get(mp3_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}: Failed to download MP3 for {word}: {e}")
            if attempt == retries - 1:
                return
            time.sleep(2)  # Wait before retrying
    
    with open(f"{word}.mp3", "wb") as f:
        f.write(response.content)
    print(f"Downloaded pronunciation for {word}")

def main():
    if not os.path.exists("pronunciations"):
        os.makedirs("pronunciations")
    
    os.chdir("pronunciations")
    
    while True:
        words = input("Enter vocabulary words separated by commas (or type 'q' to quit): ")
        if words.lower() == 'q':
            break
        words = [word.strip() for word in words.split(',')]
        for word in words:
            download_mp3(word)
            time.sleep(1)  # Adding a small delay to avoid overwhelming the server

if __name__ == "__main__":
    main()
