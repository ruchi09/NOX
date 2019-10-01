



from tkinter import *


OP_CODES={ 'COMP':'0000', 'MOV':'0001', 'INC':'0010',
           'DEC':'0011', 'SET':'0100', 'HALT':'0101',
           'JUMP':'0110','FETCH':'0111','CALL':'1000',
           'JUMPEQ':'1001', 'ADD':'1010', 'MOD':'1011',
           'OR':'1100', 'CHECK':'1101', 'AND':'1110'
           }


# OPERATIONS = {}

REGISTERS = {'A':'0000','B':'0001','PC':'0010','SOC_FRONT':'0011',
             'PROG_STACK_TOP':'0100','MAR':'0101','SOC_BACK':'0110',
             'ITYPE':'0111', 'COMM':'1000', 'CTRL':'1001','MDR':'1010',
             'ANS':'1011', 'IR': '1100', 'IHAR':'1101' }

UNARY_OPS = ['INC', 'JUMP','FETCH','JUMPEQ', 'DEC']


# def execute(file):
#     for i in file:





class ExecutionGUI(Frame):
    def __init__(self, root):

        Frame.__init__(self, root)
        self.canvas = Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both",expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        # self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        # self.frame = tk.Frame(self.canvas, background="#ffffff")
        # self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        # self.canvas.configure(yscrollcommand=self.vsb.set)
        #
        # self.vsb.pack(side="right", fill="y")
        # self.canvas.pack(side="left", fill="both", expand=True)
        # self.canvas.create_window((4,4), window=self.frame, anchor="nw",
        #                           tags="self.frame")

        # self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def populate(self):
        '''Put in some fake data'''
        for row in range(100):
            Label(self.frame, text="%s" % row, width=7, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            Label(self.frame, text=t).grid(row=row, column=1)

    def populate_code(self,b):
        pass



    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))






if __name__ == "__main__":
    root=Tk()
    t=Frame(root)
    # t.pack(side=TOP)
    ExecutionGUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
