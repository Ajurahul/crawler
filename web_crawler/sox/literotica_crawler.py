import time

import requests
import parsel
from tqdm import tqdm
# Send request by simulated browser
headers = {
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
links=[]
#https://www.literotica.com/s/my-virgin-sister?page=2
#mainlink='https://www.literotica.com/top/Group-Sex-7'
mainlink = 'https://www.literotica.com/stories/favstoriesv2.php'
try:
 response = requests.get(mainlink, headers=headers)
except:
 print('will resume in 10 secc')
 time.sleep(10)
 try:
  response = requests.get(mainlink, headers=headers)
 except:
  print('error occured in link ' + mainlink)
response.encoding = response.apparent_encoding
html = response.text
sel = parsel.Selector(html)
#links=sel.css()
links=sel.css('p[class=type_title]  ::attr(href)').extract()
print(len(links))

for link in tqdm(links):
 contents = ''
 title=''
 contents+=link
 contents+="\n\n"
 for i in range(1, 100):
  #print(str(i))
  plink = link + '?page=' + str(i)

  #print(link)
  try:
   response = requests.get(plink, headers=headers)
  except:
   print('will resume in 10 secc')
   time.sleep(10)
   try:
    response = requests.get(plink, headers=headers)
   except:
    print('error occured in link ' + link)
  response.encoding = response.apparent_encoding
  html = response.text
  sel = parsel.Selector(html)

  if(i==1 or title==''):
   title=sel.css('h1 ::text').extract_first()
   #print(title)
   contents+=title

  texts = sel.css('div[class=aa_ht] ::text').extract()
  #print(texts)
  if (texts == []):
   break
  else:
   if(i>1):
    contents += "\n\n"
    contents += "Page  " + str(i) + "\n"
  for text in texts:
   contents += "\n"
   contents += text
 for key in ['\\', '/', ':', '?', '*', '<', '>', '|', '"']:
  title = title.replace(key, '')
 file = open('E:/novels/literotica/' + title + '.txt', mode='w', encoding='utf-8')
 file.write(contents)
 time.sleep(0.2)
 #print('write')
 file.close()

