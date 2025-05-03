import requests
from bs4 import BeautifulSoup

def crawl(limit=300):
    url = "https://www.pornhub.com/video?o=tr"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.select('li.pcVideoListItem')
        results = []

        for card in cards[:limit]:
            a_tag = card.select_one('a.linkVideoThumb')
            img_tag = card.select_one('img')

            if not a_tag or not img_tag:
                continue

            href = a_tag.get('href')
            if not href:
                continue

            thumb = img_tag.get('data-thumb_url') or img_tag.get('src') or ''
            title = img_tag.get('alt') or 'Pornhub Clip'

            # Validate trước khi thêm vào kết quả
            if thumb and href:
                results.append({
                    "thumb": thumb.strip(),
                    "video": f"https://www.pornhub.com{href.strip()}",
                    "title": title.strip()
                })

        return results

    except requests.RequestException as e:
        print(f"[Pornhub Crawler] HTTP error: {e}")
    except Exception as e:
        print(f"[Pornhub Crawler] Parse error: {e}")

    return []