import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

def extract_pornhub_video(url):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'force_generic_extractor': False,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title'),
                'url': info.get('url'),
                'thumbnail': info.get('thumbnail'),
                'ext': info.get('ext'),
                'webpage_url': info.get('webpage_url'),
            }
    except Exception as e:
        print(f"[yt-dlp] Error: {e}")
        return None

def crawl(limit=30):
    url = "https://www.pornhub.com/video?o=tr"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    results = []

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.select('li.pcVideoListItem')
        for card in cards[:limit]:
            a_tag = card.select_one('a.linkVideoThumb')
            img_tag = card.select_one('img')

            if not a_tag or not img_tag:
                continue

            href = a_tag.get('href')
            if not href:
                continue

            video_page_url = f"https://www.pornhub.com{href.strip()}"
            yt_info = extract_pornhub_video(video_page_url)

            if yt_info and yt_info.get('url'):
                results.append({
                    'title': yt_info['title'],
                    'thumb': yt_info['thumbnail'],
                    'video': yt_info['url'],
                    'webpage_url': yt_info['webpage_url'],
                    'ext': yt_info['ext']
                })

    except requests.RequestException as e:
        print(f"[Pornhub Crawler] HTTP error: {e}")
    except Exception as e:
        print(f"[Pornhub Crawler] Parse error: {e}")

    return results