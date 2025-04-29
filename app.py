from utils.crawler import crawl
from utils.r2_manager import upload_media_list
import threading
import time

def crawler_cycle():
    while True:
        print("[MediaCrawler] Start crawling pornhub...")
        media_list = crawl()
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
