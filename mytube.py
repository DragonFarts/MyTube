import os
import pytube
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def download_video():
    link = link_entry.get()
    format = format_var.get()
    if not link:
        messagebox.showerror("YouTube Downloader", "Please enter a YouTube link.")
        return
    if not format:
        messagebox.showerror("YouTube Downloader", "Please select a download format.")
        return
    yt = pytube.YouTube(link)
    if format == "720p":
        stream = yt.streams.filter(res="720p").first()
    elif format == "360p":
        stream = yt.streams.filter(res="360p").first()
    elif format == "mp3":
        stream = yt.streams.filter(only_audio=True).first()
    elif format == "mp3-360p":
        stream = yt.streams.filter(res="360p", only_audio=True).first()
    else:
        messagebox.showerror("YouTube Downloader", "Invalid format specified.")
        return
    stream.download()
    if format == "mp3" or format == "mp3-360p":
        video_path = stream.default_filename
        audio_path = os.path.splitext(video_path)[0] + ".mp3"
        subprocess.run(["ffmpeg", "-i", video_path, audio_path])
        os.remove(video_path)  # Add this line to delete the MP4 file
        messagebox.showinfo("YouTube Downloader", "Audio converted successfully!")
    else:
        messagebox.showinfo("YouTube Downloader", "Video downloaded successfully!")

# Create a GUI dialog box for the user to enter the YouTube link and select the download format
root = tk.Tk()
root.title("YouTube Downloader")

link_label = tk.Label(root, text="")
link_label.pack()

link_label = tk.Label(root, text="Enter a YouTube link:")
link_label.pack()

link_entry = tk.Entry(root, width=60)
link_entry.pack()

format_label = tk.Label(root, text="Select a download format:")
format_label.pack()

format_var = tk.StringVar()
format_var.set("720p")

format_720p = tk.Radiobutton(root, text="720p", variable=format_var, value="720p")
format_720p.pack()

format_360p = tk.Radiobutton(root, text="360p", variable=format_var, value="360p")
format_360p.pack()

format_mp3 = tk.Radiobutton(root, text="MP3", variable=format_var, value="mp3")
format_mp3.pack()

format_mp3_360p = tk.Radiobutton(root, text="MP3-360p", variable=format_var, value="mp3-360p")
format_mp3_360p.pack()

download_button = tk.Button(root, text="Download", command=download_video)
link_entry.pack()
download_button.pack()

root.mainloop()
