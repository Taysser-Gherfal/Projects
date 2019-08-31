# pip install pyperclip
# pip install tabulate

import os, time, pickle, pyperclip, webbrowser
from tabulate import tabulate

def store_url(project_path):
    with open(project_path + "/url.p", "wb") as myfile:
        urls = pyperclip.paste()
        mylist = []
        mylist = urls.split("\n")
        pickle.dump(mylist, myfile)

def read_url(project_path):
    with open(project_path + "/url.p", "rb") as myfile:
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
        
        for i in urls[:-1]:
                url = i

                # MacOS
                #chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

                # Windows
                chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

                # Linux
                # chrome_path = '/usr/bin/google-chrome %s'

                webbrowser.get(chrome_path).open(url)
                print(url)


# Setting the project directory
dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\data'
f = folders(dir_path)

# The main loop
while True:
        print("==========================================")

        table = []
        for counter, i in enumerate(f):
                #print(str(counter) + ' - ' + i['path'].replace(dir_path + "\\", '') + ' - ' + str(len(read_url(i['path'])) - 1) + ' --- ' + i['date'])
                row = [counter, i['path'].replace(dir_path + "\\", ''), len(read_url(i['path'])) - 1, i['date']]
                table.append(row)

        print(tabulate(table, headers=['#', 'Name', '# URLs', 'Last Changed'], tablefmt='orgtbl'))
        print("==========================================")
        print("What would you like to do?")
        print("(s-#) Save URLs to an existing project?")
        print("(o-#) Open URLs of an existing project?")
        print("(any) To quit")
        print("------------------------------------------")
        
        answer = input("Your Answer: ")

        if answer[0] == "s":
                try:
                        project_number = answer[2:]
                        store_url(f[int(project_number)]['path'])
                except:
                        print("There was no project number")
        elif answer[0] == "o":
                try:
                        project_number = answer[2:]
                        open_urls(read_url(f[int(project_number)]['path']))
                except:
                        print("There was no project number")
        else:
                exit()