import requests
import tkinter
from tkinter import filedialog
import time

msg = str()
WriteMessage = str()
FileNumber = int()

ErrorCodes = {"10":"ERROR: File is not provided", "11":"ERROR: File is empty", "12":"ERROR: File is invalid", "20":"ERROR: Wait for an hour before the next upload", "21":"ERROR: wait for 24 hours before you're next upload", "22":"ERROR: Too many bytes sent in a hour, wait for 1 hour", "23":"ERROR: Too many bytes sent in a day, wait for 24 hours", "30":"ERROR: File type not supported by the server", "31":"ERROR: File size is too big", "32":"ERROR: File banned", "40":"ERROR: System error"}

# -------------------- FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def BackupFileToAnonfile(path, FileNumber):
    global msg
    
    print("\nSelected file is:", path)
    print(f'>> [ Trying to UPLOAD file# 0{FileNumber} to server 1 ]\n')

    RecievedResponse = requests.post('https://api.anonfiles.com/upload', files = {'file' : open(path, 'rb' ) }) # It is strongly recommended that you open files in binary mode. This is because Requests may attempt to provide the Content-Length header for you, and if it does this value will be set to the number of bytes in the file. Errors may occur if you open the file in text mode.
                                                                                                                # https://www.tutorialspoint.com/requests/requests_file_upload.htm                                                                       
      
    if (RecievedResponse.ok):                    # This checks error codes. less than 400 returns True
        NameOfFile = RecievedResponse.json()["data"]["file"]["metadata"]["name"]
        SizeOfFile = RecievedResponse.json()["data"]["file"]["metadata"]["size"]["readable"]
        LongUrl = RecievedResponse.json()["data"]["file"]["url"]["full"]
        ShortUrl = RecievedResponse.json()["data"]["file"]["url"]["short"]
        FileID = RecievedResponse.json()["data"]["file"]["metadata"]["id"]
        print(">> [ File is uploaded ]")
        print(">> [ NAME:     ", NameOfFile, "]")
        print(">> [ SIZE:     ", SizeOfFile, "]")
        print(">> [ LONG URL: ", LongUrl, "]")
        print(">> [ SHORT URL:", ShortUrl, "]")
        print(">> [ FILE ID:  ", FileID, " (Save this file id if you want to retrive this file in future without the URL.) ]")
        msg = f"{NameOfFile}  ||  {ShortUrl}  || {FileID}  ||  {SizeOfFile}"
        return(msg)
    else:
        print(ErrorCodes[ str(RecievedResponse.json()["error"]["code"])])
        print("\n\n>>>> [ Upload was UNSUCCESSFUL. ]\n>>>> [ Press any key to Continue... ]\n\n")
        return("|| Error uploading to anonfiles ")
        #input()
        #sys.exit()


def BackupFileToAnonynousfiles(path, FileNumber):
    print(f'\n>> [ Trying to UPLOAD file# 0{FileNumber} to server 2 ]\n')

    file = {'file': open(path, 'rb')}
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    RecievedResponse = requests.post('https://api.anonymousfiles.io/', files= file, headers= headers)

    if(RecievedResponse.ok):
        FileURL = RecievedResponse.json()['url']
        print(f'>> [ UPLOAD WAS SUCCESSFUL ]')
        print(f'>> [ URL: {FileURL} ]')
        return(f'|| {FileURL}')
    else:
        print("\n\n>>>> [ Upload was UNSUCCESSFUL. ]\n>>>> [ Press any key to Continue... ]\n\n")
        print(f'{RecievedResponse}')
        return("|| Error uploading to anonymousfiles ")
        #input()
        #sys.exit()


def BackupToGoFile(path, FileNumber):                                   # GOFILE IS IN BETA, SO ERRORS MIGHT OCCUR.
    ServerInfo = requests.get('https://apiv2.gofile.io/getServer')      # Getting the server info for uploading file           
    BestServerAvaliable = ServerInfo.json()['data']['server']           # Getting the best server avaliable to upload the file

    print(f'>> [ Trying to UPLOAD file# 0{FileNumber} to server 3 ]\n')
    files = {'file': open(path, 'rb')}
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    RecievedResponse = requests.post(f'https://{BestServerAvaliable}.gofile.io/uploadFile', files=files, headers = headers)
    
    if(RecievedResponse.ok):
        FileURL = RecievedResponse.json()['data']['directLink']

        print(f'>> [ UPLOAD WAS SUCCESSFUL ]')
        print(f'>> [ URL: {FileURL} ]\n\n')
        print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
        return(f'|| {FileURL}')
    else:
        print("\n\n>>>> [ Upload was UNSUCCESSFUL. ]\n>>>> [ Press any key to Continue... ]\n\n")
        print(f'{RecievedResponse}')
        return("|| Error uploading to GoFile ")
        #input()
        #sys.exit()
 

