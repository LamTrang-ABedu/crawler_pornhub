import requests
from bs4 import BeautifulSoup
              
def crawl(limit=30):
    try:
        url = "https://www.pornhub.com/video?o=tr"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        cards = soup.select('li.pcVideoListItem')
        results = []
        for card in cards[:limit]:
            a_tag = card.select_one('a.linkVideoThumb')
            img_tag = card.select_one('img')
            if a_tag and img_tag:
                video_link = "https://www.pornhub.com" + a_tag['href']
                thumb = img_tag.get('data-thumb_url') or img_tag.get('src')
                title = img_tag.get('alt', 'Pornhub Clip')
                results.append({
                    "thumb": thumb,
                    "video": video_link,
                    "title": title
                })
        return results
    except Exception as e:
        print(f"[Error] Crawl pornhub failed: {e}")
        return []
