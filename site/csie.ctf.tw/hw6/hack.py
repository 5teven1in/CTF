#!/usr/bin/python3

enc = '4201471551196f2345794008480875117347600c640c6e144206721b6e38681460126d07454463136601681a6656681b692e7808601e680c483b721a73056c076f55601268096f09'
string = 'Temporal Reverse Engineering'

by = [ enc[i: i + 2] for i in range(0, len(enc), 2) ]

for i in range(0, len(by), 2):
    print(chr(int(by[i], 16) ^ 1), end = "")
    print(chr(int(by[i + 1], 16) ^ (ord(string[i % len(string)]) + 1)), end = "")
