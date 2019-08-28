#!/usr/bin/python3

class Input_Processing_Unit():

    def __init__(self):
        self.state =0
        self.storage = []
        self.rule_table= dict()
        self.power = 0
        self.input_buffer=[]


    def read_bits(self):
        f = open("raw_traffic.txt", "r")
        a=f.read(1)
        while a:
            print("state=", self.state, "input= " , a)
            self.detector(a)

            if self.state <63:
                self.storage.append(a)
                print("Storage: ", "".join(self.storage))

            elif self.state==64:
                headers = self.Header_Extraction()
                print("headers:", headers)
                self.input_buffer.append("".join(self.storage))
                print("\n Input Buffer: ",self.input_buffer)
                self.storage=[]
                print("\n\n cleared!!")
                action = self.List_Match(headers)
                print("Action: ",action)
            a=f.read(1)

        f.close()




    def detector(self,a):
        if self.state%2==0 and a=='1':
            self.state = self.state + 1

        elif self.state%2 ==1 and a=='0':
            self.state = self.state + 1

        else:
            self.state = 0

        if self.state ==63 and a=='1':
            self.state = self.state + 1
            print("detected!!")





    def Header_Extraction(self):
        print("length: ",len(self.storage))
        if len(self.storage)> 100:
            mac_destination = self.storage[:48]
            mac_source = self.storage[48:96]
            total_len = self.storage[96:112]
            total_len = "".join(total_len)
            total_len = int(total_len, 2)
            if len(self.storage) <1500 and len(self.storage) == total_len + 64:
                print("hi")
                ip_header_length = "".join(self.storage[116:120])
                x = int(ip_header_length,2) -32*5
                protocol = "".join(self.storage[184:192])
                src_ip = "".join(self.storage[208:240])
                dest_ip = "".join(self.storage[240:272])
                src_port = "".join(self.storage[272+x:288+x])
                dest_port = "".join(self.storage[288+x:304+x])

            else:
                print("discard")
                src_ip=""
                dest_ip=""
                src_port=""
                dest_port=""
                protocol=""
        else:
            src_ip=""
            dest_ip=""
            src_port=""
            dest_port=""
            protocol=""

        return [src_ip,dest_ip,src_port,dest_port,protocol]





    def List_Match(self,headers):
        v = "".join(headers)
        if self.rule_table.get(v,None)==None:
            return 'Deny'
        else:
            return rule_table[v]









if __name__== "__main__":
    n = Input_Processing_Unit()

    print("Press enter to trigger NIC")
    a=input()


    n.read_bits()
