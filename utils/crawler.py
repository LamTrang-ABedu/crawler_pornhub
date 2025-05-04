import requests
from bs4 import BeautifulSoup
import boto3
import json
import os

R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_BUCKET_NAME = 'hopehub-storage'

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY')
    )

def crawl(source="pornhub", max_pages=100):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    existing = load_existing_media(source)
    existing_urls = set(item["video"] for item in existing)
    results = existing.copy()

    for page in range(1, max_pages + 1):
        url = f"https://www.pornhub.com/video?o=tr&page={page}"
        print(f"[Crawl] Page {page}: {url}")

        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')

            cards = soup.select('li.pcVideoListItem')
            if not cards:
                break  # Không còn kết quả

            for card in cards:
                a_tag = card.select_one('a.linkVideoThumb')
                img_tag = card.select_one('img')

                href = a_tag.get('href') if a_tag else ''
                if not href or 'viewkey=ph' not in href:
                    continue

                full_url = f"https://www.pornhub.com{href.strip()}"
                if full_url in existing_urls:
                    print(f"[Crawl] Already exists: {full_url}")
                    continue  # Bỏ qua nếu đã có

                thumb = img_tag.get('data-thumb_url') or img_tag.get('src') or ''
                title = img_tag.get('alt') or 'Pornhub Clip'

                if thumb:
                    print(f"[Crawl] Found: {full_url} - {title.strip()}")
                    results.append({
                        "thumb": thumb.strip(),
                        "video": full_url,
                        "title": title.strip()
                    })
                    existing_urls.add(full_url)

        except Exception as e:
            print(f"[Crawl Error] Page {page}: {e}")
            break

    return results

def load_existing_media(source='pornhub'):
    try:
        r2_client = get_s3_client()
        obj = r2_client.get_object(
            Bucket=R2_BUCKET_NAME,
            Key=f"MEDIA/{source}_media.json"
        )
        content = obj['Body'].read()
        return json.loads(content)
    except Exception:
        return []  # Nếu chưa có file

def upload_media_list(media, source):
    try:
        r2_client = get_s3_client()
        r2_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=f"MEDIA/{source}_media.json",
            Body=json.dumps(media, indent=2).encode('utf-8'),
            ContentType='application/json'
        )
        print(f"[Upload] Successfully uploaded {source}_media.json")
    except Exception as e:
        print(f"[Upload] Failed to upload to R2: {e}")