MOV ITYPE COMM
SET A 10E0
COMP ITYPE A
JUMPEQ @handshake



@handshake
INC SOC_BACK
MOD SOC_BACK 1000
COMP ANS SOC_FRONT
JUMPEQ @return_full
SET COMM 1100
JUMP @return







@return_full
SET COMM 1010

@return
MOV MAR PROG_STACK_TOP
FETCH MDR
DEC PROG_STACK_TOP
MOV PROG_STACK_TOP ANS
MOV PC MDR
