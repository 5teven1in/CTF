#!/usr/bin/env python

from pwn import *
import base64
import subprocess

r = remote('bamboofox.cs.nctu.edu.tw', 11016)
# r = remote('0', 11016)

cmd = "objdump -M intel -d tmp | grep 'mov    DWORD PTR \[rip' | awk -F ',' '{print $2}' | awk '{print $1}'"

r.recvuntil('base64')
prog = r.recvuntil('NOW')
prog = base64.b64decode(prog[:-3].strip())
with open('tmp', 'wb') as fd:
    fd.write(prog)
input_oo = subprocess.check_output(cmd, shell = True).split('\n')

idx = 0
def exp(num):
    global idx
    r.recvuntil('Guess O')
    for i in range(num):
        r.sendline(str(int(input_oo[idx], 16)))
        idx = idx + 1

exp(10)
exp(100)
exp(1000)

r.interactive()
