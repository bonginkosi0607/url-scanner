import re
import sys
import requests
from bs4 import BeautifulSoup

link = "https://ftl.rf.gd/"
pages = set()
print("start")
def get_links(page_url):
    global pages
    pattern = re.compile("^(/)")
    html = requests.get(page_url).text
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        if "href" in link.attrs:
            if link.attrs["href"].split("#")[0] not in pages:
                new_page = link.attrs["href"]
                if new_page not in ["#"]:
                    if new_page[0] == "/":
                        if new_page.split("/")[0] == page_url.split("/")[2]:
                            t = page_url
                            pages.add(t  + "/" + new_page.split("?")[0])
                        elif "." not in new_page.split("/")[0] and not new_page.split("/")[0] == page_url.split("/")[2]:
                            t = page_url
                            pages.add(t  + "/" + new_page.split("?")[0])
                    elif new_page[0] + new_page[1] + new_page[2] == "htt":
                        if page_url.split("/")[2] == new_page.split("/")[2]:
                            pages.add(new_page.split("?")[0])
          
get_links(link)

full_pages = set()
print("second")
for page in pages:
    try:
        html = requests.get(page, allow_redirects=False).text
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a"):
            if "href" in link.attrs:
                if link.attrs["href"].split("#")[0] not in pages and link.attrs["href"].split("#")[0] not in full_pages:
                    new_page = link.attrs["href"]
                    if new_page not in ["#"]:
                        if new_page[0] == "/":
                            if new_page.split("/")[0] == link.split("/")[2]:
                                t = link
                                full_pages.add(t  + "/" + new_page.split("?")[0])
                            elif "." not in new_page.split("/")[0] and new_page.split("/")[0] != link.split("/")[2]:
                                t = link
                                pages.add(t  + "/" + new_page.split("?")[0])
                    elif new_page[0] + new_page[1] + new_page[2] == "htt":
                        if link.split("/")[2] == new_page.split("/")[2]:
                            full_pages.add(new_page.split("?")[0])
    except:
        continue



print("third")
if len(pages) == 0:
    print("Was not able to get any links")
    sys.exit()

if len(full_pages) == 0:
    full_pages = pages
else:
    full_pages.union(pages)


def isatt(bs, attr):
     try:
         bs.attrs[attr]
         return True
     except KeyError:
         return False


website = dict()

for page in full_pages:
    soup = BeautifulSoup(requests.get(page, allow_redirects=False).text, "html.parser")
    metas = soup.find_all("meta")
    web = dict()
    try:
        web["title"] = soup.head.title.text.strip()
    except:
        talk = None
    for meta in metas:
        # property
        if isatt(meta, "property"):
            if meta.get('property') == "og:site_name":
                if isatt(meta, "content"):
                    web["site_name"] = meta.get('content') 
                    
        # name
        if isatt(meta, "name"):
            if meta.attrs['name'] == "viewport":
                if isatt(meta, "content") and meta.get('content') == "width=device-width, \
                initial-scale=1.0, maximum-scale=1.0, user-scalable=0":
                    web["responsive"] = meta.get('true') 
            if meta.get('name') == "description":
                if isatt(meta, "content"):
                    web["description"] = meta.get('content').replace("'", "\\'")  
            if meta.get('name') == "keywords":
                if isatt(meta, "content"):
                    web["keywords"] = meta.get('content')  
            if meta.get('name') == "shortcut icon":
                if isatt(meta, "href"):
                    web["shortcut icon"] = meta.get('content')
    website[page] = web
print("done")

print(str(website))
        
