
import pathlib
from typing import Iterable
from unittest import result
from urllib.parse import urljoin
from urllib.request import HTTPBasicAuthHandler
import requests
import re
from pathlib import Path
import json

from multiprocessing import Process
import os

from requests.auth import HTTPBasicAuth


BASE_URL = "https://ssr1.scrape.center"

def downloadPageHtml(pageNo:int)->str:
    fullUrl = f"{BASE_URL}/page/{pageNo}"
    html = requests.get(fullUrl).text
    return html

def parsePageHtml(html:str)->list[str]:
    # /detail/1
    ret = re.findall(r'<a.*href="(.*?)" class="name">',html)
    return ret

def parseDetail(detailUrl:str):
    detailHtml = requests.get(detailUrl).text
    coverUrl_pattern = re.compile(r'class="item.*?<img.*?src="(.*?)".*?class="cover"',re.DOTALL)
    coverUrl = coverUrl_pattern.search(detailHtml).group(1).strip()
    name = re.search(r'class="item.*?<h2.*?>(.*?)</h2>',detailHtml, re.DOTALL).group(1).strip()
    categories = re.findall(r'class=".*?category.*?<span>(.*?)</span>',detailHtml, re.DOTALL)
    score = re.search(r'class="score.*?>(.*?)</p>',detailHtml,re.DOTALL).group(1).strip()
    return {
        "cover":coverUrl,
        "name":name,
        "categories":categories,
        "score":score
    }



def parse(page:int):
    print(f"process: {os.getpid()}")
    html = downloadPageHtml(page)
    lists = parsePageHtml(html)
    detailLists= [ urljoin(BASE_URL, item) for item in lists]
    for detailUrl in detailLists:
        result = parseDetail(detailUrl)
        path = Path(f"{result['name']}.json")
        print(f"write text..{path.absolute()}")
        path.write_text(json.dumps(result, ensure_ascii=False,indent=None))
    pass

def main():
    for page in range(1,10):
        Process(target=parse, args=(page,), daemon=False).start()
      
            

def testReg():
    str="123\n456\n789"
    patternStr = r"\d*"
    print(str)
    match = re.findall(patternStr,str)
    print(match)
    pass


if __name__=="__main__":
    # main()
    # testReg()

    
    pass