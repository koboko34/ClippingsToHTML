"""
Armand Yilinkou
19/02/2023

This project was created to easily create Anki flashcards from Amazon Kindle clippings using Yomichan.

The program takes Amazon Kindle clippings formatted in KindleMate to a txt format and converts them into a
neatly formatted HTML file. The text can then easily be parsed using browser extensions such as Yomichan.

On first run, produces a single html file. On subsequent runs, user can tick checkbox to produce two html files.
The first html file (same name as source file) will contain all the clippings that have been processed until
then. The second html file (source file name + [last added]) will only contain the clippings which were added
during the latest successful conversion. This allows the user to keep a databank of all sentences converted,
while also easily knowing which sentences are yet to be parsed with Yomichan to make Anki cards.

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


def make_single_file(file_dir, persistent_file_name):
    with open(file_dir, "r", encoding="utf-16") as f:
        lines = f.readlines()

    for num, line in enumerate(lines):
        if line == "\n":
            lines[num] = "<br>"

    with open(persistent_file_name, "w", encoding="utf-16") as f:
        f.write("".join(reversed(lines)))


def make_unique_new_lines(lines, old_lines):
    new_lines = []
    old_lines_no_tag = []
    for line in old_lines:
        old_lines_no_tag.append(line.strip("<br>"))

    for new_line in lines:
        if new_line not in old_lines_no_tag and new_line != "<br>":
            new_lines.append(new_line)

    for num, line in enumerate(new_lines):
        new_lines[num] = "<br>" + line

    new_lines.reverse()
    return new_lines


def convert_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    file_dir = fd.askopenfilename(
        title='Open a file',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    if file_dir == "":
        return

    if not os.path.exists(file_dir):
        showinfo(
            title="Result",
            message="File not found!"
        )
        root.destroy()
        return

    persistent_file_name = file_dir.strip(".txt") + ".html"
    if checkbox_status.get() == 0 or not os.path.exists(persistent_file_name):
        make_single_file(file_dir, persistent_file_name)
    else:
        with open(file_dir, "r", encoding="utf-16") as f:
            lines = f.readlines()

        for num, line in enumerate(lines):
            if line == "\n":
                lines[num] = "<br>"

        with open(persistent_file_name, "r", encoding="utf-16") as f:
            old_lines = f.readlines()

        new_lines = make_unique_new_lines(lines, old_lines)

        if len(new_lines) == 0:
            showinfo(
                title="Result",
                message="No new lines found!"
            )
            root.destroy()
            return

        with open(persistent_file_name, "a", encoding="utf-16") as f:
            f.write("".join(new_lines))

        new_file_name = file_dir.strip(".txt") + " [last added]" + ".html"
        new_lines[0] = new_lines[0].strip("<br>")
        with open(new_file_name, "w", encoding="utf-16") as f:
            f.write("".join(new_lines))

    showinfo(
        title="Result",
        message="Conversion complete!"
    )

    root.destroy()
    return


root = tk.Tk()
root.title('Clippings To HTML')
root.resizable(False, False)
root.geometry('300x150')

open_button = ttk.Button(
    root,
    text='Choose source txt file',
    command=convert_file
)

checkbox_label = tk.Label(
    root,
    text="Append to previous html file and create separate file for new clippings only",
    wraplength=250
)

checkbox_status = tk.IntVar(value=1)
checkbox = ttk.Checkbutton(
    root,
    text="",
    variable=checkbox_status
)

open_button.pack(expand=True)
checkbox_label.pack()
checkbox.pack()

root.mainloop()
