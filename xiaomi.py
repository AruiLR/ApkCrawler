# -*- coding:utf-8 -*-
import requests
import time
import os
import sys
from bs4 import BeautifulSoup
import urllib
from urllib import urlretrieve
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def getsource(url): # crawl page
    html = requests.get(url).text
    return html
def get_href(root_url): # return all urls of every category range page one from last page
    category_url_dict={} #{category name:url}
    html_doc=getsource(root_url)
    soup=BeautifulSoup(html_doc,'html.parser')
    category_tag=soup.find(class_='category-list')
    for child in category_tag.children: #get url of all categories
        href_tag=child.find('a')
        category_name=child.get_text()
        category_string=href_tag.get('href')
        category_url=root_url+category_string
        category_url_dict[category_name]=category_url
    return category_url_dict
def report(count, blockSize, totalSize): # show download progress
  percent = int(count*blockSize*100/totalSize)
  sys.stdout.write("\r%d%%" % percent + ' complete')
  sys.stdout.flush()
def auto_redown(download_link,apk_path):
    try:
        urlretrieve(download_link, apk_path, reporthook=report)
    except urllib.ContentTooShortError:
        print 'Network conditions is not good. Reloading.'
        auto_redown(download_link,apk_path)
    sys.stdout.write("\rDownload complete, saved as %s" % (apk_path) + '\n\n')
    sys.stdout.flush()
def get_apk(root_url,url_dict,save_path):# root_url: address of market; url_dict:{category name:category url};save_path:where to save APKs
    conn = redis.Redis(host='localhost', port=6379)
    for category_name in url_dict:
        apk_info={} #save apk information : {name:[vendor,downlink,pubkey]}
        new_path=os.path.join(save_path,category_name)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        category_url = url_dict[category_name]
        options=Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver=webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=options)
        driver.get(category_url)
        url_list = []  # save the url of download page
        for page_num in range(67):# page number no more than 67
            category_html_doc=driver.page_source
            category_soup = BeautifulSoup(category_html_doc, 'html.parser')
            applist_tag = category_soup.find(id='all-applist')
            if (len(applist_tag.contents) != 0):
                for child1 in applist_tag.children:
                    download_page_href = child1.find('a').get('href')
                    download_page_url = root_url + download_page_href
                    url_list.append(download_page_url)
            else:
                break
            try:
                driver.find_element_by_link_text(u"下一页").click()
                driver.set_page_load_timeout(10)
                time.sleep(1.5)
            except:
                break
        driver.quit()
        for url in url_list:
            download_page_doc=getsource(url)
            download_page_soup=BeautifulSoup(download_page_doc)
            apk_name_tag=download_page_soup.find(class_='intro-titles')
            if apk_name_tag!=None:
                apk_name=apk_name_tag.contents[1].get_text()
                vendor_name=apk_name_tag.contents[0].get_text()
                apk_path = os.path.join(new_path, apk_name)
                download_link=root_url+download_page_soup.find(class_='app-info-down').find('a').get('href') #download link
                if os.path.exists(apk_path):
                    print apk_name+" has been downloaded. Download next one"
                    continue
                print "Downloading " + apk_name + '(' + vendor_name + ')' + '-----------------------'
                try:
                    auto_redown(download_link,apk_path)
                except:
                    continue
if __name__=='__main__':
    root_url='http://app.mi.com'
    save_path='#'
    name_url_dict=get_href(root_url)
    get_apk(root_url,name_url_dict,save_path)