def FileName():

    Days = {'0':'Monday', '1':'Tuesday', '2':'Wednesday', '3':'Thrusday', '4':'Friday', '5':'Saturday', '6':'Sunday'}
    Month = {'1':'Jan', '2':'Feb', '3':'Mar', '4':'Apr', '5':'May', '6':'Jun', '7':'Jul', '8':'Aug', '9':'Sept', '10':'Oct', '11':'Nov', '12':'Dec'}

    FileDayAndMonth = f'{Days[ str(time.localtime().tm_wday)] } {Month[ str(time.localtime().tm_mon)] }'         # Day and Month
    FileTime = "%02d-%02d-%02d" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)   # Time
    FileDate = "%04d-%02d-%02d" % (time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)  # Date

    return( f'{FileDate} {FileTime} {FileDayAndMonth}.txt' )

def WriteToFile(WriteMessage):
    root = tkinter.Tk()         # Created the root/main window for GUI.
    root.withdraw()             # Hides the root window that was created (but is still running).

    TextFilePath = filedialog.asksaveasfilename(parent = root, defaultextension = ".txt", filetypes = [("Text files", ".txt")], title = "Saving Text File", initialfile = FileName()) # the (initialdir = "C:\\") attribute is not filled coz if its absent then by default it takes the path to downloads folder. (although there is no official documentaion on this.)
                                                                                                                                                                                      # FileName() auto-gives the name for that file which will be returned by the function FileName
    try:
        with open(TextFilePath, 'w') as TextWriting:
            TextWriting.write("Format : [Name] [Anonfiles URL] [Anonfiles FileID] [Size] [GoFile URL] [Anonymousfiles URL]\n")
            TextWriting.write(WriteMessage)
        print(">> [ OUTPUT FILE CREATED ]\n")
        root.destroy()
    except:
        print(">> [ NO OUTPUT FILE CREATED ]\n")

   

# -------------------- SELECT FILES TO UPLOAD -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

root = tkinter.Tk()             # The root window is created. The root window is a main application window in our programs. It has a title bar and borders. These are provided by the window manager. It must be created before any other widgets.
                                # root is the master window
root.title('BackupPlusFiles')   # Name given the the popup window
root.withdraw()                 # Hides the root window that was created (but is still running).
paths = filedialog.askopenfilename(parent = root, title = "File To Backup", filetypes = [("All Files", ".*")], multiple = True ) # This returns the list of filepaths with their name.
                                                                                                                                 # The askopenfilename() function returns the file name that you selected. Here "All Files" is a Label (So it can be any random string)
                                                                                                                                 # the (initialdir = "C:\\") attribute is not filled coz if its absent then by default it takes the path to downloads folder. (although I havent found any official documentaion on this.)
root.destroy()



# -------------------- MAIN -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

for path in paths:
  FileNumber += 1  

  try:
      RecicvedMessageAnonfile = BackupFileToAnonfile(path, FileNumber)
  except:
      print("Error: 10054 [ Anonfile ]")
      FileURLFromGoFile = ' '

  time.sleep(10)
  try:                          # In case the connection is forcibly closed by host (error: 10054) then the program should not get stuck, it must continue.
      FileURLFromAnonymousfiles = BackupFileToAnonynousfiles(path, FileNumber)
  except:
      print("Error: 10054 [ Anonymousfiles ]")
      FileURLFromAnonymousfiles = ' '

  time.sleep(10)
  try:                          # In case the connection is forcibly closed by host (error: 10054) then the program should not get stuck, it must continue.
      FileURLFromGoFile = BackupToGoFile(path, FileNumber)
  except:
      print("Error: 10054 [ GoFile ]")
      FileURLFromGoFile = ' '

  WriteMessage = WriteMessage + f'\n{RecicvedMessageAnonfile} {FileURLFromGoFile} {FileURLFromAnonymousfiles}'  # WriteMessage is the message which has to be written in the text file (at last) and Recieved message is the message that is returned by the BackupFile() Function for each file.

if (paths):                                                 # After all the files are uploaded, creating the text file that will contain all the links.
    WriteToFile(WriteMessage)
else:                                                       # If no files were selected.
    print("\n\n[ NO FILE WAS SELECTED ]\n\n")

# -------------------- HOLD THE SCREEN --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("[ PRESS ENTER TO CONTINUE ] ", end = "") # Python’s print() function comes with a parameter called ‘end’. By default, the value of this parameter is ‘\n’, i.e. the new line character. You can end a print statement with any character/string using this parameter.
input()
