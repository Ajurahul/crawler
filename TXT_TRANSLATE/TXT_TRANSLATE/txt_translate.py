import sys
import os
import time
import requests
import json
import re
from bs4 import BeautifulSoup
# from parsel import Selector

# googleTranslateTKK = "448487.932609646"
googleTrans = "https://translate.googleapis.com/translate_a/t?anno=3&client=te&v=1.0&format=html&sl={}&tl={}&tk={}"
headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
class txt_translate:
    def initialisation (self):
        try:
            
            
            self.novel_name = input("WRITE NOVEL NAME: ")
            if not self.novel_name :
                self.novel_name="NOVEL"
            for key in ['\\','/',':','?','*','<','>','|','"']:
                self.novel_name = self.novel_name.replace(key,'')

            self.start = input("START NUMBER: ")
            if not self.start :
                self.start = 1
            else:
                self.start = int(self.start)
             
            self.end = input("END NUMBER: ")
            if not self.end :
                self.end = 1
            else:
                self.end = int(self.end)

            self.src = input("SOURCE LANGUAGE : ").lower()
            if not self.src :
                self.src = 'auto'


            self.dest = input("DESTINATION LANGUAGE : ").lower()
            if not self.dest :
                self.dest = 'en'

            self.type = input("TXT OR HTML (DEFAULT = TXT): ").lower()
            if not self.type :
                self.type="txt"
            if self.type == "txt":
                self.single_file = input("SINGLE FILE??: (Y/N)(DEFAULT=N): ").lower()
                if not self.type :
                    self.type="n"
            

            header = open("required/header.txt", "r")
            self.header = header.read()
            header.close()

            footer = open("required/footer.txt", "r")
            self.footer = footer.read()
            footer.close()

            style = open("required/style.css", "r")
            self.style = style.read()
            style.close()

            self.document_creating()
            self.translate_loop()
            if self.single_file == "y":
                os.chdir("../translated_novel/" + self.novel_name)
                new_file = open(self.novel_name + ".txt", "w",encoding="utf-8")
                new_file.write(self.single_txt)
                new_file.close()
            print("")
            print("DONE!!")
            print("THANK FOR USING OUR PRODUCT")
        except Exception as e:
            print("ERROR ENTRING LIGHT NOVEL")
            print(e)

    def document_creating(self):
        print("CREATING DOCUMENT...")
        try:
            if not os.path.exists('translated_novel'):
                os.mkdir('translated_novel')
            os.chdir('translated_novel')
            i = 2
            while True:
                if os.path.exists(self.novel_name):
                    if i == 2:
                        self.novel_name = self.novel_name  + "-" + str(i)
                    else:
                        self.novel_name = self.novel_name [:-1 * (len(str(i)) + 1)]  + "-" + str(i)
                    i += 1
                else:
                    os.mkdir(self.novel_name)
                    os.chdir(self.novel_name)
                    break
            if self.type == "html":
                style = open("style.css", "w",encoding="utf-8")
                style.write(self.style)
                style.close()

            print("CREATING SUCCESSFULLY")
            os.chdir("../../txt_files")
        except Exception as e:
            print("ERROR CREATING DOCUMENT")
            print("CLOSING...")
            print(e)
            sys.exit()

    def translate_loop(self):
        self.progress_bar_header()
        range_bar = 0
        range_text = 3000
        self.single_txt= ""
        if self.end == self.start :
            range_bar_unit = 50 
        else:
            range_bar_unit = 50 / (self.end - self.start)

            

        for i in range(self.start,self.end + 1):
            range_bar += range_bar_unit
                
            self.txt = ""
            self.temp_txt = ""
            self.txt_formdata = "q"
                    
            self.translate(i,range_text)

            current_message = str(i) + "/" + str(self.end )
            sys.stdout.write(" " * (self.progress - 1) + "|" + current_message + " ")
            sys.stdout.write("\b" * (self.progress + len(current_message) + 1))
                
            sys.stdout.flush()

            for j in range(int(range_bar)):
                self.progress_bar_animated()
                range_bar-= 1
        sys.stdout.write("|\n")
    def translate(self,i,range_text):
        try:
            txt = open("CHAPTER-" + str(i) + ".txt", "r",encoding="utf-8")
            txt_read = txt.read()
            txt_read_lenght = len(txt_read)
            txt.seek(0)
            if txt_read_lenght > range_text:
                for line in txt:
                    if line == '\n':
                        self.temp_txt += ""
                        self.txt_formdata += "&q"
                    else:
                        self.temp_txt += "<pre>" + line[:-1] + "</pre>"
                        self.txt_formdata += "&q=%3Cpre%3E%" + "%".join(re.findall('..',line[:-1].encode("utf-8").hex())) + "%3C%2Fpre%3E"

                    if len(self.temp_txt) > range_text:
                        self.Hash = requests.post("http://localhost:14756/",data ={'text':self.temp_txt} ).text
                        translated_txt = requests.post(googleTrans.format(self.src,self.dest,self.Hash),data=self.txt_formdata[2:],headers=headers).text
                        translated_txt = json.loads(translated_txt)
                        self.txt += "\n".join(translated_txt)
                        self.temp_txt = ""
                        self.txt_formdata = 'q'
            else:
                for line in txt:
                    if line == '\n':
                        self.temp_txt += ""
                        self.txt_formdata += "&q"
                    else:
                        self.temp_txt += "<pre>" + line[:-1] + "</pre>"
                        self.txt_formdata += "&q=%3Cpre%3E%" + "%".join(re.findall('..',line[:-1].encode("utf-8").hex())) + "%3C%2Fpre%3E"
                                    
            self.Hash = requests.post("http://localhost:14756/",data ={'text':self.temp_txt} ).text
            translated_txt = requests.post(googleTrans.format(self.src,self.dest,self.Hash),data=self.txt_formdata[2:],headers=headers).text
            translated_txt = json.loads(translated_txt)
            self.txt += "\n".join(translated_txt)

            txt.close()
        except:
            pass
        
        if self.single_file == "y":
            self.single_txt += "----------------------------------\n"
            self.single_txt += "CHAPTER-" + str(i) + "\n\n"
            
            soup = BeautifulSoup(self.txt, 'html5lib')
            for s in soup.select('i'):
                s.extract()

            results = soup.select('pre')
            for k in range(len(results)):
                self.single_txt +=  results[k].get_text(strip=True).strip() + "\n"
            self.single_txt += "\n\n"
        else:
            os.chdir("../translated_novel/" + self.novel_name)
            if self.type == "html":
                if i == self.start:
                    navigation = '<div id="navigation"><a href="#"><button>PREV</button></a><a href="CHAPTER-' + str(i + 1) + '.html"><button>NEXT</button></a></div>'
                elif i == self.end:
                    navigation = '<div id="navigation"><a href="CHAPTER-' + str(i - 1) + '.html"><button>PREV</button></a><a href="#"><button>NEXT</button></a></div>'
                else:
                    navigation = '<div id="navigation"><a href="CHAPTER-' + str(i - 1) + '.html"><button>PREV</button></a><a href="CHAPTER-' + str(i + 1) + '.html"><button>NEXT</button></a></div>'
                
                new_file = open("CHAPTER-" + str(i) + ".html", "w",encoding="utf-8")
                new_file.write(self.header)
                new_file.write(navigation)
            else:
                new_file = open("CHAPTER-" + str(i) + ".txt", "w",encoding="utf-8")
            
            # selector = Selector(text=self.txt)
            # selector.xpath("//i").remove()
            # for pre in selector.xpath("//pre/text()").getall():
                    # new_file.write("<p>" + "".join(pre) + "</p>")

            soup = BeautifulSoup(self.txt, 'html5lib')
            for s in soup.select('i'):
                s.extract()

            results = soup.select('pre')
            
            
            
            if self.type == "html":
                for k in range(len(results)):
                    new_file.write("<p>" + results[k].get_text(strip=True).strip() + '</p>')
                
                new_file.write(navigation)
                new_file.write(self.footer)
            else:
                for k in range(len(results)):
                    new_file.write(results[k].get_text(strip=True).strip() + '\n')
                
            
            new_file.close()
            os.chdir("../../txt_files")
        os.remove("CHAPTER-" + str(i) + ".txt") 
    def progress_bar_header(self):
        toolbar_width = 50
        self.progress = 51
        print("PROGRESS...")
        sys.stdout.write("│%s│" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1))

    def progress_bar_animated(self):
        sys.stdout.write("█")
        sys.stdout.flush()
        self.progress -= 1


Acc = txt_translate()
Acc.initialisation ()
time.sleep(10)