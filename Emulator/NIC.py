#!/usr/bin/python3
# preamble with SFD: (left to right)10101010 10101010 10101010 10101010 10101010 10101010 10101010 10101011
import time




class NIC():
    def __init__(self):
        self.state =0
        self.storage = []
        self.rule_table=[]
        self.instruction_memory=[]
        self.instruction_register = []
        self.power = 0




    def load_rule_table(self):

        pass





class NIC_driver():
    def __init__(self):
        self.rules= [( "1234", "a"),
                     ( "1567", "d"),
                     ( "3767", "a"),
                     ( "1887", "a")]

    def get_rule(self,i):
        return self.rule[i]
