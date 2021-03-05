import requests
import tkinter
from tkinter import filedialog


ErrorCodes = {"10":"ERROR: File is not provided", "11":"ERROR: File is empty", "12":"ERROR: File is invalid", "20":"ERROR: Wait for an hour before the next upload", "21":"ERROR: wait for 24 hours before you're next upload", "22":"ERROR: Too many bytes sent in a hour, wait for 1 hour", "23":"ERROR: Too many bytes sent in a day, wait for 24 hours", "30":"ERROR: File type not supported by the server", "31":"ERROR: File size is too big", "32":"ERROR: File banned", "40":"ERROR: System error"}


root = tkinter.Tk()  # The root window is created. The root window is a main application window in our programs. It has a title bar and borders. These are provided by the window manager. It must be created before any other widgets.
# root is the master window


root.title('BackupPlusFiles') # Name given the the popup window

path = filedialog.askopenfilename(parent = root, title = "File To Backup", initialdir = "C:\\", filetypes = [("All Files", ".*")] ) # The askopenfilename() function returns the file name that you selected. here "All Files" is a Label (So it can be given any name)
root.destroy()

print("Selected file is:", path)

RecievedResponse = requests.post('https://api.anonfiles.com/upload', files = {'file' : open(path, 'rb' ) } ) # It is strongly recommended that you open files in binary mode. This is because Requests may attempt to provide the Content-Length header for you, and if it does this value will be set to the number of bytes in the file. Errors may occur if you open the file in text mode.
                                                                                          # https://www.tutorialspoint.com/requests/requests_file_upload.htm
if (RecievedResponse.ok):
  NameOfFile = RecievedResponse.json()["data"]["file"]["metadata"]["name"]
  SizeOfFile = RecievedResponse.json()["data"]["file"]["metadata"]["size"]["readable"]
  LongUrl = RecievedResponse.json()["data"]["file"]["url"]["full"]
  ShortUrl = RecievedResponse.json()["data"]["file"]["url"]["short"]
  FileID = RecievedResponse.json()["data"]["file"]["metadata"]["id"]
  print(">> File is uploaded")
  print(">> NAME:     ", NameOfFile)
  print(">> SIZE:     ", SizeOfFile)
  print(">> LONG URL: ", LongUrl)
  print(">> SHORT URL:", ShortUrl)
  print(">>>> FILE ID:", FileID, " (Save this file id if you want to retrive this file in future without the URL.)")
else:
  print(ErrorCodes[ str(RecievedResponse.json()["error"]["code"])])


root = tkinter.Tk()

TextFilePath = filedialog.asksaveasfilename(parent = root, initialdir = "C:\\", defaultextension = ".txt", filetypes = [("Text File", '.txt')], title = "Saving the link in text file", initialfile = f'{NameOfFile}.txt')

ToBeWrittenInFile = NameOfFile + " || " + ShortUrl + SizeOfFile + LongUrl
with open( TextFilePath, 'w') as TextWriting:
  TextWriting.write(f"{NameOfFile}  ||  {ShortUrl}  ||  {SizeOfFile}  ||  {LongUrl}")
  
root.destroy()


print("PRESS ENTER TO CONTINUE")
input()
