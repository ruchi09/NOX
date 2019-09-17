#!/usr/bin/env python3
#
#
# import tkinter as tk
#



from tkinter import *
from tkinter import filedialog, messagebox


COLORS = {'color' : '#40E0D0'}
ASSEMBLING = 0
FILE_OPEN = 0
EDITING = 0
debug =0

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
        self.scrolled_text = None
        self.current_file = None

    def onOpen(self):
        global FILE_OPEN
        global root
        global runmenu


        ftypes = [('Assembly files', '*.asm'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        filename = dlg.show()
        self.current_file = filename
        if filename != '':
            with open(filename, "r+") as f:
                if self.scrolled_text == None:
                    self.scrolled_text = ScrolledText(self)
                    self.scrolled_text.pack(side="top", fill="both", expand=True)
                self.scrolled_text.delete('1.0',END)
                prog = f.read()
                self.scrolled_text.insert("1.0", prog )
                FILE_OPEN = 1
                root.title((filename + " -- Simulator"))
                runmenu.entryconfig(1,state=NORMAL)
                runmenu.entryconfig(2,state=NORMAL)

                f.close()
                # self.scrolled_text.config(state=DISABLED)

        # with open(filename, "r") as f:
        #     self.scrolled_text.insert("1.0", f.read())





    def onNew(self):
        global root
        global FILE_OPEN
        if FILE_OPEN == 0:
            self.current_file = None
            self.scrolled_text = ScrolledText(self)
            self.scrolled_text.pack(side="top", fill="both", expand=True)
            self.scrolled_text.delete('1.0',END)
            FILE_OPEN=1

        else:
            if messagebox.askyesno("Simulator","Do you want to save the changes?"):
                self.onSave()
            self.scrolled_text.delete('1.0',END)




    def onSave(self):
        f = None
        if self.current_file == None:
            ftypes = [('Assembly files', '*.asm'), ('All files', '*')]
            f = filedialog.asksaveasfile(initialdir = "~",mode='w', defaultextension=".asm", filetypes = ftypes)
            # print("filename: " , self.current_file)
            if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            self.current_file = f.name

        else:
            f = open(self.current_file,"w")

        text2save = str(self.scrolled_text.get(1.0, END)) # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close()




    def onRun(self):
        if self.scrolled_text.edit_modified():
            self.onSave()



def add_top_menu(frame):
    #creating top menu
    global ASSEMBLING
    global FILE_OPEN
    global runmenu
    menu = Menu(frame, bg = 'light sea green')
    frame.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    runmenu = Menu(menu)
    menu.add_cascade(label = 'Run', menu=runmenu)
    filemenu.add_command(label="Open", command=c.onOpen)
    filemenu.add_command(label="New", command=c.onNew)
    filemenu.add_command(label="Save", command=c.onSave)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=frame.quit)

    runmenu.add_cascade(label = 'Compile/Assemble current')
    runmenu.add_cascade(label = 'Compile/Assemble all')
    runmenu.add_cascade(label = 'Run all')
    runmenu.add_cascade(label= 'Run Step by step')
    # runmenu.add_cascade(label= 'Run Next Step')
    runmenu.entryconfig(1,state=DISABLED)
    runmenu.entryconfig(2,state=DISABLED)
    runmenu.entryconfig(3,state=DISABLED)
    runmenu.entryconfig(4,state=DISABLED)




    helpmenu = Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About')







def update_registers(T):
    T.config(state=NORMAL)
    REGISTERS = {'A':'0000','B':'0001','PC':'0010','SOC_FRONT':'0011',
                 'PROG_STACK_TOP':'0100','MAR':'0101','SOC_BACK':'0110',
                 'ITYPE':'0111', 'COMM':'1000', 'CTRL':'1001','MDR':'1010',
                 'ANS':'1011', 'IR': '1100', 'IHAR':'1101' }

    str_val = ''
    for i in REGISTERS:
        str_val = '\n\n\n' + i + " : " + REGISTERS[i]
        T.insert(END, str_val)

    T.config(state=DISABLED)

    # print("str_val=", str_val)








if __name__ == '__main__':
    global root
    # creating main window object
    root = Tk()
    root.geometry("630x650")
    root.title('Simulator')
    registers = Frame(root, width = 30)
    code = Frame(root, width = 600)
    registers.pack(side = "left",fill="both")
    code.pack(side = "right",fill="both", expand = True)

    # inserting CODE GUI in right frame
    c= Code(code)
    c.pack(side="top", fill="both", expand=True)

    #creating top menu
    add_top_menu(root)


    # inserting values in register frame
    T = Text(registers, width = 30, bg ='gray85')
    T.pack(side = 'top', fill='both',expand = True)
    T.config(state=DISABLED)
    update_registers(T)


    mainloop()
