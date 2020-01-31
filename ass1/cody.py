import sys

message = open(sys.argv[1],'r').read().strip()
message_chunks = [message[i:i+8] for i in range(0,len(message)-7)]

message_continuing = False

print(len(message_chunks))

count_frames = 0

def xor_byte(b1,b2):
    return str(int(b1)^int(b2)) 

def xor(byte1,byte2):
    output  = ""
    for i in range(0,8):
        output = output + xor_byte(byte1[i],byte2[i])
    return output

def byte2int(str):
    val = 0
    for i in range(0,8):
        val = val*2 + int(str[i])
    return val
current_message = []
ESC = "10100101"
FLAG = "10101001"
ESC_FLAG = "00100000"
escape_next = False

final_message = ""
for frame in message_chunks:
    if frame == ESC:
        escape_next = True
        continue
    if message_continuing == False and frame == FLAG:
        message_continuing = True
    elif message_continuing == True and frame == FLAG:
        message_continuing = False
        current_message = 0
        count_frames += 1
    else:
        if escape_next == True:
            frame = xor(frame,ESC_FLAG)
            escape_next = False
        else:
            print(frame,byte2int(frame))
            final_message += chr(byte2int(frame))
    

print(count_frames)
print(final_message)