'''
Created on 2020/09/03

@author: DXG
'''

import requests
import concurrent.futures
import traceback


class CustomException(Exception):
    def __init__(self, url):
        self.url = url 
        
        
def get_wiki_page_existence(key, wiki_page_url):
    accessible = True
    msg = ""
    try:
        requests.head(url=wiki_page_url, timeout=60) # 60 seconds
    except requests.ConnectTimeout:
        print("ConnectTimeout: ", wiki_page_url)
        msg = f"ConnectTimeout: {wiki_page_url}"
        accessible = False
    except Exception:
        print("Exception: ", wiki_page_url)
        msg = f"Exception: {wiki_page_url}\n"
        msg = msg + traceback.format_exc()
        accessible = False 
    return key, accessible, msg



def run_thread(wiki_page_urls):
    wiki_page_urls_dict = {}
    for key, page_url in enumerate(wiki_page_urls):
        if 'http://' in page_url:
            page_url = page_url.replace('http://','')
        if 'https://' in page_url:
            page_url = page_url.replace('https://','')
        wiki_page_urls_dict[key] = {"url": page_url, "accessible": ""}
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = []
        for url_key, data in wiki_page_urls_dict.items():
            futures.append(
                executor.submit(get_wiki_page_existence, url_key, "http://" + str(data["url"]))
            )
        print(len(futures))
        for future in concurrent.futures.as_completed(futures):
            try:
                print(future.result())
                url_key, accessible, msg = future.result()
                wiki_page_urls_dict[url_key]["accessible"] = accessible
            except:
                print(traceback.format_exc())
    print("end thread ")            
    return wiki_page_urls_dict                          