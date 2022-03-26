import time
from tqdm import tqdm
import requests
import parsel
import mtranslate

"""Get page source code"""
# Send request by simulated browser
headers = {
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
chp_id=[]
def get_chpID(base_url):
 for i in range(1, 20):
  url = base_url+"/read_"+str(i)+".html"
  #print(url)
  response = requests.get(url, headers=headers)
  response.encoding = response.apparent_encoding
  html = response.text
  # Extract content from web pages
  sel = parsel.Selector(html)
  title = sel.css('h1::text').extract_first()
  id = sel.css('ul[class=read] ::attr(chapter-id)').extract()
  #print(str(id))
  if (id == []):
   break;
  for ind in id:
   chp_id.append(ind)

title=''
def get_chapter(base_url,id):
 response = requests.get(base_url+'/'+id+'.html', headers=headers)
 response.encoding = response.apparent_encoding
 html = response.text
 sel = parsel.Selector(html)
 title = sel.css('h1::text').extract_first()
 #print("Title:   " + str(title))
 contents = sel.css('div[class=content] ::text').extract()
 contents2 = []
 contents2.append("\n\n\n"+title)
 for content in contents:
  contents2.append(content.strip())
 return "\n".join(contents2)

def getbooknameDescr(main_url):
  response=requests.get(main_url,headers=headers)
  response.encoding=response.apparent_encoding
  html=response.text
  sel=parsel.Selector(html)
  name=sel.css('p[class=name]  ::text').extract_first()
  #print("Name   :"+str(name))
  description=sel.css('div[class=intro] ::text').extract_first()
  #print("Description   :"+description)
  name_descr=[name,description]
  return name_descr


#https://m.soxscc.net/book/HuoYingKaiJuRangSiDaiHuoYingZuoXuanZeTi.html
#base_url='https://m.soxscc.net/DaiZhuoShaYinQinLaoZhiFu'
f_url='https://m.soxscc.net/'
#url_code='HuoGeWoCiDiBianXingDaShi'
url_code=input('please enter the url code :')
base_url=f_url+url_code
main_url=f_url+'book/'+url_code+'.html'
get_chpID(base_url)
print('Total chapter available :'+str(len(chp_id)))
name_descr=getbooknameDescr(main_url)
name=name_descr[0]
descr=name_descr[1]
name=mtranslate.translate(name)+'__'+name
for key in ['\\', '/', ':', '?', '*', '<', '>', '|', '"']:
 name = name.replace(key, '')
print('Grabbing Novel: '+name)
file = open('D:/Novels/soxc/'+name+'.txt', mode='w', encoding='utf-8')



chp_text="\n\nBook name:  "+name+"\n\nDescription  : "+descr+"\n\n"
i=0
for index in tqdm(range (len(chp_id)),
               desc="Loading…",
               ascii=False, ncols=75):
 i=i+1
 try:
  text=get_chapter(base_url,chp_id[i-1])
 except:
  print('exception occured will try after 10 seconds')
  time.sleep(10)
  try:
   text = get_chapter(base_url, chp_id[i-1])
  except:
   print('error occured in chapter  :'+i )

 chp_text=chp_text+text

file.write(chp_text)
print('Completed..Stored in  folder and name :'+name)
file.close()



