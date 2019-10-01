#!/usr/bin/env python3
#
#
# import tkinter as tk
#



from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from customNotebook import CustomNotebook  #user defined
import gui_assembler as assembler
from Execution import *

COLORS = {'color' : '#40E0D0',"menu":"#20b2aa","console":'#bfd9d9'}
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
        self.text.pack(side="left", fill="both")


        # expose some text methods as methods on this object
        self.insert = self.text.insert
        self.delete = self.text.delete
        self.mark_set = self.text.mark_set
        self.get = self.text.get
        self.index = self.text.index
        self.search = self.text.search
        self.config = self.text.config






class Code(Frame):
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.scrolled_text = None
        self.current_file = None
        self.cn = CustomNotebook(self, width=920, height= 500)
        self.cn.pack(side="top", fill="both")
        self.tabs = dict()
        self.filecount=0


    def onOpen(self):


        global root
        global runmenu


        ftypes = [('Assembly files', '*.asm')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        filename = dlg.show()
        self.current_file = filename


        to_be_deleted = list()
        for i in self.tabs.keys():
            if i not in self.cn.tabs():
                to_be_deleted.append(i)

        for i in to_be_deleted:
            del self.tabs[i]

        # tab_names =  self.cn.tabs()
        # print("tabnames: ", tab_names)
        # tn = [ i for i in self.tabs.keys()]
        # print("tabnames2: ", tn)
        # print("current: " , self.cn.select())

        if filename in [self.tabs[j][1] for j in self.tabs.keys()]:
            return

        if filename != '' and len(filename)>0:
            with open(filename, "r+") as f:
                # frame = tk.Frame(notebook, background=color)
                st = ScrolledText(self, width=750)
                prog = f.read()
                st.insert("1.0", prog )
                c = filename.split('/')
                c = c[len(c)-1]
                self.cn.add(st, text= c)
                self.cn.select(self.cn.index("end")-1)
                self.tabs[self.cn.select()]=(st,filename)
                print(self.cn.index("end"))

                # scrolled_text.pack(side="left", fill="both", expand=True)

                # if self.scrolled_text == None:
                #     self.scrolled_text = ScrolledText(self, width=750)
                #     self.scrolled_text.pack(side="left", fill="both", expand=True)
                # self.scrolled_text.delete('1.0',END)
                # root.title((filename + " -- Simulator"))
                runmenu.entryconfig(1,state=NORMAL)
                runmenu.entryconfig(2,state=NORMAL)

                f.close()
                # self.scrolled_text.config(state=DISABLED)

        # with open(filename, "r") as f:
        #     self.scrolled_text.insert("1.0", f.read())
        tab_names = [ self.cn.tabs()]
        print("tabnames: ", tab_names)
        tn = [ i for i in self.tabs.keys()]
        print("tabnames2: ", tn)
        print("current: " , self.cn.select())




    def onNew(self):
        global root
        self.filecount = self.filecount+1
        self.current_file = "Untitled" + str(self.filecount)
        st = ScrolledText(self, width=200)
        st.pack(side = "left",fill='both')
        self.cn.add(st, text=self.current_file)
        self.cn.select(self.cn.index("end")-1)

        self.tabs[self.cn.select()]=(st,self.current_file)
        print(self.cn.index("end"))



        # self.scrolled_text = ScrolledText(self)
        # self.scrolled_text.pack(side="top", fill="both", expand=True)
        # self.scrolled_text.delete('1.0',END)

        # if messagebox.askyesno("Simulator","Do you want to save the changes?"):
        #     self.onSave()
        # self.scrolled_text.delete('1.0',END)




    def onSave(self):
        global runmenu
        f = None
        self.current_file = self.cn.tab(self.cn.select(), "text")
        if 'Untitled' == self.current_file[:8] :
            ftypes = [('Assembly files', '*.asm')]
            f = filedialog.asksaveasfile(initialdir = "~",mode='w', defaultextension=".asm", filetypes = ftypes)
            self.tabs[self.cn.select()][1] = f.name
            # print("filename: " , self.current_file)
            if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            # self.current_file = f.name

        else:
            file = self.tabs[self.cn.select()][1]
            print("file: ",file)
            f = open(file,"w")


        runmenu.entryconfig(1,state=NORMAL)
        runmenu.entryconfig(2,state=NORMAL)
        text2save = str(self.tabs[self.cn.select()][0].get(1.0, END)) # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close()








    def onRunAll(self):
        # self.cn.forget(self.cn.index(self.cn.select()))
        # self.cn.event_generate("<<NotebookTabClosed>>")
        # tab_names =  self.cn.tabs()
        # print("\n\n[run]\ntabnames: ", tab_names)
        # tn = [ i for i in self.tabs.keys()]
        # print("tabnames2: ", tn)
        # print("current: " , self.cn.select())
        for i in self.tabs:
            self.cn.forget(self.cn.index(i))

        # e = ScrolledText(self, width=750)
        # e.insert("1.0", "prog" )
        file = "filename"
        f = Frame(self, background="#ffffff")
        Label(f, text="%s" % file, borderwidth="1",relief="solid",
                height=3, background = COLORS["console"]).pack(side=TOP, fill="x")

        e = ExecutionGUI(f)
        e.pack(side=TOP,fill="both", expand=True)
        # e.pack(side = 'top',fill ="both", expand=True)
        self.cn.add(f, text="exec")
        # self.cn.select(self.cn.index("end")-1)


    def onRunStepByStep():
        pass



    def onAssemCurrent(self):
        global console
        # print("Inside assemble current")
        filename = self.tabs[self.cn.select()][1]
        print("\n Filename", filename)
        console.config(state=NORMAL)


        cons = str(console.get(1.0, END))
        if len(cons) > 700:
            cons = cons[200:]
            console.delete('1.0',END)
            console.insert('1.0', cons)

        if assembler.assemble(filename,0) ==1:
            console.insert(END,filename+">"+assembler.error)
        else:
            console.insert(END,"\n\n"+ filename+">"+" DONE")

        console.config(state=DISABLED)


    def onAssemAll(self):
        global console
        global assembler_output
        assembler_output= dict()
        cons = str(console.get(1.0, END))
        console.config(state=NORMAL)
        if len(cons) > 700:
            cons = cons[400:]
            console.delete('1.0',END)
            console.insert('1.0', cons)

        print("tabs: ",self.tabs)
        end=0
        for _,filename in self.tabs.values():
            beg = end
            if assembler.assemble(filename,beg) ==1:
                console.insert(END,filename+">"+assembler.error)

            else:
                console.insert(END,"\n\n"+ filename+">"+" DONE")
                end = assembler.binary_file_linecount
                assembler_output[filename]=assembler.equivalent_binary
                # print("\n\n\n\n in main_gui\n\n ", assembler.equivalent_binary)

        console.config(state=DISABLED)
        print("assembler outputs in main gui\n\n\n",assembler_output)




def add_top_menu(frame):
    #creating top menu
    global ASSEMBLING
    global FILE_OPEN
    global runmenu
    global c
    menu = Menu(frame, bg = COLORS["menu"])

    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    runmenu = Menu(menu)
    menu.add_cascade(label = 'Run', menu=runmenu)

    filemenu.add_command(label="Open", command=c.onOpen)
    filemenu.add_command(label="New", command=c.onNew)
    filemenu.add_command(label="Save", command=c.onSave)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=frame.quit)



    runmenu.add_command(label = 'Compile/Assemble Current', command= c.onAssemCurrent)
    runmenu.add_command(label = 'Compile/Assemble All', command = c.onAssemAll )
    runmenu.add_command(label = 'Run all', command=c.onRunAll)
    runmenu.add_command(label= 'Run Step by step',command = c.onRunStepByStep)

    # runmenu.add_cascade(label= 'Run Next Step')
    # print(c.cn.index("end"))
    # if c.cn.index("end") ==0:
    #     runmenu.entryconfig(1,state=DISABLED)
    #     runmenu.entryconfig(2,state=DISABLED)
    #     runmenu.entryconfig(3,state=DISABLED)
    #     runmenu.entryconfig(4,state=DISABLED)




    helpmenu = Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About')

    frame.config(menu=menu)



