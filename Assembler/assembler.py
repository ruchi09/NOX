 #!/usr/bin/python3


# -----------------------------------------------------------------------
#   Author Name: Ruchi Saha
#   Problem Statement: This progran converts given assembly language to
#                       equivalent binary strings
#
# -----------------------------------------------------------------------






import sys

# ---------------------------------------------------------------------------------------------------
#                      OP_CODES DESCRIPTION
#
#  COMP A B: compares A and B and stores the result in CTRL
#  MOV A B: moves/copies content of register B to register A
#  INC A: increments address stored at register A by one memory address and stores in ANS
#  DEC A: deccrements address stored at register A by one memory address and stores in ANS
#  SET A val: stores val in A
#  HALT: do nothing
#  JUMP add: changes the value of PC (pprog counter) to 'add'
#  FETCH X: fetches the content at address STORED IN MAR and stores it in X
#  CALL add: pushes the current address to prog atack and changes the value of PC to 'add'
#  JUMPEQ A B: jump if A is equal to B
#  MOD A val: Performs A modulus val
#  STORE A: store the data contained by A to the address pointed by MAR
#  CHECK : Checks socket queue top in rule table to validate copy, sets N as 0 in CTRL if socket denied
#-----------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------
#                            REGISTERS
#
#  A,B : general purpose registers
#  SOC_FRONT : contains the address which points to front of output queue
#  SOC_BACK : contains the address which points to end of output queue
#  PROG_STACK_TOP : points to the top of program stack
#  MAR : memory address register (conventional)
#  ITYPE : interrupt type (stores the type of interrupt)
#  COMM : data and interrupt communication register (receives data and sends ack)
#  CTRL : neg,zero,carry,overflow, soc_queue full
#  MDR  : memory data register. will store fetched data
#  ANS  : temporarily stores computed value
#  IR   : Instruction register
#  IHAR : interrupt handler address register
# ----------------------------------------------------------------------

OP_CODES={ 'COMP':'0000', 'MOV':'0001', 'INC':'0010',
           'DEC':'0011', 'SET':'0100', 'HALT':'0101',
           'JUMP':'0110','FETCH':'0111','CALL':'1000',
           'JUMPEQ':'1001', 'ADD':'1010', 'MOD':'1011',
           'OR':'1100', 'CHECK':'1101', 'AND':'1110'
           }

REGISTERS = {'A':'0000','B':'0001','PC':'0010','SOC_FRONT':'0011',
             'PROG_STACK_TOP':'0100','MAR':'0101','SOC_BACK':'0110',
             'ITYPE':'0111', 'COMM':'1000', 'CTRL':'1001','MDR':'1010',
             'ANS':'1011', 'IR': '1100', 'IHAR':'1101' }

UNARY_OPS = ['INC', 'JUMP','FETCH','JUMPEQ', 'DEC']


calls = dict()



# ------------------------------------------------------------------------------
# debug_display: function to display binary instructions along with assembly
#                instructions with line numbers
#
# Parameters: z --> (list of tuples [(binary_instruction,
#                                           assembly_instruction)]) binary code
#
# Return values: no values returned
# ------------------------------------------------------------------------------

def debug_display(z):
    count = 0
    print('-' * 100)
    print('{:<16s}{:<30s}{:<32s}'.format( "   Memory","Assembly","Binary") )
    print('{:<16s}'.format( "   Address " ))


    print('-' * 100)

    for i in z:
        if i[0]!='':
            count = count + 1
            print('{:<16s}{:<30s}{:<32s}'.format( "    "+str(count),i[1],i[0]) )
        else:
            print('{:<16s}{:<30s}{:<32s}'.format( "    ",i[1],i[0]) )

        # print("line ",count, ":", i[1],i[0])



# ------------------------------------------------------------------------------
# hex_to_bin: This function converts the hexadecimal value to equivalent binary
#
# Parameters: z --> (string) Hexadecimal value
#
# Return values: b --> (string) Equivalent binary
# ------------------------------------------------------------------------------

def hex_to_bin(z):
    global a
    global linecount

    bin_hex = {'0':'0000','1':'0001','2':'0010','3':'0011',
                '4':'0100','5':'0101','6':'0110','7':'0111',
                '8':'1000','9':'1001','A':'1010','B':'1011',
                'C':'1100','D':'1101','E':'1110','F':'1111'}
    b = ""
    z=list(z)
    for i in z:
        if i in bin_hex.keys():
            b=b+bin_hex[i]
        else:
            print("\n[ERROR] Invalid value!!")
            print(" line",linecount,":"," ".join(a), "<--\n")
            exit()


    return b




# -----------------------------------------------------------------------------------
# Convert_Prog_to_bin_temp: This function checks the syntax of the assembly program
#                           and converts it into final binary  version
#
# Parameters: fp --> file pointer of the assembly file to be compiled
#                       (file should be .txt)
#
# Return values: assembly --> (list of strings) Equivalent binary of the provided
#                               file. Each element of the list is an instruction
# --------------------------------------------------------------------------------------

