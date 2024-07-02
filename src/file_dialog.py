import tkinter as tk
from tkinter import filedialog


def create_guiless_tk():
    # create a tkinter object
    root = tk.Tk()
    # remove the gui element of the tkinter object
    root.withdraw()
    # return the tk object
    return root

def request_open_folder(note) -> str:
    # create gui-less tkinter object
    root = create_guiless_tk()

    # record the directory path
    folder_dir = filedialog.askdirectory(
        title = note
    )

    root.destroy()
    return folder_dir

def request_open_file(note) -> str:
    # create gui-less tkinter object
    root = create_guiless_tk()

    # record the path
    file_dir = filedialog.askopenfilename(
        filetypes = [("All Files", "*.*")],
        title = note
    )

    root.destroy()
    return file_dir

def request_write_file(note) -> str:
   # create gui-less tkinter object
    root = create_guiless_tk()

    # record the  path
    file_dir = filedialog.asksaveasfilename(
        filetypes = [("All Files", "*.*")],
        title = note
    )

    root.destroy()
    return file_dir