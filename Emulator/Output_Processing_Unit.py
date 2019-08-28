#!/usr/bin/python3

class Output_Processing_Unit():

    def __init__(self):
        self.output_queue = [] #info about address plus address of the data in output buffer and size
        self.output_buffer = [] # data along with application layer header (encrypted)

        # self.storage = []
        self.rule_table= dict()
        self.power = 0


    def read_data(self):
        if len(self.output_queue)>0:
            packet_header_info = self.output_queue.pop(0)
            data = self.output_buffer.pop(0)
            add = packet_header_info["add"]
            del packet_header_info["add"]
            action = self.List_Match(packet_header_info)
            print("Action: ",action)
            if action !='Deny':
                packet = self.Header_Addition(packet_header_info,data)
                print("\n Packet sent!!\n\n Packet = ",packet)



    #----------------------------------------------------------------------------------------
    #   Function: send_data
    #   Parameters:  info - dict() , data - str()
    #   Return Value: None
    #----------------------------------------------------------------------------------------
    def send_data(self,info,data):
        info["add"] = len(self.output_buffer)
        self.output_queue.append(info)
        self.output_buffer.append(data)




    def Header_Addition(self, header_info,data):
        packet = "".join(header_info.values())+data
        return packet

        # print("length: ",len(self.storage))
        # if len(self.storage)> 100:
        #     mac_destination = self.storage[:48]
        #     mac_source = self.storage[48:96]
        #     total_len = self.storage[96:112]
        #     total_len = "".join(total_len)
        #     total_len = int(total_len, 2)
        #     if len(self.storage) <1500 and len(self.storage) == total_len + 64:
        #         print("hi")
        #         ip_header_length = "".join(self.storage[116:120])
        #         x = int(ip_header_length,2) -32*5
        #         protocol = "".join(self.storage[184:192])
        #         src_ip = "".join(self.storage[208:240])
        #         dest_ip = "".join(self.storage[240:272])
        #         src_port = "".join(self.storage[272+x:288+x])
        #         dest_port = "".join(self.storage[288+x:304+x])
        #
        #     else:
        #         print("discard")
        #         src_ip=""
        #         dest_ip=""
        #         src_port=""
        #         dest_port=""
        #         protocol=""
        # else:
        #     src_ip=""
        #     dest_ip=""
        #     src_port=""
        #     dest_port=""
        #     protocol=""
        #
        # return [src_ip,dest_ip,src_port,dest_port,protocol]





    def List_Match(self,headers):
        v = "".join(headers.values())
        if self.rule_table.get(v,None)==None:
            return 'Deny'
        else:
            return self.rule_table[v]





if __name__== "__main__":
    n = Output_Processing_Unit()

    print("Press enter to trigger NIC")
    a=input()
    n.rule_table["11111111111111001"] = "Accept"
    print("ruletable:  ", n.rule_table)
    n.send_data({"src":"11111111","dst":'111111001'}, "11001010101010110001")
    n.send_data({"src":"11110011","dst":'110011001'}, "110011111101010110001")

    while len(n.output_queue) >0:
        print("\n\n\n\n--------------processing packet-------------")
        n.read_data()
