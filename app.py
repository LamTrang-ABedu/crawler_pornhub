from utils.crawler import crawl, upload_media_list
import threading
import time
from flask import Flask

app = Flask(__name__)

def crawler_cycle():
    while True:
        print("[MediaCrawler] Start crawling pornhub...")
        media_list = crawl(source='pornhub', max_pages=100)
        if media_list:
            print("[MediaCrawler] Uploading media...")
            upload_media_list(media_list, source='pornhub')
        else:
            print("[MediaCrawler] No media crawled.")
        print("[MediaCrawler] Sleep 4 hours...")
        time.sleep(14400)  # 4 tiếng crawl lại

if __name__ == "__main__":
    threading.Thread(target=crawler_cycle).start()
    app.run(host="0.0.0.0", port=8000)