def Convert_Prog_to_bin_temp(fp,debug):
    global a
    global linecount
    global binary_file_linecount
    global OP_CODES
    global REGISTERS
    global UNARY_OPS
    global calls

    linecount = 0
    binary_file_linecount = 1


    assembly = []
    a=fp.readline().upper()
    while a!="":
        # print("line:",a)

        linecount = linecount+1
        if debug>0: print(" [DEBUG] line",linecount,":",a,end='')
        a = a.strip().split(' ')
        if a[0]=='' :
            # bin_temp = ""
            assembly.append((""," ".join(a)) )
            a=fp.readline()

        elif a[0][0]=='@':
            if a[0][1:] not in calls.keys():
                calls[a[0][1:]] = str(binary_file_linecount)
            assembly.append((""," ".join(a)) )
            a=fp.readline()

            # print("hi  ",a)
        elif a[0] not in OP_CODES.keys():
            print("\n[ERROR] No such command !!")
            print(" line",linecount,":"," ".join(a))
            fp.close()
            exit()
        else:
            bin_temp = OP_CODES[a[0]]
            if a[0] in ['HALT','CHECK']:
                if len(a)>1:
                    print("[ERROR] no operand expected!")
                    print(" line",linecount,":"," ".join(a))
                    fp.close()
                    exit()
                bin_temp = bin_temp + "00000000000000000000" #extra zeros are padding

            elif len(a)>2 and (a[0] in UNARY_OPS) :
                print("[ERROR] single operand expected!")
                print(" line",linecount,":"," ".join(a))
                fp.close()
                exit()

            elif (a[0] in UNARY_OPS) and len(a)==2:
                if a[0][:4]=='JUMP':
                    if a[1][0]=='@':
                        f=fp.tell()
                        add = DetectCalls(a[1][1:],fp)
                        if add == '':
                            print("[ERROR] No tag found!")
                            print(" line",linecount,":"," ".join(a), "<--\n")
                            fp.close()
                            exit()
                        fp.seek(f)
                        bin_temp = bin_temp + add + "0000000000000000" #extra zeros are padding
                    elif a[1][0]=='#':
                        add = hex_to_bin(a[1][1:])
                        bin_temp = bin_temp + add + "0000000000000000" #extra zeros are padding
                    else:
                        print("\n[ERROR] Invalid operand !!")
                        print(" line",linecount,":"," ".join(a))
                        fp.close()
                        exit()
                elif a[1] in REGISTERS.keys():
                    bin_temp = bin_temp + REGISTERS[a[1]] + "0000000000000000" #extra zeros are padding

                else:
                    print("\n[ERROR] No such operand register !!")
                    print(" line",linecount,":"," ".join(a))
                    fp.close()
                    exit()

            elif len(a) > 3:
                print("[ERROR] two operands expected!")
                print(" line",linecount,":"," ".join(a), "<--")
                fp.close()
                exit()

            else:
                # print("a0 a1",a[0],a[1])
                if a[1] in REGISTERS.keys():
                    bin_temp = bin_temp + REGISTERS[a[1]]
                    if a[0] not in {'SET', 'MOD'} :

                        if a[2] in REGISTERS.keys():
                            bin_temp = bin_temp + REGISTERS[a[2]] + '000000000000' #extra zeros are padding
                        else:
                            print("\n[ERROR] No such operand register !!")
                            print(" line",linecount,":",a[0],a[1], a[2],"<--")
                            fp.close()
                            exit()
                    else:
                        if len(a)==3:
                            if len(a[2]) ==4:
                                bin_temp = bin_temp + hex_to_bin(a[2])
                            else:
                                print("\n[ERROR] Invalid value (4 char hex required)!!")
                                print(" line",linecount,":",a[0],a[1], a[2],"<--")
                                fp.close()
                                exit()
                        else:
                            print("\n[ERROR] TWO operands required !!")
                            print(" line",linecount,":"," ".join(a) ,"<--")
                            fp.close()
                            exit()
                else:
                    print("\n[ERROR] No such operand register !!")
                    a.insert(2,'<--')
                    print(" line",linecount,":"," ".join(a))
                    fp.close()
                    exit()
        # print("line",linecount,":",a)
            assembly.append((bin_temp," ".join(a)) )
            binary_file_linecount = binary_file_linecount+1
            a = fp.readline()
    return assembly






# -------------------------------------------------------------------------
# DetectCalls: This function detects the call tags and replaces them with
#               apppropriate address
#
# Parameters: fp --> file pointer of the assembly file to be compiled
#                       (file should be .txt)
#
# Return values:  --> '' (empty string) when tag not found
# -------------------------------------------------------------------------

def DetectCalls(tag,fp):
    global binary_file_linecount
    global a
    global calls

    if tag in calls.keys():
        return '(' + calls[tag] + ')'

    data = fp.readline()
    count=binary_file_linecount+1
    while data!='':
        print("{data: }",data, count)
        if data[0] == '@':
            data = data.strip().split(' ')
            if tag == data[0][1:]:
                calls[tag] = str(count)
                return '(' + str(count) + ')'
        if len(data)>1:
            print("{data: }",data)
            count = count+1
        data = fp.readline()

    return ''






# ----------------------------------------------------------------------------
#                         DRIVER FUNCTION
# ----------------------------------------------------------------------------


if __name__ == "__main__":
    debug=1

    try:

        fp = open(sys.argv[1], "r")
        if debug>0: print("\n [DEBUG] Opened! :",sys.argv[1])
        # DetectCalls('a',fp)
        # fp.seek(0,0)
        # m = fp.readline()
        # print("\n m = ",m)
        b = Convert_Prog_to_bin_temp(fp,debug)
        fp.close()
        print("\n\n (DEBUGGER)  BINARY:")
        debug_display(b)
        print("\n\n\n\n-------------------- Binary-----------------------------")
        for i in b:
            if len(i[0]) >2:
                print("  ",i[0])



    except IOError as e:
        errno, strerror = e.args
        print("I/O error({0}): {1}".format(errno,strerror))
        # e can be printed directly without using .args:
        # print(e)
