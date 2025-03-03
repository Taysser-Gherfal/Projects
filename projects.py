# pip install pyperclip
# pip install tabulate

import os, time, pickle, pyperclip, webbrowser, subprocess
from tabulate import tabulate
from os import path

def store_url(project_path):
    with open(project_path + "/URLs.p", "wb") as myfile:
            urls = pyperclip.paste()
            mylist = []
            mylist = urls.split("\n")
            pickle.dump(mylist, myfile)

def read_url(project_path):
    # if url.p exists open it
    if path.exists(project_path + "/URLs.p"):
        with open(project_path + "/URLs.p", "rb") as myfile:
            urls = pickle.load(myfile)
    # if not create it
    else:
        with open(project_path + "/URLs.p", "wb") as myfile:
            mylist = ['']
            pickle.dump(mylist, myfile)
        with open(project_path + "/URLs.p", "rb") as myfile:
            urls = pickle.load(myfile)
    
    return urls

def folders(dir_path):
    folders = []
    x = os.walk(dir_path)

    for i in x:
        if dir_path != i[0]:
            folder = {}
            folder['path'] = i[0]
            folder['date'] = str(time.ctime(os.path.getctime(i[0])))
            folders.append(folder)

    return folders


def open_urls(urls):
        # MacOS
        # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        # Linux
        # chrome_path = '/usr/bin/google-chrome %s'

        # Chrome path on Windows
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

        # Opening a new Chrome window and giving it time to open
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(chrome_path, creationflags=DETACHED_PROCESS)
        time.sleep(2)

        # Open urls in taps
        for i in urls[:-1]:
                url = i
                webbrowser.get(chrome_path).open(url)



# The main loop
while True:

        # Setting the project directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if path.exists(dir_path + "/data"):
                dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\data'
                f = folders(dir_path)
        else:
                os.makedirs(dir_path + "/data")
                dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\data'
                f = folders(dir_path)

        # Clear the commandline 
        os.system('cls')

        table = []
        for counter, i in enumerate(f):
                #print(str(counter) + ' - ' + i['path'].replace(dir_path + "\\", '') + ' - ' + str(len(read_url(i['path'])) - 1) + ' --- ' + i['date'])
                row = [counter, i['path'].replace(dir_path + "\\", ''), len(read_url(i['path'])) - 1, i['date']]
                table.append(row)

        print(tabulate(table, headers=['#', 'Name', '# URLs', 'Last Changed'], tablefmt='orgtbl'))
        print("==========================================")
        print("(s-#) Save URLs to an existing project?")
        print("(o-#) Open URLs of an existing project?")
        print("(fld) Open project folder")
        print("(ref) Refreshs list")
        print("(any) To quit")
        print("------------------------------------------")
        
        answer = input("Your Command: ")

        # save project
        if answer[0] == "s":
                try:
                        project_number = answer[2:]
                        store_url(f[int(project_number)]['path'])
                except:
                        print("There was no project number")
        
        # open project
        elif answer[0] == "o":
                try:
                        project_number = answer[2:]
                        open_urls(read_url(f[int(project_number)]['path']))
                except:
                        print("There was no project number")
        
        # open folder path
        elif answer == "fld":
                subprocess.call("explorer "+dir_path, shell=True)
        
        # Refresh project list, by continuing the loop
        elif answer == "ref":
                continue
        
        else:
                exit()