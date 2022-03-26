# -*- coding: utf-8 -*-
import requests
import parsel
"""Crawl a chapter of a novel"""
# Request web data
headers = {
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
response = requests.get('https://m.soxscc.net/DaiZhuoShaYinQinLaoZhiFu/63227.html', headers=headers)
response.encoding = response.apparent_encoding
html = response.text
print(html)
# Extract content from web pages
sel = parsel.Selector(html)
title = sel.css('h1::text').extract_first()
print("headline"+str(title))
contents =sel.css('div[class=content] ::text').extract()
#contents = sel.css('p::text').extract() for all
contents2 = []
for content in contents:
 contents2.append(content.strip())
#print("contents")
#print(contents2)
print(contents2)
print("new line")
print("\n".join(contents2))
# Write content to text
#with open(title+'.txt', mode='w', encoding='utf-8') as f:
 #f.write("\n".join(contents2))