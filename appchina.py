# -*- coding:utf-8 -*-
import requests
import time
import os
import sys
from bs4 import BeautifulSoup
import urllib
from urllib import urlretrieve
def report(count, blockSize, totalSize): # show download progress
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
def getapk(r_url,catedict,save_path):
    for category_num in catedict:
        apk_info={}
        apk_url_list=[]
        page_num=1
        flag=True
        category_name=catedict[category_num]
        print 'Processing ' + category_name +', it may take a few minutes'
        new_save_path = os.path.join(save_path, category_name)
        if not os.path.exists(new_save_path):
            os.makedirs(new_save_path)
        while(flag):
            print "Processing page "+str(page_num)
            new_url=r_url+'/category/'+str(category_num)+'/'+str(page_num)+'_1_1_3_0_0_0.html'
            html_doc=requests.get(new_url).text
            soup=BeautifulSoup(html_doc,'html.parser')
            app_list_tag=soup.find_all(class_='app-info')
            for app_info in app_list_tag:
                href_tag=app_info.contents[1].find('a')
                apk_href=href_tag.get('href')
                apk_url=r_url+apk_href
                apk_url_list.append(apk_url)
            if soup.find(class_='next')!=None:
                page_num+=1
            else:
                flag=False
        for url in apk_url_list:
            apk_html=requests.get(url).text
            apk_soup=BeautifulSoup(apk_html,'html.parser')
            apk_name_tag = apk_soup.find(class_='app-name')
            apk_name = apk_name_tag.get_text()
            download_link_tag = apk_soup.find(class_='download_app')
            download_str = download_link_tag.get('onclick')
            pattern = re.compile("'(.*)'")
            download_link=pattern.findall(download_str)[0]
            apk_path=os.path.join(new_save_path,apk_name)
            if os.path.exists(apk_path):
                print apk_name+" has been downloaded. Download next one"
                continue
            print "Downloading " + apk_name + '-----------------------'
            try:
                auto_down(download_link,apk_path)
            except:
                continue
if __name__=='__main__':
    root_url='http://www.appchina.com'
    save_path='/home/rliu/APK/AppChina'
    category_dict={301:u'输入法',302:u'浏览器',303:u'动态壁纸',304:u'系统工具',305:u'便捷生活',306:u'影音播放',307:u'通话通讯',308:u'社交网络',
                   309:u'主题插件',310:u'拍摄美化',311:u'新闻资讯',312:u'图书阅读',313:u'学习办公',314:u'网购支付',315:u'金融理财',411:u'益智游戏',
                   412:u'射击游戏',413:u'策略游戏',414:u'动作冒险',415:u'赛车竞速',416:u'模拟经营',417:u'角色扮演',418:u'体育运动',419:u'棋牌桌游',
                   420:u'虚拟养成',421:u'音乐游戏',422:u'对战格斗',424:u'手机网游'}
    getapk(root_url,category_dict,save_path)