def disable_frame(f):
    for child in f.winfo_children():
        child.configure(state='disable')

def enable_frame(f):
    for child in frame2.winfo_children():
        child.configure(state=NORMAL)


def update_registers(T):
    T.config(state=NORMAL)
    REGISTERS = {'A':'0000','B':'0001','PC':'0010','SOC_FRONT':'0011',
                 'PROG_STACK_TOP':'0100','MAR':'0101','SOC_BACK':'0110',
                 'ITYPE':'0111', 'COMM':'1000', 'CTRL':'1001','MDR':'1010',
                 'ANS':'1011', 'IR': '1100', 'IHAR':'1101' }

    str_val = ''

    for i in REGISTERS:
        str_val = '\n\n\n  ' + i + " : " + REGISTERS[i]
        T.insert(END, str_val)

    T.config(state=DISABLED)




if __name__ == '__main__':
    global root
    global console
    global c
    # creating main window object
    root = Tk()
    root.geometry("1400x700")
    root.title('Simulator')

    registers = Frame(root, width = 30,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    pin_console_code = Frame(root, bg = 'gray95', width = 800)




    registers.pack(side = "left",fill="both")
    pin_console_code.pack(side = "right",fill="both", expand = True)


    pins = Frame(pin_console_code, width =30, bg = 'gray85')
    p = Frame(pins, width =30, bg = 'gray80', height = 50,highlightbackground="black", highlightcolor="black", highlightthickness=1)
    c= Code(pin_console_code,bg = 'gray89', width=700, height =100) # inserting CODE GUI
    console = ScrolledText(pin_console_code,bg=COLORS["console"], height = 14,width=800)
    console.config(state=DISABLED)


    console.pack(side='bottom', fill='both')
    c.pack(side="left", fill="both")
    pins.pack(side = "right",fill='both')
    p.pack(side = "bottom", pady=20)

    # adding pins
    var = IntVar()
    ch = Checkbutton(p, text="  Interrupt", variable=var, width = 20, bg='gray80')
    description = Label(p, text = "Interrupt and Data\n Communication pins ", width =15)
    note = Label(p, text = "NOTE: give interrupt data as \n4 character hexadecimal value with\n no prefixes (such as # or H)", width =15)
    L1 = Label(p, text = "Interrupt Data", width =15)
    button = Button(p, text="send")
    E1 = Entry(p, bd = 5, width=14 )

    description.pack(side = "top", pady = 10, fill='x')
    ch.pack(side = "top", pady = 10)
    note.pack(side = "bottom", fill='x')
    button.pack(side=BOTTOM, pady = 10)
    L1.pack( side = LEFT, pady = 10)
    E1.pack(side = RIGHT, fill = 'x' , pady = 10)
    # disable_frame(p)


    #creating top menu
    add_top_menu(root)


    # inserting values in register frame
    # reg = Label(registers)
    T = Text(registers, width = 30, bg ='gray80')
    T.pack(side = 'top', fill='both',expand = True)
    T.config(state=DISABLED)
    update_registers(T)


    mainloop()
