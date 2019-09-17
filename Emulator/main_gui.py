#!/usr/bin/env python3
#
#
# import tkinter as tk
#



from tkinter import *
from tkinter import filedialog



class ScrolledText(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.text = Text(self, *args, **kwargs)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        # expose some text methods as methods on this object
        self.insert = self.text.insert
        self.delete = self.text.delete
        self.mark_set = self.text.mark_set
        self.get = self.text.get
        self.index = self.text.index
        self.search = self.text.search
        self.config = self.text.config

class Code(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.scrolled_text = ScrolledText(self)
        self.scrolled_text.pack(side="top", fill="both", expand=True)

    def onOpen(self):
        self.scrolled_text.delete('1.0',END)
        ftypes = [('Python files', '*.py'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        filename = dlg.show()

        if filename != '':
            with open(filename, "r") as f:
                self.scrolled_text.insert("1.0", f.read())
                self.scrolled_text.config(state=DISABLED)

        # with open(filename, "r") as f:
        #     self.scrolled_text.insert("1.0", f.read())








if __name__ == '__main__':

    root = Tk()
    registers = Frame(root)
    code = Frame(root)
    registers.pack(side = LEFT)
    code.pack(side = RIGHT)
    c= Code(code)
    c.pack(side="top", fill="both", expand=True)
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    runmenu = Menu(menu)
    menu.add_cascade(label = 'Run', menu=runmenu)
    filemenu.add_command(label="Open", command=c.onOpen)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=root.quit)
    runmenu.add_cascade(label = 'Run all')
    runmenu.add_cascade(label= 'Step by step')
    helpmenu = Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About')
    mainloop()
