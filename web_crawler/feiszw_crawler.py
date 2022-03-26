import time

import requests
import parsel
import mtranslate

"""Get page source code"""
# Send request by simulated browser
headers = {
 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'

}
traslator=mtranslate
link_base ='https://www.feiszw.com/Html/'
code='30256'
index_url=link_base+code+'/index.html'
print(index_url)
response = requests.get(index_url,headers=headers)
response.encoding = response.apparent_encoding
html = response.text
#print(html)
sel= parsel.Selector(html)
title=sel.css('title  ::text').extract_first()
title=traslator.translate(title)
#print('title'+title)
descrip=sel.css('div[class=intro]  ::text').extract()
description=''
for descr in descrip:
 description+=descr
#print('Description :'+description)
first_chp=sel.css('div[class=chapterlist] ::attr(href)').extract_first()
#print(str(first_chp))
content=''
content+=title
content+="\n\nDescription   :"+description+"\nLink   :"+index_url
content+="\n------------------------------------------------------------------------------------------------------------"
chp_url=link_base+code+'/'+first_chp
#print(chp_url)
i=0
print('Crawling chapters....')
try:
 while True:
  i += 1
  #print('\x1b[1A\x1b[2K')
  if(i%50==0):
   print()
  print(i,end=" ")
  # if(i%10==0):
  # time.sleep(2)
  try:
   response = requests.get(chp_url, headers=headers)
  except:
   print('error occured trying in 4sec')
   time.sleep(4)
   try:
    response = requests.get(chp_url, headers=headers)
   except:
    print('Again error occured..Stopping the program')
  response.encoding = response.apparent_encoding
  html = response.text
  print(html)
  sel = parsel.Selector(html)
  chp_name = sel.css('div[class=nr_title] ::text').extract_first()
  # print(chp_name)
  content += "\n" + chp_name
  chp_list = sel.css('div[id=nr1] ::text').extract()
  # print(str(chp_list))
  chp_text = ''
  if (chp_list == []):
   print(html)
   print('error occured in link ' + chp_url + 'chp no: ' + i)
   break
  for chp in chp_list:
   if (chp == '请收藏本站阅读最新小说 m.feiszw.com' or chp == '飞速中文唯一官网:feiszw.com 备用域名：feixs.com'):
    time.sleep(0.2)
   else:
    chp_text += chp
    chp_text += "\n"
  print(chp_text)
  content += "\n" + chp_text
  content += "-------------------------------------------------------------------------------------------------------------"
  next_chp = sel.css('div[id=nr_botton] ::attr(href)').extract()
  next_chp = next_chp[2]
  chp_url = link_base + next_chp
  # print(chp_url)
  if (chp_url == index_url):
   break
except Exception as e:
 print('error occured :'+e)
for key in ['\\', '/', ':', '?', '*', '<', '>', '|', '"']:
 title = title.replace(key, '')

file = open('D:/Novels/soxc/' + title + '.txt', mode='w', encoding='utf-8')
file.write(content)
file.close()
