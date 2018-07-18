# Introduction
  This is a APK crawler which is used to automatically download lots of android applications from several application markets, such as xiaomi, anruan, appchina.
# Dependencies
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 
* [Selenium](https://pypi.org/project/selenium/)
# Details
  BeautifulSoup is a Python library for parsing static html files to extract page elements, which is less effective for getting elements loaded dynamically such as js event. We used Selenium to simulate browser behaviors to handle dynamic page.
  ```
  from selenium import webdriver
  from selenium.webdriver.chrome.options import Options
  
  # add arguments to control browser behaviors
  
  options=Options()
  options.add_argument('--headless')  # no need GUI, use driver of browser
  options.add_argument('--no-sandbox') 
  driver=webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=options)
  driver.get(url)
  html_doc=driver.page_source
  ...
  
  driver.find_element_by_link_text(u"下一页").click() #simulate browser to click the "next" button to next page
  driver.quit()
  ```
  
