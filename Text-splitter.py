import re
from pathlib import Path

data_folder = Path("C:\\Users\\Smile\\PycharmProjects\\crawler\\resource")
file_to_open = data_folder / "book.txt"
book = open(file_to_open, "r") #Here we open the book, in this case it is called book.txt
book = str(book.read()) #this is now assigning book the value of book.txt, not just the location
chapters = re.split("Chapter [0-9]+", book, flags = re.IGNORECASE) #Finds all the chapter markers in the book and makes a list of all the chapters
chapters.pop(0) # Removes the first item in list as this is ""
for i in range(1, len(chapters)+1): #Loops for the number of chapters in the book, starting at chapter 1
    writeBook = open("resource\{}.txt".format(i), "w+") #Opens a book with the name of i, if it does not exist, it creates one
    writeBook.write(chapters[i-1]) #Overwrites what is written in the book with the same chapter in the list
    writeBook.close() #Finally, it closes the text file