from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile, askopenfilenames
from tkinter.messagebox import showinfo
import os
import shutil
import subprocess
import platform


def listbox(List):
    root = Tk()
    root.geometry('400x400')
    box = []
    listbox = Listbox(root, width=40, height=10, selectmode=MULTIPLE, bg="steelblue", fg="coral")
    for i in range(len(List)):
        listbox.insert(i, List[i])
    def selected_item():
	    for i in listbox.curselection():
		        box.append(listbox.get(i))

    btn = Button(root, text='Select These Files', command=selected_item)
    btn.pack(side='bottom')
    listbox.pack()

    root.mainloop()
    #print("Listbox",box)
    return box


def getzipfilename():
    ws = Tk()
    ws.title("File Name - AESFileTransfer")
    ws.geometry('400x400')
    Label(ws, text="Enter the name of the file 👇", pady=20).pack()
    global window
    def printValue():
        global filename
        filename = window.get()
        Label(ws, text=f'the file has been named as {filename} successfully🙌!', pady=20).pack()
        ws.destroy()

    name = StringVar(ws)
    window = Entry(ws, relief="raised", textvariable=name)
    window.pack(pady=30)

    Button(ws, text="Name the file📁!!!", padx=10, pady=5, command=printValue).pack()

    ws.mainloop()
    return filename

def GetFilePathGUI():
    win = Tk()
    win.geometry("700x350")
    def open_file():
       directory = filedialog.askdirectory()
       #if file:
       global filepath
       filepath = os.path.abspath(directory)
       Label(win, text="The File is located at : " + str(filepath), font=('Aerial 11')).pack()
       label_ = Label(win, text="Close this window after finding the path of required file folder❎", font=('Georgia 13'))
       label_.pack(pady=10)
    label = Label(win, text="Click the this Find the path button to find the path of the file folder📂 to be sent!!!", font=('Georgia 13'))
    label.pack(pady=10)
    ttk.Button(win, text="Find the path", command=open_file).pack(pady=20)
    win.mainloop()
    return filepath
    
def GetIPGUI():
    master = Tk()
    Label(master, text="HOST IP ADDRESS").grid(row=0)
    Label(master, text="HOST PORT NUMBER").grid(row=1)
    
    global e1
    global e2
    
    e1 = Entry(master)
    e2 = Entry(master)
    
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    
    
    def entry():
        global HOST
        global PORT 
        HOST = e1.get()
        PORT = e2.get()
        PORT = int(PORT)
        master.quit()
    
    
    Button(master, text='Connect', command=entry).grid(row=3, column=0, sticky=W, pady=4)
    
    master.mainloop()
    return (HOST,PORT)
    master.destroy()

def InputFolderCreator():
    global file_path_collection
    file_path_collection = []
    master = Tk()
    
    def fileshow():
        File_Paths = askopenfilenames()
        for File_Path in File_Paths:
            file_path_collection.append(File_Path)
        
    def stop():
        master.quit()
        
    master.title("Instructions-AESFileTransfer")
    Label(master, text="Instructions\nChoose the files which you want to transfer to the Server\nPress choose to choose the files repeatedly and press apply to choose all the files which you have choosen till now").grid(row=0)
    Button(master, text="choose", command=fileshow).grid(row=3, column=0, sticky=W, pady=4)
    Button(master, text="apply", command=stop).grid(row=3, column=1, sticky=W, pady=4)
    
    master.mainloop()
    master.destroy()
    
    mas = Tk()
    global E
    Label(mas, text="Enter a name for the folder: ").grid(row=0)
    E = Entry(mas)
    E.grid(row=0, column=1)
    def entry():
        global Folder_Name
        Folder_Name = E.get()
        mas.quit()
    Button(mas, text='Enter the name', command=entry).grid(row=3, column=0, sticky=W, pady=4)
    mas.mainloop()
    mas.destroy()
    
    Home = os.path.expanduser('~')
    Folder_Path = Home + r'/Desktop/' + Folder_Name 
    os.mkdir(Folder_Path)
    #showinfo("Information-AESFileTransfer", f"The folder '{Folder_Name}' has been created successfully 🙌.\nPress ok to continue")
    for file_path in file_path_collection:
        shutil.copy(file_path, Folder_Path)
    #showinfo("Information-AESFileTransfer", f"In the folder '{Folder_Name}' all the selected files have been loaded successfully 🙌.\nPress ok to continue")
    #showinfo("Information-AESFileTransfer", f"Now the folder '{Folder_Name}' will be opened to show you that all the files have been loaded succesfully.\nPress ok to continue")
    if platform.system() == "Linux":
        subprocess.call(('xdg-open', Folder_Path))
    else:
        subprocess.call(('open', Folder_Path))
    return Folder_Path
        
        
def OpenEncryptedFile():
    master = Tk()
    master.title("Encryption Text Opener")
    Label(master, text="Do you want to see the encrypted file contents? ").grid(row=0)
    def yes():
        global opt 
        opt = "yes"
        master.quit()
    def no():
        global opt 
        opt = "no"
        master.quit()
    Button(master, text='Yes', command=yes).grid(row=3, column=0, sticky=W, pady=4)
    Button(master, text='NO', command=no).grid(row=3, column=1, sticky=W, pady=4)
    master.mainloop()
    master.destroy()
    return opt