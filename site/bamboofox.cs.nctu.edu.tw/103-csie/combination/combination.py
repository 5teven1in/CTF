#!/usr/bin/python
#-*- coding:utf-8 -*- 
 
import base64,binascii,zlib 
import os,random 
import sys

def myprintf(buf):
    print buf
    sys.stdout.flush()

def exit():
    sys.exit(0)
 
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)] 
 
def abc(str): 
    return sha.new(str).hexdigest() 
 
def bin2dec(string_num): 
    return str(int(string_num, 2)) 
 
def hex2dec(string_num): 
    return str(int(string_num.upper(), 16)) 
 
def dec2bin(string_num): 
    num = int(string_num) 
    mid = [] 
    while True: 
        if num == 0: break
        num,rem = divmod(num, 2) 
        mid.append(base[rem]) 
    return ''.join([str(x) for x in mid[::-1]]) 
 
def dec2hex(string_num): 
    num = int(string_num) 
    mid = [] 
    while True: 
        if num == 0: break
        num,rem = divmod(num, 16) 
        mid.append(base[rem]) 
 
    return ''.join([str(x) for x in mid[::-1]]) 
 
def hex2bin(string_num): 
    return dec2bin(hex2dec(string_num.upper())) 
 
def bin2hex(string_num): 
    return dec2hex(bin2dec(string_num)) 
 
def reverse(string): 
    return string[::-1] 
 
def read_flag(): 
    os.system('cat flag') 
 
def utf8(string): 
    return string.decode("utf8") 

def rot13(string):
    return string.encode("rot13")
 
func_names = ['fun1', 'fun2', 'fun3', 'fun4', 'fun5', 'fun6', 'fun7', 'fun8', 'fun9', "fun10"] 
 
f={} 
 
f['fun1']=reverse 
f['fun2']=base64.b64decode 
f['fun3']=zlib.decompress 
f['fun4']=dec2hex 
f['fun5']=binascii.unhexlify 
f['fun6']=utf8 
f['fun7']=bin2dec 
f['fun8']=hex2bin 
f['fun9']=hex2dec 
f['fun10']=rot13
 
def level1():
    myprintf("===Level1===")
    in1=raw_input('f1: ')
    f1='fun'+in1[:1] 
    
    if f1 not in func_names: 
        myprintf('invalid function combination')
        exit() 
    
    user_code = raw_input("plz input your passcode:\n")
    answer = "gniggubeD erawtfoS"
    try:
        if user_code == f[f1](answer):
            myprintf("Congraz! You passwd level 1!")
        else:
            myprintf("Wrong answer, you bad guy!")
            exit() 
    except:
        myprintf("Wrong function combination, you bad guy!")
        exit() 

def level2():
    myprintf("===Level2===")
    in1=raw_input('f1: ') 
    f1='fun'+in1[:1] 
    in2=raw_input('f2: ') 
    f2='fun'+in2[:2] 

    if f1 not in func_names or f2 not in func_names: 
        myprintf('invalid function combination')
        exit() 
 
    user_code = raw_input("plz input your passcode:\n")
    answer = "Q3lubHZhdCBQR1MgdmYgc2hhYXZyZSBndW5hIGpldmd2YXQgbiBjbmNyZS4="
    try:
        if user_code == f[f2](f[f1](answer)):
            myprintf("Congraz! You passwd level 2!")
        else:
            myprintf("Wrong answer, you bad guy!")
            exit() 
    except:
        myprintf("Wrong function combination, you bad guy!")
        exit() 

def level3():
    myprintf("===Level3===")
    in1=raw_input('f1: ') 
    f1='fun'+in1[:1] 
    in2=raw_input('f2: ') 
    f2='fun'+in2[:1] 
    in3=raw_input('f3: ') 
    f3='fun'+in3[:1] 

    if f1 not in func_names or f2 not in func_names or f3 not in func_names: 
        myprintf('invalid function combination')
        exit() 
 
    user_code = raw_input("plz input your passcode:\n")
    answer = "101010001101000011001010010000001110000011100100110111101100010011011000110010101101101001000000110100101110011001000000110110101101111011001000110100101100110011010010110010101100100001000000110001001111001001000000100001001000011010101000100011000100000001100100011000000110001001101000010000001100011011100100111100101110000011101000110111100100000001100010011000000110000001011000010000001110100011010000110000101101110011010110111001100100000011001100110111101110010001000000110001001101100011101010110010100101101011011000110111101110100011101010111001100101110"
    try:
        if user_code == f[f3](f[f2](f[f1](answer))):
            myprintf("Congraz! You passwd level 3!")
        else:
            myprintf("Wrong answer, you bad guy!")
            exit() 
    except:
        myprintf("Wrong function combination, you bad guy!")
        exit() 

def main(): 
    os.chdir("/home/combination")
    level1()
    level2()
    level3()

    myprintf("hey, you passed the all levels! here is your flag.")
    myprintf(read_flag())
 
myprintf("Welcome to Secure Passcode System")

main() 
