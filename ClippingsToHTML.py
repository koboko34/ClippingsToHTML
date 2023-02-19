"""
Armand Yilinkou
19/02/2023

This project was created to easily create Anki cards from Amazon Kindle clippings using Yomichan.

The program takes clippings from an Amazon Kindle in a txt format and convert them into a neatly
formatted HTML file. The text can then easily be parsed using browser extensions such as Yomichan.

Example of input file (one line of text per two line break):
向上心が皆無なのかしら

この部の目的は端的に言ってしまえば自己変革を促し、悩みを解決することだ。

「比企谷もこの調子で捻くれた根性の更生と腐った目の矯正に努めたまえ。

まぁ気にせず続けてくれ。様子を見に寄っただけなのでな」

もっと根本的なところをどうにかしないと……。
...and so on.

Example output in browser (one line of text per line break):
向上心が皆無なのかしら
この部の目的は端的に言ってしまえば自己変革を促し、悩みを解決することだ。
「比企谷もこの調子で捻くれた根性の更生と腐った目の矯正に努めたまえ。
まぁ気にせず続けてくれ。様子を見に寄っただけなのでな」
もっと根本的なところをどうにかしないと……。
...and so on.
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('Clippings To HTML')
root.resizable(False, False)
root.geometry('300x150')


def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    if filename == "":
        return

    file_dir = filename

    with open(file_dir, "r", encoding="utf-16") as f:
        lines = f.readlines()

    for num, line in enumerate(lines):
        if line == "\n":
            lines[num] = "<br>"

    new_file_name = file_dir.strip("txt") + "html"

    with open(new_file_name, "w", encoding="utf-16") as f:
        f.write("".join(lines))

    showinfo(
        title="Result",
        message="Conversion complete!"
    )

    root.destroy()


open_button = ttk.Button(
    root,
    text='Choose source txt file',
    command=select_file
)

open_button.pack(expand=True)

root.mainloop()
