import re
import requests
from bs4 import BeautifulSoup


def clean_title(title):
    # Remove invalid characters from the title and replace them with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', title)

def scrape_page_content(url):
    # try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            divs = soup.find_all("div")
            # paragraphs = soup.find_all('p')
            # spans = soup.find_all("span")
            # lis = soup.find_all("li")
            # h1s = soup.find_all("h1")
            # h2s = soup.find_all("h2")


            content = '\n'.join(div.get_text() for div in divs)
            # content += '\n'.join(paragraph.get_text() for paragraph in paragraphs)
            # content += '\n'.join(span.get_text() for span in spans)
            # content += '\n'.join(li.get_text() for li in lis)
            # content += '\n'.join(h1.get_text() for h1 in h1s)
            # content += '\n'.join(h2.get_text() for h2 in h2s)
            clean_content = []
            for c in content.split('\n'):
                if c in clean_content:
                    continue
                else:
                    clean_content.append(c)

            content = re.sub('\n+', '\n', re.sub(r'[ \t]+', ' ','\n'.join(clean_content))).strip().replace('\n ','\n').replace('\n\n', '\n')

            return content
        else:
            print(f"\tFailed to fetch {url}")
            return None
    # except:
    #     scrape_page_content(url[1:])

def scrape_page_and_subpages_content(url, main_content=True, timeout=30):
    """
    Scrapes the text content of a webpage and optionally its sub-links recursively.

    Args:
      url: The URL of the page to scrape.
      main_content: Boolean indicating whether to scrape the main content of the page.
      timeout: The maximum time to wait for a response in seconds (default: 10).

    Returns:
      A dictionary containing the combined text content of the page and its sub-links.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"\tFailed to fetch {url}: {e}")
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract content from current page
        content = {}
        if main_content:
            content[url] = {'content': scrape_page_content(url), 'main_content': True, 'link_no': 0}
            print(f"\t{0} - Scraped main-content from {url}")

        # Extract and recursively scrape sub-links
        sub_links = list({a['href'] for a in soup.find_all('a', href=True) if 'facebook' not in a['href']})
        print(f' ({len(sub_links)} links)')
        for i, sub_link in enumerate(sub_links):
            try:
                sub_content = scrape_page_content(sub_link)
                if sub_content:
                    content[sub_link] = {'content': sub_content, 'main_content': False, 'link_no': i+1}
                    print(f"\t{i+1} - Scraped sub-content from {sub_link}")
            except:
                sub_link = '/'.join(url.split('/')[:-1]) + sub_link
                try:
                    sub_content = scrape_page_content(sub_link)
                    if sub_content:
                        content[sub_link] = {'content': sub_content, 'main_content': False, 'link_no': i+1}
                        print(f"\t{i+1} - Scraped sub-content from {sub_link}")
                except:
                    print(f"\t{i+1} - Failed to scrape sub-content from {sub_link}")
        return content, len(sub_links)

    else:
        print(f"\tFailed to fetch {url}")
        return None
        



