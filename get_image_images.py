import bs4
#from urllib.request import urlopen as uReq
import urllib.request
from bs4 import BeautifulSoup as soup
import time
import wget
import os
import sys

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

# Gets the base html of an url
def new_page (url):
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    response.close()
    page_soup = soup(data, "html.parser")
    return page_soup

################################

my_url = 'https://smite.gamepedia.com'
page_html = new_page(my_url)

# obtain a list of all gods
all_gods = page_html.findAll( 'div',attrs={'style':'display: inline-block;padding:1px;padding-right:10px'})
print ("TOTAL CURRENT GODS: " + str(len (all_gods)))

#access to script directory to download the image's tree
#print('sys.argv[0] =', sys.argv[0])
pathname = os.path.dirname(sys.argv[0])
print('Creating folders in', os.path.abspath(pathname))
os.chdir(pathname)

if not os.path.exists("Smite_Images"):
    os.mkdir("Smite_Images")
os.chdir("Smite_Images")

print ("Downloading images ...")
for x in all_gods:

    # obtain the god name
    god_name_html = x.find('span', attrs={'style': 'position:absolute; width:96px; height:96px; top:0; left: 0; z-index: 1;'}).find('a')
    god_name = god_name_html['title'].replace(" ", "_")

    #now open a new page of the current god
    god_html = new_page(my_url + "/" + god_name)
    god_img = god_html.findAll('img', attrs={'height': '512'})

    for x in god_img:
        image_path = x['src']
        image_name = image_path.split("?")[0].split("/")[-1].replace("T_", "")
        print (image_name)
        wget.download(image_path, image_name)
