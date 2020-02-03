import sys
def char2binary(c):
    ascii_value = ord(c)
    ans = ""
    while ascii_value > 0:
        digit = ascii_value%2
        ans = str(digit)+ans
        ascii_value/=2
    return ans
def string2binary(s):
    ans = ""
    for c in s:
        ans = ans + char2binary(c)
    return ans
def xor(a,b):
    if a==b:
        return "0"
    else:
        return "1"
def xor_list(*l):
    ans = "0"
    for x in l:
        ans = xor(ans,x)
    return ans
def encode(s):
    l = ['0']*7
    l[:4] = s
    # print(s)
    l[0] = xor_list(s[0],s[1],s[3])
    l[1] = xor_list(s[0],s[2],s[3])
    l[2] = xor_list(s[0])
    l[3] = xor_list(s[1],s[2],s[3])
    l[4:] = s[1:]
    return l
def decode(s):
    l = ['0']*3
    l[0] = xor_list(s[0],s[2],s[4],s[6])
    l[1] = xor_list(s[1],s[2],s[5],s[6])
    l[2] = xor_list(s[3],s[4],s[5],s[6])
    return l
def is_zero(l):
    return all([x=='0' for x in l])

def byte2int(str):
    val = 0
    for i in range(0,len(str)):
        val = val*2 + int(str[i])
    return val
def char_from_list(l1,l2):
    string = "".join(l1+l2)
    print("####",string)
    return chr(byte2int(string))
def index2fix(val):
    if val == 7:
        return 6
    if val == 6:
        return 2
    if val == 5:
        return 4
    if val == 3:
        return 5
    if val == 4:
        return 0
    if val == 2:
        return 1
    if val == 1:
        return 3
    else:
        (print(val))
def fix(d,l):
    val = byte2int("".join(d))
    index = index2fix(val)
    new_d = list(l)
    new_d[index] = xor(l[index],"1")
    if index >=4:
        return False,new_d
    else:
        return False,new_d
def databits(s):
    return "".join([s[2],s[4],s[5],s[6]])
for para in open(sys.argv[1]).read().split('\n\n'):
    code = para.strip()
    print(code)
    print(len(code))
    length = len(code)
    if(length%7 != 0):
        print('INVALID')
        print()
        continue
    ans = ""
    chunks = [para[i:i+14] for i in range(0,length-13,14)]
    for j,chunk in enumerate(chunks):
        e1_string = chunk[0:7]
        e2_string = chunk[7:]

        e1 = [(x) for x in e1_string]
        e2 = [(x) for x in e2_string]

        d1 = decode(e1)
        d2 = decode(e2)
        print(d1,d2)
        if is_zero(d1) and is_zero(d2):
            print(j)
            ans += char_from_list(databits(e1),databits(e2))
        elif is_zero(d1):
            check,new_d2 = fix(d2,e2)
            print('# new_d2',new_d2)
            print('e2',e2)
            print('jaddu')
            print(encode(databits(new_d2)))
            print('jaddu')

            print(encode(databits(new_d2)) == new_d2)
            print(check or encode(databits(new_d2)) == new_d2)
            if(check or encode(databits(new_d2)) == new_d2):
                # print(entered)
                ans += char_from_list(databits(e1),databits(new_d2))
            else:
                ans += '@'
        elif is_zero(d2):
            # print('$',new_d1)
            
            check,new_d1 = fix(d1,e1)
            if(check or encode(databits(new_d1)) == new_d1):
                ans += char_from_list(databits(new_d1),databits(e2))
            else:
                ans += '@'
        else:
            check1,new_d1 = fix(d1,e1)
            check2,new_d2 = fix(d2,e2)
            print('e1,e2',e1,e2)
            print('new_d1,new_d2',new_d1,new_d2)
            v1 = encode(databits(new_d1)) == new_d1 or check1
            v2 = encode(databits(new_d2)) == new_d2 or check2

            if v1 and v2:
                ans += char_from_list(databits(new_d1),databits(new_d2))
            else:
                ans += '@'
        print(ans)