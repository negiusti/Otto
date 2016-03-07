import Tkinter as tk
import subprocess
import tkMessageBox
import time
import os
import sys


MAX_SONGS_DISPLAY = 5
SONG_DISPLAY_LINE = 7.0

def start():
    global proc
    proc = subprocess.Popen('./portaudio/SenProj', bufsize=1, stdout=subprocess.PIPE, universal_newlines=True)
    song_display()

def on_closing():
    ### terminate the c program ###
    if (proc != None):
        proc.terminate()
    ### close the GUI ###
    top.destroy()

def song_display():
    global proc
    global numSongsDisplay
    data = ""
    ### communicate with the c program ###
    data = proc.stdout.readline()
    duration = float(data.split()[len(data.split())-1])
    header.config(state=tk.NORMAL)
    ### display the current song ###
    header.insert(tk.INSERT, " ".join(data.split()[0:len(data.split())-1]) + "\n")
    
    ### unhighlight the previous song ###
    header.tag_remove("curr_song", str(numSongsDisplay + SONG_DISPLAY_LINE-1), str(numSongsDisplay + SONG_DISPLAY_LINE))

    ### highlight the current song ###
    header.tag_add("curr_song", str(numSongsDisplay + SONG_DISPLAY_LINE), str(numSongsDisplay + SONG_DISPLAY_LINE+1))
    header.tag_config("curr_song", background="yellow", foreground="black")

    ### delete a row to make room ###
    numSongsDisplay += 1
    if numSongsDisplay > MAX_SONGS_DISPLAY:
        header.delete(str(SONG_DISPLAY_LINE), str(SONG_DISPLAY_LINE+1))
        numSongsDisplay = MAX_SONGS_DISPLAY
    header.grid()
    header.config(state=tk.DISABLED)

    ### call song_display() again when the song is over ###
    top.after(int(duration*1000), song_display)

def init_GUI(top):
    global proc
    global numSongsDisplay
    proc = None
    numSongsDisplay = 0.0
    header.insert(tk.INSERT, "\n\n\n\nSongs:\n\n")
    header.tag_config("center", justify='center')
    header.tag_add("center", 1.0, "end")
    header.grid()
    header.config(state=tk.DISABLED)
    top.startButton = tk.Button(top, text='start',
        command=start)
    top.startButton.grid()

top = tk.Tk()
top.wm_title("Otto")
header = tk.Text()
sd = tk.Text()
init_GUI(top)
top.protocol("WM_DELETE_WINDOW", on_closing)
top.mainloop()