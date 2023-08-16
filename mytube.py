import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import spotipy
import youtube_dl
from pydub import AudioSegment

def download_track():
    link = link_entry.get()
    format = format_var.get()
    if not link:
        messagebox.showerror("Spotify Downloader", "Please enter a Spotify link.")
        return
    if not format:
        messagebox.showerror("Spotify Downloader", "Please select a download format.")
        return
    sp = spotipy.Spotify()
    track_info = sp.track(link)
    youtube_link = track_info['external_urls']['youtube']
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'audio.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_link])
    audio = AudioSegment.from_file('audio.ext')
    audio.export('audio.mp3', format='mp3')
    with open('audio.mp3', 'wb') as f:
        f.write(audio)
    messagebox.showinfo("Spotify Downloader", "Track downloaded successfully!")

# Create a GUI dialog box for the user to enter the Spotify link and select the download format
root = tk.Tk()
root.title("Spotify Downloader")

link_label = tk.Label(root, text="Enter a Spotify link:")
link_label.pack()

link_entry = tk.Entry(root, width=60)
link_entry.pack()

download_button = tk.Button(root, text="Download", command=download_track)
download_button.pack()

format_label = tk.Label(root, text="Select a download format:")
format_label.pack()

format_var = tk.StringVar()
format_var.set("mp3")

format_mp3 = tk.Radiobutton(root, text="MP3", variable=format_var, value="mp3")
format_mp3.pack()

root.mainloop()