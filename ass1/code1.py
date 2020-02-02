import sys

message = open(sys.argv[1],'r').read().strip()
message_chunks = [message[i:i+8] for i in range(0,len(message)-7,8)]

message_continuing = False

# print(len(message_chunks))

count_frames = 0
chars = 0
def xor_byte(b1,b2):
    return str(int(b1)^int(b2)) 

def xor(byte1,byte2):
    output  = ""
    for i in range(0,len(byte1)):
        output = output + xor_byte(byte1[i],byte2[i])
    return output

def byte2int(str):
    val = 0
    for i in range(0,8):
        val = val*2 + int(str[i])
    return val

def strip_zeros(string):
    ans = ""
    skip = True
    for i in string:
        if i == '1' or skip == False:
            skip = False
            ans += i
        else :
            continue
    return ans
        
def is2lessThan1(string1,string2):
    if len(string1)<len(string2):
        return False
    elif len(string1)>len(string2):
        return True
    l1 = len(string1)
    for i in range(l1):
        if string2[i] == '0'  and string1[i] == '1':
            return True
        elif string2[i] == '1'  and string1[i] == '0':
            return False
    return True

def align(string1,string2):
    string1 = strip_zeros(string1)
    string2 = strip_zeros(string2)
    l1 = len(string1)
    l2 = len(string2)
    if l1 < l2:
        return (False,"")
    string2 = string2 + "".join(['0'])*(l1-l2)
    return (True,string2)

def divides(string1,string2):
    string1 = strip_zeros(string1)
    if string1 == string2 or  all([x=='0' for x in string1]):
        return True
    ans,divisor = align(string1,string2)
    if ans == False:
        return False
    else:
        remainder = strip_zeros(xor(string1,divisor))
        return divides(remainder,string2)

def isdivides(chunk,divisor):
    dividents = [byte2int(x) for x in chunk]
    div = byte2int(divisor)
    remainder = 0
    for i in dividents:
        remainder = (remainder*(2**8)+i%div)%div
    if remainder == 0:
        return True
    else:
        return False
current_message = []
ESC = "10100101"
FLAG = "10101001"
ESC_FLAG = "00100000"
escape_next = False
DIVISOR = "10000011"
final_message = ""
ERRORS = []
for frame in message_chunks:
    # if frame == ESC:
    #     escape_next = True
    #     continue
    # if escape_next == True:
    #     frame = xor(frame,ESC_FLAG)
    #     escape_next = False
    if message_continuing == False and frame == FLAG:
        message_continuing = True
    elif message_continuing == True and frame == FLAG:
        message_continuing = False
        # check_bits = current_message[-1]
        
        VALID = divides("".join(current_message)[:-1],DIVISOR)
        # print("".join(current_message)[:-1],DIVISOR)
        # VALID = isdivides(current_message,DIVISOR)
        current_string = ""
        escape_next = False
        for i in current_message[:-1]:
                if i == ESC:
                    escape_next = True
                    continue
                if escape_next == True:
                    i = xor(i,ESC_FLAG)
                    escape_next = False
                current_string += chr(byte2int(i))
        count_frames += 1
        
        if VALID:
            final_message += current_string
        else:
            ERRORS.append(count_frames)
        
        # print(VALID,current_string,count_frames)
        current_message = []
        # print("#######")
    else:
        # print(frame,byte2int(frame),chr(byte2int(frame)))
        current_message.append(frame)
# print(chars)
print(count_frames)
print(",".join([str(x) for x in ERRORS]))
print(final_message,end = '')