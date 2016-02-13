import Tkinter as tk
import subprocess
import tkMessageBox
import time
import os
import sys

top = tk.Tk()
header = tk.Text()
sd = tk.Text()
numSongs = 0

def start():
    if os.path.exists("fifo.tmp"):
        subprocess.Popen('rm fifo.tmp', shell=True) 
    subprocess.Popen('./a.out', shell=True)
    songDisplay()

def on_closing():
    subprocess.Popen('killall a.out', shell=True)    
    subprocess.Popen('killall afplay', shell=True)
    if os.path.exists("fifo.tmp"):
        subprocess.Popen('rm fifo.tmp', shell=True)    
    top.destroy()

def songDisplay():
    global numSongs
    os.mkfifo("fifo.tmp")
    if os.path.exists("fifo.tmp"):
        with open("fifo.tmp", "r") as fifo:
            data = fifo.read()
            duration = float(data.split()[len(data.split())-1])
            header.config(state=tk.NORMAL)
            header.insert(tk.INSERT, " ".join(data.split()[0:len(data.split())-1]) + "\n")
            numSongs= numSongs + 1
            if numSongs > 5:
                header.delete('7.0', '8.0')
            header.grid()
            header.config(state=tk.DISABLED)
            fifo.close()
    top.after(int(duration*1000), songDisplay)

def pause():
    subprocess.Popen('killall a.out', shell=True)    
    subprocess.Popen('killall afplay', shell=True)   
    if os.path.exists("fifo.tmp"):
        subprocess.Popen('rm fifo.tmp', shell=True) 

def skip():
    subprocess.Popen('killall afplay', shell=True)
    songDisplay()

def createWidgets(top):
    header.insert(tk.INSERT, "Otto!\n\n\n\nSongs:\n\n")
    header.tag_config("center", justify='center')
    header.tag_add("center", 1.0, "end")
    header.grid()
    header.config(state=tk.DISABLED)
    top.startButton = tk.Button(top, text='start',
        command=start)
    top.startButton.grid()
    top.skipButton = tk.Button(top, text='>>',
    command=skip)
    top.skipButton.grid()
    top.quitButton = tk.Button(top, text='pause',
        command=pause)
    top.quitButton.grid()

#def helloCallBack():
   #tkMessageBox.showinfo( "Hello Python", "Hello World")

createWidgets(top)
#B = tk.Button(top, text ="Hello", command = helloCallBack)
top.protocol("WM_DELETE_WINDOW", on_closing)
#B.grid()
top.mainloop()