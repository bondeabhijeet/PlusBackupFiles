from bs4 import BeautifulSoup
import requests
import tkinter
from tkinter import filedialog
import sys

FileID = input("Enter the FileID :")

FileLink = requests.get(f'https://anonfiles.com/{FileID}').text

soup = BeautifulSoup(FileLink, 'lxml')

try:
    DirectDownloadLink = soup.find('a', class_ = 'btn btn-primary btn-block')['href']
    FileName = soup.find('h1', class_ = 'text-center text-wordwrap').text
except:
    ErrorText = soup.find('h1', class_ = 'text-center').text
    print(f"\n [ ERROR: {ErrorText} ]")
    sys.exit()


def GetPath():
    root = tkinter.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', '1')  # To bring the "Saving the file" window to top
    path = filedialog.asksaveasfilename(parent = root, filetypes = [('All Files', '.*')], initialfile = FileName, title = 'Saving the file')
    root.destroy()
    return(path)
    
path = GetPath()

if(path):
    print(" [ Downloading File ] ", end = '\r')

    FileData = requests.get(DirectDownloadLink)    
    with open(path, 'wb') as p:
        p.write(FileData.content)
    print(" [ File Downlaoded Successfully ]")
        
else:
    print(" [ ERROR: No path selected ] ")
    
