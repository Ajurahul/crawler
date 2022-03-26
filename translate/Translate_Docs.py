#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm


# In[2]:


path=input("Paste Path to folder needing translation: ") #add folder
os.chdir(path)
file_name=['\\'+f for f in os.listdir() if f.endswith(".docx")]
complete_name=[]
for f in file_name:
    complete_name.append([os.path.abspath(os.getcwd())+f,False])


# In[1]:


download_loc=os.path.join(os.getcwd(), "Translated")
if not os.path.exists(download_loc):
    os.makedirs(download_loc)
#os.mkdir(os.path.join(os.getcwd(), "Translated"))
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : download_loc} # you can also type path for downloading translated files
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe",chrome_options=chrome_options)


# In[5]:



driver.get("https://translate.google.com/?sl=zh-CN&tl=en&op=docs") #google translate doc url


# In[ ]:


for path in tqdm(complete_name,desc="Translating"):
    if path[1]==False:
        file = driver.find_element(by=By.NAME, value='file')
        file.send_keys(path[0])
        translate = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div[2]/c-wiz/div[3]/c-wiz/div[2]/c-wiz/div/div[1]/form/div[2]/div[2]/div/button[1]').click()
        download_button = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div[2]/c-wiz/div[3]/c-wiz/div[2]/c-wiz/div/div[1]/form/div[2]/div[2]/div/button[2]')
        wait = WebDriverWait(driver, 30)
        try: #try catch because some file google translate might not translate 
            element = wait.until(EC.element_to_be_clickable(download_button)) #try catch because some file google translate might not translate 
            element.click()
            path[1]=True
            driver.refresh()
        except:
            driver.refresh()
        
        
        


# In[ ]:




