import os
from pathlib import Path
from tkinter import Tk, Button, YES, Label
import webbrowser
from tkinter import messagebox


def build(res: Path) -> Tk:
    window = Tk()
    window.title("antaREST")
    window.geometry("200x100")
    window.config(background="#112446")

    link = Button(
        window,
        text="Go to server",
        bg="#e48b08",
        fg="black",
        command=lambda: webbrowser.open("http://localhost"),
    )
    link.pack(expand=YES)

    Label(window, text="Server running...", fg="#e48b08", bg="#112446").pack()

    def on_closing() -> None:
        if messagebox.askokcancel("Quit", "If you quit, server stop."):
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    return window


if __name__ == "__main__":
    print(Path("../resources").absolute())
    build(res=Path().parent / "resources").mainloop()
