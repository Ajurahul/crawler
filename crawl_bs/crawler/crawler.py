import sys
import os
import requests
import time
from bs4 import BeautifulSoup
import mtranslate

class Accumulator:
    def light_novel(self):
        print("")
        print("████████╗██████╗░██╗░░██╗░██████╗░░░░█████╗░░█████╗░")
        print("╚══██╔══╝██╔══██╗╚██╗██╔╝██╔════╝░░░██╔══██╗██╔══██╗")
        print("░░░██║░░░██████╔╝░╚███╔╝░╚█████╗░░░░██║░░╚═╝██║░░╚═╝")
        print("░░░██║░░░██╔══██╗░██╔██╗░░╚═══██╗░░░██║░░██╗██║░░██╗")
        print("░░░██║░░░██║░░██║██╔╝╚██╗██████╔╝██╗╚█████╔╝╚█████╔╝")
        print("░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░╚════╝░░╚════╝░")
        print("")
        print("░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗██╗░░░░░███████╗██████╗░")
        print("██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██║░░░░░██╔════╝██╔══██╗")
        print("██║░░╚═╝██████╔╝███████║░╚██╗████╗██╔╝██║░░░░░█████╗░░██████╔╝")
        print("██║░░██╗██╔══██╗██╔══██║░░████╔═████║░██║░░░░░██╔══╝░░██╔══██╗")
        print("╚█████╔╝██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░███████╗███████╗██║░░██║")
        print("░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝╚═╝░░╚═╝")
        print("\n")
        try:
            while True:
                self.novel_url = input("WRITE NOVEL URL: ")
                if self.novel_url :
                    break
           
            
            self.number = input("HOW MUCH CHAPTER(0=ALL CHAPTER): ")
            if not self.number :
                self.number = 0
            else:
                self.number = int(self.number)
            self.type = input("TXT OR HTML (DEFAULT = TXT): ").lower()
            if not self.type :
                self.type="txt"
            if self.type == "txt":
                self.single_file = input("SINGLE FILE??: (Y/N)(DEFAULT=Y): ").lower()
                if not self.type :
                    self.type="y"

            
            
            header = open("required/header.txt", "r")
            self.header = header.read()
            header.close()

            footer = open("required/footer.txt", "r")
            self.footer = footer.read()
            footer.close()

            style = open("required/style.css", "r")
            self.style = style.read()
            style.close()
            
            #GET CHANPTER
            self.chapters = self.get_chapter()

            #CREATING DOCUMENT FOR NOVEL
            self.document_creating()
            
            #DOWNLOADING
            self.download_loop()
            if self.single_file == "y":
                new_file = open(self.novel_name + ".txt", "w",encoding="utf-8")
                new_file.write(self.single_txt)
                new_file.close()

            sys.stdout.write("│\n")
            print("DONE!!")
            print("THANK FOR USING OUR PRODUCT")
        except Exception as e:
            print("ERROR ENTRING LIGHT NOVEL")
            print(e)
    def get_chapter(self):
        print("GETTING CHAPTERS...")
        try:
            #GETTING ALL CHAPTER LI TAGS
            page = requests.get(self.novel_url)
            soup = BeautifulSoup(page.content, 'html5lib')
            results = soup.select('.book_list li')

            novel_name = soup.select(".book_info >.infos>h1")[0].text
            self.novel_name= mtranslate.translate(novel_name,"en","auto")
            for key in ['\\','/',':','?','*','<','>','|','"']:
                self.novel_name = self.novel_name.replace(key,'')

            #MAKE A DICTIONARY FOR CHAPTER HREF AND NAME
            novel_chapters = []
            for i in range(len(results)):
                link = results[i].a
                number = link.text[2:-1]
                novel_chapters.append({
                    "number":number,
                    "link":"https://trxs.cc" + link['href']
                })
            return novel_chapters

        except Exception as e:
            print("ERROR GETTING CHAPTERS")
            print(e)
    def document_creating(self):
        print("CREATING DOCUMENT...")
        try:
            if not os.path.exists('downloads'):
                os.mkdir('downloads')
            os.chdir('downloads')
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
            print("CREATING SUCCESSFULLY")
        except Exception as e:
            print("ERROR CREATING DOCUMENT")
            print("CLOSING...")
            print(e)
            sys.exit()
    def download_loop(self):
        try:
            print("START DOWNLOADING")
            self.progress_bar_header()
            
            self.single_txt = ""
            range_bar = 0
            self.previous = "#"

            if self.number == 0:
                range_bar_unit = 50 / len(self.chapters)
                number_chapter_downloded = len(self.chapters)
            else:
                range_bar_unit = 50 / self.number
                number_chapter_downloded = self.number

            for i in range(number_chapter_downloded):
                range_bar += range_bar_unit
                self.downloader(self.chapters[i]["link"],"CHAPTER-" + str(i + 1),i + 1)
                current_message = str(i + 1) + "/" + str(number_chapter_downloded)
                sys.stdout.write(" " * (self.progress - 1) + "|" + current_message + " ")
                sys.stdout.write("\b" * (self.progress + len(current_message) + 1))
               
                sys.stdout.flush()

                for j in range(int(range_bar)):
                    self.progress_bar_animated()
                    range_bar-= 1
        except Exception as e:
            print("ERROR WHILE DOWNLOAD")
            print(e)
    

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
    def downloader(self,url,chapter_name,current_loop):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html5lib')
            for s in soup.select('.read_chapterDetail span'):
                s.extract()
            results = soup.select('.read_chapterDetail p')
            
            if self.single_file == "y":
                self.single_txt += "----------------------------------\n"
                self.single_txt += "CHAPTER-" + str(current_loop) + "\n\n"

                for i in range(len(results)):
                    self.single_txt +=results[i].text.strip() + '\n'

                self.single_txt += "\n\n"
            else:
                if self.type == "html":
                    navigation = '<div id="navigation"><a href="' + self.previous + '"><button>PREV</button></a><a href="CHAPTER-' + str(current_loop + 1) + '.html"><button>NEXT</button></a></div>'
                    new_file = open(chapter_name + ".html", "w",encoding="utf-8")
                    new_file.write(self.header)
                    new_file.write(navigation)
                    for i in range(len(results)):
                        new_file.write( "<p>" + results[i].text + "</p>")
                    new_file.write(navigation)
                    new_file.write(self.footer)
                    self.previous = chapter_name + ".html"
                else:
                    new_file = open(chapter_name + ".txt", "w",encoding="utf-8")
                    for i in range(len(results)):
                        new_file.write(results[i].text.strip() + '\n')
                
                new_file.close()
            
        except Exception as e:
            print(e)
            if self.type == "html":
                os.remove(chapter_name +  + ".html") 
            else:
                os.remove(chapter_name +  + ".txt") 
            print("ERROR HAPPEN IN " + chapter_name)

Acc = Accumulator()
Acc.light_novel()
time.sleep(10)