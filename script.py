import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_website(url, domain):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    visited = set()
    to_visit = [url]
    written = set()

    with open('new-handyman.txt', 'w') as f:
        while to_visit:
            url = to_visit.pop(0)
            if url in visited:
                continue
            visited.add(url)

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            for tag in soup.find_all(True):
                if tag.name == 'a':
                    link = urljoin(url, tag.get('href'))
                    # Skip mailto links
                    if 'mailto:' in link:
                        continue
                    if domain in link and link not in visited:
                        to_visit.append(link)
                elif tag.string:
                    line = tag.string.strip()
                    if line and line not in written:
                        f.write(line + '\n')
                        written.add(line)

scrape_website('https://handymanconnection.com', 'handymanconnection.com')