import Tkinter as tk
import subprocess
import tkMessageBox
import time
import os
import sys

top = tk.Tk()
header = tk.Text()
sd = tk.Text()
MAX_SONGS_DISPLAY = 5
numSongsDisplay = 0.0
SONG_DISPLAY_LINE = 7.0

def start():
    global p
    if os.path.exists("fifo.tmp"):
        subprocess.Popen('rm fifo.tmp')
    p = subprocess.Popen('./portaudio/SenProj')
    song_display()

def on_closing():
    p.terminate()   
    if os.path.exists("fifo.tmp"):
        subprocess.Popen('rm fifo.tmp')
    top.destroy()

def song_display():
    global numSongsDisplay
    os.mkfifo("fifo.tmp")
    if os.path.exists("fifo.tmp"):
        with open("fifo.tmp", "r") as fifo:
            data = fifo.read()
            duration = float(data.split()[len(data.split())-1])
            header.config(state=tk.NORMAL)
            header.insert(tk.INSERT, " ".join(data.split()[0:len(data.split())-1]) + "\n")
            header.tag_remove("curr", str(numSongsDisplay + SONG_DISPLAY_LINE-1), str(numSongsDisplay + SONG_DISPLAY_LINE))
            header.tag_add("curr", str(numSongsDisplay + SONG_DISPLAY_LINE), str(numSongsDisplay + SONG_DISPLAY_LINE+1))
            header.tag_config("curr", background="yellow", foreground="black")
            numSongsDisplay += 1
            if numSongsDisplay > MAX_SONGS_DISPLAY:
                header.delete(str(SONG_DISPLAY_LINE), str(SONG_DISPLAY_LINE+1))
                numSongsDisplay = MAX_SONGS_DISPLAY
            header.grid()
            header.config(state=tk.DISABLED)
            fifo.close()
    top.after(int(duration*1000), song_display)

def init_GUI(top):
    header.insert(tk.INSERT, "Otto!\n\n\n\nSongs:\n\n")
    header.tag_config("center", justify='center')
    header.tag_add("center", 1.0, "end")
    header.grid()
    header.config(state=tk.DISABLED)
    top.startButton = tk.Button(top, text='start',
        command=start)
    top.startButton.grid()

init_GUI(top)
top.protocol("WM_DELETE_WINDOW", on_closing)
top.mainloop()