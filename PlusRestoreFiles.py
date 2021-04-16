from bs4 import BeautifulSoup
import requests
import tkinter
from tkinter import filedialog
import sys
import os

#------------------------------------------------------------------------------INPUT & PROCESSING------------------------------------------------------------------------------------------------------

os.system('mode con: cols=128 lines=30')                                        # Resizing the CMD (Terminal) window

FileID = input("Enter the FileID :")
Fileinfo = requests.get(f'https://api.anonfiles.com/v2/file/{FileID}/info')     # Fetching File info using API
FilePageLink = Fileinfo.json()['data']['file']['url']['short']                  # Extracting File page url from the info recieved
FileSizeInBytes = Fileinfo.json()['data']['file']['metadata']['size']['bytes']  # Extracting File Size from the info recieved

FileLink = requests.get(FilePageLink).text                                      # Getting the raw html code of the FileDownload page for parsing through BeautifulSoup

soup = BeautifulSoup(FileLink, 'lxml')

try:
    DirectDownloadLink = soup.find('a', class_ = 'btn btn-primary btn-block')['href']
    FileName = soup.find('h1', class_ = 'text-center text-wordwrap').text
except:
    ErrorText = soup.find('h1', class_ = 'text-center').text
    print(f"\n [ ERROR: {ErrorText} ]")
    sys.exit()

#------------------------------------------------------------------------------FUNCTIONS---------------------------------------------------------------------------------------------------------------

def GetPath():
    root = tkinter.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', '1')  # To bring the "Saving the file" window to top
    Path = filedialog.asksaveasfilename(parent = root, filetypes = [('All Files', '.*')], initialfile = FileName, title = 'Saving the file')
    root.destroy()
    return(Path)

def Downloader(URL, TotalSize, Path):              # TotalSize in bytes in string type
    r = requests.get(URL, stream = True)
    print("\nFile Name:", FileName, f"[{round((TotalSize/1048576), 2)} MB]")

    TotalBytesRecieved = 0
    with open (f'{Path}', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            TotalBytesRecieved += len(chunk)     # The Total number of bytes recieved 
            PercentageUsed = ((TotalBytesRecieved)/(int(TotalSize)))*100  # To find the Percentage of the downloaded part (ie. (Total bytes recieved/Total size) * 100 )

            status = '[' + str(int(PercentageUsed)*'>').ljust(100, '-') + '] ' + f"{round(TotalBytesRecieved/1048576, 2)} MB  " + f"[{round(PercentageUsed, 2)}%] "
            # To indicate the status of the download we use status string
            # ljust : https://www.geeksforgeeks.org/python-string-ljust-rjust-center/
            # round : https://kodify.net/python/math/round-decimals/#round-decimal-places-up-and-down-round

            print(status, end='\r')

            f.write(chunk)
    if(round(PercentageUsed, 2) == 100.0):
        print(f'{status}[√]')
        #print(f"{status}[ Download Complete ]")
    else:
        print(f'{status}[×]')


#------------------------------------------------------------------------------MAIN--------------------------------------------------------------------------------------------------------------------

Path = GetPath()

if(Path):
    Downloader(DirectDownloadLink, FileSizeInBytes, Path)        
else:
    print(" [ ERROR: No Path selected ] ")

input(" [ Press Enter to continue... ] ")
#------------------------------------------------------------------------------END---------------------------------------------------------------------------------------------------------------------