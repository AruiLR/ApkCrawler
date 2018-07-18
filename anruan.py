# -*- coding:utf-8 -*-
import requests
import time
import os
import sys
from bs4 import BeautifulSoup
import urllib
from urllib import urlretrieve
def report(count, blockSize, totalSize):
    # Show download progress
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("\r%d%%" % percent + ' complete')
    sys.stdout.flush()
def auto_down(download_link,apk_path):
    try:
        urlretrieve(download_link, apk_path, reporthook=report)
    except urllib.ContentTooShortError:
        print 'Network conditions is not good. Reloading.'
        auto_redown(download_link,apk_path)
    sys.stdout.write("\rDownload complete, saved as %s" % (apk_path) + '\n\n')
    sys.stdout.flush()
def getapk(r_url,save_path):
    page_num=1
    flag=True
    url_list=[]
    while(flag):
        new_url=r_url+'index_'+str(page_num)+'.html'
        html_doc=requests.get(new_url).text
        soup=BeautifulSoup(html_doc,'html.parser')
        app_list_tag=soup.find(class_='liswrap')
        for li in app_list_tag.contents[1].contents:
            if li.find('a')!=-1:
                apk_url=li.find('a').get('href')
                url_list.append(apk_url)
            if soup.find(class_='next')!=None:
                page_num+=1
            else:
                flag=False
    for url in url_list:
        apk_html = requests.get(url).text
        apk_soup = BeautifulSoup(apk_html, 'html.parser')
        app_info_tag = apk_soup.find(class_='info_L')
        app_name_tag = app_info_tag.contents[1].contents[1]
        apk_name=app_name_tag.get_text().split(' ')[0]
        download_link_tag=apk_soup.find(class_='btn az_btn ')
        download_link=download_link_tag.find('a').get('href')
        apk_path = os.path.join(new_save_path, apk_name)
        if os.path.exists(apk_path):
            print apk_name + " has been downloaded. Download next one"
            continue
        print "Downloading " + apk_name + '-----------------------'
        try:
            auto_down(download_link, apk_path)
        except:
            continue
if __name__=='__main__':
    root_url_list=['https://soft.anruan.com/new/','https://game.anruan.com/gnew/']
    save_path='/home/rliu/APK/Anruan'
    for root_url in root_url_list:
        getapk(root_url,save_path)