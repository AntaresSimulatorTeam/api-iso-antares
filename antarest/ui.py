import os
from pathlib import Path
from tkinter import *
import webbrowser
from tkinter import messagebox


def build(res: Path):
    window = Tk()
    window.title("antaREST")
    window.geometry("200x100")
    window.config(background="#112446")
    window.iconbitmap(res / "logo.ico")

    link = Button(window, text="Go to server", bg="#e48b08", command=lambda: webbrowser.open("http://localhost"))
    link.pack(expand=YES)

    def on_closing():
        if messagebox.askokcancel("Quit", "If you quit, server stop."):
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    return window


if __name__ == "__main__":
    print(Path("../resources").absolute())
    build(res=Path().parent / "resources").mainloop()
